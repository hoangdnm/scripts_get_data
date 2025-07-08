# Crypto Data Collector - VPS Ready

🚀 Hệ thống thu thập dữ liệu crypto từ Bitget WebSocket API, được thiết kế để chạy trên VPS với cron job tự động.

## ✨ Tính năng

- ✅ Thu thập dữ liệu real-time từ Bitget WebSocket
- ✅ Lưu trữ vào SQL Server database
- ✅ Cron job tự động chạy mỗi 1 phút trong 2 tiếng
- ✅ Hỗ trợ cả Windows và Linux VPS
- ✅ Logging chi tiết và monitoring
- ✅ Health check system
- ✅ Graceful shutdown handling

## 📁 Cấu trúc project

```
scripts_get_data/
├── main.py                     # Script chính chạy tất cả data collectors
├── cron_runner.py             # Cron job runner (chạy mỗi phút trong 2h)
├── health_check.py            # Health check system
├── load_to_sql_vps.py         # Database connection (VPS optimized)
├── get_candle_raw_data.py     # Thu thập dữ liệu candle
├── get_ticker_raw_data.py     # Thu thập dữ liệu ticker
├── get_trade_raw_data.py      # Thu thập dữ liệu trade
├── ws_client.py               # WebSocket client
├── rest_api.py                # REST API helper
├── requirements.txt           # Python dependencies
├── .env.example              # Template cấu hình
├── start_vps.sh              # Script khởi động Linux
├── start_windows.bat         # Script khởi động Windows
├── test_linux.sh             # Test runner Linux
├── test_windows.bat          # Test runner Windows
├── run_tests.py              # Full test suite
├── quick_test.py             # Quick test script
├── crypto-data-collector.service  # Systemd service
├── VPS_SETUP.md              # Hướng dẫn setup VPS
└── log/                      # Thư mục logs
```

## 🚀 Quick Start

### 1. Chuẩn bị

```bash
# Clone/download project
git clone YOUR_REPO_URL
cd scripts_get_data

# Copy và cấu hình environment
cp .env.example .env
nano .env  # Chỉnh sửa thông tin database
```

### 2. Cài đặt dependencies

```bash
# Windows
pip install -r requirements.txt

# Linux/VPS
pip3 install -r requirements.txt
```

### 3. Chạy

#### Windows
```bash
# Chạy script khởi động
start_windows.bat

# Hoặc chạy trực tiếp
python cron_runner.py 2
```

#### Linux/VPS
```bash
# Cấp quyền thực thi
chmod +x start_vps.sh

# Chạy script khởi động
./start_vps.sh

# Hoặc chạy trực tiếp
python3 cron_runner.py 2
```

## 📊 Cách thức hoạt động

1. **cron_runner.py** khởi động và chạy trong 2 tiếng (có thể tùy chỉnh)
2. Mỗi 60 giây, nó sẽ gọi **main.py**
3. **main.py** chạy đồng thời 3 script thu thập dữ liệu:
   - `get_candle_raw_data.py` - Dữ liệu nến (1m candlestick)
   - `get_ticker_raw_data.py` - Dữ liệu ticker
   - `get_trade_raw_data.py` - Dữ liệu trade
4. Mỗi script kết nối WebSocket, thu thập dữ liệu và lưu vào database
5. Tất cả hoạt động được log chi tiết

## 🧪 Testing

### Quick Test (Khuyến nghị)
```bash
# Windows
python quick_test.py

# Linux/VPS
python3 quick_test.py
```

### Full Test Suite
```bash
# Windows
python run_tests.py

# Linux/VPS
python3 run_tests.py
```

### Interactive Test Menu
```bash
# Windows
test_windows.bat

# Linux/VPS
chmod +x test_linux.sh
./test_linux.sh
```

### Test từng component riêng lẻ

#### 1. Test Database Connection
```bash
python3 -c "from quick_test import quick_test_database; quick_test_database()"
```

#### 2. Test WebSocket Connection
```bash
python3 -c "from quick_test import quick_test_websocket; quick_test_websocket()"
```

#### 3. Test Individual Scripts
```bash
# Test candle data
python3 get_candle_raw_data.py

# Test ticker data
python3 get_ticker_raw_data.py

# Test trade data
python3 get_trade_raw_data.py
```

#### 4. Test Main Process
```bash
python3 main.py
```

#### 5. Test Cron Runner (2 phút)
```bash
python3 cron_runner.py 0.033
```

#### 6. Test Health Check
```bash
python3 health_check.py
```

### Các loại test

| Test | Mô tả | Thời gian |
|------|--------|-----------|
| Quick Test | Test cơ bản: import, database, websocket | ~30s |
| Full Test | Test toàn bộ hệ thống | ~3 phút |
| Database Test | Chỉ test kết nối database | ~5s |
| WebSocket Test | Chỉ test WebSocket connection | ~10s |
| Cron Test | Test cron runner trong 2 phút | ~2 phút |
| Health Check | Kiểm tra tình trạng hệ thống | ~10s |

### Hiểu kết quả test

#### ✅ Test thành công
```
🎉 KHAI BÁO: Hệ thống đã sẵn sàng cho production!
Bạn có thể deploy lên VPS và setup cron job.
```

#### ❌ Test thất bại
```
❌ CẢNH BÁO: Hệ thống chưa sẵn sàng!
Vui lòng sửa các lỗi trước khi deploy.
```

### Troubleshooting Test Issues

1. **Import Error**: Chạy `pip install -r requirements.txt`
2. **Database Error**: Kiểm tra file `.env` và database connection
3. **WebSocket Error**: Kiểm tra internet connection
4. **Permission Error**: Chạy `chmod +x *.py *.sh`

## 🛠️ Cấu hình

### Environment Variables (.env)
```env
# Database
DB_USER=sa
DB_PASSWORD=YourStrong!Pass123
DB_NAME=Coin_Analysis_DB
DB_SERVER=localhost,1433

# Application
RUN_DURATION_HOURS=2
CYCLE_INTERVAL_SECONDS=60
```

### Tùy chỉnh thời gian chạy
```bash
# Chạy 1 giờ thay vì 2 giờ
python3 cron_runner.py 1

# Chạy 30 phút (0.5 giờ)
python3 cron_runner.py 0.5
```

## 🔧 VPS Setup

Xem chi tiết trong [VPS_SETUP.md](VPS_SETUP.md)

### Quick VPS Setup
```bash
# 1. Cài đặt dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv -y

# 2. Cài đặt SQL Server ODBC Driver
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt update && sudo apt install msodbcsql17 unixodbc-dev -y

# 3. Upload project và chạy
scp -r ./scripts_get_data/* user@vps:/home/user/crypto_data_collector/
ssh user@vps
cd /home/user/crypto_data_collector
pip3 install -r requirements.txt
./start_vps.sh
```

## 📈 Monitoring

### Health Check
```bash
# Kiểm tra tình trạng hệ thống
python3 health_check.py
```

### Logs
```bash
# Theo dõi logs chính
tail -f cron_runner.log

# Theo dõi logs từng module
tail -f log/candle_loader.log
tail -f log/ticker_loader.log
tail -f log/trade_loader.log
```

### Process monitoring
```bash
# Xem processes đang chạy
ps aux | grep python

# Kill process nếu cần
pkill -f "python.*cron_runner.py"
```

## 🗓️ Cron Job Setup

### Manual Cron (Linux)
```bash
# Mở crontab
crontab -e

# Chạy mỗi 2 tiếng
0 */2 * * * cd /path/to/crypto_data_collector && python3 cron_runner.py 2 >> cron.log 2>&1

# Chạy vào giờ cụ thể
0 8,10,12,14,16,18 * * * cd /path/to/crypto_data_collector && python3 cron_runner.py 2 >> cron.log 2>&1
```

### Systemd Service (Linux)
```bash
# Copy service file
sudo cp crypto-data-collector.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable crypto-data-collector
sudo systemctl start crypto-data-collector
```

## 🔒 Security

- Sử dụng environment variables cho credentials
- File permissions được set đúng
- Database connection encrypted
- Graceful shutdown handling

## 🚨 Troubleshooting

### Common Issues

1. **Database connection error**
   - Kiểm tra credentials trong .env
   - Kiểm tra firewall/network
   - Kiểm tra SQL Server driver

2. **Permission denied**
   ```bash
   chmod +x *.py *.sh
   chown -R user:user /path/to/project
   ```

3. **Memory issues**
   - Giảm số lượng concurrent processes
   - Tăng swap space
   - Tối ưu database queries

4. **WebSocket connection timeout**
   - Kiểm tra network connectivity
   - Tăng timeout settings
   - Retry mechanism

### Debug Mode
```bash
# Chạy với debug logging
LOG_LEVEL=DEBUG python3 cron_runner.py 2
```

## 📋 Requirements

- Python 3.7+
- SQL Server database
- Network connectivity
- Minimum 1GB RAM
- 10GB free disk space

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra logs trong thư mục `log/`
2. Chạy `health_check.py` để diagnose
3. Xem [VPS_SETUP.md](VPS_SETUP.md) để biết chi tiết setup
