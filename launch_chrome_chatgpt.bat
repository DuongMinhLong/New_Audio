@echo off
chcp 65001 >nul
echo [INFO] Dang khoi dong Chrome CDP port 9222 cho ChatGPT...
python tools\chatwithgpt_server.py --launch
pause
