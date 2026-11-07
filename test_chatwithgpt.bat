@echo off
chcp 65001 >nul
echo [INFO] Kiem tra trang thai MCP chatwithgpt...
python tools\chatwithgpt_server.py --status
echo.
echo [INFO] Gui thu tin nhan test den ChatGPT...
python tools\chatwithgpt_server.py --test "Xin chào! Bạn có thể hỗ trợ tôi viết nội dung cho kênh Audio Youtube không?"
pause
