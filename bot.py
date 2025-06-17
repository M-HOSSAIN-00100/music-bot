import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# টেলিগ্রাম API কনফিগ
API_ID = os.environ.get("API_ID", "123456")  # my.telegram.org থেকে নিন
API_HASH = os.environ.get("API_HASH", "abcdef12345")  # my.telegram.org থেকে নিন
BOT_TOKEN = os.environ.get("BOT_TOKEN", "123:abc")  # @BotFather থেকে নিন

# স্ট্রিমিং URL (লাইভ মিউজিক সোর্স)
STREAM_URL = "http://stream.radioparadise.com/flac"  # আপনার পছন্দের লাইভ স্ট্রিম URL

app = Client(
    "music_stream_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command(["start", "help"]))
async def start(_, message: Message):
    await message.reply_text(
        "🎵 **হ্যালো! আমি লাইভ মিউজিক স্ট্রিমিং বট**\n\n"
        "• /play - লাইভ মিউজিক স্ট্রিম শুরু করুন\n"
        "• /stop - মিউজিক বন্ধ করুন\n"
        "• /source - বর্তমান স্ট্রিম সোর্স দেখুন"
    )

@app.on_message(filters.command("play"))
async def play_music(_, message: Message):
    chat_id = message.chat.id
    try:
        # গ্রুপে জয়েন করুন
        await app.send_message(chat_id, "🔊 **লাইভ স্ট্রিম শুরু হচ্ছে...**")
        
        # স্ট্রিমিং শুরু করুন
        await app.stream_audio(
            chat_id=chat_id,
            audio_path=STREAM_URL
        )
        await app.send_message(chat_id, "✅ **স্ট্রিমিং সফলভাবে শুরু হয়েছে!**")
    except Exception as e:
        await message.reply_text(f"❌ ত্রুটি: {str(e)}")
        logger.error(f"Play error: {e}")

@app.on_message(filters.command("source"))
async def show_source(_, message: Message):
    await message.reply_text(f"📡 **বর্তমান স্ট্রিম সোর্স:**\n`{STREAM_URL}`")

@app.on_message(filters.command("stop"))
async def stop_music(_, message: Message):
    chat_id = message.chat.id
    try:
        await app.leave_chat(chat_id)
        await message.reply_text("⏹️ **স্ট্রিমিং বন্ধ করা হয়েছে**")
    except Exception as e:
        await message.reply_text(f"❌ ত্রুটি: {str(e)}")
        logger.error(f"Stop error: {e}")

if __name__ == "__main__":
    logger.info("বট চালু হলো...")
    app.run()
