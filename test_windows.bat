@echo off
echo 🧪 WINDOWS TEST RUNNER - Crypto Data Collector
echo ================================================

:: Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python không được cài đặt
    pause
    exit /b 1
)

echo ✅ Python đã cài đặt
echo.

:: Cài đặt dependencies
echo 📦 Cài đặt dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Lỗi cài đặt dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies đã cài đặt
echo.

:: Chạy quick test
echo 🔍 Chạy quick test...
python quick_test.py
if %errorlevel% neq 0 (
    echo ❌ Quick test thất bại
    pause
    exit /b 1
)

echo.
echo 🎯 Chọn loại test:
echo [1] Quick Test (đã chạy)
echo [2] Full Test (toàn bộ hệ thống)
echo [3] Database Test Only
echo [4] WebSocket Test Only
echo [5] Cron Test (2 phút)
echo [6] Health Check
echo [0] Thoát

set /p choice=Nhập lựa chọn (0-6): 

if "%choice%"=="0" goto :end
if "%choice%"=="1" (
    echo 🔍 Chạy lại quick test...
    python quick_test.py
    goto :end
)
if "%choice%"=="2" (
    echo 🧪 Chạy full test...
    python run_tests.py
    goto :end
)
if "%choice%"=="3" (
    echo 🔍 Test database connection...
    python -c "from quick_test import quick_test_database; quick_test_database()"
    goto :end
)
if "%choice%"=="4" (
    echo 🔍 Test WebSocket connection...
    python -c "from quick_test import quick_test_websocket; quick_test_websocket()"
    goto :end
)
if "%choice%"=="5" (
    echo 🔍 Test cron runner (2 phút)...
    python cron_runner.py 0.033
    goto :end
)
if "%choice%"=="6" (
    echo 🔍 Health check...
    python health_check.py
    goto :end
)

echo ❌ Lựa chọn không hợp lệ

:end
echo.
echo 📊 Test hoàn thành. Kiểm tra logs để biết chi tiết.
pause
