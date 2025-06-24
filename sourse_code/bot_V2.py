from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
import os
import ai_V5

load_dotenv()

router = Router()


class Form(StatesGroup):
    waiting_for_intro = State()
    waiting_for_answers = State()


hello_message = '''
🌟 Добро пожаловать в ASTfy! 🌟

Я помогу тебе:
1️⃣ Определить твои сильные стороны 
2️⃣ Выявить профессиональные склонности
3️⃣ Подобрать подходящие профессии

<b>Просто нажми кнопку "🔍 Начать тестирование", и мы начнём!</b>
'''


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔍 Начать тестирование")
    return builder.as_markup(resize_keyboard=True)


def get_restart_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="/start")
    return builder.as_markup(resize_keyboard=True)


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        hello_message,
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "🔍 Начать тестирование")
async def start_testing(message: Message, state: FSMContext):
    await message.answer(
        "Давай начнем! Для начала расскажи о себе, своих увлечениях и хобби",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Form.waiting_for_intro)


@router.message(Form.waiting_for_intro)
async def process_intro(message: Message, state: FSMContext):
    try:
        response = ai_V5.main(message.text)
        if 'посмотрите, что нашлось в поиске' in response.lower():
            await message.answer(
                "Произошла ошибка, начните тест заново",
                reply_markup=get_restart_keyboard()
            )
            await state.clear()
            return

        await state.set_state(Form.waiting_for_answers)
        await message.answer(
            f"Отлично! Теперь ответь на пару вопросов:\n\n{response}\n\n"
            "<b>P.S. Пиши настолько развернуто, на сколько это возможно😉</b>",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )

    except Exception as e:
        await message.answer(
            f"Произошла ошибка: {str(e)}",
            reply_markup=get_restart_keyboard()
        )
        await state.clear()


@router.message(Form.waiting_for_answers)
async def process_answers(message: Message, state: FSMContext):
    try:
        response = ai_V5.ans(message.text)
        if 'посмотрите, что нашлось в поиске' in response.lower():
            await message.answer(
                "Произошла ошибка, начните тест заново",
                reply_markup=get_restart_keyboard()
            )
        else:
            await message.answer(
                f"Супер! Вот ряд профессий, которые могут тебе подойти:\n\n{response}\n\n"
                "Чтобы начать заново, нажмите /start",
                parse_mode="HTML",
                reply_markup=get_restart_keyboard()
            )

        await state.clear()

    except Exception as e:
        await message.answer(
            f"Произошла ошибка: {str(e)}",
            reply_markup=get_restart_keyboard()
        )
        await state.clear()


async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())