#BOT_TOKEN = '6119057214:AAFfWbstixdSv64T34PMfUIDVcHSmKzEWJs'

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)

BOT_TOKEN = '6119057214:AAFfWbstixdSv64T34PMfUIDVcHSmKzEWJs'

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()

# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher(storage=storage)

class Form(StatesGroup):
    sex = State()
    MCV = State()
    ACT = State()
    ALT = State()
    BMI = State()

@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Привет, этот бот рассчитает индекс ANI\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform')

@dp.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Введите пол пациента (m/w)')
    await state.set_state(Form.sex)


@dp.message(Form.sex)
async def process_name(message: Message, state: FSMContext) -> None:
    #await message.answer(f'Пол пациента:\r\n{message.text}\r\nВведите MCV')
    await message.answer(f'Введите MCV')
    await state.update_data(sex=message.text)
    await state.set_state(Form.MCV)

@dp.message(Form.MCV)
async def process_name(message: Message, state: FSMContext) -> None:
    await message.answer(f'Введите ACT')
    await state.update_data(MCV=message.text)

    await state.set_state(Form.ACT)

@dp.message(Form.ACT)
async def process_name(message: Message, state: FSMContext) -> None:
    await message.answer(f'Введите ALT')
    await state.update_data(ACT=message.text)
    await state.set_state(Form.ALT)


@dp.message(Form.ALT)
async def process_name(message: Message, state: FSMContext) -> None:
    await message.answer(f'Введите BMI')
    await state.update_data(ALT=message.text)
    await state.set_state(Form.BMI)


@dp.message(Form.BMI)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(BMI=message.text)

    context_data = await state.get_data()
    sex = context_data.get('sex')
    MCV = context_data.get('MCV')
    ACT = context_data.get('ACT')
    ALT = context_data.get('ALT')

    #data_user=f"{sex}, {MCV}, {ACT}, {ALT}, {message.text}"
    #await message.answer(f"{sex}, {MCV}, {ACT}, {ALT}, {message.text}")
    if sex == 'w':
        await message.answer(f'Индекс ANI:\r\n{float(-58.5 + 0.637 * float(MCV) + 3.91 * (float(ACT)/float(ALT)) - 0.406 * float(message.text))}')
    else:
        await message.answer(f"Индекс ANI:\r\n{float(-58.5 + 0.637 * float(MCV) + 3.91 * (float(ACT) / float(ALT)) - 0.406 * float(message.text)) + 6.35}")

# сделать расчет по формуле в зависимости от пола пациента
   # await message.answer(float(MCV)*float(ACT))






    await state.clear()


# Запускаем поллинг
if __name__ == '__main__':
    dp.run_polling(bot)




