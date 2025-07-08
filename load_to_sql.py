import pandas as pd
from sqlalchemy import create_engine
def load_to_db(schema_name, table_name, df):
    """
    Lưu DataFrame vào schema và bảng cụ thể trong cơ sở dữ liệu.
    """
    user_name='sa'
    password='YourStrong!Passw0rd'
    database='Coin_Analysis_DB'
    server='34.61.216.41,1433'  # IP VPS + port
    # Đảm bảo đã cài đặt ODBC Driver 17 cho SQL Server
    driver='ODBC Driver 17 for SQL Server'
    engine = create_engine(
        f"mssql+pyodbc://{user_name}:{password}@{server}/{database}?driver={driver}"
    )
    df.to_sql(table_name, con=engine, schema=schema_name, if_exists='append', index=False)
    print(f"Data saved to {schema_name}.{table_name}")