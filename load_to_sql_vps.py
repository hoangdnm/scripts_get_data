import pandas as pd
from sqlalchemy import create_engine
import os

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
    if os.name == 'nt':  # Windows
        driver = 'ODBC+Driver+17+for+SQL+Server'
    else:  # Linux/Unix
        driver = 'ODBC+Driver+17+for+SQL+Server'
    
    try:
        engine = create_engine(
            f"mssql+pyodbc://{user_name}:{password}@{server}/{database}?driver={driver}"
        )
        df.to_sql(table_name, con=engine, schema=schema_name, if_exists='append', index=False)
        print(f"✅ Data saved to {schema_name}.{table_name}")
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        raise
