# 🤖 Telegram Auto Reaction Bot

A Telegram bot that **instantly reacts to every new post** with a random emoji in **groups, channels and inbox (private chat)**.

## ✨ Features

- ⚡ Instant random emoji reaction on every new post
- 👥 Works in **groups**, 📢 **channels** and 💬 **inbox**
- 🖼 Reacts to everything: text, photo, video, voice, PDF, files, etc.
- 🎯 Respects the chat's allowed reactions (works even if a channel restricts emojis)
- 👋 `/start` guide with **Add to Group / Add to Channel** buttons
- 🔒 **Force-join**: users must join your channel before using the bot
- 🔑 Token stored safely in an environment variable

## 💬 Commands

| Command | Description |
|---|---|
| `/start` | Show the guide and add buttons |
| `/addgroup` | Add the bot to a group |
| `/addchannel` | Add the bot to a channel |
| `/help` | How to use the bot |
| `/about` | About the bot |

---

## 📁 Project Structure

```
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── .python-version     # Python version for hosting
├── Procfile            # Worker config (Railway etc.)
├── .gitignore
└── README.md
```

**requirements.txt**
```
python-telegram-bot==21.6
```

**.python-version**
```
3.12.8
```

**Procfile**
```
worker: python bot.py
```

**.gitignore**
```
.env
__pycache__/
```

---

## 🛠 Step 1: Create the bot

1. Open [@BotFather](https://t.me/BotFather) and send `/newbot`
2. Choose a name and a username, then **copy the bot token**
3. Send `/setprivacy` → select your bot → **Disable**

> ⚠️ Never put your token directly in the code or on GitHub. If it leaks, send `/revoke` to BotFather to get a new one.

## 🔒 Step 2: Set up Force-Join (optional but included)

The bot only works for users who joined your channel.

1. Open `bot.py` and change these two lines to **your** channel:
   ```python
   FORCE_CHANNEL = "@YourChannelUsername"
   FORCE_CHANNEL_URL = "https://t.me/YourChannelUsername"
   ```
2. **Add the bot as an Admin in that channel.**
   Channel → Manage Channel → Administrators → Add Admin → select your bot.

> Without this step the bot cannot check membership, and every user will be blocked.

---

## ☁️ Step 3: Deploy

Fork or upload this repo to your GitHub first, then pick **one** option below.

### Option A: Render (Web Service, free)

1. Go to [render.com](https://render.com) → **New +** → **Web Service**
2. Connect your GitHub repo
3. Fill in the settings:

   | Field | Value |
   |---|---|
   | Language | Python 3 |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `python bot.py` |
   | Instance Type | Free |

4. Open **Environment** → **Add Environment Variable**:

   | Key | Value |
   |---|---|
   | `BOT_TOKEN` | your bot token from BotFather |
   | `PYTHON_VERSION` | `3.12.8` |

5. Click **Create Web Service**. After the build finishes it should show **Live** ✅

> 💡 The bot includes a tiny web server so Render can detect an open port.

**Keep it awake 24/7 (free plan):**
Render's free Web Service sleeps after 15 minutes without traffic. To prevent that:

1. Create a free account on [uptimerobot.com](https://uptimerobot.com)
2. **Add New Monitor** → type **HTTP(s)**
3. URL: your Render URL (e.g. `https://your-bot.onrender.com`)
4. Monitoring interval: **5 minutes**

### Option B: Railway

1. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
2. Open the **Variables** tab and add `BOT_TOKEN` = your token
3. Railway uses the `Procfile` (`worker: python bot.py`) automatically
4. Deploy ✅

### Option C: Koyeb / other platforms

- Build command: `pip install -r requirements.txt`
- Run command: `python bot.py`
- Environment variable: `BOT_TOKEN`
- Set the Python version to **3.12**

### Option D: VPS / your own PC

```bash
git clone
https://github.com/CYBER-SHAKIL/TELEGRAM-POST-REACT-BOT.git
cd YOUR_REPO
pip install -r requirements.txt

# Linux / macOS
export BOT_TOKEN="your_bot_token_here"
# Windows (PowerShell)
$env:BOT_TOKEN="your_bot_token_here"

python bot.py
```

To keep it running on a VPS, use `screen`, `tmux` or `pm2`.

---

## ➕ Step 4: Add the bot to your chats

### Group
1. Send `/start` to the bot and tap **Add to Group** (or add it manually)
2. Make the bot an **Admin**
3. Send any message. The bot reacts instantly 🎉

### Channel
1. Tap **Add to Channel** in the bot, or add it manually as an **Admin**
2. Give it permission to **post/edit messages**
3. Channel Settings → **Reactions** → make sure reactions are **enabled**
4. Post anything. The bot reacts instantly 🎉

### Inbox
Just send any message to the bot and it will react.

---

## 🎨 Customize

**Change emojis**: edit the `EMOJIS` list in `bot.py`. Only Telegram's official reaction emojis work:

```
👍 🔥 ❤ 😁 🎉 🤩 👏 💯 😍 🥰 ⚡ 🏆 🤗 😎 🙏
```

**Change messages**: edit `WELCOME`, `HELP` and `ABOUT` at the top of `bot.py`.

---

## 🧯 Troubleshooting

| Problem | Fix |
|---|---|
| `RuntimeError: There is no current event loop` | Python 3.14 is being used. Set `PYTHON_VERSION=3.12.8` (or add `.python-version`) and redeploy with **Clear build cache** |
| `InvalidToken ... rejected by the server` | `BOT_TOKEN` is missing or wrong. Check the environment variable (no quotes, no spaces) |
| Render stuck on **"No open ports detected"** | Make sure you are using the latest `bot.py` with the built-in web server, and the service type is **Web Service** |
| "You haven't joined yet" even after joining | The bot is **not Admin** in your force-join channel. Add it as Admin |
| Bot reacts in groups but not in channels | Bot must be **Admin** in the channel, and channel **Reactions** must be enabled. Remove the bot and add it again as Admin |
| Bot doesn't react in a group | Disable privacy via `/setprivacy` in BotFather and make the bot Admin |
| Bot stops after some time on Render free | Set up UptimeRobot (see Option A) |
| `Reaction error` in logs | Check the log message. Usually the bot lacks permission or the emoji is not allowed in that chat |

**Where to see logs:** Render → your service → **Logs** tab.

---

## ⚠️ Notes

- The bot cannot react to its own messages
- Reactions only work with Telegram's official emoji list
- Never commit your bot token to GitHub

## 📄 License

MIT. Free to use and modify.
