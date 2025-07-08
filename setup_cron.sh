#!/bin/bash
# Script để setup cron job tự động dừng sau 2 tiếng

echo "🕐 Setting up cron job for 2 hours (120 minutes)..."

# Tạo file cron tạm thời
CRON_FILE="/tmp/crypto_cron.txt"
PROJECT_DIR="/home/user/Demo"  # Thay đổi đường dẫn này

# Lấy thời gian hiện tại
START_TIME=$(date +%s)
END_TIME=$((START_TIME + 7200))  # 2 hours = 7200 seconds

echo "📅 Start time: $(date -d @$START_TIME)"
echo "📅 End time: $(date -d @$END_TIME)"

# Tạo cron job chạy mỗi phút
echo "* * * * * $PROJECT_DIR/cron_wrapper.sh" > "$CRON_FILE"

# Tạo cron job để xóa cron sau 2 tiếng
echo "$(date -d @$END_TIME '+%M %H %d %m *') crontab -r" >> "$CRON_FILE"

# Cài đặt cron job
crontab "$CRON_FILE"

echo "✅ Cron job đã được thiết lập!"
echo "📊 Để kiểm tra:"
echo "   crontab -l"
echo "📋 Để xem log:"
echo "   tail -f $PROJECT_DIR/scripts_get_data/log/cron_job.log"
echo "🛑 Để dừng sớm:"
echo "   crontab -r"

# Xóa file tạm
rm "$CRON_FILE"

# Hiển thị cron job hiện tại
echo "🔍 Current cron jobs:"
crontab -l
