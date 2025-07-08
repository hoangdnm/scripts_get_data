#!/usr/bin/env python3
"""
Health Check Script - Kiểm tra tình trạng hệ thống
"""
import os
import sys
import time
import logging
import psutil
import subprocess
from datetime import datetime

class HealthChecker:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('health_check.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_python_packages(self):
        """Kiểm tra các package Python cần thiết"""
        required_packages = [
            'pandas', 'sqlalchemy', 'pyodbc', 'websocket-client', 'requests'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                self.logger.info(f"✅ Package {package} - OK")
            except ImportError:
                missing_packages.append(package)
                self.logger.error(f"❌ Package {package} - MISSING")
        
        return len(missing_packages) == 0
    
    def check_database_connection(self):
        """Kiểm tra kết nối database"""
        try:
            from load_to_sql_vps import load_to_db
            import pandas as pd
            
            # Tạo test dataframe
            test_df = pd.DataFrame({
                'test_col': [1, 2, 3],
                'timestamp': [datetime.now()] * 3
            })
            
            # Thử kết nối (không thực sự insert)
            load_to_db('raw', 'health_check_test', test_df)
            self.logger.info("✅ Database connection - OK")
            return True
        except Exception as e:
            self.logger.error(f"❌ Database connection - FAILED: {e}")
            return False
    
    def check_file_permissions(self):
        """Kiểm tra quyền file"""
        critical_files = [
            'main.py', 'cron_runner.py', 'load_to_sql_vps.py',
            'get_candle_raw_data.py', 'get_ticker_raw_data.py', 'get_trade_raw_data.py'
        ]
        
        all_good = True
        for file in critical_files:
            file_path = os.path.join(self.current_dir, file)
            if os.path.exists(file_path):
                if os.access(file_path, os.R_OK):
                    self.logger.info(f"✅ File {file} - Readable")
                else:
                    self.logger.error(f"❌ File {file} - NOT Readable")
                    all_good = False
            else:
                self.logger.error(f"❌ File {file} - NOT Found")
                all_good = False
        
        return all_good
    
    def check_system_resources(self):
        """Kiểm tra tài nguyên hệ thống"""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        self.logger.info(f"🖥️  CPU Usage: {cpu_percent}%")
        
        # Memory
        memory = psutil.virtual_memory()
        self.logger.info(f"💾 Memory Usage: {memory.percent}% ({memory.used/1024/1024/1024:.1f}GB/{memory.total/1024/1024/1024:.1f}GB)")
        
        # Disk
        disk = psutil.disk_usage(self.current_dir)
        self.logger.info(f"💿 Disk Usage: {disk.percent}% ({disk.used/1024/1024/1024:.1f}GB/{disk.total/1024/1024/1024:.1f}GB)")
        
        # Network
        net = psutil.net_io_counters()
        self.logger.info(f"🌐 Network: Sent {net.bytes_sent/1024/1024:.1f}MB, Received {net.bytes_recv/1024/1024:.1f}MB")
        
        # Warning thresholds
        warnings = []
        if cpu_percent > 80:
            warnings.append(f"High CPU usage: {cpu_percent}%")
        if memory.percent > 80:
            warnings.append(f"High memory usage: {memory.percent}%")
        if disk.percent > 90:
            warnings.append(f"High disk usage: {disk.percent}%")
        
        return warnings
    
    def check_processes(self):
        """Kiểm tra các process đang chạy"""
        python_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] in ['python', 'python3']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    if 'cron_runner.py' in cmdline or 'main.py' in cmdline:
                        python_processes.append({
                            'pid': proc.info['pid'],
                            'cmdline': cmdline
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if python_processes:
            self.logger.info(f"🏃 Running processes: {len(python_processes)}")
            for proc in python_processes:
                self.logger.info(f"   PID {proc['pid']}: {proc['cmdline']}")
        else:
            self.logger.warning("⚠️  No crypto data collector processes found")
        
        return len(python_processes) > 0
    
    def check_log_files(self):
        """Kiểm tra log files"""
        log_dir = os.path.join(self.current_dir, 'log')
        if not os.path.exists(log_dir):
            self.logger.warning("⚠️  Log directory not found")
            return False
        
        log_files = ['candle_loader.log', 'ticker_loader.log', 'trade_loader.log']
        for log_file in log_files:
            log_path = os.path.join(log_dir, log_file)
            if os.path.exists(log_path):
                size = os.path.getsize(log_path)
                modified = datetime.fromtimestamp(os.path.getmtime(log_path))
                self.logger.info(f"📄 {log_file}: {size} bytes, modified {modified}")
            else:
                self.logger.warning(f"⚠️  Log file not found: {log_file}")
        
        return True
    
    def run_health_check(self):
        """Chạy tất cả health checks"""
        self.logger.info("🔍 Starting health check...")
        
        results = {
            'packages': self.check_python_packages(),
            'database': self.check_database_connection(),
            'files': self.check_file_permissions(),
            'logs': self.check_log_files(),
            'processes': self.check_processes()
        }
        
        warnings = self.check_system_resources()
        
        # Tổng kết
        passed = sum(results.values())
        total = len(results)
        
        self.logger.info(f"📊 Health Check Results: {passed}/{total} checks passed")
        
        if warnings:
            self.logger.warning("⚠️  System warnings:")
            for warning in warnings:
                self.logger.warning(f"   - {warning}")
        
        if passed == total and not warnings:
            self.logger.info("✅ All systems healthy!")
            return True
        else:
            self.logger.error("❌ Some issues detected")
            return False

def main():
    checker = HealthChecker()
    success = checker.run_health_check()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
