import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.client.bot import DefaultBotProperties
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 829329480


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

payment_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💸 Оплатить", callback_data = 'pay')
        ]])

@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer(
         "<b>Привет!</b>\n\n"
        "Добро пожаловать! Представляем тебе методическое пособие:\n\n"
        "📘<b>«Поликлиническая практика. Первые шаги. Амбулаторный приём без паники»</b>\n\n"
        "Это незаменимая методичка для студентов и начинающих врачей — всё, что нужно, чтобы уверенно начать работу в поликлинике без стресса и паники.\n\n"
        "💡 Внутри ты найдёшь:\n"
        "— Разбор типовых клинических случаев\n"
        "— Чёткую структуру амбулаторного приёма\n"
        "— Полезные советы и лайфхаки\n\n"
        "💸 Стоимость — *5000 тг*\n"
        "📩 По всем вопросам — пиши мне @Indira120297!",
        parse_mode=ParseMode.HTML, reply_markup=payment_keyboard
    )

@dp.callback_query(F.data == "pay")
async def pay(callback: types.CallbackQuery):
    await callback.message.edit_text("🧾 Оплата методички «Поликлиническая практика. Первые шаги. Амбулаторный приём без паники»\n\n"
                                  "Стоимость: 5 000 ₸\n\n"
                                  "Для получения методички, пожалуйста, произведите оплату по следующим реквизитам:\n"
                                  "Kaspi Gold:💳 4400430311951799\n\n"
                                  "После оплаты отправьте, пожалуйста, скриншот чека в этот чат для подтверждения."
                                  "После проверки вам будет выдана методичка в PDF-формате.")

@dp.message(F.photo | F.document)
async def check_handler(message: types.Message):
    user = message.from_user
    user_id = user.id
    username = user.username or "без ника"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Одобрить", callback_data=f"approve:{user_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить", callback_data=f"decline:{user_id}"
                )
            ]
        ]
    )


    await bot.send_photo(
    chat_id=ADMIN_ID,
    photo=message.photo[-1].file_id,
    caption=f"🧾 Чек от @{username} (ID: {user_id})", reply_markup=keyboard)

    await message.answer("Чек отправлен администратору. Ожидайте подтверждения.")


@dp.callback_query(F.data.startswith("approve:"))
async def approve_callback(callback: types.CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    await callback.answer("Одобрено ✅")

    await callback.message.edit_caption(callback.message.caption + "\n\n✅ Оплата подтверждена")

    
    file_path="мет пособие.pdf"
    document = types.FSInputFile(file_path)

    await bot.send_document(
        chat_id=user_id,
        document=document,
        caption="Спасибо за оплату! Вот ваш файл 📄"
    )


@dp.callback_query(F.data.startswith("decline:"))
async def decline_callback(callback: types.CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    await callback.answer("Отклонено ❌")

    await callback.message.edit_caption(callback.message.caption + "\n\n❌ Оплата не подтверждена")

    await bot.send_message(
        chat_id=user_id,
        text="Оплата не подтверждена. Проверьте чек и попробуйте снова."
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
         asyncio.run(main())
    except KeyboardInterrupt:

        print("Bot is disconnect!")
