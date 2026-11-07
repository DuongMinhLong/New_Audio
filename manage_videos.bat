@echo off
chcp 65001 >nul
title RADIO 2AM - QUẢN LÝ VIDEO, TIÊU ĐỀ HIẾU KỲ & SHOPEE AFFILIATE

cd /d "%~dp0"
python manage_videos.py
pause
