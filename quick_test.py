#!/usr/bin/env python3
"""
Quick Test Script - Test nhanh các component chính
"""
import os
import sys
import time
import logging
from datetime import datetime

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler('quick_test.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def quick_test_database():
    """Test nhanh database connection"""
    logger = logging.getLogger(__name__)
    logger.info("🔍 Testing database connection...")
    
    try:
        from load_to_sql_vps import load_to_db
        import pandas as pd
        
        # Tạo test data
        test_df = pd.DataFrame({
            'test_id': [1],
            'test_message': ['Quick test'],
            'timestamp': [datetime.now()]
        })
        
        # Test connection
        load_to_db('raw', 'quick_test', test_df)
        logger.info("✅ Database connection: OK")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection: FAILED - {e}")
        return False

def quick_test_websocket():
    """Test nhanh websocket connection"""
    logger = logging.getLogger(__name__)
    logger.info("🔍 Testing WebSocket connection...")
    
    try:
        from ws_client import BitgetWS
        from rest_api import target_list_coin
        
        # Test với 1 coin và thời gian ngắn
        df = BitgetWS(
            inst_type="SPOT",
            channel="ticker",
            inst_ids=target_list_coin[:1],  # Chỉ test 1 coin
            dur_sec=2
        ).run()
        
        if len(df) > 0:
            logger.info("✅ WebSocket connection: OK")
            return True
        else:
            logger.error("❌ WebSocket connection: No data received")
            return False
            
    except Exception as e:
        logger.error(f"❌ WebSocket connection: FAILED - {e}")
        return False

def quick_test_scripts():
    """Test nhanh các script chính"""
    logger = logging.getLogger(__name__)
    logger.info("🔍 Testing main scripts...")
    
    try:
        # Test import các module chính
        import main
        import cron_runner
        import health_check
        
        logger.info("✅ Script imports: OK")
        return True
        
    except Exception as e:
        logger.error(f"❌ Script imports: FAILED - {e}")
        return False

def main():
    """Quick test runner"""
    logger = setup_logging()
    
    logger.info("🚀 QUICK TEST - Crypto Data Collector")
    logger.info("=" * 50)
    
    tests = [
        ("Scripts Import", quick_test_scripts),
        ("Database Connection", quick_test_database),
        ("WebSocket Connection", quick_test_websocket)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"Test {test_name} failed: {e}")
            results[test_name] = False
    
    # Kết quả
    passed = sum(results.values())
    total = len(results)
    
    logger.info("=" * 50)
    logger.info(f"📊 QUICK TEST RESULTS: {passed}/{total}")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"   {test_name}: {status}")
    
    if passed == total:
        logger.info("🎉 Quick test PASSED! Hệ thống hoạt động cơ bản.")
        logger.info("💡 Chạy 'python run_tests.py' để test đầy đủ.")
        return True
    else:
        logger.error("❌ Quick test FAILED! Kiểm tra lại cấu hình.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
