from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import os

TOKEN = os.getenv("TOKEN")

questions = [
    {
        "q": "كم عدد قارات العالم؟",
        "options": ["5", "6", "7"],
        "correct": "7"
    },
    {
        "q": "ما عاصمة تونس؟",
        "options": ["صفاقس", "تونس", "سوسة"],
        "correct": "تونس"
    }
]

points = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    points[user.id] = points.get(user.id, 0)
    await update.message.reply_text(
        "🎮 مرحبًا بك في لعبة الأسئلة!\n"
        "اكتب /play للعب 🎯"
    )

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(questions)
    context.user_data["correct"] = q["correct"]

    buttons = [
        [InlineKeyboardButton(opt, callback_data=opt)]
        for opt in q["options"]
    ]

    await update.message.reply_text(
        f"❓ {q['q']}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == context.user_data.get("correct"):
        points[user_id] += 10
        await query.edit_message_text("✅ إجابة صحيحة! +10 نقاط 🎉")
    else:
        await query.edit_message_text("❌ إجابة خاطئة")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("play", play))
app.add_handler(CallbackQueryHandler(answer))

app.run_polling()
