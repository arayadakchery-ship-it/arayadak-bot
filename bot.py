from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from config import BOT_TOKEN, WHATSAPP
from products import products


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 محصولات", callback_data="products")],
        [InlineKeyboardButton("🔍 جستجوی کالا", callback_data="search")],
        [InlineKeyboardButton("📝 درخواست قطعه", callback_data="request")],
        [InlineKeyboardButton("💬 واتساپ", url=f"https://wa.me/{WHATSAPP}")],
    ]

    await update.message.reply_text(
        "🚗 به ربات آرا یدک خوش آمدید\n\n"
        "تامین قطعات لایتینگ تیگو ۷ پرو و تیگو ۸ پرو مکس",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "products":
        text = "🛒 محصولات آرا یدک:\n\n"
        for p in products:
            text += f"{p['id']} - {p['name']}\n"

        await query.edit_message_text(text)

    elif query.data == "search":
        await query.edit_message_text(
            "🔍 نام کالا یا کد OEM را ارسال کنید."
        )

    elif query.data == "request":
        await query.edit_message_text(
            "📝 نام قطعه مورد نظر خود را ارسال کنید."
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Arayadak Bot Started")
    app.run_polling()


if __name__ == "__main__":
    main()
