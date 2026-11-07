@echo off
chcp 65001 >nul
echo ======================================================================
echo    YOUTUBE LONG-FORM PRODUCTION PIPELINE (10 - 25 PHUT)
echo ======================================================================
echo  1. Outline: Claude Sonnet 5.5 Max
echo  2. 3-Step Review tung Part: Gemini 3.8 Flash High
echo  3. Master Polish: Claude Sonnet 5.5 Max
echo  4. Audio: ChatGPT Read Aloud thu am tung Part
echo  5. Audio Concat: FFmpeg ghep noi + Chuan hoa EBU R128 (-14 LUFS)
echo  6. Video 16:9 1080p: B-roll cinematic + Subtitle Netflix + Mix BGM
echo ======================================================================

set /p slug="Nhap slug video (Mac dinh: xa_hoi_met_moi_long): "
if "%slug%"=="" set slug=xa_hoi_met_moi_long

echo.
echo Chon che do chay:
echo   1. Toan bo tu A-Z tu Kich ban den Render Video (all)
echo   2. Chi tao de cuong Outline (outline)
echo   3. Chi viet va hoan thien kich ban (script)
echo   4. Chi thu am ChatGPT tung Part (audio)
echo   5. Chi ghep noi cac part audio da co (concat)
echo   6. Chi dung Video 16:9 Full HD tu audio co san (video)
set /p opt="Nhap lua chon [1-6] (Mac dinh: 1): "

if "%opt%"=="2" set mode=outline
if "%opt%"=="3" set mode=script
if "%opt%"=="4" set mode=audio
if "%opt%"=="5" set mode=concat
if "%opt%"=="6" set mode=video
if "%opt%"=="" set mode=all
if "%opt%"=="1" set mode=all

echo.
echo Dang khoi chay: python tools/longform_pipeline.py --slug %slug% --mode %mode%
python tools/longform_pipeline.py --slug %slug% --mode %mode%

echo.
pause
