import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN, WHATSAPP
from database import add_order, create_tables
from products import products

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def _main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 محصولات", callback_data="products")],
        [InlineKeyboardButton("🔍 جستجوی کالا", callback_data="search")],
        [InlineKeyboardButton("📝 درخواست قطعه", callback_data="request")],
        [InlineKeyboardButton("💬 واتساپ", url=f"https://wa.me/{WHATSAPP}")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🚗 به ربات آرا یدک خوش آمدید\n\n"
        "تامین قطعات لایتینگ تیگو ۷ پرو و تیگو ۸ پرو مکس",
        reply_markup=_main_keyboard(),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "products":
        context.user_data["state"] = None
        text = "🛒 محصولات آرا یدک:\n\n"
        for p in products:
            text += f"{p['id']} - {p['name']}\n"
        await query.edit_message_text(text)

    elif query.data == "search":
        context.user_data["state"] = "search"
        await query.edit_message_text(
            "🔍 نام کالا یا کد OEM را ارسال کنید."
        )

    elif query.data == "request":
        context.user_data["state"] = "request"
        await query.edit_message_text(
            "📝 نام قطعه مورد نظر خود را ارسال کنید."
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")
    text = update.message.text.strip()

    if state == "search":
        query_lower = text.lower()
        results = [
            p for p in products
            if query_lower in p["name"].lower()
            or (p["oem"] and query_lower in p["oem"].lower())
        ]
        if results:
            reply = "🔍 نتایج جستجو:\n\n"
            for p in results:
                reply += f"{p['id']} - {p['name']}\n"
        else:
            reply = "❌ کالایی با این مشخصات یافت نشد."
        await update.message.reply_text(reply)
        context.user_data["state"] = None

    elif state == "request":
        user_id = update.effective_user.id
        try:
            add_order(user_id, "", "", text)
            await update.message.reply_text(
                "✅ درخواست شما ثبت شد. به زودی با شما تماس می‌گیریم."
            )
        except Exception as e:
            logger.error("Error saving order for user %s: %s", user_id, e)
            await update.message.reply_text(
                "⚠️ خطایی در ثبت درخواست رخ داد. لطفاً دوباره تلاش کنید."
            )
        context.user_data["state"] = None

    else:
        await update.message.reply_text(
            "از منوی زیر انتخاب کنید:",
            reply_markup=_main_keyboard(),
        )


def main():
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Arayadak Bot Started")
    app.run_polling()


if __name__ == "__main__":
    main()
