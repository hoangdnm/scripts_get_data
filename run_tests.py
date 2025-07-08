#!/usr/bin/env python3
"""
Test Script - Chạy test toàn bộ hệ thống
"""
import os
import sys
import time
import subprocess
import logging
from datetime import datetime

class TestRunner:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging cho test"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('test_results.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def test_python_environment(self):
        """Test 1: Kiểm tra Python environment"""
        self.logger.info("🧪 Test 1: Python Environment")
        
        # Kiểm tra Python version
        python_version = sys.version_info
        self.logger.info(f"   Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
            self.logger.error("   ❌ Python version phải >= 3.7")
            return False
        
        self.logger.info("   ✅ Python version OK")
        return True
    
    def test_dependencies(self):
        """Test 2: Kiểm tra dependencies"""
        self.logger.info("🧪 Test 2: Dependencies")
        
        required_packages = [
            'pandas', 'sqlalchemy', 'pyodbc', 'websocket-client', 'requests', 'psutil'
        ]
        
        missing = []
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                self.logger.info(f"   ✅ {package}")
            except ImportError:
                missing.append(package)
                self.logger.error(f"   ❌ {package} - MISSING")
        
        if missing:
            self.logger.error(f"   Cần cài đặt: pip install {' '.join(missing)}")
            return False
        
        return True
    
    def test_files_exist(self):
        """Test 3: Kiểm tra files cần thiết"""
        self.logger.info("🧪 Test 3: Required Files")
        
        required_files = [
            'main.py', 'cron_runner.py', 'health_check.py',
            'load_to_sql_vps.py', 'get_candle_raw_data.py', 
            'get_ticker_raw_data.py', 'get_trade_raw_data.py',
            'ws_client.py', 'rest_api.py', 'requirements.txt'
        ]
        
        missing = []
        for file in required_files:
            if os.path.exists(file):
                self.logger.info(f"   ✅ {file}")
            else:
                missing.append(file)
                self.logger.error(f"   ❌ {file} - NOT FOUND")
        
        return len(missing) == 0
    
    def test_database_connection(self):
        """Test 4: Kiểm tra kết nối database"""
        self.logger.info("🧪 Test 4: Database Connection")
        
        try:
            from load_to_sql_vps import load_to_db
            import pandas as pd
            
            # Tạo test dataframe nhỏ
            test_df = pd.DataFrame({
                'test_id': [1, 2],
                'test_value': ['test1', 'test2'],
                'timestamp': [datetime.now(), datetime.now()]
            })
            
            # Thử kết nối (chỉ test connection, không insert thật)
            self.logger.info("   Testing database connection...")
            load_to_db('raw', 'test_connection', test_df)
            self.logger.info("   ✅ Database connection OK")
            return True
            
        except Exception as e:
            self.logger.error(f"   ❌ Database connection failed: {e}")
            return False
    
    def test_individual_scripts(self):
        """Test 5: Chạy thử từng script individual"""
        self.logger.info("🧪 Test 5: Individual Scripts")
        
        scripts = [
            'get_candle_raw_data.py',
            'get_ticker_raw_data.py', 
            'get_trade_raw_data.py'
        ]
        
        results = {}
        python_cmd = sys.executable if sys.executable else 'python3'
        
        for script in scripts:
            try:
                self.logger.info(f"   Testing {script}...")
                result = subprocess.run(
                    [python_cmd, script],
                    cwd=self.current_dir,
                    capture_output=True,
                    text=True,
                    timeout=30  # 30s timeout
                )
                
                if result.returncode == 0:
                    self.logger.info(f"   ✅ {script} - OK")
                    results[script] = True
                else:
                    self.logger.error(f"   ❌ {script} - FAILED")
                    self.logger.error(f"      Error: {result.stderr}")
                    results[script] = False
                    
            except subprocess.TimeoutExpired:
                self.logger.error(f"   ❌ {script} - TIMEOUT")
                results[script] = False
            except Exception as e:
                self.logger.error(f"   ❌ {script} - ERROR: {e}")
                results[script] = False
        
        return all(results.values())
    
    def test_main_script(self):
        """Test 6: Chạy thử main.py"""
        self.logger.info("🧪 Test 6: Main Script")
        
        try:
            python_cmd = sys.executable if sys.executable else 'python3'
            result = subprocess.run(
                [python_cmd, 'main.py'],
                cwd=self.current_dir,
                capture_output=True,
                text=True,
                timeout=60  # 60s timeout
            )
            
            if result.returncode == 0:
                self.logger.info("   ✅ Main script OK")
                return True
            else:
                self.logger.error(f"   ❌ Main script failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("   ❌ Main script timeout")
            return False
        except Exception as e:
            self.logger.error(f"   ❌ Main script error: {e}")
            return False
    
    def test_cron_runner_short(self):
        """Test 7: Chạy thử cron runner trong thời gian ngắn"""
        self.logger.info("🧪 Test 7: Cron Runner (Short Test)")
        
        try:
            python_cmd = sys.executable if sys.executable else 'python3'
            self.logger.info("   Running cron_runner.py for 2 minutes...")
            
            result = subprocess.run(
                [python_cmd, 'cron_runner.py', '0.033'],  # 2 phút = 0.033 giờ
                cwd=self.current_dir,
                capture_output=True,
                text=True,
                timeout=150  # 150s timeout
            )
            
            if result.returncode == 0:
                self.logger.info("   ✅ Cron runner test OK")
                return True
            else:
                self.logger.error(f"   ❌ Cron runner failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("   ❌ Cron runner timeout")
            return False
        except Exception as e:
            self.logger.error(f"   ❌ Cron runner error: {e}")
            return False
    
    def test_health_check(self):
        """Test 8: Chạy health check"""
        self.logger.info("🧪 Test 8: Health Check")
        
        try:
            python_cmd = sys.executable if sys.executable else 'python3'
            result = subprocess.run(
                [python_cmd, 'health_check.py'],
                cwd=self.current_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.logger.info("   ✅ Health check OK")
                return True
            else:
                self.logger.error(f"   ❌ Health check failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("   ❌ Health check timeout")
            return False
        except Exception as e:
            self.logger.error(f"   ❌ Health check error: {e}")
            return False
    
    def run_all_tests(self):
        """Chạy tất cả tests"""
        self.logger.info("🚀 Bắt đầu test toàn bộ hệ thống")
        self.logger.info("=" * 50)
        
        tests = [
            ("Python Environment", self.test_python_environment),
            ("Dependencies", self.test_dependencies),
            ("Required Files", self.test_files_exist),
            ("Database Connection", self.test_database_connection),
            ("Individual Scripts", self.test_individual_scripts),
            ("Main Script", self.test_main_script),
            ("Cron Runner", self.test_cron_runner_short),
            ("Health Check", self.test_health_check)
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                self.logger.error(f"Test {test_name} failed with exception: {e}")
                results[test_name] = False
            
            self.logger.info("-" * 30)
        
        # Tổng kết
        passed = sum(results.values())
        total = len(results)
        
        self.logger.info("=" * 50)
        self.logger.info(f"📊 KẾT QUẢ TEST: {passed}/{total} tests passed")
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.logger.info(f"   {test_name}: {status}")
        
        if passed == total:
            self.logger.info("🎉 TẤT CẢ TEST THÀNH CÔNG! Hệ thống sẵn sàng deploy.")
            return True
        else:
            self.logger.error("❌ CÓ TEST THẤT BẠI! Vui lòng kiểm tra lại.")
            return False

def main():
    """Entry point"""
    runner = TestRunner()
    success = runner.run_all_tests()
    
    print("\n" + "="*50)
    if success:
        print("🎉 KHAI BÁO: Hệ thống đã sẵn sàng cho production!")
        print("Bạn có thể deploy lên VPS và setup cron job.")
    else:
        print("❌ CẢNH BÁO: Hệ thống chưa sẵn sàng!")
        print("Vui lòng sửa các lỗi trước khi deploy.")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
