#!/usr/bin/env bash
# 溜溜交易手册 · skill 安装器（macOS / Linux）
#
# 用法：
#   bash install-skill.sh                # 装到用户级 ~/.dsh/skills
#   bash install-skill.sh --project      # 装到当前项目 ./.dsh/skills
#   bash install-skill.sh --force        # 覆盖已安装版本
#   bash install-skill.sh --uninstall    # 卸载
set -euo pipefail

NAME="liuliu-trading-system"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<EOF
溜溜交易手册 · skill 安装器

用法: bash install-skill.sh [选项]

选项:
  --project      安装到当前项目的 .dsh/skills/（仅该项目生效）
  --force, -f    覆盖已存在的安装
  --uninstall    卸载
  -h, --help     显示帮助

默认安装到: \${DSH_HOME:-~/.dsh}/skills/$NAME
EOF
}

MODE="user"
FORCE=0
UNINSTALL=0
while [ $# -gt 0 ]; do
  case "$1" in
    --project) MODE="project"; shift ;;
    --force|-f) FORCE=1; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "未知参数: $1" >&2; usage; exit 1 ;;
  esac
done

if [ "$MODE" = "project" ]; then
  BASE="$(pwd)/.dsh/skills"
else
  BASE="${DSH_HOME:-$HOME/.dsh}/skills"
fi
DEST="$BASE/$NAME"

if [ "$UNINSTALL" = "1" ]; then
  if [ ! -d "$DEST" ]; then
    echo "未安装: $DEST"
    exit 0
  fi
  rm -rf "$DEST"
  echo "已卸载: $DEST"
  exit 0
fi

if [ ! -f "$SRC/SKILL.md" ]; then
  echo "错误：$SRC 下没有 SKILL.md，请在仓库根目录运行本脚本。" >&2
  exit 1
fi

if [ -e "$DEST" ]; then
  if [ "$FORCE" != "1" ]; then
    echo "已存在: $DEST" >&2
    echo "如需覆盖请加 --force，或先执行 --uninstall" >&2
    exit 1
  fi
  rm -rf "$DEST"
fi

mkdir -p "$DEST"
cp -R "$SRC/SKILL.md" "$DEST/"
[ -f "$SRC/README.md" ] && cp -R "$SRC/README.md" "$DEST/"
for dir in references assets; do
  if [ -d "$SRC/$dir" ]; then
    cp -R "$SRC/$dir" "$DEST/"
  fi
done

if ! head -n 5 "$DEST/SKILL.md" | grep -q "^name: $NAME\$"; then
  echo "⚠ SKILL.md 的 name 字段与目录名不一致，技能可能不会被加载" >&2
fi

echo "已安装: $DEST"
echo "验证: 新开会话问「有哪些可用技能？」，或直接说「用 $NAME 分析 600519」"
echo "说明: dashboard/ 是独立看板，不需要安装进 skills 目录。"
