from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message

import k
import text

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=k.menu)


@router.callback_query(F.data == "catalog")
async def input_text_prompt(msg: Message):
    await msg.answer("catalog")


@router.callback_query(F.data == "account")
async def input_text_prompt(msg: Message):
    await msg.answer("account")


@router.callback_query(F.data == "help")
async def input_text_prompt(msg: Message):
    await msg.answer("help")

@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=k.menu)