from random import randint
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import asyncio

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
users = {}

def init_user(user_id):
    if user_id not in users:
        users[user_id] = {'play': False, 'guess_num': None}


@dp.message(CommandStart())
async def starting_message(message: Message):
    await message.answer('привет это бот guess number, жми /play чтобы начать')


@dp.message(Command('play'))
async def play_game(message: Message):
    user_id = message.from_user.id

    init_user(user_id)
    users[user_id]['play'] = True
    guess_num = randint(1, 100)
    users[user_id]['guess_num'] = guess_num

    await message.answer('загадал число от 1 до 100, попробуй угадать')


@dp.message()
async def guess(message: Message):
    user_id = message.from_user.id
    user_text = message.text

    init_user(user_id)

    if users[user_id]['play']==True:
        guess_num_user = users[user_id]['guess_num']

        if user_text.isdigit():
            user_num = int(user_text)
            if user_num == guess_num_user:
                await message.reply('это был правильный ответ')
                users[user_id] = {'play': False, 'guess_num': None}
                return None
            if user_num > guess_num_user:
                await message.answer('слишком много')
            else:
                await message.answer('слишком мало')
        else:
            await message.answer('введите положительное число')
    else:
        await message.answer('сначала нажмите /play')


async def main():
    # 1. Принудительно сбрасываем вебхук и чистим старую очередь
    await bot.delete_webhook(drop_pending_updates=True)
    print('Бот запущен и готов к работе!')

    # 2. Запускаем поллинг
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Запускаем всю эту конструкцию через asyncio.run
    asyncio.run(main())
