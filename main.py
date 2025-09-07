import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

# Cấu hình
API_TOKEN = os.environ.get('API_TOKEN', '8373272204:AAHBkXwttNCX-IG_JIjMDcpk1dgnrKeUCe8')
ADMIN_ID = os.environ.get('ADMIN_ID', '6002194595')
REQUIRED_GROUPS = ['-1002990515618', '-4941121629', '-1003060169211']

bot = telebot.TeleBot(API_TOKEN)

# Database đơn giản
users = {}
tasks = []
user_states = {}

# Hàm kiểm tra thành viên
def is_member_all_groups(user_id):
    # Tạm thời return True để test
    # Trên thực tế cần tích hợp API kiểm tra
    return True

# Lệnh start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"joined": False, "ref_count": 0}
    
    if is_member_all_groups(user_id):
        users[user_id]["joined"] = True
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📱 Mở Menu", callback_data="menu"))
        bot.send_message(message.chat.id, "✅ Chào mừng bạn! Bạn đã xác thực thành công.\nGõ /menu để xem tính năng.", reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        for i, group_id in enumerate(REQUIRED_GROUPS, 1):
            markup.add(InlineKeyboardButton(f"👥 Tham gia nhóm {i}", url="https://t.me/+dXQjLXuHPHk5NDM1"))
        markup.add(InlineKeyboardButton("🔄 Đã tham gia - Kiểm tra lại", callback_data="check_again"))
        bot.send_message(message.chat.id, "❌ Bạn chưa tham gia đầy đủ các nhóm! Vui lòng tham gia tất cả nhóm sau đó kiểm tra lại.", reply_markup=markup)

# Xử lý callback
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "menu":
        show_menu(call)
    elif call.data == "invite_ref":
        invite_ref(call)
    elif call.data == "check_again":
        check_again(call)

# Hiển thị menu
def show_menu(call):
    user_id = call.from_user.id
    markup = InlineKeyboardMarkup()
    
    if str(user_id) == ADMIN_ID:
        markup.add(InlineKeyboardButton("📤 Mời người dùng", callback_data="invite_ref"))
        markup.add(InlineKeyboardButton("➕ Thêm nhiệm vụ", callback_data="add_task"))
        markup.add(InlineKeyboardButton("📊 Xem số liệu", callback_data="stats"))
    else:
        markup.add(InlineKeyboardButton("📤 Mời người dùng", callback_data="invite_ref"))
        markup.add(InlineKeyboardButton("📝 Nhiệm vụ", callback_data="user_tasks"))
    
    bot.edit_message_text("🎛️ Chọn một tùy chọn:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# Mời người dùng
def invite_ref(call):
    user_id = call.from_user.id
    ref_link = f"https://t.me/ThanhTungVtabs_bot?start={user_id}"
    bot.edit_message_text(f"🔗 Link mời của bạn:\n`{ref_link}`\n\nMỗi người dùng tham gia qua link này sẽ được tính điểm ref của bạn!", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

# Kiểm tra lại
def check_again(call):
    user_id = call.from_user.id
    if is_member_all_groups(user_id):
        users[user_id]["joined"] = True
        bot.edit_message_text("✅ Xác thực thành công! Bạn đã tham gia đầy đủ các nhóm.\nGõ /menu để xem tính năng.", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "❌ Bạn vẫn chưa tham gia đầy đủ các nhóm!", show_alert=True)

# Chạy bot
if __name__ == "__main__":
    print("Bot đang chạy...")
    bot.infinity_polling()
