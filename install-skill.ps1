<#
溜溜交易手册 · skill 安装器（Windows PowerShell）

用法：
  powershell -ExecutionPolicy Bypass -File .\install-skill.ps1
  powershell -ExecutionPolicy Bypass -File .\install-skill.ps1 -Project
  powershell -ExecutionPolicy Bypass -File .\install-skill.ps1 -Force
  powershell -ExecutionPolicy Bypass -File .\install-skill.ps1 -Uninstall
#>
[CmdletBinding()]
param(
    [switch]$Project,
    [switch]$Force,
    [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'
$Name = 'liuliu-trading-system'
$Src  = $PSScriptRoot

if ($env:DSH_HOME) { $DshHome = $env:DSH_HOME }
else { $DshHome = Join-Path $env:USERPROFILE '.dsh' }

if ($Project) { $Base = Join-Path (Get-Location).Path '.dsh\skills' }
else { $Base = Join-Path $DshHome 'skills' }

$Dest = Join-Path $Base $Name

if ($Uninstall) {
    if (-not (Test-Path $Dest)) {
        Write-Host "未安装: $Dest"
        exit 0
    }
    Remove-Item -Recurse -Force $Dest
    Write-Host "已卸载: $Dest"
    exit 0
}

if (-not (Test-Path (Join-Path $Src 'SKILL.md'))) {
    Write-Error "错误：$Src 下没有 SKILL.md，请在仓库根目录运行本脚本。"
    exit 1
}

if (Test-Path $Dest) {
    if (-not $Force) {
        Write-Error "已存在: $Dest`n如需覆盖请加 -Force，或先执行 -Uninstall"
        exit 1
    }
    Remove-Item -Recurse -Force $Dest
}

New-Item -ItemType Directory -Force -Path $Dest | Out-Null

Copy-Item -Path (Join-Path $Src 'SKILL.md') -Destination $Dest -Force
if (Test-Path (Join-Path $Src 'README.md')) {
    Copy-Item -Path (Join-Path $Src 'README.md') -Destination $Dest -Force
}
foreach ($dir in @('references', 'assets')) {
    $from = Join-Path $Src $dir
    if (Test-Path $from) {
        Copy-Item -Path $from -Destination $Dest -Recurse -Force
    }
}

$head = Get-Content -Path (Join-Path $Dest 'SKILL.md') -TotalCount 5
if (-not ($head -match "^name: $Name$")) {
    Write-Warning "SKILL.md 的 name 字段与目录名不一致，技能可能不会被加载"
}

Write-Host "已安装: $Dest"
Write-Host "验证: 新开会话问「有哪些可用技能？」，或直接说「用 $Name 分析 600519」"
Write-Host "说明: dashboard/ 是独立看板，不需要安装进 skills 目录。"
