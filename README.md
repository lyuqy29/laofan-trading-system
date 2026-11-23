# liuliu-trading-system · 溜溜交易手册

老樊「微产品论」量价时空交易系统，封装为 DSH 个人技能。

- 入口：`liuliu-trading-system/SKILL.md`
- 内容：九大交易模型、移动平均带三类买卖点、背离共振、止损与仓位、检查清单、交易计划模板

## 方式一：一键安装（Windows）

解压后，在解压目录右键「在终端中打开」，执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\install-skill.ps1
```

默认安装到 `%USERPROFILE%\.dsh\skills\liuliu-trading-system`。

## 方式二：手动复制（Windows / macOS / Linux 通用）

把 `liuliu-trading-system` 整个文件夹复制到：

| 系统 | 用户级目录（推荐） |
|---|---|
| Windows | `C:\Users\<你>\.dsh\skills\` |
| macOS / Linux | `~/.dsh/skills/` |

也支持项目级：复制到项目根目录的 `.dsh/skills/` 或 `.agents/skills/`，只在该项目生效。

macOS / Linux 也可一键：

```bash
bash install-skill.sh
```

## 验证

1. 重启 DSH（或新开一个会话）。
2. 在会话中问：「有哪些可用技能？」或直接说「用 liuliu-trading-system 分析……」。
3. 如果技能列表里出现 `liuliu-trading-system`，即安装成功。

若未出现：确认目录结构是 `<skills>/liuliu-trading-system/SKILL.md`（不是多套一层文件夹），且 `SKILL.md` 开头有 `---` 包裹的 `name` 与 `description`。

## 更新

用新版本覆盖整个 `liuliu-trading-system` 文件夹即可（技能会在下次会话或文件变更后重新加载）。

## 卸载

删除 `~/.dsh/skills/liuliu-trading-system` 文件夹。

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
