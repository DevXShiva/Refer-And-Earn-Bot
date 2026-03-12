import os
import logging
import datetime
import asyncio
import threading
import time
from flask import Flask
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
import motor.motor_asyncio

# --- CONFIGURATION ---
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- FLASK SERVER ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "Bot is alive! 🚀 Aiogram Mode ON", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- BOT CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
FSUB_CHANNEL_IDS = [int(x) for x in os.getenv("FSUB_CHANNEL_IDS", "").split(",") if x.strip()]

# --- 💎 WITHDRAWAL CONFIG (Updated with Big Basket) 💎 ---
COUPON_CONFIG = {
    500: {"cost": 1, "name": "SHEIN"},
    1000: {"cost": 5, "name": "SHEIN"},
    1500: {"cost": 10, "name": "BIG BASKET 🛒"}, # New Big Basket Option
    2000: {"cost": 25, "name": "SHEIN"},
    4000: {"cost": 35, "name": "SHEIN"}
}

# --- DATABASE ---
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client['shein_bot_db']
users_col, coupons_col, redeemed_col, admin_logs_col = db.users, db.coupons, db.redeemed, db.admin_logs

# --- FSM STATES ---
class AdminStates(StatesGroup):
    waiting_for_coupons = State()

# --- SPEED CACHE ---
user_fsub_cache = {}
CACHE_DURATION = 60 

# --- INITIALIZE BOT ---
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# --- KEYBOARDS ---
def main_menu_kb():
    kb = [
        [KeyboardButton(text="🔗 My Link"), KeyboardButton(text="💎 Balance")],
        [KeyboardButton(text="🎟 Coupon Stock"), KeyboardButton(text="💸 Withdraw")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# --- FSUB LOGIC ---
async def is_member(user_id: int):
    if not FSUB_CHANNEL_IDS: return True
    for ch_id in FSUB_CHANNEL_IDS:
        try:
            member = await bot.get_chat_member(ch_id, user_id)
            if member.status in ["left", "kicked"]: return False
        except: return False
    return True

# --- HANDLERS ---

@dp.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    referrer_id = int(command.args) if command.args and command.args.isdigit() and int(command.args) != user_id else None
    
    if not await is_member(user_id):
        kb = [[InlineKeyboardButton(text="📢 Join Channel", url=f"https://t.me/yourchannel")]] # Add link logic here
        kb.append([InlineKeyboardButton(text="✅ Joined", callback_data="check_join")])
        await message.answer("⛔️ <b>Access Denied!</b>\nPlease join our channels to use the bot.", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))
        return

    user = await users_col.find_one({'user_id': user_id})
    if not user:
        await users_col.insert_one({
            'user_id': user_id, 'balance': 0.0, 'referred_by': referrer_id, 'created_at': datetime.datetime.now(), 'last_active': datetime.datetime.now()
        })
        if referrer_id:
            await users_col.update_one({'user_id': referrer_id}, {'$inc': {'balance': 1.0, 'referral_count': 1}})
            if LOG_CHANNEL_ID: await bot.send_message(LOG_CHANNEL_ID, f"#NewUser Joined via {referrer_id}")

    await message.answer(f"👋 Welcome {message.from_user.first_name}!", reply_markup=main_menu_kb())

@dp.message(F.text == "🔗 My Link")
async def my_link(message: types.Message):
    me = await bot.get_me()
    link = f"https://t.me/{me.username}?start={message.from_user.id}"
    await message.answer(f"🔗 <b>Your Link:</b>\n{link}\n\nEarn 1 💎 per referral!")

@dp.message(F.text == "💎 Balance")
async def balance_check(message: types.Message):
    user = await users_col.find_one({'user_id': message.from_user.id})
    await message.answer(f"💎 <b>Balance:</b> {user['balance']} 💎")

@dp.message(F.text == "🎟 Coupon Stock")
async def stock_check(message: types.Message):
    text = "🎟 <b>Current Stock:</b>\n\n"
    for amt, data in COUPON_CONFIG.items():
        count = await coupons_col.count_documents({'amount': amt, 'is_used': False})
        text += f"• {data['name']} ({amt} 🎟): {count}\n"
    await message.answer(text)

@dp.message(F.text == "💸 Withdraw")
async def withdraw_menu(message: types.Message):
    user = await users_col.find_one({'user_id': message.from_user.id})
    if user['balance'] <= 0:
        await message.answer("❌ Insufficient Balance!")
        return
    
    kb = []
    for amt, data in COUPON_CONFIG.items():
        kb.append([InlineKeyboardButton(text=f"{data['name']} {amt} (Cost: {data['cost']} 💎)", callback_data=f"redeem_{amt}")])
    
    await message.answer("💸 <b>Select withdrawal amount:</b>", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

@dp.callback_query(F.data.startswith("redeem_"))
async def redeem_process(callback: types.CallbackQuery):
    amount = int(callback.data.split("_")[1])
    cost = COUPON_CONFIG[amount]['cost']
    user_id = callback.from_user.id
    
    user = await users_col.find_one({'user_id': user_id})
    if user['balance'] < cost:
        await callback.answer("❌ Not enough diamonds!", show_alert=True)
        return

    coupon = await coupons_col.find_one_and_update(
        {'amount': amount, 'is_used': False},
        {'$set': {'is_used': True, 'used_by': user_id, 'used_at': datetime.datetime.now()}}
    )

    if not coupon:
        await callback.answer("❌ Out of stock!", show_alert=True)
        return

    await users_col.update_one({'user_id': user_id}, {'$inc': {'balance': -float(cost)}})
    await callback.message.edit_text(f"✅ <b>Redeemed!</b>\n\nType: {COUPON_CONFIG[amount]['name']}\nCode: <code>{coupon['code']}</code>")

# --- ADMIN COMMANDS ---

@dp.message(Command("admin"), F.from_user.id.in_(ADMIN_IDS))
async def admin_panel(message: types.Message):
    kb = []
    for amt, data in COUPON_CONFIG.items():
        kb.append([InlineKeyboardButton(text=f"➕ Add {data['name']} ({amt})", callback_data=f"admin_add_{amt}")])
    await message.answer("👑 <b>Admin Panel:</b>", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

@dp.callback_query(F.data.startswith("admin_add_"))
async def admin_add_start(callback: types.CallbackQuery, state: FSMContext):
    amount = int(callback.data.split("_")[2])
    await state.update_data(add_amt=amount)
    await callback.message.answer(f"Send codes for {amount} 🎟 (one per line):")
    await state.set_state(AdminStates.waiting_for_coupons)

@dp.message(AdminStates.waiting_for_coupons)
async def admin_save_codes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    amount = data['add_amt']
    codes = [c.strip() for c in message.text.splitlines() if c.strip()]
    
    added = 0
    for code in codes:
        if not await coupons_col.find_one({'code': code}):
            await coupons_col.insert_one({'code': code, 'amount': amount, 'is_used': False, 'added_at': datetime.datetime.now()})
            added += 1
            
    await message.answer(f"✅ Added {added} new coupons for {amount} 🎟.")
    await state.clear()

@dp.message(Command("delete"), F.from_user.id.in_(ADMIN_IDS))
async def delete_codes(message: types.Message, command: CommandObject):
    if not command.args: return
    codes = command.args.split()
    res = await coupons_col.delete_many({'code': {'$in': codes}})
    await message.answer(f"🗑 Deleted {res.deleted_count} codes.")

# --- START BOT ---
async def main():
    threading.Thread(target=run_flask, daemon=True).start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        logger.info("Bot Stopped")
