import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from telegram.constants import ParseMode

# Lấy biến môi trường (Render sẽ cung cấp)
API_TOKEN = os.environ.get('API_TOKEN', '8373272204:AAHBkXwttNCX-IG_JIjMDcpk1dgnrKeUCe8')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '6002194595'))
GROUP_ID = os.environ.get('GROUP_ID', '-1001234567890')  # Thay bằng ID nhóm thật của bạn

# Các phần còn lại của code giữ nguyên (như trong hướng dẫn trước)
# ... (dán toàn bộ code từ hướng dẫn trước vào đây, từ phần `ADD_TASK = range(1)` đến `main()`)

# Sửa phần main() để chạy webhook trên Render
def main():
    # Tạo Application
    application = Application.builder().token(API_TOKEN).build()

    # Thêm handlers (giống như trước)
    # ... (dán các handlers từ code cũ)

    # Chạy webhook (cho Render)
    if 'RENDER' in os.environ:
        # Trên Render
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get('PORT', 10000)),
            url_path=API_TOKEN,
            webhook_url=f"https://your-bot-name.onrender.com/{API_TOKEN}"
        )
    else:
        # Chạy local (cho testing)
        application.run_polling()

if __name__ == "__main__":
    main()
