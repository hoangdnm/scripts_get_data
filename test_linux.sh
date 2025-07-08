#!/bin/bash
# Linux/VPS Test Runner

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🧪 LINUX TEST RUNNER - Crypto Data Collector${NC}"
echo "================================================"

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 không được cài đặt${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 đã cài đặt: $(python3 --version)${NC}"

# Cài đặt dependencies
echo -e "${YELLOW}📦 Cài đặt dependencies...${NC}"
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Lỗi cài đặt dependencies${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependencies đã cài đặt${NC}"

# Cấp quyền thực thi
chmod +x *.py
chmod +x *.sh

# Chạy quick test
echo -e "${YELLOW}🔍 Chạy quick test...${NC}"
python3 quick_test.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Quick test thất bại${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}🎯 Chọn loại test:${NC}"
echo "[1] Quick Test (đã chạy)"
echo "[2] Full Test (toàn bộ hệ thống)"
echo "[3] Database Test Only"
echo "[4] WebSocket Test Only"
echo "[5] Cron Test (2 phút)"
echo "[6] Health Check"
echo "[7] Performance Test"
echo "[0] Thoát"

read -p "Nhập lựa chọn (0-7): " choice

case $choice in
    0)
        echo "Thoát..."
        exit 0
        ;;
    1)
        echo -e "${YELLOW}🔍 Chạy lại quick test...${NC}"
        python3 quick_test.py
        ;;
    2)
        echo -e "${YELLOW}🧪 Chạy full test...${NC}"
        python3 run_tests.py
        ;;
    3)
        echo -e "${YELLOW}🔍 Test database connection...${NC}"
        python3 -c "from quick_test import quick_test_database; quick_test_database()"
        ;;
    4)
        echo -e "${YELLOW}🔍 Test WebSocket connection...${NC}"
        python3 -c "from quick_test import quick_test_websocket; quick_test_websocket()"
        ;;
    5)
        echo -e "${YELLOW}🔍 Test cron runner (2 phút)...${NC}"
        python3 cron_runner.py 0.033
        ;;
    6)
        echo -e "${YELLOW}🔍 Health check...${NC}"
        python3 health_check.py
        ;;
    7)
        echo -e "${YELLOW}🔍 Performance test...${NC}"
        # Chạy system monitoring trong 30s
        python3 -c "
import psutil
import time
print('CPU:', psutil.cpu_percent(interval=1))
print('Memory:', psutil.virtual_memory().percent)
print('Disk:', psutil.disk_usage('.').percent)
"
        ;;
    *)
        echo -e "${RED}❌ Lựa chọn không hợp lệ${NC}"
        ;;
esac

echo ""
echo -e "${GREEN}📊 Test hoàn thành. Kiểm tra logs để biết chi tiết.${NC}"
