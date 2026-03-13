import os
import logging
import datetime
import asyncio
import threading
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

# --- CUSTOM BUTTON CLASS ---
class StyledButton(InlineKeyboardButton):
    def __init__(self, text, callback_data=None, url=None, style=None, **kwargs):
        super().__init__(text=text, callback_data=callback_data, url=url, **kwargs)
        self.style = style

# --- CONFIGURATION ---
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- BOT CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# --- 💎 WITHDRAWAL CONFIG 💎 ---
# Yahan humne specify kiya hai ki kis button ka style kya hoga
COUPON_CONFIG = {
    500: {"cost": 1, "name": "SHEIN", "style": "default"}, # Normal button
    1000: {"cost": 5, "name": "SHEIN", "style": "default"}, # Normal button
    1500: {"cost": 4, "name": "BIG BASKET 🛒", "style": "success"}, # Green button
    2000: {"cost": 25, "name": "SHEIN", "style": "default"},
    4000: {"cost": 35, "name": "SHEIN", "style": "default"}
}

# --- DATABASE ---
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client['shein_bot_db']
users_col, coupons_col = db.users, db.coupons

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# --- KEYBOARDS ---

def get_withdrawal_keyboard():
    keyboard = []
    
    # Coupons buttons loop
    for amt, data in COUPON_CONFIG.items():
        # Specific style allocation
        btn_style = data.get("style", "default") 
        
        keyboard.append([
            StyledButton(
                text=f"{data['name']} {amt} (Cost: {data['cost']} 💎)", 
                callback_data=f"redeem_{amt}",
                style=btn_style # Sirf Big Basket success hoga, baaki default
            )
        ])
    
    # Final Action Buttons
    # Yahan Delete hamesha Red (danger) aur Confirm hamesha Green (success) rahega
    keyboard.append([
        StyledButton(text="❌ Delete", callback_data="del", style="danger"),
        StyledButton(text="✅ Confirm", callback_data="ok", style="success")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- HANDLERS ---

@dp.message(F.text == "💸 Withdraw")
async def withdraw_menu(message: types.Message):
    user = await users_col.find_one({'user_id': message.from_user.id})
    if not user or user.get('balance', 0) <= 0:
        await message.answer("❌ Insufficient Balance!")
        return
    
    markup = get_withdrawal_keyboard()
    await message.answer("💸 <b>Withdrawal Portal</b>\nSelect your reward:", reply_markup=markup)

@dp.callback_query(F.data == "del")
async def delete_callback(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer("Closed")

# --- ADMIN COMMANDS ---

@dp.message(Command("admin"), F.from_user.id.in_(ADMIN_IDS))
async def admin_panel(message: types.Message):
    kb = []
    for amt, data in COUPON_CONFIG.items():
        kb.append([StyledButton(text=f"➕ Add {data['name']} ({amt})", callback_data=f"admin_add_{amt}", style="success")])
    await message.answer("👑 <b>Admin Panel:</b>", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

@dp.callback_query(F.data.startswith("admin_add_"))
async def admin_add_start(callback: types.CallbackQuery, state: FSMContext):
    amount = int(callback.data.split("_")[2])
    await state.update_data(add_amt=amount)
    await callback.message.answer(f"Send codes for {amount} 🎟:")
    await state.set_state(AdminStates.waiting_for_coupons)

@dp.message(AdminStates.waiting_for_coupons)
async def admin_save_codes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    codes = [c.strip() for c in message.text.splitlines() if c.strip()]
    for code in codes:
        await coupons_col.insert_one({'code': code, 'amount': data['add_amt'], 'is_used': False, 'added_at': datetime.datetime.now()})
    await message.answer(f"✅ Added {len(codes)} codes.")
    await state.clear()

# --- MAIN ---
async def main():
    threading.Thread(target=run_flask, daemon=True).start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    try: asyncio.run(main())
    except: logger.info("Bot Stopped")
