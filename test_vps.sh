#!/bin/bash
# Test script to verify VPS deployment

echo "🔍 Testing VPS deployment..."

# Test Python installation
echo "📋 Python version:"
python3 --version

# Test pip packages
echo "📦 Testing Python packages..."
python3 -c "import pandas; print('✅ pandas OK')"
python3 -c "import sqlalchemy; print('✅ sqlalchemy OK')"
python3 -c "import pyodbc; print('✅ pyodbc OK')"
python3 -c "import websocket; print('✅ websocket OK')"
python3 -c "import requests; print('✅ requests OK')"

# Test Docker
echo "🐳 Docker version:"
docker --version
docker-compose --version

# Test database connection
echo "🗄️ Testing database connection..."
docker ps | grep mssql_server

# Test ODBC driver
echo "🔌 Testing ODBC driver..."
odbcinst -j
odbcinst -q -d | grep "SQL Server"

# Test network connectivity
echo "🌐 Testing network connectivity..."
ping -c 3 google.com

# Test ports
echo "🔌 Testing ports..."
netstat -tlnp | grep 1235

echo "🎯 Testing database connection with Python..."
python3 -c "
import pyodbc
try:
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost,1235;UID=sa;PWD=YourStrong!Pass123')
    print('✅ Database connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"

# Test cron service
echo "⏰ Testing cron service..."
systemctl status cron || systemctl status crond

# Test script permissions
echo "🔐 Testing script permissions..."
ls -la cron_wrapper.sh
ls -la setup_cron.sh
ls -la cron_manager.sh

echo "✅ VPS deployment test completed!"
