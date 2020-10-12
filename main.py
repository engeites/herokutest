from aiogram import Bot, Dispatcher, executor, types

BOT_TOKEN = '1193921223:AAECFjhRA-_BeaPMoYsTNfmpDr_Pi_dcqzY'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def main(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)