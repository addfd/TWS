from aiogram.types import BotCommand


private = [
    BotCommand(command='menu', description='Посмотреть меню'),
    BotCommand(command='about', description='О нас'),
    BotCommand(command='payment', description='Варианты оплаты'),
    BotCommand(command='shipping', description='Варианты доставки'),
    BotCommand(command='login', description='Авторизоваться'),
    BotCommand(command='ls', description='Список авторизованных администраторов')
]