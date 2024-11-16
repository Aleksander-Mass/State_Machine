from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

api = "При отправке вашего кода на GitHub не забудьте убрать ключ для подключения к вашему боту!"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.\n"
                         "Введите команду 'Calories', чтобы узнать свою норму калорий.")


@dp.message_handler(text="Calories")
async def set_age(message: types.Message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Попробуйте еще раз:")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост в сантиметрах:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Рост должен быть числом. Попробуйте еще раз:")
        return
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес в килограммах:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Вес должен быть числом. Попробуйте еще раз:")
        return
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    # Формула Миффлина - Сан Жеора для женщин:
    # BMR = 10 * вес + 6.25 * рост - 5 * возраст - 161
    bmr = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] - 161
    await message.answer(f"Ваша норма калорий: {bmr:.2f}")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

###
"""
Alex, [15.11.2024 17:52]
/start

Vika, [15.11.2024 17:52]
Привет! Я бот, помогающий твоему здоровью.
Введите команду 'Calories', чтобы узнать свою норму калорий.

Alex, [15.11.2024 17:52]
Calories

Vika, [15.11.2024 17:52]
Введите свой возраст:

Alex, [15.11.2024 17:52]
66

Vika, [15.11.2024 17:52]
Введите свой рост в сантиметрах:

Alex, [15.11.2024 17:52]
182

Vika, [15.11.2024 17:52]
Введите свой вес в килограммах:

Alex, [15.11.2024 17:53]
87

Vika, [15.11.2024 17:53]
Ваша норма калорий: 1516.50
"""