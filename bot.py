import os
import random
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, ReactionTypeEmoji
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]

EMOJIS = ["👍", "🔥", "❤", "😁", "🎉", "🤩", "👏", "💯", "😍", "🥰", "⚡", "🏆", "🤗", "😎", "🙏"]

class Ping(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")
    def log_message(self, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Ping).serve_forever()

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
    threading.Thread(target=run_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(
        (filters.ChatType.GROUPS | filters.ChatType.CHANNEL) & ~filters.COMMAND,
        react,
    ))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
