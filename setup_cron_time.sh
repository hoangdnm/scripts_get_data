#!/bin/bash
# Script để setup cron job với thời gian cụ thể

echo "🕐 Setting up cron job with specific time range..."

# Nhập thời gian bắt đầu và kết thúc
read -p "Enter start time (HH:MM, e.g., 09:30): " START_TIME
read -p "Enter end time (HH:MM, e.g., 11:30): " END_TIME

# Tách giờ và phút
START_HOUR=$(echo $START_TIME | cut -d':' -f1)
START_MIN=$(echo $START_TIME | cut -d':' -f2)
END_HOUR=$(echo $END_TIME | cut -d':' -f1)
END_MIN=$(echo $END_TIME | cut -d':' -f2)

PROJECT_DIR="/home/user/Demo"  # Thay đổi đường dẫn này
CRON_FILE="/tmp/crypto_cron_time.txt"

# Tạo cron job chạy mỗi phút trong khoảng thời gian chỉ định
if [ "$START_HOUR" -le "$END_HOUR" ]; then
    # Cùng ngày
    echo "* $START_HOUR-$END_HOUR * * * $PROJECT_DIR/cron_wrapper.sh" > "$CRON_FILE"
else
    # Qua ngày (ví dụ: 23:00 - 01:00)
    echo "* $START_HOUR-23,0-$END_HOUR * * * $PROJECT_DIR/cron_wrapper.sh" > "$CRON_FILE"
fi

# Cài đặt cron job
crontab "$CRON_FILE"

echo "✅ Cron job đã được thiết lập từ $START_TIME đến $END_TIME!"
echo "📊 Để kiểm tra:"
echo "   crontab -l"
echo "📋 Để xem log:"
echo "   tail -f $PROJECT_DIR/scripts_get_data/log/cron_job.log"
echo "🛑 Để dừng:"
echo "   crontab -r"

# Xóa file tạm
rm "$CRON_FILE"

# Hiển thị cron job hiện tại
echo "🔍 Current cron jobs:"
crontab -l
