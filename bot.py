from discord.ext import commands
import os

token = os.environ.get('token')

client = commands.Bot(command_prefix = '%')
CHNLCMND = 695252473509707846
CHNLMSG = 697026084734238801
CHNLINFO = 697025872124706916
KodyId = 569461495407312902
BumerId = 413070873310789644
TimBoxGameId = 487612969736339457
@client.event
async def on_ready():
    print('Бот готов')

@client.command()
async def Help(ctx):
    if ctx.channel.id == CHNLCMND:
        await ctx.send('```Команды:```\n``%Help`` - Помощь по командам бота\n``%JoinClan ИмяКлана`` - вступить в клан\n``%LeaveClan`` - выйти из клана в котором вы состоите\n``%ChangeMain ИмяПользователя`` - сменить лидера клана на другого члена клана (для лидера клана)\n``%ChangeName ИмяКлана НаИмяКлана`` - изменяет имя клана(для админов и лидера клана)\n``%MembersClan ИмяКлана`` - список членов клана\n``%AddClan ИмяКлана`` - создает клан\n``%CreateTable`` - создает топ кланов (для админов)\n``%DeleteClan ИмяКлана`` - удаляет клан (очки клана тоже удаляются, для админов и лидера клана)\n``%AddPoint кол-во ИмяКлана`` - добавляет очки клану (для админов)')

@client.command()
async def MembersClan(ctx, arg1):
    if ctx.channel.id == CHNLCMND:
        with open('members.txt', 'r') as f:
            SS = f.read()
        SS = SS.split()
        msg = f'```Члены клана {arg1}:```\n'
        for i in range(0, len(SS), 2):
            if SS[i] == arg1:
                msg += f'``{SS[i + 1]}``\n'
        await ctx.send(msg)

@client.command()
async def ChangeMain(ctx, arg1):
    if ctx.channel.id == CHNLCMND:
        S = False
        with open('clanAuthor.txt', 'r') as f:
            SS = f.read()
        SS = SS.split()
        ClanName = ''
        for i in range(1, len(SS), 2):
            if SS[i] == str(ctx.author):
                S = True
                ClanName = SS[i - 1]

        if S == True:
            S = False
            with open('members.txt', 'r') as f:
                SS = f.read()
            SS = SS.split()
            for i in range(1, len(SS), 2):
                if SS[i] == arg1:
                    S = True
            if S == True:
                with open('clanAuthor.txt', 'r') as f:
                    old_data = f.read()
                SS  = old_data.split()
                WC = ''
                for i in range(1, len(SS), 2):
                    if SS[i] == str(ctx.author):
                        WC = f'{SS[i - 1]} {SS[i]}'
                new_data = old_data.replace(f'{WC[0]} {WC[1]}', f'{WC[0]} {arg1}')
                with open('clanAuthor.txt', 'w') as f:
                    f.write(new_data)
                chnlinfo = client.get_channel(CHNLINFO)
                await chnlinfo.send(f'{str(ctx.author)} сменил лидера клана {ClanName} на {arg1}')
                await ctx.send(f'Вы сменили лидера клана {ClanName} на {arg1}')
            else:
                ctx.send(f'{arg1} не член клана {ClanName}')
        else:
            await ctx.send(f'Вы не глава клана {ClanName}')

@client.command()
async def LeaveClan(ctx):
    if ctx.channel.id == CHNLCMND:
        with open('members.txt', 'r') as f:
            SS = f.read()
        SS = SS.split()
        S = False
        for i in range(1, len(SS), 2):
            if SS[i] == str(ctx.author):
                S = True
                break
        if S == True:
            with open('clanAuthor.txt', 'r') as f:
                SS = f.read()
            SS = SS.split()
            for i in range(1, len(SS), 2):
                if SS[i] == str(ctx.author):
                    S = False
                    break
            if S == True:
                with open('members.txt', 'r') as f:
                    old_data = f.read()
                SS = old_data.split()
                WC = ''
                for i in range(1, len(SS), 2):
                    if SS[i] == str(ctx.author):
                        WC = f'{SS[i - 1]} {SS[i]}'
                new_data = old_data.replace(WC, '')
                with open('clan.txt', 'w') as f:
                    f.write(new_data)
                chnlinfo = client.get_channel(CHNLINFO)
                WC = WC.split()
                await chnlinfo.send(f'{str(ctx.author)} вышел из клана {WC[0]}')
                await ctx.send(f'Вы вышли из клана {WC[0]}')
            else:
                await ctx.send('Вы лидер клана, вы не можете покинуть его')
        else:
            await ctx.send('Вы не состоите в клане')

@client.command()
async def JoinClan(ctx, arg1):
    if ctx.channel.id == CHNLCMND:
        S = False
        with  open('clan.txt', 'r') as f:
            SS = f.read()
        SS = SS.split()
        for i in range(0, len(SS), 2):
            if SS[i] == arg1:
                S = True
                break

        if S == True:
            with open('members.txt', 'r') as f:
                SS = f.read()
            SS = SS.split()
            NameClan = ''
            for i in range(1, len(SS), 2):
                if SS[i] == str(ctx.author):
                    S = False
                    NameClan = SS[i - 1]
                    break
            if S == True:
                with open('members.txt', 'a') as f:
                    f.write(f'{arg1} {str(ctx.author)} ')
                await ctx.send(f'Вы вошли в клан ``{arg1}``')
                chnlinfo = client.get_channel(CHNLINFO)
                await chnlinfo.send(f'``{str(ctx.author)}`` вошел в клан ``{arg1}``')
            else:
                await ctx.send(f'Вы уже состоите в клане ``{NameClan}``')
        else:
            await ctx.send(f'Клана ``{arg1}`` не существует')

@client.command()
async def ChangeName(ctx, arg1, arg2):
    if ctx.channel.id == CHNLCMND:
        with open('clanAuthor.txt', 'r') as f:
            SS = f.read()
        SS = SS.split()
        for i in range(0, len(SS), 2):
            if SS[i] == arg1:
                author = SS[i + 1]
        if ctx.author.id == KodyId or ctx.author.id == BumerId or ctx.author.id == TimBoxGameId or ctx.author == author:
            with open('clan.txt', 'r') as f:
                old_data = f.read()
            SS = old_data.split()
            WC = ''
            for i in range(len(SS)):
                if SS[i] == arg1:
                    WC = SS[i]
            new_data = old_data.replace(WC, arg2)
            with open('clan.txt', 'w') as f:
                f.write(new_data)
            chnl = client.get_channel(CHNLMSG)
            with open('msg.txt', 'r') as f:
                message = await chnl.fetch_message(f.read())
            with open('clan.txt', 'r') as f:
                lines = f.read()
                clans = lines
            SS = clans.split()
            for i in range(1, len(SS), 2):
                SS[i] = int(SS[i])
            b = dict(zip(SS[0::2], SS[1::2]))
            b = {k: b[k] for k in sorted(b, key=b.get, reverse=True)}
            msg = '```Лучшие кланы:```\n'
            for i in range(int(len(SS)) // 2):
                msg += f'``{str(i + 1)}. {list(b.keys())[i]} {str(list(b.values())[i])} очков``\n'
            with open('clanAuthor.txt', 'r') as f:
                old_data = f.read()
            SS = old_data.split()
            WC = ''
            for i in range(len(SS)):
                if SS[i] == arg1:
                    WC = f'{SS[i]} {SS[i + 1]}'
            new_data = old_data.replace(WC,'')
            with open('clanAuthor.txt', 'w') as f:
                f.write(new_data)
            chnlinfo = client.get_channel(CHNLINFO)
            await message.edit(content=msg)
            await chnlinfo.send(f'``{ctx.author}`` изменил название клана с ``{arg1}`` на ``{arg2}``')
            await ctx.send(f'Вы изменили имя клана c ``{arg1}`` на ``{arg2}``')
        else:
            await ctx.send('Вы не можете использовать эту команду')

@client.command()
async def DeleteClan(ctx, arg1):
    if ctx.channel.id == CHNLCMND:
        Yes = False
        with open('clanAuthor.txt', 'r') as f:
            SS = f.read()
        SS = SS.split()
        for i in range(0, len(SS), 2):
            if SS[i] == arg1:
                Yes == True
                break
        if ctx.author.id == KodyId or ctx.author.id == BumerId or ctx.author.id == TimBoxGameId or Yes == True:
            with open('clan.txt', 'r') as f:
                old_data = f.read()
            SS = old_data.split()
            WC = ''
            for i in range(len(SS)):
                if SS[i] == arg1:
                    WC = SS[i] + ' ' + SS[i + 1]
            new_data = old_data.replace(WC,'')
            chnl = client.get_channel(CHNLMSG)
            with open('clan.txt', 'w') as f:
                f.write(new_data)
            with open('msg.txt', 'r') as f:
                message = await chnl.fetch_message(f.read())
            with open('clan.txt', 'r') as f:
                lines = f.read()
                clans = lines
            SS = clans.split()
            for i in range(1, len(SS), 2):
                SS[i] = int(SS[i])
            b = dict(zip(SS[0::2], SS[1::2]))
            b = {k: b[k] for k in sorted(b, key=b.get, reverse=True)}
            msg = '```Лучшие кланы:```\n'
            for i in range(int(len(SS)) // 2):
                msg += f'``{str(i + 1)}. {list(b.keys())[i]} {str(list(b.values())[i])} очков``\n'
            with open('clanAuthor.txt', 'r') as f:
                old_data = f.read()
            SS = old_data.split()
            WC = ''
            for i in range(len(SS)):
                if SS[i] == arg1:
                    WC = f'{SS[i]} {SS[i + 1]}'
            new_data = old_data.replace(WC,'')
            with open('clanAuthor.txt', 'w') as f:
                f.write(new_data)
            await message.edit(content=msg)
            chnlinfo = client.get_channel(CHNLINFO)
            await chnlinfo.send(f'``{ctx.author}`` удалил клан ``{arg1}``')
            await ctx.send(f'Вы удалили клан ``{arg1}``')
        else:
            await ctx.send('Вы не можете использовать эту команду')

@client.command()
async def AddPoint(ctx, arg1:int, arg2):
    if ctx.channel.id == CHNLCMND:
        if ctx.author.id == KodyId or ctx.author.id == BumerId or ctx.author.id == TimBoxGameId:
            with open('clan.txt', 'r') as f:
                old_data = f.read()
            SS = old_data.split()
            WC = ''
            for i in range(len(SS)):
                if SS[i] == arg2:
                    WC = SS[i] + ' ' + SS[i + 1]
            S = WC.split()
            new_data = old_data.replace(WC, S[0] + ' ' + str(int(S[1]) + arg1))
            chnl = client.get_channel(CHNLMSG)
            with open('clan.txt', 'w') as f:
                f.write(new_data)
            with open('msg.txt', 'r') as f:
                message = await chnl.fetch_message(f.read())
            with open('clan.txt', 'r') as f:
                lines = f.read()
                clans = lines
            SS = clans.split()
            for i in range(1, len(SS), 2):
                SS[i] = int(SS[i])
            b = dict(zip(SS[0::2], SS[1::2]))
            b = {k: b[k] for k in sorted(b, key=b.get, reverse=True)}
            msg = '```Лучшие кланы:```\n'
            for i in range(int(len(SS)) // 2):
                msg += f'``{str(i + 1)}. {list(b.keys())[i]} {str(list(b.values())[i])} очков``\n'
            await message.edit(content=msg)
            chnlinfo = client.get_channel(CHNLINFO)
            await chnlinfo.send(f'``{ctx.author}`` добавил ``{arg1}`` очков к клану ``{arg2}``')
            await ctx.send(f'Вы добавили ``{arg1}`` очков к клану ``{arg2}``')
        else:
            await ctx.send('Вы не можете использовать эту команду')

@client.command()
async def AddClan(ctx, arg1):
    if ctx.channel.id == CHNLCMND:
        with open('clan.txt', 'r') as f:
            lines = f.read()
            clans = lines
        SS = clans.split()
        S = 0
        S2 = True
        with open('clan.txt', 'r'):
            for i in range(0, len(SS), 2):
                if SS[i] == arg1:
                    await ctx.send('Клан с таким именем уже существует')
                    break
                else:
                    S += 1
        with open('clanAuthor.txt', 'r') as f:
            SSS = f.read().split()
        for i in range(1, len(SSS), 2):
            if SSS[i] == str(ctx.author):
                S2 = False
        if S == int(len(SS))//2:
            if S2 == True:
                chnl = client.get_channel(CHNLMSG)
                chnlinfo = client.get_channel(CHNLINFO)
                with open('clan.txt', 'a') as f:
                    f.write(arg1 + ' 0 ')
                with open('clanAuthor.txt', 'a')as f:
                    f.write(arg1 + ' ' + str(ctx.author) + ' ')
                with open('msg.txt', 'r') as f:
                    message = await chnl.fetch_message(f.read())
                with open('clan.txt', 'r') as f:
                    lines = f.read()
                    clans = lines
                SS = clans.split()
                for i in range(1, len(SS), 2):
                    SS[i] = int(SS[i])
                b = dict(zip(SS[0::2], SS[1::2]))
                b = {k: b[k] for k in sorted(b, key=b.get, reverse=True)}
                msg = '```Лучшие кланы:```\n'
                for i in range(int(len(SS)) // 2):
                    msg += f'``{str(i + 1)}. {list(b.keys())[i]} {str(list(b.values())[i])} очков``\n'
                await message.edit(content=msg)
                await chnlinfo.send(f'``{ctx.author}`` создал клан ``{arg1}``')
                await ctx.send(f'Вы создали клан ``{arg1}``')
                with open('members.txt', 'a')as f:
                    f.write(f'{arg1} {ctx.author} ')
            else:
                await ctx.send('Вы не можете создать больше одного клана')

@client.command()
async def CreateTable(ctx):
    if ctx.channel.id == CHNLCMND:
        if ctx.author.id == KodyId or ctx.author.id == BumerId or ctx.author.id == TimBoxGameId:
            with open('clan.txt', 'r') as f:
                lines = f.read()
                clans = lines
            SS = clans.split()
            for i in range(1, len(SS), 2):
                SS[i] = int(SS[i])
            b = dict(zip(SS[0::2], SS[1::2]))
            b = {k: b[k] for k in sorted(b, key=b.get, reverse=True)}
            msg = '```Лучшие кланы:```\n'
            for i in range(int(len(SS))//2):
                msg += f'``{str(i + 1)}. {list(b.keys())[i]} {str(list(b.values())[i])} очков``\n'
            chnl = client.get_channel(CHNLMSG)
            message = await chnl.send(content=msg)
            await ctx.send('Вы создали топ кланов')
            with open('msg.txt', 'w') as f:
                f.write(str(message.id))
        else:
            await ctx.send('Вы не можете использовать эту команду')
client.run(token)
