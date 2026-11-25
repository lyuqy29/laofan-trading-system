# liuliu-trading-system · 溜溜交易手册

源自量价时空交易方法论，封装为 DSH 个人技能。

- 入口：`liuliu-trading-system/SKILL.md`
- 内容：九大交易模型、移动平均带三类买卖点、背离共振、止损与仓位、检查清单、交易计划模板
- 看板：`dashboard/`（双体系，可切换「量价时空 / 梅森体系」）

## 安装

### 一键安装

macOS / Linux：

```bash
bash install-skill.sh              # 用户级：~/.dsh/skills
bash install-skill.sh --project    # 项目级：当前目录 ./.dsh/skills
bash install-skill.sh --force      # 覆盖已安装版本
bash install-skill.sh --uninstall  # 卸载
```

Windows（PowerShell）：

```powershell
powershell -ExecutionPolicy Bypass -File .\install-skill.ps1
powershell -ExecutionPolicy Bypass -File .\install-skill.ps1 -Project
powershell -ExecutionPolicy Bypass -File .\install-skill.ps1 -Force
powershell -ExecutionPolicy Bypass -File .\install-skill.ps1 -Uninstall
```

默认安装位置：

| 系统 | 用户级目录 |
|---|---|
| Windows | `%USERPROFILE%\.dsh\skills\liuliu-trading-system` |
| macOS / Linux | `~/.dsh/skills/liuliu-trading-system` |

设置环境变量 `DSH_HOME` 可以改变用户级根目录。

### 手动安装

把 `SKILL.md`、`README.md`、`references/`、`assets/` 复制到 `<skills>/liuliu-trading-system/` 即可。
`dashboard/` 是独立看板，**不需要**复制进 skills 目录。

## 验证

1. 在会话中问「有哪些可用技能？」或直接说「用 liuliu-trading-system 分析……」。
2. 技能列表里出现 `liuliu-trading-system` 即安装成功。

目录是热加载的，通常无需重启；若列表没刷新，新开一个会话即可。

若未出现：确认目录结构是 `<skills>/liuliu-trading-system/SKILL.md`（不是多套一层），且 `SKILL.md` 开头有 `---` 包裹的 `name` 与 `description`。

## 更新

用新版本覆盖整个目录：

```bash
bash install-skill.sh --force
```

## 卸载

```bash
bash install-skill.sh --uninstall
```

## 配套看板（双体系）

仓库 `dashboard/` 是本地可视化看板，**顶部可在「量价时空」与「梅森体系」之间切换**，
两个技能共用一套行情层与页面框架。

```bash
cd dashboard
bash start.sh          # 默认 http://127.0.0.1:8777
PORT=9000 bash start.sh
```

**量价时空（4 页）**

- 单票分析 / 自选对比 / 持仓管理 / 体系说明书
- 判定逻辑与技能同一套口径（六要素打分、双十仓位、−12% 静态止损）
- 截图见 `dashboard/docs/`

**梅森体系（5 页）**

| 页面 | 内容 |
|---|---|
| 大盘时机 | 三大指数均线三态 + 三天不新低 + 否决线 → 防守/试探/进攻 |
| 主线板块 | 板块今日/5日/60日、涨跌家数、领涨股 |
| 个股位置 | 均线三态、距 MA20 分区、三大买点信号、止损与建议仓位 |
| 交易计划 | 解析 `plans/*.md`，实时校验触发/等待/已破止损 |
| 体系自检 | 16 项下单前清单，勾选进度本地保存 |

深链：`/?sys=ms&view=timing`、`/?sys=ms&view=plan`、`/?sys=ms&view=stock&code=601985`

> 梅森体系的完整方法论在其独立仓库 `lyuqy29/meisen-trading-system`；
> 本合同名 `dashboard/` 与那边保持一致，`plans/` 里放交易计划即可自动校验。

## 说明

- 这是课程内容整理与交易纪律工具，不构成投资建议。
- 带「※」的量化口径是为便于执行补充的操作定义，课程原话以经验描述为主。
