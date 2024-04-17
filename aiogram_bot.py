import asyncio, datetime
import sqlite3 as sq 


from decimal import Decimal
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


#emoji for flags
emoji = {
    'A': '\U0001F1E6',
    'B': '\U0001F1E7',
    'C': '\U0001F1E8',
    'D': '\U0001F1E9',
    'E': '\U0001F1EA',
    'F': '\U0001F1EB',
    'G': '\U0001F1EC',
    'H': '\U0001F1ED',
    'I': '\U0001F1EE',
    'J': '\U0001F1EF',
    'K': '\U0001F1F0',
    'L': '\U0001F1F1',
    'M': '\U0001F1F2',
    'N': '\U0001F1F3',
    'O': '\U0001F1F4',
    'P': '\U0001F1F5',
    'Q': '\U0001F1F6',
    'R': '\U0001F1F7',
    'S': '\U0001F1F8',
    'T': '\U0001F1F9',
    'U': '\U0001F1FA',
    'V': '\U0001F1FB',
    'W': '\U0001F1FC',
    'X': '\U0001F1FD',
    'Y': '\U0001F1FE',
    'Z': '\U0001F1FF'
    }

ans = {}
values = ['AED', 'AMD', 'AUD', 'AZN', 'BGN', 'BYN', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP',
        'HKD', 'HUF', 'INR', 'JPY', 'KGS', 'KRW', 'KZT', 'MDL', 'NOK', 'PLN', 'SEK', 'SGD', 'THB',
        'TJS', 'TRY', 'USD', 'ZAR']

bot = Bot("TOKEN_BOT")
dp = Dispatcher()

first_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⬅'),
            KeyboardButton(text='➡')
        ]
    ],
    resize_keyboard=True
)

time_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='5 минут'),
            KeyboardButton(text='20 минут'),
            KeyboardButton(text='1 час')
        ],
        [
            KeyboardButton(text='5 часов'),
            KeyboardButton(text='12 часов'),
            KeyboardButton(text='1 день')
        ],
        [
            KeyboardButton(text='⬅'),
            KeyboardButton(text='➡')
        ]
    ],
    resize_keyboard=True
)

acces_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да ✅'),
            KeyboardButton(text='Нет ❌')
        ]
    ],
    resize_keyboard=True
)

stop_sled = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Прекратить отслеживание валют ❌')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

#communication using arrows
def cal_kb():
    builder = ReplyKeyboardBuilder()
    [builder.button(text=f'{i}{emoji[i[0]]}{emoji[i[1]]}') for i in values]
    builder.button(text=f'⬅')
    builder.button(text=f'➡')
    builder.adjust(5)
    return builder.as_markup(resize_keyboard=True)

#start command handler
@dp.message(Command('start'))
async def start(message: Message):
    await message.answer("Это телеграмм бот для отслеживания курсов валют.\nДля коммуникации используйте стрелочки.", reply_markup=first_kb)
    ans[message.chat.id] = {'page': 0}

#reverse arrow back
@dp.message(F.text == '⬅')
async def st_l(message: Message):
    ans[message.chat.id]['page'] = ans[message.chat.id]['page'] - 1 if ans[message.chat.id]['page'] > 0 else 0
    if ans[message.chat.id]['page'] == 0:
        await message.answer('Для выбора валют нажмите ➡', reply_markup=first_kb)
    elif ans[message.chat.id]['page'] == 1:
        ans[message.chat.id]['values'] = []
        await message.answer('Выберите валюты', reply_markup=cal_kb())
    elif ans[message.chat.id]['page'] == 2:
        await message.answer('Выберите время', reply_markup=time_kb)

#forward arrow reverse   
@dp.message(F.text == '➡')
async def st_vp(message: Message):
    ans[message.chat.id]['page'] = ans[message.chat.id]['page'] + 1 if ans[message.chat.id]['page'] < 3 else 3
    if ans[message.chat.id]['page'] == 1:
        ans[message.chat.id]['values'] = []
        await message.answer('Выберите валюты', reply_markup=cal_kb())
    elif ans[message.chat.id]['page'] == 2:
        ans[message.chat.id]['responce'] = True
        await message.answer('Выберите время', reply_markup=time_kb)
    elif ans[message.chat.id]['page'] == 3:
        await message.answer(f'Вы сохранили такие валюты: {', '.join([f'{i}{emoji[i[0]]}{emoji[i[1]]}' for i in ans[message.chat.id]['values']])}\nВы выбрали время: {ans[message.chat.id]['user_time_vib']}')
        await message.answer('Подтвердить ввод?', reply_markup=acces_kb)

#adding user currencies
@dp.message(F.text[:-2].in_(values))
async def valiti(message: Message):
    if message.text[:-2] in values:
        if message.text[:-2] not in ans[message.chat.id]['values']:
            ans[message.chat.id]['values'].append(message.text[:-2])

#time handler
@dp.message(F.text.in_(['5 минут', '20 минут', '1 час', '5 часов', '12 часов', '1 день']))
async def time_vb(message: Message):
    ans[message.chat.id]['user_time_vib'] = message.text
    if message.text == '5 минут':
        ans[message.chat.id]['minutes'] = 5
    elif message.text == '20 минут':
        ans[message.chat.id]['minutes'] = 20
    elif message.text == '1 час':
        ans[message.chat.id]['minutes'] = 60
    elif message.text == '5 часов':
        ans[message.chat.id]['minutes'] = 300
    elif message.text == '12 часов':
        ans[message.chat.id]['minutes'] = 720
    elif message.text == '1 день':
        ans[message.chat.id]['minutes'] = 1440

#command handler YES, NO
@dp.message(F.text.in_(['Да ✅', 'Нет ❌']))
async def acces(message: Message):
    if message.text == 'Нет ❌':
        ans[message.chat.id]['page'] -= 1
        await message.answer('Выберите время', reply_markup=time_kb)
    elif message.text == 'Да ✅':
        await message.answer("Для прекращения отслеживания валют нажмите на кнопку ''Прекратить отслеживание валют ❌''", reply_markup=stop_sled)
        ans[message.chat.id]['start_time_minutes'] = int(str(datetime.datetime.now())[:-10][8:10]) * 1440 + int(str(datetime.datetime.now())[:-10][11:13]) * 60 + int(str(datetime.datetime.now())[:-10][14:])
        with sq.connect('date_base.db') as date:
            cur = date.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE TYPE='table'")
            ans[message.chat.id]['values_currents_start'] = dict(cur.execute(f"""SELECT * FROM '{str(list(cur)[-1]).rstrip("'',)").strip("(''")}'"""))
        ans[message.chat.id]['prosh_currents'] = ans[message.chat.id]['values_currents_start']
        await message.answer("\n".join(['Курсы валют до отслеживания:'] + [f'Валюта {i}{emoji[i[0]]}{emoji[i[1]]} стоит {ans[message.chat.id]['values_currents_start'][i]} ₽' for i in ans[message.chat.id]['values']]))
        ans[message.chat.id]['cnt'] = 0
        
        while ans[message.chat.id]['responce']:
            ans[message.chat.id]['user_text_ans_values'] = []
            if ans[message.chat.id]['cnt'] == 120:
                with sq.connect('date_base.db') as date:
                    cur = date.cursor()
                    cur.execute("SELECT name FROM sqlite_master WHERE TYPE='table'")
                    ans[message.chat.id]['start_time_time'] = str(list(cur)[-1]).rstrip("'',)").strip("(''")
                    ans[message.chat.id]['values_currents_now'] = dict(cur.execute(f"""SELECT * FROM '{ans[message.chat.id]['start_time_time']}'"""))
                    ans[message.chat.id]['now_time'] = (int(ans[message.chat.id]['start_time_time'][8:10]) * 1440 + int(ans[message.chat.id]['start_time_time'][11:13]) * 60 + int(ans[message.chat.id]['start_time_time'][14:]))
                
                if (ans[message.chat.id]['now_time'] - ans[message.chat.id]['start_time_minutes']) >= ans[message.chat.id]['minutes']:
                    ans[message.chat.id]['responce'] = False
                for i in ans[message.chat.id]['values']:
                    ans[message.chat.id]['user_text_ans_values'].append(f'{i}{emoji[i[0]]}{emoji[i[1]]} {ans[message.chat.id]['values_currents_now'][i]} ₽')
                    if ans[message.chat.id]['values_currents_start'][i] > ans[message.chat.id]['values_currents_now'][i]:
                        ans[message.chat.id]['user_text_ans_values'].append(f'-{round(Decimal(ans[message.chat.id]['values_currents_start'][i]) - Decimal(ans[message.chat.id]['values_currents_now'][i]), 6)} ₽ от старта📉')
                    elif ans[message.chat.id]['values_currents_start'][i] < ans[message.chat.id]['values_currents_now'][i]:
                        ans[message.chat.id]['user_text_ans_values'].append(f'+{round(Decimal(ans[message.chat.id]['values_currents_now'][i]) - Decimal(ans[message.chat.id]['values_currents_start'][i]), 6)} ₽ от старта📈')
                    if ans[message.chat.id]['prosh_currents'][i] > ans[message.chat.id]['values_currents_now'][i]:
                        ans[message.chat.id]['user_text_ans_values'].append(f'-{round(Decimal(ans[message.chat.id]['prosh_currents'][i]) - Decimal(ans[message.chat.id]['values_currents_now'][i]), 6)} ₽ от прошлого📉')
                    elif ans[message.chat.id]['prosh_currents'][i] < ans[message.chat.id]['values_currents_now'][i]:
                        ans[message.chat.id]['user_text_ans_values'].append(f'+{round(Decimal(ans[message.chat.id]['values_currents_now'][i]) - Decimal(ans[message.chat.id]['prosh_currents'][i]), 6)} ₽ от прошлого📈')
                    ans[message.chat.id]['user_text_ans_values'].append(' ')
                if len(ans[message.chat.id]['user_text_ans_values']) != 1:
                    await message.answer("\n".join(ans[message.chat.id]['user_text_ans_values']))
                ans[message.chat.id]['prosh_currents'] = ans[message.chat.id]['values_currents_now']
                ans[message.chat.id]['cnt'] = 0
            else:
                ans[message.chat.id]['cnt'] += 1
                await asyncio.sleep(1)
        await message.answer("Для повторной работы нажмите ''/start''")
        await message.answer('Отслеживание закончилось', reply_markup=ReplyKeyboardRemove())

#stop tracking function
@dp.message(F.text == 'Прекратить отслеживание валют ❌')
async def stran(message: Message):
    ans[message.chat.id]['responce'] = False

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())