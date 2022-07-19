import os

import discord
from discord import utils, guild
from discord.ext import commands

import redis
import json

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=Discordbot.prefix, intents=intents)

redis_url = os.environ['REDIS_URL']
Token = os.environ['Token']
#  Создаём базу данных либо загружаем готовую
if redis_url is None:

    try:
        data = json.load(open('Database.json', 'r', encoding='utf-8'))  # выводим нашу базу данных

    except FileNotFoundError:

        data = {
            "post_id": 997535717926379690,
            "roles": {
                "😀": 997530892283154436,
                "😭": 997530944640667759,
                "🤙": 997530971425488956
            },
            "administrators": {
                "admins": [
                    "Qwerty64511.CREED#1408",
                    "STORM_RES#7416"
                ],
                "editors": [
                    "Qwerty64511.CREED#1408",
                    "STORM_RES#7416"
                ]
            },
            "excroles": {},
            "Max_roles_per_user": 10,
            "prefix": "!",
            "twitchlist": [
                "nigga",
                "naga",
                "ниггер",
                "нига",
                "нага",
                "faggot",
                "пидор",
                "пидорас",
                "педик",
                "гомик",
                "петух",
                "хач",
                "жид",
                "хиджаб",
                "даун",
                "аутист",
                "дебил",
                "retard",
                "негр",
                "негры",
                "нигер",
                "пидорас",
                "негр",
                "virgin",
                "simp",
                "incel",
                "девственник",
                "cимп",
                "инцел",
                "cunt",
                "пизда",
                "куколд",
                "nigger"
            ]
        }


else:

    redis_db = redis.from_url(redis_url)
    raw_data = redis_db.get('Database')
    print('Вывод базы данных')

    if raw_data is None:

        data = {
            "post_id": 997535717926379690,

            "roles": {
                "😀": 997530892283154436,
                "😭": 997530944640667759,
                "🤙": 997530971425488956
            },
            "administrators": {
                "admins": [
                    "Qwerty64511.CREED#1408",
                    "STORM_RES#7416"
                ],
                "editors": [
                    "Qwerty64511.CREED#1408",
                    "STORM_RES#7416"
                ]
            },
            "excroles": {},
            "Max_roles_per_user": 10,
            "prefix": "!",
            "twitchlist": [
                "nigga",
                "naga",
                "ниггер",
                "нига",
                "нага",
                "faggot",
                "пидор",
                "пидорас",
                "педик",
                "гомик",
                "петух",
                "хач",
                "жид",
                "хиджаб",
                "даун",
                "аутист",
                "дебил",
                "retard",
                "негр",
                "негры",
                "нигер",
                "пидорас",
                "негр",
                "virgin",
                "simp",
                "incel",
                "девственник",
                "cимп",
                "инцел",
                "cunt",
                "пизда",
                "куколд",
                "nigger"
            ]
        }

    else:
        data = json.loads(raw_data)  # выводим нашу базу данных
        print('Вывели')

bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    print('bot connected')


async def number(emoji):
    for i in range(len(data['roles'])):

        if emoji in data['roles'][i]:
            return i


async def check(text):
    for i in range(len(data['twitchlist'])):
        if data['twitchlist'][i] in text.lower().replace(' ', ''):
            return 1
    return 0


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == data['post_id']:

        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        emoji = payload.emoji.name
        member = payload.member

        if emoji in data['roles']:

            role = utils.get(message.guild.roles, id=data['roles'][emoji])

            print(f'{member} Получил роль {role}')
            await member.add_roles(role)

        else:
            print(f'Я не вижу данного эмоджи в базе. {emoji}')


@bot.event
async def on_raw_reaction_remove(payload):
    if data['post_id'] == payload.message_id:

        emoji = payload.emoji.name  # эмоджи при нажатии на которое выдается роль

        if emoji in data['roles']:  # само эмоджи

            guild = await(bot.fetch_guild(payload.guild_id))
            role = discord.utils.get(guild.roles, id=data['roles'][emoji])  # определяем роль которую будем выдавать

            member = await(guild.fetch_member(payload.user_id))

            if member is not None:  # проверяем есть ли он на сервере

                await member.remove_roles(role)  # забираем рольку
                print(f'{member} лишился роли {role}')

            else:
                print(f'{member} Не найден на сервере')

        else:
            print(f'{emoji} not found')


@bot.command()
async def base_info(ctx):
    author = ctx.message.author

    await author.send('''Первым делом тебе необходимо ознакомиться с каналом #правила. 
После этого получить необходимые роли в #добавление-ролей. 
Приятного времяпровождения на сервере CREED.   
UPD: для полной информации о функционале бота, напишите !tech_info 
С уважением, @Qwerty64511.CREED#1408''')

    print(f'Пользователь {author} получил базовую информацию о сервере')


@bot.command()
async def tech_info(ctx):
    author = ctx.message.author

    await author.send('''Функционал: добавление/удаление роли по реакции 
Приветствие пользователя при присоединении к серверу 
Фильтрация мата в сообщениях - в разработке 
Полный список команд: 
!base_info - базовая информация 
!tech_info - техническая информация 
С уважением, @Qwerty64511.CREED#1408''')

    if str(author) in (data['administrators']['admins'] or data['administrators']['editors']):
        await author.send('''Специально для администраторов, редакторов: 
!add_emoji - Добавляет эмодзи и номер роли в базу данных 
Пример работы: !add_emoji 😋 11112222 Необходимы как минимум права редактора 
!become_admin - введите команду и припишите к ней пароль, чтобы стать админом 
Пример: !become_admin 1488 
!add_banworld - Добавляет запретные слова
Пример: !add_banworld шлюпка. Слова Вводить с МАЛОЙ буквы!!!!!!!!
Обращение от разработчика: Если вы, гении засрёте мне базу данных говном. 
Будете использовать команды криво, или ещё что-то. Я блять вам в фуфайку насру.''')

    print(f'Пользователь {author} получил техническую информацию о сервере')


@bot.event
async def on_member_join(member):
    print(f'{member} присоединился к серверу')

    await member.send(f'''Приветствуем {member}, на сервере CREED. Написав команду !base_info 
ты узнаешь всю необходимую информацию по серверу.
С уважением @Qwerty64511.CREED#1408''')


# Ниже Админ панельки
# <-----|----->

# Допилить удаление эмоджи из базы

async def change_data():
    if redis_url is None:  # Обработка базы данных, если нет подключения к редис
        json.dump(data,
                  open('Database.json', 'w', encoding='utf-8'),
                  indent=2,
                  ensure_ascii=False,
                  )
        # Загружаем базу данных из редис

    else:
        redis_db = redis.from_url(redis_url)
        redis_db.set('data', json.dumps(data))


@bot.command()
async def add_emoji(ctx, emoji, text):
    author = ctx.message.author

    if str(author) in (data['administrators']['admins'] or data['administrators']['editors']):

        print(f'{author} Отправил {emoji} и роль {text}')

        data['roles'][emoji] = int(text)

        await change_data()

    else:

        await author.send('''Вы не являетесь администратором. 
Обратитесь к Qwerty64511.CREED#1408 за доступом''')


@bot.command()
async def add_banworld(ctx, *, text):
    author = ctx.message.author

    if str(author) in (data['administrators']['admins'] or data['administrators']['editors']):
        if text not in data['twitchlist']:
            data['twitchlist'] += [str(text)]

            await change_data()

            print(f'слово {text} добавлено')

    else:
        await author.send('''Вы не являетесь администратором. 
    Обратитесь к Qwerty64511.CREED#1408 за доступом''')


@bot.command()
async def delit_banworld(ctx, *, text):
    author = ctx.message.author

    if str(author) in (data['administrators']['admins'] or data['administrators']['editors']):
        if text in data['twitchlist']:

            data['twitchlist'].remove(str(text))

            await change_data()

            print(f'слово {text} удалено')
        else:
            author.send(f'Я не вижу данного слова {text} в базе')

    else:
        await author.send('''Вы не являетесь администратором. 
    Обратитесь к Qwerty64511.CREED#1408 за доступом''')


@bot.command()
async def delit_emoji(ctx, emoji):
    author = ctx.message.author

    if str(author) in (data['administrators']['admins'] or data['administrators']['editors']):
        del data['roles'][emoji]

        await change_data()

        print(f'{emoji} удалён из базы данных')


@bot.command()
async def become_admin(ctx, *, text):  # сделать ручное добавление админа (Человек не просто пишет, его добавляют,
    # а человек пишет ник другого человека и его добавляют в список. Сделать 2 вида админов: редактор, технический.
    # Сделать красивый вывод базы данных(И нужынх данных из неё) при помощи команды. Пришить интерактивную клавиатуру
    author = ctx.message.author

    if str(author) not in (data['administrators']['admins']):

        if text == '12345':
            print(f'{author} Добавлен в список технических администраторов')
            data['administrators']['admins'] += [str(author)]

            await change_data()

    if str(author) not in data['administrators']['editors']:
        if text == '123456':

            print(f'{author} Добавлен в список редакторов')
            data['administrators']['editors'] += [str(author)]

            await change_data()

            author.send('Вы стали редактором бота сервера CREED')

        else:

            await author.send('Пароль введён не верно')
            print(f'{author} пытался зайти в админ панель')

    else:

        await author.send('Вы уже в системе')


@bot.event
async def on_message(message):
    mes = message.content

    if '!' in mes:
        await bot.process_commands(message)

    else:
        if check(mes):
            await message.delete()

            print(f'Сообщение удалено {message.content}')


bot.run(Token)
