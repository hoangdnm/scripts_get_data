import subprocess
import time
import os
import sys
import logging
from datetime import datetime

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main_process.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Lấy thư mục hiện tại của script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Danh sách các file cần chạy (sử dụng path tương đối)
files = [
    'get_candle_raw_data.py',
    'get_ticker_raw_data.py', 
    'get_trade_raw_data.py'
]

def run_scripts():
    """Chạy tất cả các script thu thập dữ liệu"""
    start_time = datetime.now()
    logging.info(f"Bắt đầu chạy tại: {start_time}")
    
    processes = []
    
    try:
        # Khởi động tất cả tiến trình
        for file in files:
            file_path = os.path.join(current_dir, file)
            if os.path.exists(file_path):
                logging.info(f"Đang chạy {file}...")
                # Sử dụng python3 thay vì python cho VPS Linux
                python_cmd = sys.executable if sys.executable else 'python3'
                p = subprocess.Popen([python_cmd, file_path], 
                                   cwd=current_dir,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
                processes.append((p, file))
            else:
                logging.error(f"File không tồn tại: {file_path}")
        
        # Chờ tất cả tiến trình hoàn tất
        for p, file in processes:
            stdout, stderr = p.communicate()
            if p.returncode == 0:
                logging.info(f"✅ {file} hoàn thành thành công")
            else:
                logging.error(f"❌ {file} lỗi: {stderr.decode()}")
    
    except Exception as e:
        logging.error(f"❌ Lỗi trong quá trình chạy: {e}")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logging.info(f"Hoàn thành tại: {end_time}, thời gian: {duration:.2f} giây")

if __name__ == "__main__":
    run_scripts()
