#!/bin/bash
# VPS Startup Script cho crypto data collector

# Màu sắc cho output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Crypto Data Collector - VPS Startup Script${NC}"
echo "================================================="

# Lấy thư mục hiện tại
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "${YELLOW}📁 Working directory: ${SCRIPT_DIR}${NC}"

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 không được cài đặt${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 version: $(python3 --version)${NC}"

# Kiểm tra pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 không được cài đặt${NC}"
    exit 1
fi

# Cài đặt dependencies
echo -e "${YELLOW}📦 Cài đặt dependencies...${NC}"
pip3 install -r requirements.txt

# Kiểm tra các file cần thiết
REQUIRED_FILES=("main.py" "cron_runner.py" "get_candle_raw_data.py" "get_ticker_raw_data.py" "get_trade_raw_data.py")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ File không tồn tại: $file${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ Tất cả file cần thiết đã sẵn sàng${NC}"

# Tạo thư mục logs nếu chưa có
mkdir -p log

# Cấp quyền thực thi cho các script
chmod +x cron_runner.py
chmod +x main.py

echo -e "${GREEN}✅ Cấp quyền thực thi hoàn tất${NC}"

# Hỏi user muốn chạy bao lâu
echo -e "${YELLOW}⏰ Nhập thời gian chạy (giờ) [mặc định: 2]:${NC}"
read -r DURATION
DURATION=${DURATION:-2}

echo -e "${GREEN}🎯 Sẽ chạy trong ${DURATION} giờ${NC}"

# Chạy cron runner
echo -e "${YELLOW}🚀 Bắt đầu chạy cron job...${NC}"
echo "Nhấn Ctrl+C để dừng"
echo "================================================="

python3 cron_runner.py $DURATION
