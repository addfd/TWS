from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)
from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import (
    orm_add_product,
    orm_delete_product,
    orm_get_product,
    orm_get_products,
    orm_update_product,
)
from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard
from filters.password_manager import login

user_private_router = Router()


# -----------------------------------------------------


class LoginAdmin(StatesGroup):
    # Шаги состояний
    name = State()
    password = State()


@user_private_router.message(StateFilter(None), Command("login"))
async def begin_login(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите логин", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(LoginAdmin.name)


@user_private_router.message(LoginAdmin.name, or_f(F.text, F.text == "."))
async def password(message: types.Message, state: FSMContext):

    await state.update_data(name=message.text)
    await message.answer("Введите пароль")
    await state.set_state(LoginAdmin.password)


@user_private_router.message(LoginAdmin.password, or_f(F.text, F.text == "."))
async def check(message: types.Message, state: FSMContext, bot: Bot):

    await state.update_data(password=message.text)
    data = await state.get_data()
    re = await login(data["name"], data["password"], message.from_user.id, bot.my_admins_list)
    await message.answer(re)
    await state.clear()
# -----------------------------------------------------


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        f"Привет {types.from_user.full_name}, я TWS",
        reply_markup=get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            placeholder="Что вас интересует?",
            sizes=(2, 2)
        ),
    )


# @user_private_router.message(F.text.lower() == "меню")
@user_private_router.message(or_f(Command("menu"), (F.text.lower() == "меню")))
async def menu_cmd(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<b>{product.name}</b>\
                    \n<i>{product.description}</i>\nСтоимость: {round(product.price, 2)}", parse_mode=ParseMode.HTML
        )
    await message.answer("Вот меню:")


@user_private_router.message(F.text.lower() == "о магазине")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer(f'<a href="https://github.com/addfd/TWS">GitHub</a>', parse_mode=ParseMode.HTML)


@user_private_router.message(F.text.lower() == "варианты оплаты")
@user_private_router.message(Command("payment"))
async def payment_cmd(message: types.Message):
    text = as_marked_section(
        Bold("Варианты оплаты:"),
        "Картой в боте",
        "При получении",
        "В заведении",
        marker="✅ ",
    )
    await message.answer(text.as_html(), parse_mode=ParseMode.HTML)


@user_private_router.message(
    (F.text.lower().contains("доставка")) | (F.text.lower() == "варианты доставки"))
@user_private_router.message(Command("shipping"))
async def shipping_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Варианты доставки заказа:"),
            "Курьер",
            "Самовывоз",
            marker="✅ ",
        ),
        sep="\n----------------------\n",
    )
    await message.answer(text.as_html(), parse_mode=ParseMode.HTML)
