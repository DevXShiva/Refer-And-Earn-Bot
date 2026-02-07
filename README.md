🛍️ SHEIN REFER COUPON Bot
<div align="center">
https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/Telegram-Bot-blue
https://img.shields.io/badge/MongoDB-Atlas-green
https://img.shields.io/badge/License-MIT-yellow
https://img.shields.io/badge/Status-Active-brightgreen

Automated Coupon Distribution System with Multi-Channel Support

Features • Installation • Configuration • Usage • Admin Guide • Database

</div>
📸 Bot Preview
<div align="center">
🏠 Main Menu
https://via.placeholder.com/400x250/1a1a2e/ffffff?text=%F0%9F%94%97+My+Link+%F0%9F%92%8E+Balance+%F0%9F%8E%9F+Coupon+Stock+%F0%9F%92%B8+Withdraw

📊 Coupon Stock
https://via.placeholder.com/400x150/16213e/ffffff?text=%F0%9F%8E%9F+Coupon+Stock%250A%E2%80%A2+500+Coupons:+1110%250A%E2%80%A2+1000+Coupons:+22%250A%E2%80%A2+2000+Coupons:+0%250A%E2%80%A2+4000+Coupons:+6

👑 Admin Panel
https://via.placeholder.com/400x300/0f3460/ffffff?text=%F0%9F%91%91+Admin+Panel%250A%F0%9F%91%A5+Total+Users:+100%250A%F0%9F%9F%A2+Active+Today:+50%250A%F0%9F%8E%9F+Total+Coupons:+500%250A%E2%9C%85+Used+Coupons:+250%250A%F0%9F%94%84+Available:+250

</div>
✨ Features
🎯 Core Features
✅ Automated Coupon Distribution - Instant coupon delivery

✅ Multi-Channel Subscription - Force join multiple channels

✅ Referral System - Earn rewards for inviting friends

✅ Real-time Balance - Live balance tracking

✅ Coupon Stock Management - Track available coupons

✅ Admin Dashboard - Complete control panel

🔒 Security Features
🔐 Channel Verification - Mandatory subscription check

🛡️ Multi-Admin Support - Multiple admin accounts

📊 Usage Tracking - Prevent coupon reuse

📝 Audit Logs - Complete action logging

🚫 Anti-Abuse - No loopholes in balance system

📱 User Experience
⚡ Instant Responses - <1 second reply time

📱 Mobile Optimized - Perfect for mobile users

🎨 Beautiful UI - Emoji-rich interface

🔄 Real-time Updates - Live stock and balance

📨 Notifications - Instant success messages

🚀 Quick Start
Prerequisites
Python 3.8 or higher

MongoDB Atlas account

Telegram Bot Token from @BotFather

Installation
bash
# Clone the repository
git clone [https://github.com/yourusername/shein-coupon-bot.git](https://github.com/DevXShiva/Refer-And-Earn-Bot)
cd shein-coupon-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
Environment Configuration
Edit .env file:

env
# Required
BOT4_TOKEN=your_telegram_bot_token_here
MONGO_URI=your_mongodb_atlas_connection_string
LOG_CHANNEL_ID=-4444444444

# Optional (defaults shown)
PORT=8080

# Admin Configuration (add more IDs as needed)
# Format: ADMIN_IDS = [11111, 2222222]

# Force Subscribe Channels (add more as needed)
# Format: FSUB_CHANNEL_IDS = [-111111111111, -222222222]
Database Setup
The bot automatically creates the following collections:

users - User profiles and balances

coupons - Coupon inventory

redeemed - Redemption history

admin_logs - Admin activity logs

Running the Bot
bash
# Run directly
python bot.py

# Or using runner
python runner.py
⚙️ Configuration
Admin Setup
python
# In .env or directly in bot.py
ADMIN_IDS = [
    XXXXXXX,    # Admin 1
    YYYYYYY     # Admin 2
    # Add more admin IDs here
]
Channel Setup
python
FSUB_CHANNEL_IDS = [
    -X,   # Channel 1
    -Y,   # Channel 2
    -Z,   # Channel 3
    # Add more channel IDs here
]
Coupon Rates
python
# Fixed rates (modifiable in code)
COUPON_RATES = {
    500: 1,    # 1 🧩 = 500 ₪ coupon
    1000: 6,   # 6 🧩 = 1000 ₪ coupon
    2000: 15,  # 15 🧩 = 2000 ₪ coupon
    4000: 25   # 25 🧩 = 4000 ₪ coupon
}
📖 User Guide
Getting Started
Start the bot: /start

Join required channels (if any)

Use menu buttons to navigate

Earning Coins (🧩)
Referral System: Share your referral link

Each successful referral: 1 🧩

Balance shown in: 💎 Balance section

Redeeming Coupons
Click 💸 Withdraw

Select coupon amount

Confirm redemption

Receive coupon code instantly

Available Coupon Amounts
🎟 500 ₪ Coupon - Cost: 1 🧩

🎟 1000 ₪ Coupon - Cost: 6 🧩

🎟 2000 ₪ Coupon - Cost: 15 🧩

🎟 4000 ₪ Coupon - Cost: 25 🧩

👑 Admin Guide
Accessing Admin Panel
Ensure your ID is in ADMIN_IDS

Use /admin command

Or click 👑 Admin Panel button

Admin Features
📊 Statistics Dashboard
Real-time user statistics

Coupon inventory tracking

Redemption analytics

Daily active users

🎟 Coupon Management
bash
# Adding coupons through bot:
1. Click "➕ Add 500 Coupons" (or other amounts)
2. Send coupon codes (one per line)
3. System validates and stores automatically
Example coupon codes format:

text
SHEIN500ABC123
SHEIN500XYZ789
SHEIN500DEF456
📈 Real-time Monitoring
New user join notifications

Coupon redemption alerts

Admin action logs

System health status

Log Channel Features
The bot sends automatic notifications to your log channel:

text
#NewUser Joined 🚀
👤 Name: John Doe
🆔 ID: 5298223577
🕒 Time: 2026-02-06 11:38:31 PM

🎟 New Redemption
👤 User: John (ID: 5298223577)
💰 Amount: 500 ₪
🔢 Code: SHEIN500ABC
🕒 Time: 2026-02-06 11:38:31 PM

👑 Admin Action
👤 Admin: Admin Name
🎟 Added: 10 x 500 ₪ coupons
🕒 Time: 2026-02-06 11:38:31 PM
🗄️ Database Schema
Users Collection
javascript
{
  user_id: Number,           // Telegram User ID
  username: String,          // Telegram username
  first_name: String,        // User's first name
  last_name: String,         // User's last name
  balance: Number,           // Current balance (🧩)
  referral_count: Number,    // Successful referrals
  referral_code: String,     // Unique referral code
  created_at: DateTime,      // Account creation date
  last_active: DateTime,     // Last activity timestamp
  is_banned: Boolean         // Account status
}
Coupons Collection
javascript
{
  code: String,             // Unique coupon code
  amount: Number,           // Coupon value (500, 1000, etc.)
  is_used: Boolean,         // Usage status
  added_at: DateTime,       // When added to system
  used_by: Number,          // User ID who redeemed
  used_at: DateTime         // Redemption timestamp
}
Redemption History
javascript
{
  user_id: Number,          // User who redeemed
  code: String,             // Coupon code used
  redeemed_at: DateTime     // Redemption timestamp
}
🔧 Technical Details
Architecture
text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram API  │───▶│   Python Bot    │───▶│   MongoDB       │
│                 │    │                 │    │   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Users       │◀───│   Bot Logic     │◀───│   Data Models   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
Dependencies
txt
python-telegram-bot==20.7    # Telegram Bot API wrapper
pymongo==4.6.1              # MongoDB driver
python-dotenv==1.0.0        # Environment management
File Structure
text
shein-coupon-bot/
├── bot.py                 # Main bot application
├── runner.py              # Bot runner script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .env                  # Environment variables
├── README.md             # This file
└── logs/                 # Log directory (auto-created)
🚨 Error Handling
The bot includes comprehensive error handling:

✅ Database connection errors - Automatic retry

✅ Telegram API errors - Graceful degradation

✅ Invalid coupon codes - Automatic filtering

✅ Duplicate entries - Prevention and logging

✅ Rate limiting - Built-in protection

📈 Monitoring & Analytics
Built-in Analytics
Daily active users

Coupon redemption rates

User growth tracking

Channel subscription rates

Admin activity monitoring

Health Checks
python
# Automatic health monitoring
1. Database connectivity
2. Telegram API status
3. Coupon stock levels
4. User activity patterns
🔄 Updates & Maintenance
Regular Maintenance Tasks
Backup database regularly

Monitor log channel for issues

Update coupon stock as needed

Review admin logs for security

Update Procedure
bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart bot
# (Stop current instance first)
python bot.py
🤝 Contributing
We welcome contributions! Please follow these steps:

Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add AmazingFeature')

Push to branch (git push origin feature/AmazingFeature)

Open a Pull Request

Code Standards
Follow PEP 8 guidelines

Add comments for complex logic

Update documentation for new features

Write tests for new functionality

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🆘 Support
Common Issues & Solutions
Issue	Solution
Bot not starting	Check BOT_TOKEN in .env
Database errors	Verify MONGO_URI connection string
Channel join not detected	Ensure bot is admin in channels
Coupons not adding	Check coupon code format
Getting Help
Check Issues

Review the documentation

Contact: [Your Contact Information]

🏆 Features Comparison
Feature	This Bot	Other Bots
Multi-Channel Support	✅ Unlimited	❌ Limited
Admin Dashboard	✅ Complete	⚠️ Basic
Real-time Logging	✅ Full	⚠️ Partial
Database	✅ MongoDB	❌ JSON files
Security	✅ High	⚠️ Medium
Scalability	✅ Excellent	❌ Poor
🌟 Why Choose This Bot?
Professional Grade - Enterprise-level architecture

Highly Scalable - MongoDB backend handles growth

Secure - Multi-layer security features

Feature-Rich - Everything you need in one package

Easy to Maintain - Clean code, full documentation

Active Support - Regular updates and fixes

<div align="center">
🚀 Ready to launch your coupon distribution system?

https://img.shields.io/badge/Deploy_Now-Instructions-blueviolet
https://img.shields.io/badge/Request_Demo-Contact_Us-success

Star this repo if you find it useful! ⭐

</div>
📞 Contact
Developer: Your Name
Email: your.email@example.com
Telegram: @yourusername
Issues: GitHub Issues

Last Updated: February 2024
Version: 1.0.0
