from handlers.admin import admin_features
import csv



pp = {}

with open('filters/pp.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    for row in csvreader:
        pp[row[0]] = row[1]


async def login(name, password, id, list):
    if name not in pp:
        return "Неправильный логин или пароль"
    if pp[name] == password:
        if id in list or name in [list[x] for x in list]:
            return "Пользователь уже авторизирован"
        list[id] = name
        print(list)
        print([list[x] for x in list])
        await admin_features
        return "Вы авторизовались"
    return "Неправильный логин или пароль"
