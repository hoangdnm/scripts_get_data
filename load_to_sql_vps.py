import pandas as pd
from sqlalchemy import create_engine
import os
import platform

# Load environment variables từ .env file nếu có
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Nếu không có python-dotenv, sẽ dùng system env vars

def load_to_db(schema_name, table_name, df):
    """
    Lưu DataFrame vào schema và bảng cụ thể trong cơ sở dữ liệu.
    """
    # Sử dụng environment variables hoặc config mặc định
    user_name = os.getenv('DB_USER', 'sa')
    password = os.getenv('DB_PASSWORD', 'YourStrong!Pass123')
    database = os.getenv('DB_NAME', 'Coin_Analysis_DB')
    server = os.getenv('DB_SERVER', 'localhost,1235')
    
    # Chọn driver phù hợp với OS
    system = platform.system().lower()
    if system == 'windows':
        driver = 'ODBC+Driver+17+for+SQL+Server'
    elif system == 'linux':
        # Kiểm tra driver có sẵn trên Linux
        try:
            import pyodbc
            drivers = pyodbc.drivers()
            if 'ODBC Driver 17 for SQL Server' in drivers:
                driver = 'ODBC+Driver+17+for+SQL+Server'
            elif 'ODBC Driver 18 for SQL Server' in drivers:
                driver = 'ODBC+Driver+18+for+SQL+Server'
            else:
                driver = 'ODBC+Driver+17+for+SQL+Server'  # Fallback
        except ImportError:
            driver = 'ODBC+Driver+17+for+SQL+Server'
    else:
        driver = 'ODBC+Driver+17+for+SQL+Server'  # Default
    
    try:
        # Thêm trust server certificate cho Linux
        connection_string = f"mssql+pyodbc://{user_name}:{password}@{server}/{database}?driver={driver}"
        
        # Thêm các tham số bổ sung cho VPS/Linux
        if system == 'linux':
            connection_string += "&TrustServerCertificate=yes"
        
        engine = create_engine(connection_string)
        df.to_sql(table_name, con=engine, schema=schema_name, if_exists='append', index=False)
        print(f"✅ Data saved to {schema_name}.{table_name} ({len(df)} rows)")
        
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        print(f"Connection string: {connection_string}")
        print(f"System: {system}")
        raise
