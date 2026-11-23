#!/usr/bin/env python3
"""溜溜交易手册 —— 本地服务（体系：源自量价时空交易方法论）。

只依赖标准库。启动后浏览器打开 http://127.0.0.1:8777

接口：
  GET  /api/analyze?code=600519      单票分析（模型匹配 + 交易计划）
  GET  /api/compare?codes=a,b,c      多票对比排序
  GET  /api/watchlist                读自选
  POST /api/watchlist                增删自选 {"code":"600519","action":"add|remove"}
  GET  /api/health
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
import traceback
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import market          # noqa: E402
import models          # noqa: E402

WEB = os.path.join(HERE, "web")
DATA = os.path.join(HERE, "data")
WATCHLIST = os.path.join(DATA, "watchlist.json")
CACHE_TTL = 90
_cache = {}
_cache_lock = threading.Lock()

DEFAULT_WATCHLIST = ["600519", "300750", "002594", "601127", "600030"]


def analyze(code: str) -> dict:
    key = code.strip().lower()
    now = time.time()
    with _cache_lock:
        hit = _cache.get(key)
        if hit and now - hit[0] < CACHE_TTL:
            return hit[1]
    ctx = market.build_context(code)
    ev = models.evaluate(ctx)
    payload = {
        "ok": True,
        "ctx": {k: v for k, v in ctx.items()
                if k not in ("bars_full", "events_raw")},
        "result": ev,
        "accuracy_note": "机械口径检测，仅覆盖可量化的部分；筹码分布与题材级别需人工确认。",
    }
    with _cache_lock:
        _cache[key] = (now, payload)
    return payload


def compare(codes: list[str]) -> dict:
    rows = []
    for c in codes:
        try:
            p = analyze(c)
            ctx, plan = p["ctx"], p["result"]["plan"]
            rows.append({
                "code": ctx["code"], "name": ctx["name"],
                "close": ctx["close"], "chg": round(ctx["chg"], 2),
                "trend": ctx["trend"], "position": ctx["position"],
                "bias60": round(ctx["bias60"], 1),
                "model": plan["model"], "level": plan["level"],
                "decision": plan["decision"], "tone": plan["tone"],
                "grade": plan["grade"], "cap": plan["cap_max"],
                "cap_now": plan["cap_now"],
                "events": len(ctx["recent_events"]),
                "score": p["result"]["models"][0]["score"] if p["result"]["models"] else 0,
            })
        except Exception as exc:  # noqa: BLE001
            rows.append({"code": c, "error": str(exc)})
    ok = [r for r in rows if "error" not in r]

    def rank(r):
        # 可交易性优先，其次模型等级，再比模型得分与活跃度
        dec = {"可试仓": 3, "观察待确认": 2, "观察区": 1, "规避": 0}.get(r["decision"], 0)
        lv = 2 if r["level"] == "标准版" else 1 if r["level"] == "弱化版" else 0
        return (dec, lv, r["score"], r["events"])
    ok.sort(key=rank, reverse=True)
    rows = ok + [r for r in rows if "error" in r]
    return {"ok": True, "rows": rows}


def load_watchlist() -> list[str]:
    try:
        with open(WATCHLIST, encoding="utf-8") as f:
            d = json.load(f)
            if isinstance(d, list) and d:
                return d
    except FileNotFoundError:
        pass
    except Exception:  # noqa: BLE001
        pass
    return list(DEFAULT_WATCHLIST)


def save_watchlist(codes: list[str]) -> None:
    os.makedirs(DATA, exist_ok=True)
    with open(WATCHLIST, "w", encoding="utf-8") as f:
        json.dump(codes, f, ensure_ascii=False, indent=2)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=WEB, **kw)

    def log_message(self, fmt, *args):  # 精简日志
        sys.stderr.write("[dash] %s\n" % (fmt % args))

    def _json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _err(self, msg, status=400):
        self._json({"ok": False, "error": msg}, status)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path == "/api/health":
                return self._json({"ok": True, "ts": time.strftime("%Y-%m-%d %H:%M:%S")})
            if u.path == "/api/analyze":
                code = (q.get("code") or [""])[0]
                if not code:
                    return self._err("缺少 code 参数")
                return self._json(analyze(code))
            if u.path == "/api/compare":
                codes = [x for x in (q.get("codes") or [""])[0].split(",") if x]
                if not codes:
                    return self._err("缺少 codes 参数")
                return self._json(compare(codes[:12]))
            if u.path == "/api/watchlist":
                return self._json({"ok": True, "codes": load_watchlist()})
            if u.path.startswith("/api/"):
                return self._err("未知接口", 404)
        except (ValueError, RuntimeError) as exc:
            return self._err(str(exc), 400)
        except Exception as exc:  # noqa: BLE001
            traceback.print_exc()
            return self._err(f"{type(exc).__name__}: {exc}", 500)
        return super().do_GET()

    def do_POST(self):
        u = urlparse(self.path)
        if u.path != "/api/watchlist":
            return self._err("未知接口", 404)
        try:
            length = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(length) or b"{}")
            code = market.symbol_of(str(body.get("code", "")))[2:]
            action = body.get("action", "add")
            codes = load_watchlist()
            if action == "add" and code not in codes:
                codes.append(code)
            elif action == "remove":
                codes = [c for c in codes if c != code]
            save_watchlist(codes)
            return self._json({"ok": True, "codes": codes})
        except Exception as exc:  # noqa: BLE001
            return self._err(str(exc), 500)


def main():
    port = int(os.environ.get("PORT", "8777"))
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"看板已启动: http://127.0.0.1:{port}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
