import random
from telegram import Update, ReactionTypeEmoji
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "YOUR_BOT_TOKEN"

# Telegram er allowed reaction emoji list
EMOJIS = ["👍", "🔥", "❤", "😁", "🎉", "🤩", "👏", "💯", "😍", "🥰", "⚡", "🏆", "🤗", "😎", "🙏"]

async def react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg:
        return
    try:
        await context.bot.set_message_reaction(
            chat_id=msg.chat_id,
            message_id=msg.message_id,
            reaction=[ReactionTypeEmoji(random.choice(EMOJIS))],
        )
    except Exception as e:
        print("Reaction error:", e)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(
        (filters.ChatType.GROUPS | filters.ChatType.CHANNEL) & ~filters.COMMAND,
        react,
    ))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
