#!/bin/bash
# Cron job wrapper script - chạy mỗi phút trong 2 tiếng

# Đường dẫn đến project (thay đổi theo VPS của bạn)
PROJECT_DIR="/home/user/Demo"  # Thay đổi đường dẫn này
PYTHON_ENV="$PROJECT_DIR/venv/bin/python3"
SCRIPT_PATH="$PROJECT_DIR/scripts_get_data/main.py"
LOG_FILE="$PROJECT_DIR/scripts_get_data/log/cron_job.log"

# Chuyển đến thư mục project
cd "$PROJECT_DIR"

# Activate virtual environment và chạy script
echo "$(date): Starting crypto data collection..." >> "$LOG_FILE"
source venv/bin/activate
python3 scripts_get_data/main.py >> "$LOG_FILE" 2>&1
echo "$(date): Finished crypto data collection" >> "$LOG_FILE"
echo "----------------------------------------" >> "$LOG_FILE"
