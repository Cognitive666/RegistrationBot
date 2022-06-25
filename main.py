import discord
from discord import utils, guild
import random
from discord.ext import commands
import config
import pytils.translit
import json


class MyClient(discord.Client):

    async def on_message(self, message):
        global s, password, login, pass_counter, names_checker, err_counter, name,nickname
        pass_counter = 0
        name = " "
        nickname = ""
        err_counter = 0
        names_checker = 0
        if message.author == self.user:
            return

        s = message.content
        s.lower()
        if message.content.lower().startswith("повторить") or message.content.lower().startswith("регистрация"):
            pass_counter = 0
            nickname =""
            await message.channel.send(

                f"{message.author.mention},пожалуйста, введите '"'моё имя'"' и Ваши настоящие имя и фамилию.Сообщение не должно содержать цифр и символов латиницы.Например: моё имя Иванов Иван")

        if message.content.lower().startswith("моё имя "):
            nickname = message.content
            s = message.content.lower()
            counter = 0
            s = s.replace("моё имя ", "")
            for i in range(len(s)):

                buffer = s[i]
                if buffer == " ":
                    counter = i + 1
                else:
                    if i == 0 or i == counter:
                        name += buffer.upper()
                    else:
                        name += buffer
                for j in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
                    if buffer == j:
                        err_counter = 888

            name.replace(" ", "")
            name = pytils.translit.translify(name)
            login = name

            if err_counter == 888:
                await message.channel.send(
                    f"{message.author.mention} Ваше сообщение содержит запрещённые символы.Напишите '"'Повторить'"' и введите своё имя ещё раз.")
            else:
                await message.channel.send(
                    f"Хорошо,{message.author.mention} Ваш логин:" + login + "  " + "Ваш логин должен полностью соответсвовать вашим имени и фамилии, только записанным на транслите.Если всё верно, то напишите '"'Принять'"' ,если это не так, напишите '"'Повторить'"'")
        if message.content.lower().startswith("принять"):
            if pass_counter == 0:
                alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

                password = random.choice(alphabet) + random.choice(alphabet) + random.choice(alphabet) + random.choice(
                    alphabet) + random.choice(alphabet) + random.choice(alphabet) + random.choice(
                    alphabet) + random.choice(alphabet) + random.choice(alphabet) + random.choice(alphabet)
                pass_counter += 1

            with open(config.Json_PATH, "r") as read_file:
                User_data = json.load(read_file)

                for usernames in User_data:

                    if User_data[usernames]['username'] == login:
                        names_checker = 1
            if names_checker == 1:
                await message.channel.send(
                    f"{message.author.mention}, введённый логин совпадает с логином другого игрока.Если вы ввели "
                    f"своё имя некорректно, введите'"'Повторить'"',если вы указали своё имя верно, обратитесь к "
                    "администратору сервера.")
            else:
                with open(config.Buffer_PATH, "w") as f:
                    reg_command = "config auth.std.core register" + " " + login + " " + "null@null.com" + " " + password
                    f.write(reg_command)
                    author = message.author  # получаем автора сообщения
                    guild = self.get_guild(config.Server_ID)  # получаем объект сервера*
                    role = guild.get_role(config.GamerRole_ID)  # получаем объект роли*
                    await author.add_roles(role)  # выдаем автору роль

                    await message.author.send(
                        f"{message.author.mention}Ваши данные записаны! Ваш логин:" + login + "Ваш пароль:" + password + ".Теперь вам доступны все чаты на сервере в дискорде и вход в мир.")
                    await message.author.edit(nick=nickname)

client = MyClient()
client.run(config.API_TOKEN)
