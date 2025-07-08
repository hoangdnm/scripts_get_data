# 🧪 Testing Guide - Crypto Data Collector

## Tổng quan

Hệ thống có 3 level testing:
1. **Quick Test** - Test nhanh các component chính (~30s)
2. **Full Test** - Test toàn bộ hệ thống (~3 phút)
3. **Interactive Test** - Menu test tương tác với nhiều tùy chọn

## 🚀 Cách chạy test

### 1. Quick Test (Khuyến nghị cho lần đầu)

```bash
# Windows
python quick_test.py

# Linux/VPS
python3 quick_test.py
```

**Nội dung test:**
- ✅ Import các module chính
- ✅ Kết nối database
- ✅ Kết nối WebSocket

### 2. Full Test Suite

```bash
# Windows
python run_tests.py

# Linux/VPS
python3 run_tests.py
```

**Nội dung test:**
- ✅ Python environment
- ✅ Dependencies
- ✅ Required files
- ✅ Database connection
- ✅ Individual scripts
- ✅ Main script
- ✅ Cron runner (2 phút)
- ✅ Health check

### 3. Interactive Test Menu

```bash
# Windows
test_windows.bat

# Linux/VPS
chmod +x test_linux.sh
./test_linux.sh
```

**Menu options:**
- [1] Quick Test
- [2] Full Test
- [3] Database Test Only
- [4] WebSocket Test Only
- [5] Cron Test (2 phút)
- [6] Health Check
- [7] Performance Test (Linux only)

## 🎯 Test scenarios chi tiết

### A. Pre-deployment Tests

#### 1. Environment Setup Test
```bash
# Kiểm tra Python version
python --version

# Kiểm tra dependencies
pip install -r requirements.txt
```

#### 2. Configuration Test
```bash
# Tạo file .env
cp .env.example .env

# Test database config
python3 -c "
from load_to_sql_vps import load_to_db
import pandas as pd
from datetime import datetime
df = pd.DataFrame({'test': [1], 'time': [datetime.now()]})
load_to_db('raw', 'test_config', df)
print('✅ Database config OK')
"
```

#### 3. Network Test
```bash
# Test WebSocket connection
python3 -c "
from ws_client import BitgetWS
from rest_api import target_list_coin
df = BitgetWS('SPOT', 'ticker', target_list_coin[:1], 3).run()
print(f'✅ WebSocket OK: {len(df)} records')
"
```

### B. Functional Tests

#### 1. Individual Script Tests
```bash
# Test từng script riêng lẻ
python3 get_candle_raw_data.py
python3 get_ticker_raw_data.py
python3 get_trade_raw_data.py
```

#### 2. Main Process Test
```bash
# Test main process
python3 main.py
```

#### 3. Cron Runner Test
```bash
# Test cron runner trong thời gian ngắn
python3 cron_runner.py 0.1  # 6 phút
```

### C. Performance Tests

#### 1. Resource Usage Test
```bash
# Monitor system resources
python3 -c "
import psutil
import time
print('=== SYSTEM RESOURCES ===')
print(f'CPU: {psutil.cpu_percent(interval=1)}%')
print(f'Memory: {psutil.virtual_memory().percent}%')
print(f'Disk: {psutil.disk_usage(\".\").percent}%')
"
```

#### 2. Database Performance Test
```bash
# Test database performance
python3 -c "
import time
import pandas as pd
from load_to_sql_vps import load_to_db
from datetime import datetime

start = time.time()
df = pd.DataFrame({
    'id': range(1000),
    'value': ['test'] * 1000,
    'timestamp': [datetime.now()] * 1000
})
load_to_db('raw', 'perf_test', df)
end = time.time()
print(f'Database write: {end-start:.2f}s for 1000 records')
"
```

### D. Stress Tests

#### 1. Concurrent Connection Test
```bash
# Test multiple concurrent connections
python3 -c "
import threading
import time
from ws_client import BitgetWS
from rest_api import target_list_coin

def test_connection():
    try:
        df = BitgetWS('SPOT', 'ticker', target_list_coin[:1], 2).run()
        print(f'Thread completed: {len(df)} records')
    except Exception as e:
        print(f'Thread failed: {e}')

threads = []
for i in range(3):
    t = threading.Thread(target=test_connection)
    threads.append(t)
    t.start()
    time.sleep(1)

for t in threads:
    t.join()
print('Stress test completed')
"
```

#### 2. Extended Run Test
```bash
# Test chạy liên tục 10 phút
python3 cron_runner.py 0.167
```

## 📊 Hiểu kết quả test

### ✅ Success Indicators
```
✅ Database connection: OK
✅ WebSocket connection: OK
✅ All scripts: PASS
📊 KẾT QUẢ TEST: 8/8 tests passed
🎉 TẤT CẢ TEST THÀNH CÔNG!
```

### ❌ Failure Indicators
```
❌ Database connection: FAILED
❌ WebSocket connection: TIMEOUT
📊 KẾT QUẢ TEST: 6/8 tests passed
❌ CÓ TEST THẤT BẠI!
```

### ⚠️ Warning Indicators
```
⚠️ High CPU usage: 85%
⚠️ High memory usage: 90%
⚠️ No crypto data collector processes found
```

## 🚨 Troubleshooting

### Common Issues & Solutions

#### 1. Import Errors
**Problem:** `ModuleNotFoundError: No module named 'pandas'`
**Solution:**
```bash
pip install -r requirements.txt
# hoặc
pip install pandas sqlalchemy pyodbc websocket-client requests psutil
```

#### 2. Database Connection Errors
**Problem:** `❌ Database connection: FAILED`
**Solutions:**
```bash
# Kiểm tra .env file
cat .env

# Test connection string
python3 -c "import os; print(f'DB_SERVER: {os.getenv(\"DB_SERVER\")}')"

# Test với sqlalchemy
python3 -c "
from sqlalchemy import create_engine
engine = create_engine('mssql+pyodbc://sa:password@server/db?driver=ODBC+Driver+17+for+SQL+Server')
print('Connection test passed')
"
```

#### 3. WebSocket Connection Errors
**Problem:** `❌ WebSocket connection: TIMEOUT`
**Solutions:**
```bash
# Kiểm tra internet connection
ping api.bitget.com

# Test với timeout dài hơn
python3 -c "
from ws_client import BitgetWS
from rest_api import target_list_coin
df = BitgetWS('SPOT', 'ticker', target_list_coin[:1], 10).run()
print('WebSocket test passed')
"
```

#### 4. Permission Errors
**Problem:** `Permission denied`
**Solutions:**
```bash
# Linux/VPS
chmod +x *.py *.sh
chown -R $USER:$USER .

# Windows
# Chạy Command Prompt as Administrator
```

#### 5. Memory Issues
**Problem:** `❌ Memory usage: 90%`
**Solutions:**
```bash
# Giảm số lượng coins test
# Tăng swap space (Linux)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Tối ưu Python memory
export PYTHONMALLOC=pymalloc
```

## 📋 Test Checklist

### Before VPS Deployment
- [ ] Quick test passes
- [ ] Database connection works
- [ ] WebSocket connection stable
- [ ] All individual scripts work
- [ ] Main process completes
- [ ] .env file configured
- [ ] No permission issues

### After VPS Deployment
- [ ] Dependencies installed
- [ ] ODBC drivers installed
- [ ] Quick test passes on VPS
- [ ] Cron test (2 minutes) works
- [ ] Health check passes
- [ ] Logs are being created
- [ ] Database writes successful

### Production Readiness
- [ ] Full test suite passes
- [ ] Performance acceptable
- [ ] No memory leaks
- [ ] Error handling works
- [ ] Graceful shutdown works
- [ ] Monitoring setup
- [ ] Backup strategy

## 🔧 Advanced Testing

### Custom Test Scenarios

#### 1. Network Interruption Test
```bash
# Test behavior when network is interrupted
python3 -c "
import time
from ws_client import BitgetWS
from rest_api import target_list_coin

try:
    df = BitgetWS('SPOT', 'ticker', target_list_coin[:1], 30).run()
    print('Network test passed')
except Exception as e:
    print(f'Network interruption handled: {e}')
"
```

#### 2. Database Failure Test
```bash
# Test với wrong database config
DB_SERVER=wrong_server python3 quick_test.py
```

#### 3. Resource Exhaustion Test
```bash
# Test với limited memory
python3 -c "
import resource
resource.setrlimit(resource.RLIMIT_AS, (100*1024*1024, 100*1024*1024))  # 100MB limit
" && python3 quick_test.py
```

## 📈 Performance Benchmarks

### Expected Performance
- Quick test: < 30 seconds
- Full test: < 3 minutes
- Database write: < 1 second/1000 records
- WebSocket connection: < 5 seconds
- Memory usage: < 500MB
- CPU usage: < 50%

### Performance Monitoring
```bash
# Continuous monitoring
watch -n 5 'python3 -c "
import psutil
print(f\"CPU: {psutil.cpu_percent()}%\")
print(f\"Memory: {psutil.virtual_memory().percent}%\")
print(f\"Processes: {len([p for p in psutil.process_iter() if \"python\" in p.name()])}\")"'
```

## 💡 Best Practices

1. **Test Order**: Quick → Full → Production
2. **Environment**: Test local → Test VPS → Production
3. **Data**: Test with small dataset first
4. **Monitoring**: Always check logs after tests
5. **Cleanup**: Remove test data after testing
6. **Documentation**: Record test results
7. **Automation**: Use scripts for repetitive tests

## 🎯 Next Steps

After successful testing:
1. Deploy to VPS
2. Setup cron job
3. Configure monitoring
4. Setup backups
5. Document production setup
