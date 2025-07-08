#!/usr/bin/env python3
"""
Cron job runner - Chạy liên tục trong 2 tiếng, mỗi phút chạy 1 lần
"""
import os
import sys
import time
import logging
import subprocess
from datetime import datetime, timedelta
import signal

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cron_runner.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class CronRunner:
    def __init__(self, duration_hours=2.0):
        self.duration_hours = duration_hours
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.main_script = os.path.join(self.current_dir, 'main.py')
        self.running = True
        
        # Đăng ký signal handler cho graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Xử lý tín hiệu dừng"""
        logging.info(f"Nhận tín hiệu {signum}, đang dừng...")
        self.running = False
    
    def run_main_script(self):
        """Chạy main.py"""
        try:
            python_cmd = sys.executable if sys.executable else 'python3'
            result = subprocess.run([python_cmd, self.main_script], 
                                  cwd=self.current_dir,
                                  capture_output=True,
                                  text=True,
                                  timeout=50)  # Timeout 50s để đảm bảo hoàn thành trong 1 phút
            
            if result.returncode == 0:
                logging.info("✅ Main script chạy thành công")
                return True
            else:
                logging.error(f"❌ Main script lỗi: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logging.error("❌ Main script timeout (>50s)")
            return False
        except Exception as e:
            logging.error(f"❌ Lỗi khi chạy main script: {e}")
            return False
    
    def run(self):
        """Chạy cron job trong thời gian xác định"""
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=self.duration_hours)
        
        logging.info(f"🚀 Bắt đầu cron job - Chạy từ {start_time} đến {end_time}")
        logging.info(f"📊 Sẽ chạy mỗi 60 giây trong {self.duration_hours} tiếng")
        
        cycle_count = 0
        success_count = 0
        
        while self.running and datetime.now() < end_time:
            cycle_start = datetime.now()
            cycle_count += 1
            
            logging.info(f"📅 Cycle {cycle_count} - {cycle_start.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Chạy main script
            if self.run_main_script():
                success_count += 1
            
            # Tính thời gian đã chạy và thời gian chờ
            cycle_duration = (datetime.now() - cycle_start).total_seconds()
            wait_time = max(0, 60 - cycle_duration)  # Chờ để tròn 60s
            
            if wait_time > 0 and self.running:
                logging.info(f"⏳ Chờ {wait_time:.1f}s cho cycle tiếp theo...")
                time.sleep(wait_time)
        
        # Thống kê cuối
        total_duration = (datetime.now() - start_time).total_seconds()
        success_rate = (success_count / cycle_count * 100) if cycle_count > 0 else 0
        
        logging.info(f"🏁 Kết thúc cron job:")
        logging.info(f"   - Tổng thời gian chạy: {total_duration/3600:.2f} giờ")
        logging.info(f"   - Tổng số cycle: {cycle_count}")
        logging.info(f"   - Thành công: {success_count}/{cycle_count} ({success_rate:.1f}%)")

def main():
    """Entry point"""
    # Kiểm tra arguments
    duration_hours = 2
    if len(sys.argv) > 1:
        try:
            duration_hours = float(sys.argv[1])
        except ValueError:
            logging.error("Tham số thời gian không hợp lệ")
            sys.exit(1)
    
    # Chạy cron runner
    runner = CronRunner(duration_hours)
    runner.run()

if __name__ == "__main__":
    main()
