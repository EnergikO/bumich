from random import randint
from time import time
from discord.ext import commands
from settings import settings
import finctions

client = commands.Bot(command_prefix=settings['prefix'])

time_for_purge = 15  # Удаления сообщений. НЕ админы могут только раз в столько секунд
time_last_purge = 0  # Сколько секунд назад последний раз удаляли сообщения


@client.event
async def on_ready():
    print(f"{settings['botName']} successful launch!")


@client.command()
# Удаляет столько сообщений, сколько попросят.
# На пользователей, не имеющих статуса админа/модератора наложены ограничения
async def clear(ctx, count=None):
    # Создаём видимость работы
    await ctx.trigger_typing()

    # Проверка, ввели ли числа или нет
    if finctions.may_be_class(count):
        count = int(count)
    else:

        await ctx.send('Некорректное кол-во')
        return

    # Сколько сообщений можно удалять НЕ админам/модераторам
    max_delete_not_admin = 10

    user_top_role = ctx.message.author.top_role

    # Только этим ролям доступно удаление без ограничений
    if str(user_top_role) == "Admin" or str(user_top_role) == "Moderator":
        await ctx.message.channel.purge(limit=count + 1)

    else:
        # Если малое кол-во, то можно удалить
        if count <= max_delete_not_admin:

            # Чтобы кто-то не удалил всё за 1500 сообщений в секунду
            global time_last_purge

            if time() - time_last_purge >= time_for_purge:
                # Обновление счёта времени
                time_last_purge = time()
                # Само удаление сообщений
                await ctx.message.channel.purge(limit=count + 1)
            else:
                await ctx.send('Прошло недостаточно времени')
        else:
            await ctx.send(f'Нет права на удаления такого количества сообщений, разрешено удалять '
                           f'{max_delete_not_admin} сообщений за раз')


@client.command()
# Пишет в чат набор из случайных подбрасываний монетки, нет ограничений
async def coin(ctx, count=None):
    # Создаём видимость работы
    await ctx.trigger_typing()

    # Проверка, ввели ли числа или нет
    if finctions.may_be_class(count):
        count = int(count)
    else:

        await ctx.send('Некорректное кол-во')
        return

    answer = ''
    for i in range(count):
        temp_coin = randint(0, 1)

        if temp_coin == 1:
            answer += 'Орёл '
        else:
            answer += 'Решка '

    # Вывод
    await ctx.send(answer)


@client.command()
# Выводит инструкции, по заданной команде
async def commands(ctx, command_name=None):
    # Создаём видимость работы
    await ctx.trigger_typing()

    # Лист всех команд
    commands_name = ['clear', 'coin', 'commands / help', 'roll', 'stop']

    if command_name is None:
        what_send = '```Вот, что я могу:\n'
        for command in commands_name:
            what_send += command + '\n'
        what_send += '```'

        await ctx.send(what_send)

    elif command_name == 'clear':
        await ctx.send(
            '.clear <количество_сообщений>\n\n' +

            'Удаляет столько сообщений, сколько попросят.\n' +
            'На пользователей, не имеющих статуса админа/модератора наложены ограничения\n\n'

            'Временно не работает в ЛС с ботом')
    elif command_name == 'coin':
        await ctx.send(
            '.coin <количество_бросков>\n\n' +

            'Пишет в чат набор из случайных подбрасываний монетки, нет ограничений\n'
        )
    elif command_name in 'commands / help':
        await ctx.send(
            '.commands <команда>\n\n' +

            'Выводит инструкции по заданной команде'
        )
    elif command_name == 'roll':
        await ctx.send(
            '.roll <граница 1> <граница 2> <количество чисел>\n' +
            'Значения по умолчанию:\n'
            '<граница 1> - 100\n<граница 2> - 1\n'
            '<количество чисел> - 1\n\n'

            'Пишет в чат набор из случайных чисел, нет ограничений, ввод диапазона чисел в любом порядке'
        )
    elif command_name == 'stop':
        await ctx.send(
            'Иди своей дорогой сталкер'
        )
    else:
        await ctx.send(
            'Такой команды нет'
        )


@client.command()
# Пишет в чат набор из случайных чисел, нет ограничений, ввод диапазона чисел в любом порядке
async def roll(ctx, roll_first_number=None, roll_second_number=None, count=None):
    # Создаём видимость работы
    await ctx.trigger_typing()

    # Проверка, что ввели, а что нет
    # То, что не ввели или ввели неверно значения возьмутся по умолчанию

    if finctions.may_be_class(roll_first_number):  roll_first_number = int(roll_first_number)
    else:  roll_first_number = 100

    if finctions.may_be_class(roll_second_number):  roll_second_number = int(roll_second_number)
    else:  roll_second_number = 1

    if finctions.may_be_class(count): count = abs(int(count))

    else:  count = 1

    # Проверка и замена для стабильной работы рандома
    if roll_first_number > roll_second_number:
        roll_first_number, roll_second_number = roll_second_number, roll_first_number

    # Проверка на правильность выходного предложения
    if count == 1:
        temp_str = f'Случайное число от {roll_first_number} до {roll_second_number}:\n'
    else:
        temp_str = f'Случайные числа от {roll_first_number} до {roll_second_number} (их тут {count}):\n'

    # Вычисления случайных чисел
    for i in range(count):
        temp_str += str(randint(roll_first_number, roll_second_number)) + ' '

    # Вывод
    await ctx.send(temp_str)


@client.command()
# Иди своей дорогой сталкер
async def stop(ctx):
    if ctx.message.author.id == 401105274955497482:
        await ctx.send('Ну, я пошёл...')
        exit()
    else:
        await ctx.send('Ты не мой братик, тебе нельзя мной командовать.')

client.run(settings["token"])
