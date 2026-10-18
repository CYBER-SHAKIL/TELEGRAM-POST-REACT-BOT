# 🤖 Telegram Auto Reaction Bot

A simple Telegram bot that instantly reacts to every new post in a group or channel with a random emoji.

## ✨ Features

- Reacts instantly to every new message in groups and channels
- Picks a random emoji from Telegram's supported reaction list
- Lightweight and easy to deploy
- Token is loaded from an environment variable (safe for public repos)

## 📋 Requirements

- Python 3.9+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

## 🚀 Setup

### 1. Create the bot

1. Open [@BotFather](https://t.me/BotFather) and send `/newbot`
2. Copy the bot token
3. Send `/setprivacy` → select your bot → choose **Disable**
   (otherwise the bot can't see all group messages)

### 2. Clone and install

```bash
git clone https://github.com/CYBER-SHAKIL/TELEGRAM-POST-REACT-BOT.git
cd YOUR_REPO
pip install -r requirements.txt
```

### 3. Set the bot token

**Linux / macOS**
```bash
export BOT_TOKEN="your_bot_token_here"
```

**Windows (PowerShell)**
```powershell
$env:BOT_TOKEN="your_bot_token_here"
```

### 4. Run

```bash
python bot.py
```

## ➕ Add the bot to a group or channel

1. Add the bot to your group or channel
2. Make it an **Admin** (required for reactions, and always required in channels)
3. Send any message. The bot will react instantly 🎉

## ☁️ Deploy (24/7)

You can host it on [Railway](https://railway.app) or [Render](https://render.com):

1. Push this repo to GitHub
2. Create a new project from the repo
3. Add an environment variable: `BOT_TOKEN` = your token
4. Set the start command to `python bot.py` (or use the included `Procfile` as a worker)

## 🎨 Customize emojis

Edit the `EMOJIS` list in `bot.py`. Only Telegram's official reaction emojis work, for example:

```
👍 🔥 ❤ 😁 🎉 🤩 👏 💯 😍 🥰 ⚡ 🏆 🤗 😎 🙏
```

## 📁 Project structure

```
├── bot.py             # Main bot code
├── requirements.txt   # Python dependencies
├── Procfile           # Worker config for hosting
├── .gitignore
└── README.md
```

## ⚠️ Notes

- Never commit your bot token to GitHub
- The bot cannot react to its own messages
- Unsupported emojis will cause a reaction error

## 📄 License

MIT. Free to use and modify.
