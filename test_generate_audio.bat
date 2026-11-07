@echo off
chcp 65001 >nul
echo =======================================================
echo    ChatGPT Automated Read Aloud Audio Generator
echo =======================================================
echo.

cd /d "%~dp0"

echo [1/3] Kiem tra ket noi Chrome CDP va FFmpeg...
python tools\chatwithgpt_server.py --status
echo.

if "%~1"=="" (
    set /p PROMPT_TEXT="Nhap noi dung ban muon tao giong doc (hoac Enter de dung mac dinh): "
) else (
    set "PROMPT_TEXT=%~1"
)

if "%PROMPT_TEXT%"=="" (
    set "PROMPT_TEXT=Xin chào, đây là giọng đọc tiếng Việt chất lượng cao được tạo tự động từ ChatGPT."
)

if "%~2"=="" (
    set "OUTPUT_NAME=demo_voice"
) else (
    set "OUTPUT_NAME=%~2"
)

echo.
echo [2/3] Dang gui toi ChatGPT va trich xuat audio Read Aloud...
python tools\chatwithgpt_server.py --audio "%PROMPT_TEXT%" "%OUTPUT_NAME%"
echo.

echo [3/3] Danh sach file da duoc tao trong thu muc outputs:
dir /b outputs\%OUTPUT_NAME%.*
echo.
echo =======================================================
echo   Hoan thanh! File MP3 da san sang trong thu muc outputs/
echo =======================================================
pause
