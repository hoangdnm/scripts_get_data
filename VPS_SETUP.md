# Hướng dẫn Setup VPS cho Crypto Data Collector

## 1. Chuẩn bị VPS (Ubuntu/Debian)

### Cài đặt dependencies cơ bản
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Cài đặt Python 3 và pip
sudo apt install python3 python3-pip python3-venv -y

# Cài đặt Microsoft ODBC Driver cho SQL Server
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt update
sudo apt install msodbcsql17 unixodbc-dev -y
```

### Cài đặt development tools
```bash
sudo apt install build-essential -y
```

## 2. Upload và setup project

### Tạo thư mục làm việc
```bash
mkdir -p /home/ubuntu/crypto_data_collector
cd /home/ubuntu/crypto_data_collector
```

### Upload files qua SCP/SFTP
```bash
# Từ máy local upload tất cả files
scp -r ./scripts_get_data/* ubuntu@YOUR_VPS_IP:/home/ubuntu/crypto_data_collector/
```

### Hoặc clone từ git repository
```bash
# Nếu bạn có git repo
git clone YOUR_REPO_URL /home/ubuntu/crypto_data_collector
cd /home/ubuntu/crypto_data_collector
```

## 3. Cấu hình environment

### Tạo file .env
```bash
cp .env.example .env
nano .env
```

### Chỉnh sửa thông tin database trong .env
```
DB_USER=sa
DB_PASSWORD=YourStrong!Pass123
DB_NAME=Coin_Analysis_DB
DB_SERVER=YOUR_DB_SERVER,1433
```

### Cài đặt Python packages
```bash
pip3 install -r requirements.txt
```

## 4. Test chạy thử

### Chạy thử 1 lần
```bash
python3 main.py
```

### Chạy thử cron runner
```bash
python3 cron_runner.py 0.1  # Chạy thử 6 phút
```

## 5. Setup như systemd service (tùy chọn)

### Copy service file
```bash
sudo cp crypto-data-collector.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable crypto-data-collector
```

### Khởi động service
```bash
sudo systemctl start crypto-data-collector
sudo systemctl status crypto-data-collector
```

### Xem logs
```bash
journalctl -u crypto-data-collector -f
```

## 6. Setup cron job thủ công

### Mở crontab
```bash
crontab -e
```

### Thêm job chạy mỗi 2 tiếng
```bash
# Chạy vào lúc 8:00, 10:00, 12:00, 14:00, 16:00, 18:00 mỗi ngày
0 8,10,12,14,16,18 * * * cd /home/ubuntu/crypto_data_collector && python3 cron_runner.py 2 >> /home/ubuntu/crypto_data_collector/cron.log 2>&1
```

### Hoặc chạy liên tục mỗi 2 tiếng
```bash
# Chạy mỗi 2 tiếng, bắt đầu từ 0:00
0 */2 * * * cd /home/ubuntu/crypto_data_collector && python3 cron_runner.py 2 >> /home/ubuntu/crypto_data_collector/cron.log 2>&1
```

## 7. Monitoring và troubleshooting

### Xem logs
```bash
# Xem logs của application
tail -f /home/ubuntu/crypto_data_collector/cron_runner.log

# Xem logs của cron
tail -f /home/ubuntu/crypto_data_collector/cron.log

# Xem logs của từng module
tail -f /home/ubuntu/crypto_data_collector/log/candle_loader.log
tail -f /home/ubuntu/crypto_data_collector/log/ticker_loader.log
tail -f /home/ubuntu/crypto_data_collector/log/trade_loader.log
```

### Kiểm tra processes
```bash
# Xem các process đang chạy
ps aux | grep python3

# Kill process nếu cần
pkill -f "python3.*cron_runner.py"
```

### Test kết nối database
```bash
# Chạy test connection
python3 -c "from load_to_sql_vps import load_to_db; import pandas as pd; df = pd.DataFrame({'test': [1]}); load_to_db('raw', 'test_table', df)"
```

## 8. Performance optimization

### Tăng memory cho Python
```bash
export PYTHONMALLOC=pymalloc
```

### Tối ưu TCP connections
```bash
# Thêm vào /etc/sysctl.conf
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_probes = 3
net.ipv4.tcp_keepalive_intvl = 90
```

## 9. Backup và recovery

### Backup định kỳ
```bash
# Thêm vào crontab backup logs
0 0 * * * tar -czf /home/ubuntu/backup/logs_$(date +\%Y\%m\%d).tar.gz /home/ubuntu/crypto_data_collector/log/
```

### Cleanup logs cũ
```bash
# Xóa logs cũ hơn 7 ngày
find /home/ubuntu/crypto_data_collector/log/ -name "*.log" -mtime +7 -delete
```

## 10. Security considerations

### Firewall
```bash
# Chỉ mở port cần thiết
sudo ufw enable
sudo ufw allow 22  # SSH
sudo ufw allow 1433  # SQL Server (nếu cần)
```

### File permissions
```bash
# Đảm bảo file permissions đúng
chmod 600 .env
chmod 755 *.py
chmod 755 *.sh
```

## Troubleshooting thường gặp

### Lỗi ODBC Driver
```bash
# Kiểm tra driver có sẵn
odbcinst -q -d
```

### Lỗi kết nối database
- Kiểm tra firewall
- Kiểm tra connection string
- Kiểm tra credentials

### Lỗi memory
- Tăng swap space
- Giảm số lượng concurrent processes

### Lỗi permissions
```bash
# Fix permissions
sudo chown -R ubuntu:ubuntu /home/ubuntu/crypto_data_collector
```
