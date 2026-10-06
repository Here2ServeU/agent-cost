# One-time setup for Windows (PowerShell).
#
#   .\setup.ps1
#
# If Windows says running scripts is disabled, run this once first:
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
#
# Makes a private Python box for this project (.venv), installs the one
# package it needs, and runs the six-proof check so you know it works.

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. See 'Install the tools' in README.md."
    exit 1
}

Write-Host "1/3  making a private Python box for this project (.venv)"
py -m venv .venv

Write-Host "2/3  installing the one package it needs (prometheus-client)"
.\.venv\Scripts\python.exe -m pip install --quiet --upgrade pip
.\.venv\Scripts\python.exe -m pip install --quiet -r requirements.txt

Write-Host "3/3  running the check"
.\.venv\Scripts\python.exe verify.py
.\.venv\Scripts\python.exe reset.py | Out-Null

Write-Host ""
Write-Host "Ready. In every new PowerShell window, first run:"
Write-Host "    .venv\Scripts\Activate.ps1"
