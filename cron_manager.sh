#!/bin/bash
# Script để giám sát và quản lý cron job

echo "📊 Crypto Data Collection Cron Job Manager"
echo "=========================================="

while true; do
    echo ""
    echo "1. 🚀 Setup cron job (2 hours from now)"
    echo "2. ⏰ Setup cron job (specific time range)"
    echo "3. 📋 View current cron jobs"
    echo "4. 📊 View logs (live)"
    echo "5. 📈 View log summary"
    echo "6. 🛑 Stop cron job"
    echo "7. 🔄 Restart cron job"
    echo "8. 🚪 Exit"
    echo ""
    
    read -p "Select option (1-8): " choice
    
    case $choice in
        1)
            echo "🚀 Setting up cron job for 2 hours..."
            chmod +x setup_cron.sh
            ./setup_cron.sh
            ;;
        2)
            echo "⏰ Setting up cron job with specific time..."
            chmod +x setup_cron_time.sh
            ./setup_cron_time.sh
            ;;
        3)
            echo "📋 Current cron jobs:"
            crontab -l
            ;;
        4)
            echo "📊 Viewing logs (Press Ctrl+C to exit)..."
            tail -f scripts_get_data/log/cron_job.log
            ;;
        5)
            echo "📈 Log summary:"
            echo "Total runs: $(grep -c "Starting crypto data collection" scripts_get_data/log/cron_job.log)"
            echo "Errors: $(grep -c "Error\|Failed\|❌" scripts_get_data/log/cron_job.log)"
            echo "Success: $(grep -c "✅\|Success" scripts_get_data/log/cron_job.log)"
            echo ""
            echo "Last 5 runs:"
            tail -n 20 scripts_get_data/log/cron_job.log | grep "Starting crypto data collection" | tail -5
            ;;
        6)
            echo "🛑 Stopping cron job..."
            crontab -r
            echo "✅ Cron job stopped!"
            ;;
        7)
            echo "🔄 Restarting cron job..."
            crontab -r
            sleep 2
            chmod +x setup_cron.sh
            ./setup_cron.sh
            ;;
        8)
            echo "🚪 Exiting..."
            exit 0
            ;;
        *)
            echo "❌ Invalid option. Please select 1-8."
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done
