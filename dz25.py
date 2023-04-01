from random import randint as ran 
import asyncio
import logging
import sys
import time
import datetime
from os import path


from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import requests
import json
from kb import choice_keyboard, backup_keyboard, list_keyboard


def call_data(query_data,source) -> list:
    json_source = source + '/courses.json'
    if path.exists(json_source):
        with open(json_source,'r') as file:
            course_data = json.load(file)
        for i in range(len(course_data['courses'])):
            if (course_data['courses'][i]['date'] + 300) < round(time.time()):
                are_5minup = True
            else:
                are_5minup = False
                break
        if are_5minup:
            uah = requests.get('http://api.monobank.ua/bank/currency').json()
            needed_courses = uah[0:7]
            dict_of_courses = {'courses':needed_courses}
            with open(json_source, 'w') as file:
                json.dump(dict_of_courses,file)
    else:
        uah = requests.get('http://api.monobank.ua/bank/currency').json()
        needed_courses = uah[0:7]
        dict_of_courses = {'courses':needed_courses}
        with open(json_source,'w') as file:
            json.dump(dict_of_courses,file)
    with open(json_source,'r') as file:
        course_data = json.load(file)
    name_of_valute = text[query_data][0]
    if text[query_data][1] in [0,1,2]:
        valute_value = str(course_data['courses'][text[query_data][1]]['rateBuy'])
        if text[query_data][1] == 2:
            valute_value += '$'
        else:
            valute_value += 'грн'
    else:
        valute_value = str(course_data['courses'][text[query_data][1]]['rateCross']) + 'грн'

    return [name_of_valute,valute_value]


source = 'monobank'

with open(source + '/text_and_data.txt','r') as file:
    text = json.load(file)



API_TOKEN ='5485255207:AAEPMHtr1dJPAz82t1EYeNbl8-hicVG7yOU'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storege = MemoryStorage()
dp = Dispatcher(bot, storage=storege)

class Form_curs(StatesGroup):
    start_state = State()
    valute_choice = State()
    valute_shows = State()


@dp.message_handler(commands=['start'],state='*')
async def start(message: types.Message,state:FSMContext):
        await message.answer(text['start'],reply_markup=list_keyboard)
        await Form_curs.start_state.set()


@dp.callback_query_handler(state=[Form_curs.start_state,Form_curs.valute_shows])
async def choose_your_valute(query: types.CallbackQuery,state:FSMContext):
    await query.message.edit_text(text['choice'],reply_markup=choice_keyboard)
    await Form_curs.valute_choice.set()


@dp.callback_query_handler(state=Form_curs.valute_choice)
async def valute_shows(query: types.CallbackQuery,state:FSMContext):
    valute_data = call_data(query.data,source)
    await query.message.edit_text(f'Курс {valute_data[0]}:\n {valute_data[1]}',reply_markup=backup_keyboard)
    await Form_curs.valute_shows.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)