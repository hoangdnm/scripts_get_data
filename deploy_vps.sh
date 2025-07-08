#!/bin/bash
# VPS Deployment Script for Crypto Data Collection

echo "🚀 Starting VPS deployment..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python
echo "🐍 Installing Python and pip..."
sudo apt install python3-pip python3-venv python3-dev -y

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker

# Install Docker Compose
echo "📋 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install ODBC Driver for SQL Server (Ubuntu/Debian)
echo "🔌 Installing ODBC Driver for SQL Server..."
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# Create virtual environment
echo "🔧 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating log directories..."
mkdir -p scripts_get_data/log

# Fix permissions
echo "🔐 Setting permissions..."
chmod +x scripts_get_data/*.py

# Start database
echo "🗄️ Starting MSSQL database..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 30

# Create database
echo "🏗️ Creating database..."
docker exec mssql_server /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "YourStrong!Pass123" -Q "CREATE DATABASE Coin_Analysis_DB" || true

echo "✅ Deployment completed!"
echo "🎯 To run the application:"
echo "   source venv/bin/activate"
echo "   python3 scripts_get_data/main.py"
echo ""
echo "📊 To check logs:"
echo "   tail -f scripts_get_data/log/*.log"
echo ""
echo "🐳 To check database:"
echo "   docker logs mssql_server"
