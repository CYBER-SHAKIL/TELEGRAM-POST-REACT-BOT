import os
import random
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReactionTypeEmoji,
    Update,
)
from telegram.constants import ChatMemberStatus, ChatType, ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]

# Users must join this channel to use the bot
FORCE_CHANNEL = "@Shakil_X9X"
FORCE_CHANNEL_URL = "https://t.me/Shakil_X9X"

EMOJIS = ["👍", "🔥", "❤", "😁", "🎉", "🤩", "👏", "💯", "😍", "🥰", "⚡", "🏆", "🤗", "😎", "🙏"]

WELCOME = (
    "👋 <b>Welcome to Auto Reaction Bot!</b>\n\n"
    "I instantly react to every new post with a random emoji ⚡\n\n"
    "<b>How to use:</b>\n"
    "1️⃣ Tap <b>Add to Group</b> or <b>Add to Channel</b> below\n"
    "2️⃣ Make me an <b>Admin</b>\n"
    "3️⃣ Done! I'll react to every new post 🎉\n\n"
    "💬 You can also send me any message here and I'll react to it.\n\n"
    "<b>Commands:</b>\n"
    "/start - Show this guide\n"
    "/addgroup - Add me to a group\n"
    "/addchannel - Add me to a channel\n"
    "/help - How to use\n"
    "/about - About the bot"
)

HELP = (
    "📖 <b>Help</b>\n\n"
    "<b>Group:</b> Add me and make me Admin.\n"
    "<b>Channel:</b> Add me as Admin (with permission to post/edit messages), "
    "and make sure <b>Reactions</b> are enabled in channel settings.\n"
    "<b>Inbox:</b> Just send me a message.\n\n"
    "⚠️ You must join " + FORCE_CHANNEL + " to use this bot."
)

ABOUT = (
    "🤖 <b>Auto Reaction Bot</b>\n\n"
    "Reacts to every new post in groups, channels and inbox with a random emoji.\n\n"
    "📢 Updates: " + FORCE_CHANNEL
)


# ---------- tiny web server (needed for Render Web Service) ----------
class Ping(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, *args):
        pass


def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Ping).serve_forever()


# ---------- helpers ----------
def add_group_url(username):
    return f"https://t.me/{username}?startgroup=true&admin=delete_messages"


def add_channel_url(username):
    return f"https://t.me/{username}?startchannel=true&admin=post_messages+edit_messages"


def main_kb(username):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("➕ Add to Group", url=add_group_url(username)),
                InlineKeyboardButton("📢 Add to Channel", url=add_channel_url(username)),
            ],
            [InlineKeyboardButton("🔔 Updates Channel", url=FORCE_CHANNEL_URL)],
        ]
    )


def join_kb():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📢 Join Channel", url=FORCE_CHANNEL_URL)],
            [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")],
        ]
    )


JOIN_TEXT = (
    "🚫 <b>Access Denied</b>\n\n"
    "To use this bot you must join our channel first:\n"
    + FORCE_CHANNEL
    + "\n\nAfter joining, tap <b>I've Joined</b>."
)


ERROR_TEXT = (
    "⚠️ <b>Verification error</b>\n\n"
    "I couldn't check your membership. The bot owner must make this bot an "
    "<b>Admin</b> in " + FORCE_CHANNEL + "."
)


async def is_joined(bot, user_id):
    """True = joined, False = not joined, None = check failed (bot not admin etc.)"""
    try:
        m = await bot.get_chat_member(FORCE_CHANNEL, user_id)
        return m.status in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        )
    except Exception as e:
        print("Join check error (is the bot admin in the channel?):", e)
        return None


async def gate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user = update.effective_user
    joined = await is_joined(context.bot, user.id) if user else False
    if joined:
        return True
    if joined is None:
        await update.effective_message.reply_text(ERROR_TEXT, parse_mode=ParseMode.HTML)
        return False
    await update.effective_message.reply_text(
        JOIN_TEXT, parse_mode=ParseMode.HTML, reply_markup=join_kb()
    )
    return False


# ---------- commands ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, context):
        return
    await update.message.reply_text(
        WELCOME, parse_mode=ParseMode.HTML, reply_markup=main_kb(context.bot.username)
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, context):
        return
    await update.message.reply_text(
        HELP, parse_mode=ParseMode.HTML, reply_markup=main_kb(context.bot.username)
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, context):
        return
    await update.message.reply_text(ABOUT, parse_mode=ParseMode.HTML)


async def addgroup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, context):
        return
    kb = InlineKeyboardMarkup(
        [[InlineKeyboardButton("➕ Add to Group", url=add_group_url(context.bot.username))]]
    )
    await update.message.reply_text(
        "👥 Tap the button below, choose your group, and make me <b>Admin</b>.",
        parse_mode=ParseMode.HTML,
        reply_markup=kb,
    )


async def addchannel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, context):
        return
    kb = InlineKeyboardMarkup(
        [[InlineKeyboardButton("📢 Add to Channel", url=add_channel_url(context.bot.username))]]
    )
    await update.message.reply_text(
        "📢 Tap the button below, choose your channel, and confirm Admin rights.\n\n"
        "Also make sure <b>Reactions</b> are enabled in your channel settings.",
        parse_mode=ParseMode.HTML,
        reply_markup=kb,
    )


async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    joined = await is_joined(context.bot, q.from_user.id)
    if joined:
        await q.answer("✅ Verified!")
        await q.message.edit_text(
            WELCOME, parse_mode=ParseMode.HTML, reply_markup=main_kb(context.bot.username)
        )
    elif joined is None:
        await q.answer(
            "⚠️ Bot must be Admin in " + FORCE_CHANNEL + " to verify. Tell the bot owner.",
            show_alert=True,
        )
    else:
        await q.answer("❌ You haven't joined yet! Join first, then tap again.", show_alert=True)


# ---------- reactions ----------
_allowed_cache = {}


async def pick_emoji(bot, chat_id, chat_type):
    """Pick a random emoji the chat actually allows (channels can restrict reactions)."""
    if chat_type == ChatType.PRIVATE:
        return random.choice(EMOJIS)
    cached = _allowed_cache.get(chat_id)
    if not cached or time.time() - cached[0] > 600:
        allowed = None  # None = all emojis allowed
        try:
            chat = await bot.get_chat(chat_id)
            ar = chat.available_reactions
            if ar is not None:
                allowed = [r.emoji for r in ar if isinstance(r, ReactionTypeEmoji)]
        except Exception as e:
            print("get_chat error:", e)
        cached = (time.time(), allowed)
        _allowed_cache[chat_id] = cached
    allowed = cached[1]
    pool = EMOJIS if allowed is None else allowed
    return random.choice(pool) if pool else None


async def react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg:
        return
    try:
        emoji = await pick_emoji(context.bot, msg.chat_id, msg.chat.type)
        if not emoji:
            return
        await context.bot.set_message_reaction(
            chat_id=msg.chat_id,
            message_id=msg.message_id,
            reaction=[ReactionTypeEmoji(emoji)],
        )
    except Exception as e:
        print("Reaction error:", e)


async def private_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, context):
        return
    await react(update, context)


# ---------- when bot is added to a group/channel ----------
async def on_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = update.my_chat_member
    if r.chat.type == ChatType.PRIVATE:
        return
    active = (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR)
    was_in = r.old_chat_member.status in active
    now_in = r.new_chat_member.status in active
    if now_in and not was_in:
        user = r.from_user
        if await is_joined(context.bot, user.id) is False:
            try:
                await context.bot.send_message(
                    user.id, JOIN_TEXT, parse_mode=ParseMode.HTML, reply_markup=join_kb()
                )
            except Exception:
                pass
            try:
                await context.bot.leave_chat(r.chat.id)
            except Exception as e:
                print("Leave error:", e)


async def post_init(app: Application):
    await app.bot.set_my_commands(
        [
            BotCommand("start", "Start the bot"),
            BotCommand("addgroup", "Add bot to a group"),
            BotCommand("addchannel", "Add bot to a channel"),
            BotCommand("help", "How to use"),
            BotCommand("about", "About the bot"),
        ]
    )


def main():
    threading.Thread(target=run_server, daemon=True).start()

    app = Application.builder().token(TOKEN).post_init(post_init).build()

    private = filters.ChatType.PRIVATE
    app.add_handler(CommandHandler("start", start, filters=private))
    app.add_handler(CommandHandler("help", help_cmd, filters=private))
    app.add_handler(CommandHandler("about", about, filters=private))
    app.add_handler(CommandHandler("addgroup", addgroup, filters=private))
    app.add_handler(CommandHandler("addchannel", addchannel, filters=private))
    app.add_handler(CallbackQueryHandler(check_join, pattern="^check_join$"))
    app.add_handler(ChatMemberHandler(on_added, ChatMemberHandler.MY_CHAT_MEMBER))

    # inbox
    app.add_handler(MessageHandler(private & ~filters.COMMAND, private_msg))
    # groups
    app.add_handler(
        MessageHandler(filters.ChatType.GROUPS & ~filters.COMMAND & ~filters.StatusUpdate.ALL, react)
    )
    # channels
    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, react))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
