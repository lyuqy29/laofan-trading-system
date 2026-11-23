# liuliu-trading-system · 溜溜交易手册

源自量价时空交易方法论，封装为 DSH 个人技能。

- 入口：`liuliu-trading-system/SKILL.md`
- 内容：九大交易模型、移动平均带三类买卖点、背离共振、止损与仓位、检查清单、交易计划模板

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

## 配套看板

仓库 `dashboard/` 目录是本体系的本地可视化看板：输入代码即可看到均线带、BIAS、九大模型扫描与交易计划。

```bash
cd dashboard
bash start.sh          # 默认 http://127.0.0.1:8777
```

- 三个页签：单票分析 / 自选对比 / 体系说明书
- 判定逻辑与技能同一套口径（六要素打分、双十仓位、−12% 静态止损）
- 截图见 `dashboard/docs/`

## 说明

- 这是课程内容整理与交易纪律工具，不构成投资建议。
- 带「※」的量化口径是为便于执行补充的操作定义，课程原话以经验描述为主。
