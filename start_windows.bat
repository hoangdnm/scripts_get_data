@echo off
:: Windows Startup Script cho crypto data collector

echo 🚀 Crypto Data Collector - Windows Startup Script
echo =================================================

:: Lấy thư mục hiện tại
cd /d "%~dp0"
echo 📁 Working directory: %CD%

:: Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python không được cài đặt
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo ✅ %%i

:: Cài đặt dependencies
echo 📦 Cài đặt dependencies...
pip install -r requirements.txt

:: Kiểm tra các file cần thiết
set "files=main.py cron_runner.py get_candle_raw_data.py get_ticker_raw_data.py get_trade_raw_data.py"
for %%f in (%files%) do (
    if not exist "%%f" (
        echo ❌ File không tồn tại: %%f
        pause
        exit /b 1
    )
)

echo ✅ Tất cả file cần thiết đã sẵn sàng

:: Tạo thư mục logs nếu chưa có
if not exist "log" mkdir log

:: Hỏi user muốn chạy bao lâu
set /p duration=⏰ Nhập thời gian chạy (giờ) [mặc định: 2]: 
if "%duration%"=="" set duration=2

echo 🎯 Sẽ chạy trong %duration% giờ

:: Chạy cron runner
echo 🚀 Bắt đầu chạy cron job...
echo Nhấn Ctrl+C để dừng
echo =================================================

python cron_runner.py %duration%

pause
