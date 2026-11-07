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
    user_id = message.from_user.id
    init_user(user_id)
    if users[user_id]['play']:
        await message.answer('Куда стартуешь?\nВо время игры я реагирую только на команды /cancel, /help и на число')
    else:
        await message.answer('Привет! Это бот \'угадай число\'\nжми /play чтобы начать\n---> /help')


@dp.message(Command('help'))
async def helping_message(message: Message):
    await message.answer('/start - начальное сообшение бота\n/play - начать игру\n/cancel - отменить игру')


@dp.message(Command('cancel'))
async def cancel_game(message: Message):
    user_id = message.from_user.id
    init_user(user_id)
    if users[user_id]['play']:
        users[user_id] = {'play': False, 'guess_num': None}
        await message.answer('Игра отменена. Если захочешь еще, то жми /play')
    else:
        await message.answer('Ты даже не начал играть!\nЧтобы начать нажми /play')


@dp.message(Command('play'))
async def start_play_game(message: Message):
    user_id = message.from_user.id
    init_user(user_id)
    if users[user_id]['play']:
        await message.answer(
            'Ты же уже в игре!\n Во время игры я реагирую только на команды /cancel, /help и на число ')
    else:
        init_user(user_id)
        users[user_id]['play'] = True
        guess_num = randint(1, 100)
        users[user_id]['guess_num'] = guess_num

        await message.answer('Загадал число от 1 до 100, попробуй угадать!')


@dp.message(lambda m: m.text and m.text.isdigit() and 1 <= int(m.text) <= 100)
async def playing_game(message: Message):
    user_id = message.from_user.id
    user_text = message.text

    init_user(user_id)

    if users[user_id]['play']:
        guess_num_user = users[user_id]['guess_num']

        user_num = int(user_text)
        if user_num == guess_num_user:
            await message.reply('это был правильный ответ! Хочешь еще? ---> /play')
            users[user_id] = {'play': False, 'guess_num': None}
        elif user_num > guess_num_user:
            await message.answer('МногоВАТО')
        elif user_num < guess_num_user:
            await message.answer('МалоВАТО')
    else:
        await message.answer('Еще не играем...\nЧтобы начать игру нажми /play')


@dp.message()
async def answer_on_trash(message: Message):
    user_id=message.from_user.id
    init_user(user_id)
    if users[user_id]['play']:
        await message.answer(
            'Мы же сейчас играем. '
            'Присылай, пожалуйста, числа от 1 до 100'
        )
    else:
         await message.answer('Бот еще сильно ограничен, если нужна помошь - нажми /help')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print('Бот запущен и готов к работе!')

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
