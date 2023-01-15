from imports import *
print("спасибо за устоновку можешь узнать о нас больше - @ptsub")
logging.basicConfig(level=logging.INFO)
#CoinGecko
#api = CoinGeckoAPI()
# bot init
bot = Bot(token=cash_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["курс"])
async def start_cmd(message):
       msg = message 
       chat_id = message.chat.id
       user_name = msg.from_user.full_name
       reply_user_id = message.reply_to_message.from_user.id
       reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
       reply_user_name = str(reply_user_name[0])
       if message.reply_to_message:
          await bot.send_message(message.chat.id, f"[🕵️‍♂️] Ник пользователя | {reply_user_name} \n[🆔] | - <code>{reply_user_id}</code>", parse_mode='html')
       else:
          await bot.send_message(message.shat.id, f"Курс валюты, вот весь курс валют!                          10е16 = 25₽, 100е26 = 40₽, 100е50 = 100₽")

@dp.message_handler(commands=['gamevb'])
async def start_cmd(message):
   msg = message
   user_id = msg.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   period = 5

   balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
   balance = int(balance[0])

   gamevbmenu = InlineKeyboardMarkup(row_width=1)
   gamevb = InlineKeyboardButton(text='ИГРАТЬ 🎮', callback_data='gamevb')
   gamevbmenu.add(gamevb)

   get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
   last_stavka = f"{int(get[0])}"
   stavkatime = time.time() - float(last_stavka)
   if stavkatime > period:
      if balance > 0:
         await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вы уверены что хотите сыграть в GAME-VB ? 🧊

ℹ️ | В этой игре вы играете сразу на весь <b>баланс</b>

↘️ Выберите одну кнопку ниже         
""",reply_markup=gamevbmenu,  parse_mode='html')
      else:
         await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас недостаточно средств! ", parse_mode='html')
   else:
      await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд", parse_mode='html')         






@dp.message_handler(commands=['m'])
async def start_cmd(message):
   try:
      text = ' '.join(message.text.split()[2:])

      msg = message
      user_id = msg.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_id = int(message.text.split()[1])
      reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
      reply_user_name = str(reply_user_name[0])

      period = 5
      get = cursor.execute("SELECT stavka FROM time_sms WHERE user_id = ?", (message.from_user.id,)).fetchone()
      last_stavka = f"{int(get[0])}"
      stavkatime = time.time() - float(last_stavka)

      if len(text) > 35:
         await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, сообщение не может быть более чем 35 символов ", parse_mode='html')
         return
      if stavkatime > period:
         await bot.send_message(user_id, f"💬 | [Я ➡️ <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>] {text}", parse_mode='html')
         await bot.send_message(reply_user_id, f"💬 | [<a href='tg://user?id={user_id}'>{user_name}</a> ➡️ Я] {text}", parse_mode='html')
         cursor.execute(f'UPDATE time_sms SET stavka = {time.time()} WHERE user_id = {user_id}')
         connect.commit()
         return
      else:
         await bot.send_message(user_id, f"🆘 | Игрок, сообщение писать можно раз в 5 секунд", parse_mode='html')
         return
   except:
      await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! Либо вы не правильно ID, или данный игрок ещë не играет в бота", parse_mode='html')
      return

@dp.message_handler(commands=['info'])
async def start_cmd(message):
    msg = message
    user_id = msg.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    if not message.reply_to_message:
       await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, эта команда должна быть ответом на сообщение", parse_mode='html')
       return
       
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    reply_user_id = message.reply_to_message.from_user.id

    balance = cursor.execute(f"SELECT balance from users where user_id = {reply_user_id}").fetchone()
    balance = int(balance[0])
    balance2 = '{:,}'.format(balance)

    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    bank = cursor.execute(f"SELECT bank from users where user_id = {reply_user_id}").fetchone()
    bank = int(bank[0])
    bank3 = '{:,}'.format(bank)

    user_tg_name = message.from_user.get_mention(as_html=True)

    reply_user_status = cursor.execute(f"SELECT user_status from users where user_id = {reply_user_id}").fetchone()
    reply_user_status = str(reply_user_status[0])

    ethereum = cursor.execute(f"SELECT ethereum from users where user_id = {reply_user_id}").fetchone()
    ethereum = int(ethereum[0])
    ethereum2 = '{:,}'.format(ethereum)

    rating = cursor.execute(f"SELECT rating from users where user_id = {reply_user_id}").fetchone()
    rating = int(rating[0])
    rating2 = '{:,}'.format(rating)

    status_block = cursor.execute(f"SELECT status_block from users where user_id = {reply_user_id}").fetchone()
    status_block = str(status_block[0])

    time_register = cursor.execute(f"SELECT time_register from users where user_id = {reply_user_id}").fetchone()
    time_register = time_register[0]

    pref = cursor.execute(f"SELECT pref from users where user_id = {reply_user_id}").fetchone()
    pref = str(pref[0])

    donate_coins = cursor.execute(f"SELECT donate_coins from users where user_id = {reply_user_id}").fetchone()
    donate_coins = int(donate_coins[0])
    donate_coins2 = '{:,}'.format(donate_coins)

    bank2 = cursor.execute(f"SELECT bank2 from users where user_id = {reply_user_id}").fetchone()
    bank2 = int(bank2[0])
    bank22 = '{:,}'.format(bank2)

    depozit = cursor.execute(f"SELECT depozit from users where user_id = {reply_user_id}").fetchone()
    depozit = int(depozit[0])
    depozit2 = '{:,}'.format(depozit)

    if user_status in ['Owner', 'Helper_Admin', 'Admin', 'Player']:
       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные о <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> :

'💢профиль:\n🥷Ник: {user_name}\n🔎ID: «{user_id}»\n💥Статус: {statuss}\n💸Баланс: {balance3}\n🏦В банке: {bank3}\n {bitcoin3}\n👑Рейтинг: {rating3}\n Имущество:\n{imushestvo}\n\n🪀Всего сыграно игр: {games}\n🧿Дата регистрации: {times}', parse_mode='html')     
       """, parse_mode='html')


@dp.message_handler(commands=['info_id'])
async def start_cmd(message):
    msg = message
    user_id = msg.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    

    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    reply_user_id = int(message.text.split()[1])

    balance = cursor.execute(f"SELECT balance from users where user_id = {reply_user_id}").fetchone()
    balance = int(balance[0])
    balance2 = '{:,}'.format(balance)

    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    bank = cursor.execute(f"SELECT bank from users where user_id = {reply_user_id}").fetchone()
    bank = int(bank[0])
    bank3 = '{:,}'.format(bank)

    user_tg_name = message.from_user.get_mention(as_html=True)

    reply_user_status = cursor.execute(f"SELECT user_status from users where user_id = {reply_user_id}").fetchone()
    reply_user_status = str(reply_user_status[0])

    ethereum = cursor.execute(f"SELECT ethereum from users where user_id = {reply_user_id}").fetchone()
    ethereum = int(ethereum[0])
    ethereum2 = '{:,}'.format(ethereum)

    rating = cursor.execute(f"SELECT rating from users where user_id = {reply_user_id}").fetchone()
    rating = int(rating[0])
    rating2 = '{:,}'.format(rating)

    status_block = cursor.execute(f"SELECT status_block from users where user_id = {reply_user_id}").fetchone()
    status_block = str(status_block[0])

    time_register = cursor.execute(f"SELECT time_register from users where user_id = {reply_user_id}").fetchone()
    time_register = time_register[0]

    pref = cursor.execute(f"SELECT pref from users where user_id = {reply_user_id}").fetchone()
    pref = str(pref[0])

    donate_coins = cursor.execute(f"SELECT donate_coins from users where user_id = {reply_user_id}").fetchone()
    donate_coins = int(donate_coins[0])
    donate_coins2 = '{:,}'.format(donate_coins)

    bank2 = cursor.execute(f"SELECT bank2 from users where user_id = {reply_user_id}").fetchone()
    bank2 = int(bank2[0])
    bank22 = '{:,}'.format(bank2)

    depozit = cursor.execute(f"SELECT depozit from users where user_id = {reply_user_id}").fetchone()
    depozit = int(depozit[0])
    depozit2 = '{:,}'.format(depozit)

    if user_status != ['Owner', 'Helper_Admin', 'Admin']:
       user_status2 = 'Пользователь'
    if user_status in ['Owner', 'Helper_Admin', 'Admin']:
       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные о <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> :

💻 | Телеграм: {user_tg_name}
🟢 | Статус: {reply_user_status}
🟩 | Статус блокировки: {status_block}

🌪 | Ник: {reply_user_name}
🕸 | Баланс: {balance2}$
🏹 | Банковский счёт: {bank3}$
🏪 | Хранительный счёт: {bank22}$
🏛 | Депозит: {depozit2}$
🟪 | Эфириум: {ethereum2} 🟣
💥 | Рейтинг: {rating2} 💎
👻 | Donate-Coins: {donate_coins2} 🪙
реклама:
{reklama11}

📆 | Дата регистрации: {time_register}     
       """, parse_mode='html')

@dp.message_handler(commands=['/ping'])
async def zeus_ping(message: types.Message):
    a = time.time()
    bot_msg = await message.answer(f'Проверяю пинг...')
    if bot_msg:
        b = time.time()
    await bot_msg.edit_text(f'#PING: <i>{round((b-a)*100, 2)}</i> мс')
    

@dp.message_handler(commands=['sql'])
async def sql(message: types.Message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    
    if message.from_user.id == 5197897742:
        try:
         cursor.execute(message.text[message.text.find(' '):])
         connect.commit()
         a = time.time()
         bot_msg = await message.answer(f'🕘Please wait while me doing SQL request', parse_mode="Markdown")
         if bot_msg:
          b = time.time()
          await bot_msg.edit_text(f"🚀*SQL Запрос был выполнен за {round((b-a)*1000)} ms*", parse_mode="Markdown")
        except:
         await message.answer(f"❌Возникла ошибка при изменении в БД[Данной таблицы/игрока нету в БД]")


@dp.message_handler(lambda m: m.text.lower() in ["купоны", "Купоны"])
async def promiki(message):
	list = cursor.execute(f'SELECT * FROM promiki ORDER BY reward DESC').fetchmany(30)
	top_list = []
	rec = cursor.execute('SELECT * FROM promiki').fetchall()
	vsego2 = len(rec)
	if vsego2 == 0:
		return await message.answer('Купонов еще нет или их удалили.')
	num = 0
	for user in list:
		num += 1
		top_list.append(f'{num}. {user[1]} | На одного: $  {user[2]}  | Активаций: {user[3]} | Активировали: {user[4]}')
	top = "\n".join(top_list)
	return await message.answer(f'Вот все купоны: {vsego2}\n\n' + top)

@dp.message_handler(lambda t: t.text.startswith("купон создать") or t.text.startswith("Купон создать") or t.text.startswith("+Купон") or t.text.startswith("+купон"))
async def promo(message):
	user_name = cursor.execute(f"SELECT user_name from users where user_id = {message.from_user.id}").fetchone()
	balance = cursor.execute(f"SELECT balance from users where user_id = {message.from_user.id}").fetchone()
	balance = round(int(balance[0]))
	balance2 = '{:,}'.format(balance).replace(',', '.')
	user_name = user_name[0]
	try:
		name = message.text.split()[2]
		akt = int(message.text.split()[3])
		dengi5 = message.text.split()[4]
	except:
		await message.answer(f'️❌Неправильно введены аргументы!\n❕ купон создать  [название] [количество использований] [сумма]')
	cursor.execute(f"SELECT promo_name FROM promiki WHERE promo_name = '{name}' ") # тг превращает ' в "
	akt2 = '{:,}'.format(akt).replace(',', '.')
	dengi4 = (dengi5).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '').replace("$", "").replace('м', '000000').replace('m', '000000')
	dengi3 = float(dengi4)
	dengi = int(dengi3)
	denfi = int(dengi*akt)
	denfi2 = '{:,}'.format(denfi).replace(',', '.')
	dengi2 = '{:,}'.format(dengi).replace(',', '.')
	if cursor.fetchone() != None:
		return await message.answer(f'Данный купон "{name}" занят.')
	if dengi*akt > balance:
		return await message.answer(f'❗️ У вас недостаточно средств\nНа балансе: {balance2}')
	if len(name) < 3 or len(name) > 24:
		return await message.answer(f'❕Вы не можете создать купон с названием меньше 3 символов и больше 24 символов.')
	if akt < 2:
		return await message.answer(f'❌ Извини, но нельзя создавать купоны, где количество активаций 1')
	if dengi < 100:
		return await message.answer(f'❌ Извини, но нельзя создавать купоны, где на одного пользователя дают: 100$')
	cursor.execute(f"INSERT INTO promiki VALUES ({message.from_user.id}, '{name}', {dengi}, {akt}, 0)")
	connect.commit()
	cursor.execute(f'UPDATE users SET balance = {balance-dengi*akt} WHERE user_id = {message.from_user.id}')
	connect.commit()
	return await message.answer(f'\n🎫Купон: {name}\n🌪 Содержит: {denfi2}$\n👥 Количество использований: {akt2} раз(a)\n👤 На одного человека: {dengi2}$')
	
@dp.message_handler(lambda t: t.text.startswith("купон") or t.text.startswith("Купон"))
async def promoco(message):
	try:
		vvod = message.text.split()[1]
	except:
		return await message.answer(f' Вы не ввели имя купона 😕')
	cursor.execute(f"SELECT activation FROM promo WHERE user_id = {message.from_user.id} AND promo_name = '{vvod}'")
	if cursor.fetchone() != None:
		return await message.answer(f'❌ 😞 Вы уже активировали данный купон')
	cursor.execute(f"SELECT promo_name FROM promiki WHERE promo_name = '{vvod}'")
	if cursor.fetchone() == None:
		return await message.answer('Данного купона не существует.')
	cursor.execute(f"SELECT users, max_users, reward FROM promiki WHERE promo_name = '{vvod}'")
	for k in cursor.fetchall():
		if k[0] >= k[1]:
			pp = '{:,}'.format(k[1]).replace(',', '.')
			return await message.answer(f'👥 Этот купон уже активировало все <code>{pp}</code> пользователей.', parse_mode='html')
	cursor.execute(f"UPDATE promiki SET users = users + 1 WHERE promo_name = '{vvod}'")
	cursor.execute(f"UPDATE users SET balance = balance + {k[2]} WHERE user_id = {message.from_user.id}")
	cursor.execute(f"INSERT INTO promo VALUES ({message.from_user.id}, 1, '{vvod}')")
	connect.commit()
	money = '{:,}'.format(k[2]).replace(',', '.')
	balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
	balance = round(int(balance[0]))
	balik2 = '{:,}'.format(balance).replace(',', '.')
	return await message.answer(f'🎫 Вы активировали купон\n✅ На ваш баланс зачислено: <code>{money}</code>$\nТеперь ваш баланс составляет: <code>{balik2}</code>$', parse_mode='html')


@dp.message_handler(commands=['channel_mute'], commands_prefix='!?./', is_chat_admin=True)
async def mute(message):
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
       await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
       return
    try:
       muteint = float(message.text.split()[1])
       mutetype = message.text.split()[2]
       comment = " ".join(message.text.split()[3:])
    except IndexError:
       await message.reply('ℹ | Не хватает аргументов!\nПример:\n<code>/мут 1 ч причина</code>')
       return
    if mutetype == "ч" or mutetype == "часов" or mutetype == "час":
       dt = datetime.now() + timedelta(hours=muteint)
       timestamp = dt.timestamp()
       await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
       await message.reply(f'👤 | Администратор: {name1}\n🛑 | Замутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | Срок: {muteint} {mutetype}\n📃 | Причина: {comment}',  parse_mode='html')
    if mutetype == "м" or mutetype == "минут" or mutetype == "минуты":
       dt = datetime.now() + timedelta(minutes=muteint)
       timestamp = dt.timestamp()
       await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
       await message.reply(f'👤 | Администратор: {name1}\n🛑 | Замутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | Срок: {muteint} {mutetype}\n📃 | Причина: {comment}',  parse_mode='html')
    if mutetype == "д" or mutetype == "дней" or mutetype == "день":
       dt = datetime.now() + timedelta(days=muteint)
       timestamp = dt.timestamp()
       await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
       await message.reply(f'👤 | Администратор: {name1}\n | 🛑Замутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | Срок: {muteint} {mutetype}\n📃 | Причина: {comment}',  parse_mode='html')

@dp.message_handler(commands=['channel_unmute'], commands_prefix='!?./', is_chat_admin=True)
async def unmute(message):
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
       await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
       return
    await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True))
    await message.reply(f'👤 | Администратор: {name1}\n🔊 | Размутил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>',  parse_mode='html')

@dp.message_handler(commands=['channel_ban', 'channel_kick'], commands_prefix='!?./', is_chat_admin=True)
async def ban(message):
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
       await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
       return
    comment = " ".join(message.text.split()[1:])
    await bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False))
    await message.reply(f'👤 | Администратор: {name1}\n🛑 | Забанил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | Срок: навсегда\n📃 | Причина: {comment}',  parse_mode='html')

@dp.message_handler(commands=['channel_unban'], commands_prefix='!?./', is_chat_admin=True)
async def unban(message):
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
       await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
       return
    await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True))
    await message.reply(f'👤 | Администратор: {name1}\n📲 | Разбанил: <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>',  parse_mode='html')
@dp.message_handler(commands=['report'])
async def report(message):
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_id = message.from_user.id

    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    text = message.text[7:]
    
    if text == '':
       await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, репорт не может быть пустым", parse_mode='html')
       return
    rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
    for row in rows:
       await bot.send_message(row[0], f"<b>🆘ВАМ ПРИШЁЛ РЕПОРТ🆘</b>\n👨 | Отправитель: <a href='tg://user?id={user_id}'>{user_name}</a>\n💬 |Сообщение: <i>{text}</i>", parse_mode='html')

    await bot.send_message(5197897742,f"""
<b>🆘ВАМ ПРИШЁЛ РЕПОРТ🆘</b>
👨 | Отправитель: <a href='tg://user?id={user_id}'>{user_name}</a>  
💬 |Сообщение: <i>{text}</i>
    """, parse_mode='html')  
    await bot.send_message(message.chat.id, f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш репорт был успешно отправлен администрации", parse_mode='html')






@dp.message_handler(commands=['unwarn'])
async def posting(message):
    if not message.reply_to_message:
       await message.reply("🆘 | Эта команда должна быть ответом на сообщение!")
       return   
    reply_user_id = message.reply_to_message.from_user.id

    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])
    user_id = message.from_user.id
    

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    warn = cursor.execute(f"SELECT warn from warn where user_id = {reply_user_id}").fetchone()
    warn = int(warn[0])

    warn2 = warn - 1
   
    if user_status == 'Owner':
       if warn2 < 0:
          await bot.send_message(message.chat.id, f"🆘 | Нельзя забирать больше варнов чем у самого игрока")
          return
    if user_status == 'Helper_Admin':
       if warn2 < 0:
          await bot.send_message(message.chat.id, f"🙅‍♂️ | Нельзя забирать больше варнов чем у самого игрока")
          return
    if user_status == 'Owner':
       await bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn - 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await bot.send_message(5197897742, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       await bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn - 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    else:
       await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная команда доступна от прав администратора \"HELPER-ADMINS\"", parse_mode='html')



@dp.message_handler(commands=['unwarn_id'])
async def posting(message):
    reply_user_id = int(message.text.split()[1])

    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])
    user_id = message.from_user.id
    

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    warn = cursor.execute(f"SELECT warn from warn where user_id = {reply_user_id}").fetchone()
    warn = int(warn[0])

    warn2 = warn - 1
   
    if user_status == 'Owner':
       if warn2 < 0:
          await bot.send_message(message.chat.id, f"🆘 | Нельзя забирать больше варнов чем у самого игрока")
          return
    if user_status == 'Helper_Admin':
       if warn2 < 0:
          await bot.send_message(message.chat.id, f"🆘 | Нельзя забирать больше варнов чем у самого игрока")
          return
    if user_status == 'Owner':
       await bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn - 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await bot.send_message(5197897742, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       await bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Отбор варнов по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn - 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    else:
       await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная команда доступна от прав администратора \"HELPER-ADMINS\"", parse_mode='html')


@dp.message_handler(commands=['warn_id'])
async def posting(message):
    reply_user_id = int(message.text.split()[1])

    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])
    user_id = message.from_user.id
    

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    warn = cursor.execute(f"SELECT warn from warn where user_id = {reply_user_id}").fetchone()
    warn = int(warn[0])

    warn2 = warn + 1
   
    if user_status == 'Owner':
       if warn2 > 5:
          await bot.send_message(reply_user_id, f"⚠️ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> , ваш аккаунт был заблокирован из-за 6\6 варнов", parse_mode='html')

          await bot.send_message(message.chat.id, f"⚠️ | Аккаунт: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> был заблокирован ", parse_mode='html')
          cursor.execute(f'UPDATE users SET status_block = "on" WHERE user_id = {reply_user_id}')
          cursor.execute(f'UPDATE warn SET warn = {0} WHERE user_id = {reply_user_id}')
          connect.commit()
          return
    if user_status == 'Helper_Admin':
       if warn2 > 5:
          await bot.send_message(reply_user_id, f"⚠️ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> , ваш аккаунт был заблокирован из-за 6\6 варнов", parse_mode='html')

          await bot.send_message(5197897742, f"⚠️ | Аккаунт: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> был заблокирован ", parse_mode='html')

          await bot.send_message(message.chat.id, f"⚠️ | Аккаунт: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> был заблокирован ", parse_mode='html')
          cursor.execute(f'UPDATE users SET status_block = "on" WHERE user_id = {reply_user_id}')
          cursor.execute(f'UPDATE warn SET warn = {0} WHERE user_id = {reply_user_id}')
          connect.commit()
          return
    if user_status == 'Owner':
       await bot.send_message(message.chat.id, f"""
👮 | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна по ID
👤 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn + 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await bot.send_message(5197897742, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')

       await bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна по ID
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn + 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    else:
       await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная команда доступна от прав администратора \"HELPER-ADMINS\"", parse_mode='html')


@dp.message_handler(commands=['warn'])
async def posting(message):
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    reply_user_name = str(reply_user_name[0])
    user_id = message.from_user.id
    reply_user_id = message.reply_to_message.from_user.id

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    warn = cursor.execute("SELECT warn from warn where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    warn = int(warn[0])

    warn2 = warn + 1
   
    if user_status == 'Owner':
       if warn2 > 5:
          await bot.send_message(message.chat.id, f"⚠️ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> , ваш аккаунт был заблокирован ", parse_mode='html')
          cursor.execute(f'UPDATE users SET status_block = "on" WHERE user_id = {reply_user_id}')
          cursor.execute(f'UPDATE warn SET warn = {0} WHERE user_id = {reply_user_id}')
          connect.commit()
          return
    if user_status == 'Helper_Admin':
       if warn2 > 5:
          await bot.send_message(message.chat.id, f"⚠️ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> , ваш аккаунт был заблокирован ", parse_mode='html')
          cursor.execute(f'UPDATE users SET status_block = "on" WHERE user_id = {reply_user_id}')
          cursor.execute(f'UPDATE warn SET warn = {0} WHERE user_id = {reply_user_id}')
          connect.commit()
          return
    if user_status == 'Owner':
       await bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn + 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await bot.send_message(5197897742, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')

       await bot.send_message(message.chat.id, f"""
⛔️ | Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>   
⚙️ | Действие: Выдача варна
👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
🛑 | Варнов у игрока: {warn2}/6     
       """, parse_mode='html')
       cursor.execute(f'UPDATE warn SET warn = {warn + 1} WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    else:
       await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная команда доступна от прав администратора \"HELPER-ADMINS\"", parse_mode='html')
    
    
       



@dp.message_handler(commands=['post'])
async def posting(message):
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_id = message.from_user.id
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    text = message.text[5:]
    
    if user_status == 'Owner':
       rows = cursor.execute('SELECT user_id FROM users').fetchall()
       for row in rows:
          await bot.send_message(row[0], text, parse_mode='html')
    else:
       await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, данная команда доступна от прав администратора \"OWNER\"", parse_mode='html')          


@dp.message_handler(commands=['help_admins'])
async def help_admins(message):
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_id = message.from_user.id

    await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация для администрации чата ⛔️

1️⃣ /channel_mute [количество] [м\д\ч] [причина] - Выдача затычки игроку 
2️⃣ /channel_ban [количество] [м\д\ч] [причина] - Выдача бана игроку
3️⃣ /channel_unmute - снятие затычки игроку 
4️⃣ /channel_unban - снятие бана игроку 

ℹ️Команды работают ответом на сообщение нарушителя     
    """, parse_mode='html')

@dp.message_handler(commands=['reset'])
async def start_cmd(message):
    msg = message
    user_id = msg.from_user.id
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    

    if user_status == 'Owner':
       await bot.send_message(message.chat.id, f"👮|Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Масовое обнуление\n💈 | Время: навсегда\n👨 |Игроку: Всем игрокам", parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {10000}')
       cursor.execute(f'UPDATE users SET user_name = "Игрок"')
       cursor.execute(f'UPDATE users SET bank = {1000}')
       cursor.execute(f'UPDATE users SET depozit = {0}')
       cursor.execute(f'UPDATE users SET rating = {0}')
       cursor.execute(f'UPDATE users SET ethereum = {100}')
       cursor.execute(f'UPDATE mine SET iron = {0}')
       cursor.execute(f'UPDATE mine SET metall = {0}')
       cursor.execute(f'UPDATE mine SET silver = {0}')
       cursor.execute(f'UPDATE mine SET bronza = {0}')
       cursor.execute(f'UPDATE mine SET gold = {0}')
       cursor.execute(f'UPDATE farm SET linen = {0}')
       cursor.execute(f'UPDATE farm SET cotton = {0}')
       cursor.execute(f'UPDATE house SET house = {0}')
       cursor.execute(f'UPDATE house SET basement = {0}')
       cursor.execute(f'UPDATE cars SET cars = {0}')
       cursor.execute(f'UPDATE cars SET hp = {0}')
       cursor.execute(f'UPDATE cars SET benz = {0}')
       cursor.execute(f'UPDATE bot_time SET stavka_games = {0} ')
       cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} ')
       cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} ')
       cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} ')
       cursor.execute(f'UPDATE bot_time SET time_pick = {0} ')
       cursor.execute(f'UPDATE bot_time SET time_rake = {0} ')
       cursor.execute(f'UPDATE bot_time SET time_craft = {0} ')
       cursor.execute(f'UPDATE bot_time SET time_kit = {0} ')

       connect.commit()
       full_name = msg.from_user.full_name
       print(f'{full_name} сделал масовое обнуление')
       return
    else:
       await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"OWNER\"", parse_mode='html')


@dp.message_handler(commands=['unban_id'])
async def start_cmd(message):

    
    msg = message
    user_id = msg.from_user.id
    reply_user_id = int(message.text.split()[1])

    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    

    if user_status == 'Owner':
       await bot.send_message(reply_user_id, f"⛔ | CheckIP / <a href='tg://user?id={user_id}'>{reply_user_name}</a>, ваш аккаунт был разблокирован по ID", parse_mode='html')

       await bot.send_message(message.chat.id, f"⛔️ |CheckIP / Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта по ID\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "off"  WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await bot.send_message(reply_user_id, f"💁‍♂️ | <a href='tg://user?id={user_id}'>{reply_user_name}</a>, ваш аккаунт был разблокирован по ID", parse_mode='html')
       await bot.send_message(5197897742, f"⛔️ |CheckIP / Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта по ID\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')

       await bot.send_message(message.chat.id, f"⛔️ |CheckIP / Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта по ID\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "off"  WHERE user_id = {reply_user_id}')
       connect.commit()
       full_name = msg.from_user.full_name
       reply_full_name = msg.reply_to_message.from_user.full_name
       print(f'CheckIP / {full_name} выдал разбан игроку: {reply_full_name}')
       return
    else:
       await bot.send_message(message.chat.id, f"🆘 | CheckIP-admin  /<a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"HELPER ADMIN\"", parse_mode='html')


@dp.message_handler(commands=['unban'])
async def start_cmd(message):
    if not message.reply_to_message:
       await message.reply("CheckIP-erorr / Эта команда должна быть ответом на сообщение!")
       return

    msg = message
    user_id = msg.from_user.id
    reply_user_id = msg.reply_to_message.from_user.id
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    reply_user_name = str(reply_user_name[0])

    

    if user_status == 'Owner':
       await bot.send_message(message.chat.id, f"⛔️ |CheckIP  / Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "off"  WHERE user_id = {reply_user_id}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await bot.send_message(5197897742, f"⛔️ |CheckIP / Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')

       await bot.send_message(message.chat.id, f"⛔️ |CheckIP / Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Разбан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "off"  WHERE user_id = {reply_user_id}')
       connect.commit()
       full_name = msg.from_user.full_name
       reply_full_name = msg.reply_to_message.from_user.full_name
       print(f'CheckIP / {full_name} выдал разбан игроку: {reply_full_name}')
       return
    else:
       await bot.send_message(message.chat.id, f"🆘 | CheckIP  / <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"HELPER ADMIN\"", parse_mode='html')


@dp.message_handler(commands=['ban_id'])
async def start_cmd(message):
    msg = message
    user_id = msg.from_user.id
    reply_user_id = int(message.text.split()[1])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    


    if user_status == 'Owner':
       await bot.send_message(reply_user_id, f"📛 | CheckIP / <a href='tg://user?id={user_id}'>{reply_user_name}</a>, ваш аккаунт был заблокирован по ID", parse_mode='html')

       await bot.send_message(message.chat.id, f"⛔️ |CheckIP  / Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "on"  WHERE user_id = {reply_user_id}')
       full_name = msg.from_user.full_name
       
       print(f'CheckIP / {full_name} выдал бан игроку: {reply_user_name}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await bot.send_message(reply_user_id, f"📛 | <a href='tg://user?id={user_id}'>{reply_user_name}</a>, ваш аккаунт был заблокирован по ID", parse_mode='html')
       await bot.send_message(5197897742, f"⛔️ |CheckIP / Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')

       await bot.send_message(message.chat.id, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "on"  WHERE user_id = {reply_user_id}')
       full_name = msg.from_user.full_name
       
       print(f'CheckIP / {full_name} выдал бан игроку: {reply_user_name}')
       connect.commit()
       return
    else:
       await bot.send_message(message.chat.id, f"🆘 |CheckIP  /  <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"HELPER ADMIN\"", parse_mode='html')





@dp.message_handler(commands=['ban'])
async def start_cmd(message):
    if not message.reply_to_message:
       await message.reply("CheckIP-erorr / Эта команда должна быть ответом на сообщение!")
       return


    msg = message
    user_id = msg.from_user.id
    reply_user_id = msg.reply_to_message.from_user.id
    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    reply_user_name = str(reply_user_name[0])

    


    if user_status == 'Owner':
       await bot.send_message(message.chat.id, f"⛔️ |CheckIP / Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "on"  WHERE user_id = {reply_user_id}')
       full_name = msg.from_user.full_name
       reply_full_name = msg.reply_to_message.from_user.full_name
       print(f'{full_name} выдал бан игроку: {reply_full_name}')
       connect.commit()
       return
    if user_status == 'Helper_Admin':
       await bot.send_message(5197897742, f"⛔️ |CheckIP  / Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')

       await bot.send_message(message.chat.id, f"⛔️ |CheckIP  / Администратор: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Бан аккаунта\n💈 | Время: навсегда\n👨 |Игроку: <a href='tg://user?id={user_id}'>{reply_user_name}</a>", parse_mode='html')
       cursor.execute(f'UPDATE users SET status_block = "on"  WHERE user_id = {reply_user_id}')
       full_name = msg.from_user.full_name
       reply_full_name = msg.reply_to_message.from_user.full_name
       print(f'CheckIP  / {full_name} выдал бан игроку: {reply_full_name}')
       connect.commit()
       return
    else:
       await bot.send_message(message.chat.id, f"🆘 | CheckIP / <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна только с категории администратора \"HELPER ADMIN\"", parse_mode='html')




@dp.message_handler(commands=['reset_id'])
async def start_cmd(message):

    msg = message
    user_id = msg.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    reply_user_id = int(message.text.split()[1])

    text = ' '.join(message.text.split()[2:])


    reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
    reply_user_name = str(reply_user_name[0])

    if user_status == 'Helper_Admin':
       await bot.send_message(5197897742, f"""
!CheckIP  модуль администрации!
⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ |Действие: Обнуление по ID
💈 |Причина: {text} 
👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       """, parse_mode='html')

       await bot.send_message(message.chat.id, f"""
!CheckIP  модуль администрации!
⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ |Действие: Обнуление по ID
💈 |Причина: {text} 
👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {10000} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE farm SET linen = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE farm SET cotton = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_games = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_pick = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_rake = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_craft = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_kit = {0} WHERE user_id = "{reply_user_id}"')
       connect.commit()
       await bot.send_message(reply_user_id, f"""
!CheckIP  модуль администрации!
<b>🆘 | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, ВАС ОБНУЛИЛИ! | 🆘</b>
💭 | Причина: <i>{text}</i>
⛔️ | Администратором: <a href='tg://user?id={user_id}'>{user_name}</a> 
       """, parse_mode='html')
       return

    if user_status == 'Owner':
       await bot.send_message(message.chat.id, f"""
!CheckIP  модуль администрации!
⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> 
⚙️ |Действие: Обнуление по ID
💈 |Причина: {text} 
👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE farm SET linen = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE farm SET cotton = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_games = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_pick = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_rake = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_craft = {0} WHERE user_id = "{reply_user_id}"')
       cursor.execute(f'UPDATE bot_time SET time_kit = {0} WHERE user_id = "{reply_user_id}"')
       connect.commit()
       await bot.send_message(reply_user_id, f"""
!CheckIP  модуль администрации!
<b>🆘 | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, ВЫ БЫЛИ ОБНУЛЕНЫ | 🆘</b>
💭 | Причина: <i>{text}</i>
⛔️ | Администратором: <a href='tg://user?id={user_id}'>{user_name}</a> 
       """, parse_mode='html')
       return
    else:
       await bot.send_message(message.chat.id, f"🆘 |CheckIP / <a href='tg://user?id={user_id}'>{user_name}</a> , данная функция доступна от прав админитсратора \"ХЕЛПЕР АДМИН\"", parse_mode='html')


@dp.message_handler(commands=['start', 'старт'])
async def start_cmd(message):
    
    
    reg = InlineKeyboardMarkup(row_width=1)
    register_help = InlineKeyboardButton(text='🆘 Помощь', callback_data='register_help')
    reg.add(register_help)


    name = message.from_user.get_mention(as_html=True)
    L_photo = open('a/start.jpg', 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo=L_photo, caption=f'''
👋 Привет, {name} 
   | Я бот для игры в различные игры.
 Тебе выдан подарок в размере 10.000$.
 Так же ты можешь добавить меня в беседу для игры с друзьями.
 🆘 Чтобы узнать все команды введи "Помощь" |
    ''', reply_markup=reg, parse_mode='html')
    
										
###########################################БАЛАНС###########################################
###########################################
@dp.message_handler()
async def prof_user(message: types.Message):
    msg = message
    host = message.text.lower()
    user_id = msg.from_user.id
    full_name = msg.from_user.full_name
    user_name = "человек"
    user_status = "Vip"
    status_block = "off"
    stats_status = "off"
    pref = "игрок"
    chat_id = message.chat.id
    result = time.localtime()

    if int(result.tm_mon) <= 9:
      p = "0"
    else:
      p = ''
    times = f'{result.tm_mday}.{p}{result.tm_mon}.{result.tm_year} | {result.tm_hour}:{result.tm_min}:{result.tm_sec}'
    times2 = str(times)

    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None:
       cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, user_name, full_name, user_status, 10000, 0, 0, 0, status_block, times2, pref, 0, 0, 0, 0, stats_status))
       cursor.execute("INSERT INTO mine VALUES(?, ?, ?, ?, ?, ?, ?, ?);",(user_id, full_name,status_block, 0, 0, 0, 0, 0))
       cursor.execute("INSERT INTO farm VALUES(?, ?, ?, ?, ?);",(user_id, full_name,status_block, 0, 0))
       cursor.execute("INSERT INTO house VALUES(?, ?, ?, ?);",(user_id, user_name, 0, 0))
       cursor.execute("INSERT INTO cars VALUES(?, ?, ?, ?, ?);",(user_id, user_name, 0, 0, 0))
       cursor.execute("INSERT INTO user_case VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO bot_time VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, 0, 0, 0, 0, 0, 0, 0, 0))
       cursor.execute("INSERT INTO promo1 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO warn VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO time_bank VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO ob_time VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO warn VALUES(?, ?);",(user_id, 0))
       connect.commit()
       print(f'Зарегестрировался в боте пользователь: {full_name}')
    
       name = message.from_user.get_mention(as_html=True)
       
       L_photo = open('a/start.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=L_photo, caption=f'''
👋 Привет, {name} 
   | Я бот для игры в различные игры.
Тебе выдан подарок в размере 10.000$.
Так же ты можешь добавить меня в беседу для игры с друзьями.
🆘 Чтобы узнать все команды введи "Помощь"
    ''', reply_markup=reg, parse_mode='html')
       
    else:
       status_console = 'off'
       avatarka_start = 'none'
       cursor.execute("INSERT INTO console VALUES(?, ?);",(user_id, status_console))
       cursor.execute("INSERT INTO time_prefix VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO time_sms VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO promo1 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO channel_pov VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO avatarka VALUES(?, ?);",(user_id, avatarka_start))
       cursor.execute("INSERT INTO reput VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO h_module VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO promo2 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo3 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo4 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo5 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo6 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo7 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo8 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo9 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo10 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo11 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo12 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo13 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo14 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo15 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo16 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo17 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo18 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo19 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo20 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo21 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo22 VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO promo23 VALUES(?, ?, ?);",(user_id, 0, 0))
       connect.commit()
       
    
    

    
    
   
    

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return

    if message.forward_date != None:
       msg = message
       user_id = msg.from_user.id
       
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a> , в боте запрещено пересылать сообщение!", parse_mode='html')
       return


    period = 2
    get = cursor.execute("SELECT stavka FROM ob_time WHERE user_id = ?",(message.from_user.id,)).fetchone()
    last_stavka = f"{int(get[0])}"
    stavkatime = time.time() - float(last_stavka)
    if stavkatime < period:
       return
    else:
       user_id = message.from_user.id
       cursor.execute(f'UPDATE ob_time SET stavka = {time.time()} WHERE user_id = {user_id}')
       connect.commit()
####
    if message.text.lower() in ['репорт', 'система репорта', 'репорты']:
       msg = message
       user_id = msg.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       await bot.send_message(message.chat.id , f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот информация за систему репортов ⛔️

⚠️ | Правила по использованию репортов
      1️⃣ | Материться, оскорблять кого-либо, проявлять неуважение к администрации и тому подобное.
      2️⃣ | Капсить, писать неразборчиво, использовать спам, писать один и тот-же текст несколько раз получивши на него ответ.
      3️⃣ | Всячески дразнить администрацию и отвлекать от работы.
      4️⃣ | Запрещено интересоваться/писать вещи которые ни коем образом ни относятся к игре
      5️⃣ | Запрещена реклама в любом её проявлении
      6️⃣ | Запрещено обращаться к своим друзьям администраторам по личным вопросам
      7️⃣ | Запрещено клеветать на игроков, обвинять их в нарушениях, которые они не совершали.
      8️⃣ | Репорт работает по принципу - Вопрос/Просьба/Жалоба (исключение - Приветствие) и не иначе. Иные формы обращения будут оставаться без ответа и будет выдано наказание.

⚠️ | Форма отправки репорта - /report [сообщение]

⛔️Прошу вас соблюдать правила отправки репорта
       """, parse_mode='html')
    if message.text.lower() in ["баланс", "Баланс", "Б", "б", "Balans", "balans"]:
       msg = message
       user_id = msg.from_user.id
       
       chat_id = message.chat.id
       pref = cursor.execute("SELECT pref from users where user_id = ?",(message.from_user.id,)).fetchone()
       pref = str(pref[0])
       
       avatarka = cursor.execute("SELECT avatarka from avatarka where user_id = ?",(message.from_user.id,)).fetchone()
       avatarka = avatarka[0]

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = int(balance[0])
       balance2 = '{:,}'.format(balance).replace(',', '.')
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = int(bank[0])
       bank2 = '{:,}'.format(bank).replace(',', '.')
       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?",(message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])
       ethereum2 = '{:,}'.format(ethereum).replace(',', '.')

       c = 999999999999999999999999999999999999999999999999999999999999999999
       if balance >= 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance).replace(',', '.')
       else:
        pass
       if bank >= 999999999999999999999999999999999999999999999999999999999999999999:
          bank = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          bank2 = '{:,}'.format(bank).replace(',', '.')
       else:
        pass
       if ethereum >= 999999999999999999999999999999999999999999999999999999999999999999:
          ethereum = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET ethereum = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          ethereum2 = '{:,}'.format(ethereum).replace(',', '.')
       else:
        pass
        summ120000 = Decimal(balance + bank)
        summ130000 = round(summ120000)
        summ130000 = '{:,}'.format(summ130000).replace(',', '.')
       if avatarka == 'apper':
          ava = open('a/apper.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, f"🌀 |<b> Никнейм</b>:<i><a href='tg://user?id={user_id}'>{user_name}</a></i> \n🖋 | Префикс: <i>{pref}</i> \n💸 | Деньги: <code>{balance2}</code>$ \n🟣 | Эфириум: {ethereum2}🟪\n💵Всего средств: <code>{summ130000}</code>\n\n<b>🌀 | Ваш скин: ANIME</b>", parse_mode='html')
          return
       
       if avatarka == 'admin':
          ava = open('a/админ.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, f"🦸‍♂️| Ник:<i><a href='tg://user?id={user_id}'>{user_name}</a></i> \n✏️ | Префикс: <i>{pref}</i> \n💰 | Деньги: <code>{balance2}</code>$ \n🏦 | Банк: <code>{bank2}</code>$\n🟣 | Эфириум: {ethereum2}🟪\n<b>🦸‍♂️ Ваш скин: IRON MAN (железный человек)</b>\n\n💵Всего средств: <code>{summ130000}</code>", parse_mode='html')
          return
       
       if avatarka == 'girl':
          ava = open('a/girl.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, f"👫 | Ник:<i><a href='tg://user?id={user_id}'>{user_name}</a></i> \n✏️ | Префикс: <i>{pref}</i> \n💰 | Деньги: <code>{balance2}</code>$ \n🏦 | Банк: <code>{bank2}</code>$\n🟣 | Эфириум: {ethereum2}🟪\n🟣 | Эфириум: <code>{ethereum2}</code>🟪\n\n💵Всего средств: <code>{summ130000}</code>", parse_mode='html')
          return
       
       if avatarka == 'cheat':
          ava = open('a/cheat.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, f"⛄ | Ник:<i><a href='tg://user?id={user_id}'>{user_name}</a></i> \n💼 | Префикс: <i>{pref}</i> \n💰 | Деньги: <code>{balance2}</code>$ \n🏦 | Банк: <code>{bank2}</code>$\n🟣 | Эфириум: {ethereum2}🟪\n<b>⛄ Ваш скин: СКУИК</b>\n\n💵Всего средств: <code>{summ130000}</code>", parse_mode='html')
          return
       
       if avatarka == 'dyp':
          ava = open('a/дюп.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, f"🥷 | Ник:<i><a href='tg://user?id={user_id}'>{user_name}</a></i>  \n💰 | Деньги: <code>{balance2}</code>$ \n🏦 | Банк: <code>{bank2}</code>$\n🟣 | Эфириум: {ethereum2}🟪\n<b>🥷Ваш скин: ИТЧАЧИ</b>\n\n💵Всего средств: <code>{summ130000}</code>", parse_mode='html')
          return
       
       if avatarka == 'strach':
          ava = open('a/страж.jpg', 'rb')
          await bot.send_photo(message.chat.id, ava, f"🎭 | <b>Никнейм:<i><a href='tg://user?id={user_id}'>{user_name}</a></i></b> \n🖋 | Префикс: <i>{pref}</i> \n💰 | Деньги: <code>{balance2}</code>$\n🟣 | Эфириум: {ethereum2}🟪 \n\n💵Всего средств: <code>{summ130000}</code>", parse_mode='html')
          return
       
       await bot.send_message(message.chat.id, f"⛄ | <b>Никнейм</b>:<i><a href='tg://user?id={user_id}'>{user_name}</a></i> \n✏️ | Префикс: <i>{pref}</i> \n💵Всего средств: <code>{summ130000}</code>", parse_mode='html')
    ################################################ПРОФИЛЬ#############################################################
    if message.text.lower() in ["профиль", "Профиль", "П"]:
       msg = message
       chat_id = message.chat.id
       
       user_id = msg.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reput = cursor.execute("SELECT reput from reput where user_id = ?",(message.from_user.id,)).fetchone()
       reput = int(reput[0])

       avatarka = cursor.execute("SELECT avatarka from avatarka where user_id = ?",(message.from_user.id,)).fetchone()
       avatarka = avatarka[0]

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?",(message.from_user.id,)).fetchone()
       rating = cursor.execute("SELECT rating from users where user_id = ?",(message.from_user.id,)).fetchone()
       pref = cursor.execute("SELECT pref from users where user_id = ?",(message.from_user.id,)).fetchone()
       pref = str(pref[0])
       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])
       donate_coins2 = '{:,}'.format(donate_coins)
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       game = cursor.execute("SELECT game from users where user_id = ?",(message.from_user.id,)).fetchone()
       game = int(game[0])
       game2 = '{:,}'.format(game)

       balance = int(balance[0])
       bank = int(bank[0])
       rating = int(rating[0])
       ethereum = int(ethereum[0])

       cars = cursor.execute("SELECT cars from cars where user_id = ?",(message.from_user.id,)).fetchone()
       cars = int(cars[0])

       house = cursor.execute("SELECT house from house where user_id = ?",(message.from_user.id,)).fetchone()
       house = int(house[0])

       d5 = 0

       if house == 1:
          house2 = '\n    🏠Дом: Коробка\n'
          d5 += 1
       if house == 2:
          house2 = '\n    🏠Дом: Сарай\n'
          d5 += 1
       if house == 3:
          house2 = '\n    🏠Дом: Маленький домик\n'
          d5 += 1
       if house == 4:
          house2 = '\n    🏠Дом: Квартира\n'
          d5 += 1
       if house == 5:
          house2 = '\n    🏠Дом: Огромный дом\n'
          d5 += 1
       if house == 6:
          house2 = '\n    🏠Дом: Коттедж\n'
          d5 += 1
       if house == 7:
          house2 = '\n    🏠Дом: Вилла\n'
          d5 += 1
       if house == 8:
          house2 = '\n    🏠Дом: Загородный дом\n'
          d5 += 1
       else:
          house2 = ''
       if cars == 1:
          cars2 = '    🚘Машина: Самокат\n'
          d5 += 1
       if cars == 2:
          cars2 = '    🚘Машина: Велосипед\n'
          d5 += 1
       if cars == 3:
          cars2 = '    🚘Машина: Гироскутер\n'
          d5 += 1
       if cars == 4:
          cars2 = '    🚘Машина: Сегвей\n'
          d5 += 1
       if cars == 5:
          cars2 = '    🚘Машина: Мопед\n'
          d5 += 1
       if cars == 6:
          cars2 = '    🚘Машина: Мотоцикл\n'
          d5 += 1
       if cars == 7:
          cars2 = '    🚘Машина: ВАЗ 2109\n'
          d5 += 1
       if cars == 8:
          cars2 = '    🚘Машина: Квадроцикл\n'
          d5 += 1
       if cars == 9:
          cars2 = '    🚘Машина: Багги\n'
          d5 += 1
       if cars == 10:
          cars2 = '    🚘Машина: Вездеход\n'
          d5 += 1
       if cars == 11:
          cars2 = '    🚘Машина: Лада Xray\n'
          d5 += 1
       if cars == 12:
          cars2 = '    🚘Машина: Audi Q7\n'
          d5 += 1
       if cars == 13:
          cars2 = '    🚘Машина: BMW X6\n'
          d5 += 1
       if cars == 14:
          cars2 = '    🚘Машина: Toyota FT-HS\n'
          d5 += 1
       if cars == 15:
          cars2 = '    🚘Машина: BMW Z4 M\n'
          d5 += 1
       if cars == 16:
          cars2 = '    🚘Машина: Subaru WRX STI\n'
          d5 += 1
       if cars == 17:
          cars2 = '    🚘Машина: Lamborghini Veneno\n'
          d5 += 1
       if cars == 18:
          cars2 = '    🚘Машина: Tesla Roadster\n'
          d5 += 1
       else:
          cars2 = ''

       if d5 == 0:
          d6 = '\n      У вас нету имущества 🙁'
       else:
          d6 = '🏞 | Имущество:'
       
       c = 999999999999999999999999
       if user_status == 'Player':
          priv = 'Пользователь'
       if user_status == 'Vip':
          priv = 'ВИП❤️'
       if user_status == 'Premium':
          priv = ' ПРЕМИУМ🧡'
       if user_status == 'Platina':
          priv = ' ПЛАТИНА💛'
       if user_status == 'Helper':
          priv = ' ХЕЛПЕР💚'
       if user_status == 'Sponsor':
          priv = ' СПОНСОР💙'
       if user_status == 'Osnovatel':
          priv = ' ОСНОВАТЕЛЬ💜'
       if user_status == 'Vladelec':
          priv = ' ВЛАДЕЛЕЦ🖤'
       if user_status == 'Bog':
          priv = ' БОГ🤍'
       if user_status == 'Vlaselin':
          priv = ' ВЛАСТЕЛИН🤎'
       if user_status == 'Owner':
          priv = 'РАЗРАБОТЧИК✅'
       if user_status == 'Admin':
          priv = 'АДМИНИСТРАТОР⛔️'
       if user_status == 'Helper_Admin':
          priv = 'HELPER АДМИНИСТРАТОР⛔️'

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit() 
       else:
        pass
       if int(balance) in range(0, 1000):
          balance3 = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
          balance3 = int(balance3[0])
       if int(balance) in range(1000, 999999):
          balance1 = balance / 1000
          balance2 = round(balance1)
          balance3 = f'{balance2} тыс'
       if int(balance) in range(1000000, 999999999):
          balance1 = balance / 1000000
          balance2 = round(balance1)
          balance3 = f'{balance2} млн'
       if int(balance) in range(1000000000, 999999999999):
          balance1 = balance / 1000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} млрд'
       if int(balance) in range(1000000000000, 999999999999999):
          balance1 = balance / 1000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} трлн'
       if int(balance) in range(1000000000000000, 999999999999999999):
          balance1 = balance / 1000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} квдр'
       if int(balance) in range(1000000000000000000, 999999999999999999999):
          balance1 = balance / 1000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} квнт'
       if int(balance) in range(1000000000000000000000, 999999999999999999999999):
          balance1 = balance / 1000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} скст'
       if int(balance) in range(1000000000000000000000000, 999999999999999999999999999):
          balance1 = balance / 1000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} трикс'
       if int(balance) in range(1000000000000000000000000000,999999999999999999999999999999):
          balance1 = balance / 1000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} твинкс'
       if int(balance) in range(1000000000000000000000000000000, 999999999999999999999999999999999):
          balance1 = balance / 1000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} септ'
       if int(balance) in range(1000000000000000000000000000000000, 999999999999999999999999999999999999):
          balance1 = balance / 1000000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} октл'
       if int(balance) in range(1000000000000000000000000000000000000, 999999999999999999999999999999999999999):
          balance1 = balance / 1000000000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} нонл'
       if int(balance) in range(1000000000000000000000000000000000000000, 999999999999999999999999999999999999999999):
          balance1 = balance / 1000000000000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} декал'
       if int(balance) in range(1000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999):
          balance1 = balance / 1000000000000000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} эндк'
       if int(balance) in range(1000000000000000000000000000000000000000000000,999999999999999999999999999999999999999999999999):
          balance1 = balance / 1000000000000000000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} доктл'
       if int(balance) in range(1000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999) :
          balance1 = balance / 1000000000000000000000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} гугл'
       if int(balance) in range(1000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999) :
          balance1 = balance / 1000000000000000000000000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} кинд'
       if int(balance) in range(1000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999999) :
          balance1 = balance / 1000000000000000000000000000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} трипт'
       if int(balance) in range(1000000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999999999) :
          balance1 = balance / 1000000000000000000000000000000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} срист'
       if int(balance) in range(1000000000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999999999999):
          balance1 = balance / 1000000000000000000000000000000000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} манит'
       if int(balance) >= 1000000000000000000000000000000000000000000000000000000000000000:
          balance1 = balance / 100000000000000000000000000000000000000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} гвинт'
       if int(balance) >= 1000000000000000000000000000000000000000000000000000000000000000000000:
          balance1 = balance / 100000000000000000000000000000000000000000000000000000000000000000000000
          balance2 = round(balance1)
          balance3 = f'{balance2} клаунд'

       if ethereum >= 999999999999999999999999999999999999999999999999999999999999999999:
          ethereum = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET ethereum = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit() 
       else:
        pass
       if int(ethereum) in range(0, 1000):
          ethereum3 = cursor.execute("SELECT ethereum from users where user_id = ?",(message.from_user.id,)).fetchone()
          ethereum3 = int(ethereum3[0])
       if int(ethereum) in range(1000, 999999):
          ethereum1 = ethereum / 1000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} тыс'
       if int(ethereum) in range(1000000, 999999999):
          ethereum1 = ethereum / 1000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} млн'
       if int(ethereum) in range(1000000000, 999999999999):
          ethereum1 = ethereum / 1000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} млрд'
       if int(ethereum) in range(1000000000000, 999999999999999):
          ethereum1 = ethereum / 1000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} трлн'
       if int(ethereum) in range(1000000000000000, 999999999999999999):
          ethereum1 = ethereum / 1000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} квдр'
       if int(ethereum) in range(1000000000000000000, 999999999999999999999):
          ethereum1 = ethereum / 1000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} квнт'
       if int(ethereum) in range(1000000000000000000000, 999999999999999999999999):
          ethereum1 = ethereum / 1000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} скст'  
       if int(ethereum) in range(1000000000000000000000000, 999999999999999999999999):
          ethereum1 = ethereum / 1000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} трикс'
       if int(ethereum) >= 1000000000000000000000000000:
          ethereum1 = ethereum / 1000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} твинкс'
       if int(ethereum) in range(1000000000000000000000000000000, 999999999999999999999999999999999):
          ethereum1 = ethereum / 1000000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} септ'
       if int(ethereum) in range(1000000000000000000000000000000000, 999999999999999999999999999999999999):
          ethereum1 = ethereum / 1000000000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} октл'
       if int(ethereum) in range(1000000000000000000000000000000000000, 999999999999999999999999999999999999999):
          ethereum1 = ethereum / 1000000000000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} нонл'
       if int(ethereum) in range(1000000000000000000000000000000000000000, 999999999999999999999999999999999999999999):
          ethereum1 = ethereum / 1000000000000000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} декал'
       if int(ethereum) in range(1000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999):
          ethereum1 = ethereum / 1000000000000000000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} эндк'
       if int(ethereum) >= 1000000000000000000000000000000000000000000000:
          ethereum1 = ethereum / 1000000000000000000000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} доктл'
       if int(ethereum) in range(1000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999) :
          ethereum1 = ethereum / 1000000000000000000000000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} гугл'
       if int(ethereum) in range(1000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999) :
          ethereum1 = ethereum / 1000000000000000000000000000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} кинд'
       if int(ethereum) in range(1000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999) :
          ethereum1 = ethereum / 1000000000000000000000000000000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} трипт'
       if int(ethereum) in range(1000000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999999) :
          ethereum1 = ethereum / 1000000000000000000000000000000000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} срист'
       if int(ethereum) in range(1000000000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999999999999):
          ethereum1 = balance / 1000000000000000000000000000000000000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} манит'
       if int(ethereum) >= 1000000000000000000000000000000000000000000000000000000000000000:
          ethereum1 = balance / 1000000000000000000000000000000000000000000000000000000000000000
          ethereum2 = round(ethereum1)
          ethereum3 = f'{ethereum2} гвинт'
       if bank >= 999999999999999999999999999999999999999999999999999999999999999999:
          bank = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()   
       else:
        pass
       if int(bank) in range(0, 1000):
          bank3 = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
          bank3 = int(bank3[0])
       if int(bank) in range(1000, 999999):
          bank1 = bank / 1000
          bank2 = round(bank1)
          bank3 = f'{bank2} тыс'
       if int(bank) in range(1000000, 999999999):
          bank1 = bank / 1000000
          bank2 = round(bank1)
          bank3 = f'{bank2} млн'
       if int(bank) in range(1000000000, 999999999999):
          bank1 = bank / 1000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} млрд'
       if int(bank) in range(1000000000000, 999999999999999):
          bank1 = bank / 1000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} трлн'
       if int(bank) in range(1000000000000000, 999999999999999999):
          bank1 = bank / 1000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} квдр'
       if int(bank) in range(1000000000000000000, 999999999999999999999):
          bank1 = bank / 1000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} квнт'
       if int(bank) in range(1000000000000000000000, 999999999999999999999999):
          bank1 = bank / 1000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} скст'
       if int(bank) in range(1000000000000000000000000, 999999999999999999999999):
          bank1 = bank / 1000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} трикс'
       if int(bank) >= 1000000000000000000000000000:
          bank1 = bank / 1000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} твинкс'
       if int(bank) in range(1000000000000000000000000000000, 999999999999999999999999999999999):
          bank1 = bank / 1000000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} септ'
       if int(bank) in range(1000000000000000000000000000000000, 999999999999999999999999999999999999):
          bank1 = bank / 1000000000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} октл'
       if int(bank) in range(1000000000000000000000000000000000000, 999999999999999999999999999999999999999):
          bank1 = bank / 1000000000000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} нонл'
       if int(bank) in range(1000000000000000000000000000000000000000, 999999999999999999999999999999999999999999):
          bank1 = bank / 1000000000000000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} декал'
       if int(bank) in range(1000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999):
          bank1 = bank / 1000000000000000000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} эндк'
       if int(bank) >= 1000000000000000000000000000000000000000000000:
          bank1 = bank / 1000000000000000000000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} доктл'
       if int(bank) in range(1000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999) :
          bank1 = bank / 1000000000000000000000000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} гугл'
       if int(bank) in range(1000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999) :
          bank1 = bank / 1000000000000000000000000000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} кинд'
       if int(bank) in range(1000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999) :
          bank1 = bank / 1000000000000000000000000000000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} трипт'
       if int(bank) in range(1000000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999999) :
          bank1 = bank / 1000000000000000000000000000000000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} срист'
       if int(bank) in range(1000000000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999999999999):
          bank1 = bank / 1000000000000000000000000000000000000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} манит'
       if int(bank) >= 1000000000000000000000000000000000000000000000000000000000000000:
          bank1 = bank / 1000000000000000000000000000000000000000000000000000000000000000
          bank2 = round(bank1)
          bank3 = f'{bank2} гвинт'
       if rating >= 999999999999999999999999999999999999999999999999999999999999999999:
          rating = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET rating = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
       else:
        pass
       if int(rating) in range(0, 1000):
          rating3 = cursor.execute("SELECT rating from users where user_id = ?",(message.from_user.id,)).fetchone()
          rating3 = int(rating3[0])
       if int(rating) in range(1000, 999999):
          rating1 = rating / 1000
          rating2 = round(rating1)
          rating3 = f'{rating2} тыс'
       if int(rating) in range(1000000, 999999999):
          rating1 = rating / 1000000
          rating2 = round(rating1)
          rating3 = f'{rating2} млн'
       if int(rating) in range(1000000000, 999999999999):
          rating1 = rating / 1000000000
          rating2 = round(rating1) 
          rating3 = f'{rating2} млрд'
       if int(rating) in range(1000000000000, 999999999999999):
          rating1 = rating / 1000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} трлн'
       if int(rating) in range(1000000000000000, 999999999999999999):
          rating1 = rating / 1000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} квдр'
       if int(rating) in range(1000000000000000000, 999999999999999999999):
          rating1 = rating / 1000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} квнт'
       if int(rating) in range(1000000000000000000000, 999999999999999999999999):
          rating1 = rating / 1000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} скст'
       if int(rating) in range(1000000000000000000000000, 999999999999999999999999):
          rating1 = rating / 1000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} трикс'
       if int(rating) >= 1000000000000000000000000000:
          rating1 = rating / 1000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} твинкс'
       if int(rating) in range(1000000000000000000000000000000, 999999999999999999999999999999999):
          rating1 = rating / 1000000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} септ'
       if int(rating) in range(1000000000000000000000000000000000, 999999999999999999999999999999999999):
          rating1 = rating / 1000000000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} октл'
       if int(rating) in range(1000000000000000000000000000000000000, 999999999999999999999999999999999999999):
          rating1 = rating / 1000000000000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} нонл'
       if int(rating) in range(1000000000000000000000000000000000000000, 999999999999999999999999999999999999999999):
          rating1 = rating / 1000000000000000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} декал'
       if int(rating) in range(1000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999):
          rating1 = rating / 1000000000000000000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} эндк'
       if int(rating) >= 1000000000000000000000000000000000000000000000:
          rating1 = rating / 1000000000000000000000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} доктл'
       if int(rating) in range(1000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999) :
          rating1 = rating / 1000000000000000000000000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} гугл'
       if int(rating) in range(1000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999) :
          rating1 = rating / 1000000000000000000000000000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} кинд'
       if int(rating) in range(1000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999) :
          rating1 = rating / 1000000000000000000000000000000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} трипт'
       if int(rating) in range(1000000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999999) :
          rating1 = rating / 1000000000000000000000000000000000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} срист'
       if int(rating) in range(1000000000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999999999999):
          rating1 = balance / 1000000000000000000000000000000000000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} манит'
       if int(rating) >= 1000000000000000000000000000000000000000000000000000000000000000:
          rating1 = balance / 1000000000000000000000000000000000000000000000000000000000000000
          rating2 = round(rating1)
          rating3 = f'{rating2} гвинт'

       times = cursor.execute("SELECT time_register FROM users WHERE user_id=?", (message.from_user.id,)).fetchall()
       times2 = times[0]


       await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , ваш #профиль : \n🔎 | ID: {user_id}\n⛄ | Префикс: {pref} \n💰| Деньги: {balance3}$\nВсего сыгранно игр: {game2}",  parse_mode='html')
###########################################БАНК###########################################
    # bank
    if message.text.lower() in ['Супер банк', 'Супер банк']:
       msg = message
       chat_id = message.chat.id
       
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank_hran = cursor.execute("SELECT bank2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = int(bank[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?",(message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       bank_hran = int(bank_hran[0])
       bank_hran2 = '{:,}'.format(bank_hran)
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = int(bank[0])
       depozit2 = '{:,}'.format(depozit)
       bank2 = '{:,}'.format(bank)
       if user_status == 'Player':
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
       if user_status == 'Vip':
          procent = '9%'
          i = 9
          stats_depozit = 'Вип'
       if user_status == 'Premium':
          procent = '13%'
          i = 13
          stats_depozit = 'Премиум'
       if user_status == 'Platina':
          procent = '17%'
          i = 17
          stats_depozit = 'Платина'
       if user_status == 'Helper':
          procent = '21%'
          i = 21
          stats_depozit = 'Хелпер'
       if user_status == 'Sponsor':
          procent = '24%'
          i = 24
          stats_depozit = 'Спонсор'
       if user_status == 'Osnovatel':
          procent = '27%'
          i = 27
          stats_depozit = 'Основатель'
       if user_status == 'Vladelec':
          procent = '29%'
          i = 29
          stats_depozit = 'Владелец'
       if user_status == 'Bog':
          procent = '32%'
          i = 32
          stats_depozit = 'Бог'
       if user_status == 'Vlaselin':
          procent = '36%'
          i = 36
          stats_depozit = 'Властелин'

       else:
          procent = '30%'
          i = 6
          stats_depozit = 'Обычный'
          
          money_vivod = depozit / i
          money_vivod2 = int(money_vivod)
          money_vivod3 = '{:,}'.format(money_vivod2)

       c = 999999999999999999999999999999999999999999999999999999999999999999
       if bank >= 999999999999999999999999999999999999999999999999999999999999999999:
          bank = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank = {999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          bank2 = '{:,}'.format(bank)
       else:
          pass
       if bank_hran >= 999999999999999999999999999999999999999999999999999999999999999999:
          bank_hran = 999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank2 = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          bank_hran2 = '{:,}'.format(bank_hran)
       else:
          pass
       if depozit >= 999999999999999999999999999999999999999999999999999999999999999999999999:
          depozit = 999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET depozit = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          depozit2 = '{:,}'.format(depozit)

       

       await bot.send_message(message.chat.id,f"<a href='tg://user?id={user_id}'>{user_name}</a> , 🦸‍♂️вот данные о вашем супер банке 🦸‍♂️\n\n🦸‍♂️ | Владелец: {user_name}\n🏛 | Основной счёт: {bank2}$\n💳 | Хранительный счёт: {bank_hran2}$\n💰 | Деньги на депозите: {depozit2}$\n     💎 Статус депозита: {stats_depozit}\n     📈 Процент под депозит: {procent}\n      💵 Деньги на вывод: {money_vivod3}$", parse_mode='html')
    if message.text.startswith('процент'):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i2 = str(msg.text.split()[1])
       summ = int(msg.text.split()[2])
       summ2 = '{:,}'.format(summ)

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       if user_status == 'Player':
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
       if user_status == 'Vip':
          procent = '9%'
          i = 9
          stats_depozit = 'Вип'
       if user_status == 'Premium':
          procent = '13%'
          i = 13
          stats_depozit = 'Премиум'
       if user_status == 'Platina':
          procent = '17%'
          i = 17
          stats_depozit = 'Платина'
       if user_status == 'Helper':
          procent = '21%'
          i = 21
          stats_depozit = 'Хелпер'
       if user_status == 'Sponsor':
          procent = '24%'
          i = 24
          stats_depozit = 'Спонсор'
       if user_status == 'Osnovatel':
          procent = '27%'
          i = 27
          stats_depozit = 'Основатель'
       if user_status == 'Vladelec':
          procent = '29%'
          i = 29
          stats_depozit = 'Владелец'
       if user_status == 'Bog':
          procent = '32%'
          i = 32
          stats_depozit = 'Бог'
       if user_status == 'Vlaselin':
          procent = '36%'
          i = 36
          stats_depozit = 'Властелин'

       else:
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
          
          money_vivod = depozit / i
          money_vivod2 = int(money_vivod)
          money_vivod3 = '{:,}'.format(money_vivod2)
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i2 == 'снять':
          if summ <= money_vivod2 :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли проценты с депозита {summ2}$ 💵", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но снимать с процентов депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
   

    if message.text.startswith('Процент'):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i2 = str(msg.text.split()[1])
       summ = int(msg.text.split()[2])
       summ2 = '{:,}'.format(summ)

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       if user_status == 'Player':
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
       if user_status == 'Vip':
          procent = '9%'
          i = 9
          stats_depozit = 'Вип'
       if user_status == 'Premium':
          procent = '13%'
          i = 13
          stats_depozit = 'Премиум'
       if user_status == 'Platina':
          procent = '17%'
          i = 17
          stats_depozit = 'Платина'
       if user_status == 'Helper':
          procent = '21%'
          i = 21
          stats_depozit = 'Хелпер'
       if user_status == 'Sponsor':
          procent = '24%'
          i = 24
          stats_depozit = 'Спонсор'
       if user_status == 'Osnovatel':
          procent = '27%'
          i = 27
          stats_depozit = 'Основатель'
       if user_status == 'Vladelec':
          procent = '29%'
          i = 29
          stats_depozit = 'Владелец'
       if user_status == 'Bog':
          procent = '32%'
          i = 32
          stats_depozit = 'Бог'
       if user_status == 'Vlaselin':
          procent = '36%'
          i = 36
          stats_depozit = 'Властелин'

       else:
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
          
          money_vivod = depozit / i
          money_vivod2 = int(money_vivod)
          money_vivod3 = '{:,}'.format(money_vivod2)
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i2 == 'снять':
          if summ <= money_vivod2 :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли проценты с депозита {summ2}$ 💵", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но снимать с процентов депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , 🙅‍♂️| нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
   
    if message.text.startswith('депозит'):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i = str(msg.text.split()[1])
       summ = int(msg.text.split()[2])
       summ2 = '{:,}'.format(summ)

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i == 'положить':
          if summ <= balance :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно положили на депозит {summ2}$ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя ложить отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
       if i == 'снять':
          if summ <= depozit :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли с депозита {summ2}$ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
          
    if message.text.startswith('Депозит'):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i = str(msg.text.split()[1])
       summ = int(msg.text.split()[2])
       summ2 = '{:,}'.format(summ)

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i == 'положить':
          if summ <= balance :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно положили на депозит {summ2}$ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя ложить отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
       if i == 'снять':
          if summ <= depozit :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли с депозита {summ2}$ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
          


    if message.text.startswith("Супер банк положить"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       bank_p = float(msg.text.split()[2])

       if bank_p >= 999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя ложить в супер банк больше лимита")
          return

       print(f"{name} положил в супер банк: {bank_p}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_p)
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       period = 180
       get = cursor.execute(f"SELECT stavka FROM time_bank WHERE user_id = {user_id}").fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if bank_p > 0:
             if balance >= bank_p:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , 🦸‍♂️вы успешно положили в супер банк {bank2}$ {rwin}",
                                        parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bank = {bank + bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE time_bank SET stavka = {time.time()} WHERE user_id = {user_id}')
                connect.commit()

             elif int(balance) < int(bank_p):
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств! {rloser}", parse_mode='html')

          if bank_p <= 0:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя положить в супер банк отрицательное число! {rloser}",
                                     parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ложить в супер банк можно раз в 3 минуты", parse_mode='html')
    if message.text.startswith("супер банк положить"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       bank_p = float(msg.text.split()[2])

       if bank_p >= 999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя ложить в супер банк больше лимита")
          return

       print(f"{name} положил в супер банк: {bank_p}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_p)
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       period = 180
       get = cursor.execute(f"SELECT stavka FROM time_bank WHERE user_id = {user_id}").fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if bank_p > 0:
             if balance >= bank_p:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , 🦸‍♂️ вы успешно положили в супер банк {bank2}$ {rwin}",
                                        parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bank = {bank + bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE time_bank SET stavka = {time.time()} WHERE user_id = {user_id}')
                connect.commit()

             elif int(balance) < int(bank_p):
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств! {rloser}", parse_mode='html')

          if bank_p <= 0:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя положить в супер банк отрицательное число! {rloser}",
                                     parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🤷‍♂️ | <a href='tg://user?id={user_id}'>{user_name}</a>, ложить в супер банк можно раз в 3 минуты", parse_mode='html')

    if message.text.startswith("Супер банк снять"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       bank_s = float(msg.text.split()[2])
       print(f"{name} снял с супер банка: {bank_s}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_s)
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       if bank_s > 0:
          if bank >= bank_s:
             await bot.send_message(message.chat.id,
                                    f"<a href='tg://user?id={user_id}'>{user_name}</a>, 🦸‍♂️ вы успешно сняли с супер банковского счёта {bank2}$ {rwin}",
                                    parse_mode='html')
             cursor.execute(f'UPDATE users SET bank = {bank - bank_s} WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance + bank_s} WHERE user_id = "{user_id}"')
             connect.commit()

          elif int(bank) < int(bank_s):
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств в супер банке! {rloser}",
                                    parse_mode='html')

    if message.text.startswith("супер банк снять"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       bank_s = float(msg.text.split()[2])
       print(f"{name} снял с супер банка: {bank_s}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_s)
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       if bank_s > 0:
          if bank >= bank_s:
             await bot.send_message(message.chat.id,
                                    f"<a href='tg://user?id={user_id}'>{user_name}</a>, 🦸‍♂️ вы успешно сняли с супер банковского счёта {bank2}$ {rwin}",
                                    parse_mode='html')
             cursor.execute(f'UPDATE users SET bank = {bank - bank_s} WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance + bank_s} WHERE user_id = "{user_id}"')
             connect.commit()

          elif int(bank) < int(bank_s):
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, в вашем супер банке недостаточно средств {rloser}",
                                    parse_mode='html')


###########################################БАНК###########################################
    # bank
    if message.text.lower() in ["Банк", "банк"]:
       msg = message
       chat_id = message.chat.id
       
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank_hran = cursor.execute("SELECT bank2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = int(bank[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?",(message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       bank_hran = int(bank_hran[0])
       bank_hran2 = '{:,}'.format(bank_hran)
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = int(bank[0])
       depozit2 = '{:,}'.format(depozit)
       bank2 = '{:,}'.format(bank)
       if user_status == 'Player':
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
       if user_status == 'Vip':
          procent = '9%'
          i = 9
          stats_depozit = 'Вип'
       if user_status == 'Premium':
          procent = '13%'
          i = 13
          stats_depozit = 'Премиум'
       if user_status == 'Platina':
          procent = '17%'
          i = 17
          stats_depozit = 'Платина'
       if user_status == 'Helper':
          procent = '21%'
          i = 21
          stats_depozit = 'Хелпер'
       if user_status == 'Sponsor':
          procent = '24%'
          i = 24
          stats_depozit = 'Спонсор'
       if user_status == 'Osnovatel':
          procent = '27%'
          i = 27
          stats_depozit = 'Основатель'
       if user_status == 'Vladelec':
          procent = '29%'
          i = 29
          stats_depozit = 'Владелец'
       if user_status == 'Bog':
          procent = '32%'
          i = 32
          stats_depozit = 'Бог'
       if user_status == 'Vlaselin':
          procent = '36%'
          i = 36
          stats_depozit = 'Властелин'

       else:
          procent = '30%'
          i = 6
          stats_depozit = 'Обычный'
          
          money_vivod = depozit / i
          money_vivod2 = int(money_vivod)
          money_vivod3 = '{:,}'.format(money_vivod2)

       c = 999999999999999999999999999999999999999999999999999999999999999999
       if bank >= 999999999999999999999999999999999999999999999999999999999999999999:
          bank = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank = {999999999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          bank2 = '{:,}'.format(bank)
       else:
          pass
       if bank_hran >= 999999999999999999999999999999999999999999999999999999999999999999:
          bank_hran = 999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET bank2 = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          bank_hran2 = '{:,}'.format(bank_hran)
       else:
          pass
       if depozit >= 999999999999999999999999999999999999999999999999999999999999999999999999:
          depozit = 999999999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET depozit = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          depozit2 = '{:,}'.format(depozit)

       

       await bot.send_message(message.chat.id,f"<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные о вашем банке 🏦\n\n👨‍💼 | Владелец: {user_name}\n🏛 | Основной счёт: {bank2}$\n💳 | Хранительный счёт: {bank_hran2}$\n💰 | Деньги на депозите: {depozit2}$\n     💎 Статус депозита: {stats_depozit}\n     📈 Процент под депозит: {procent}\n      💵 Деньги на вывод: {money_vivod3}$", parse_mode='html')
    if message.text.startswith('процент'):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i2 = str(msg.text.split()[1])
       summ = int(msg.text.split()[2])
       summ2 = '{:,}'.format(summ)

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       if user_status == 'Player':
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
       if user_status == 'Vip':
          procent = '9%'
          i = 9
          stats_depozit = 'Вип'
       if user_status == 'Premium':
          procent = '13%'
          i = 13
          stats_depozit = 'Премиум'
       if user_status == 'Platina':
          procent = '17%'
          i = 17
          stats_depozit = 'Платина'
       if user_status == 'Helper':
          procent = '21%'
          i = 21
          stats_depozit = 'Хелпер'
       if user_status == 'Sponsor':
          procent = '24%'
          i = 24
          stats_depozit = 'Спонсор'
       if user_status == 'Osnovatel':
          procent = '27%'
          i = 27
          stats_depozit = 'Основатель'
       if user_status == 'Vladelec':
          procent = '29%'
          i = 29
          stats_depozit = 'Владелец'
       if user_status == 'Bog':
          procent = '32%'
          i = 32
          stats_depozit = 'Бог'
       if user_status == 'Vlaselin':
          procent = '36%'
          i = 36
          stats_depozit = 'Властелин'

       else:
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
          
          money_vivod = depozit / i
          money_vivod2 = int(money_vivod)
          money_vivod3 = '{:,}'.format(money_vivod2)
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i2 == 'снять':
          if summ <= money_vivod2 :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли проценты с депозита {summ2}$ 💵", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но снимать с процентов депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
   

    if message.text.startswith('Процент'):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i2 = str(msg.text.split()[1])
       summ = int(msg.text.split()[2])
       summ2 = '{:,}'.format(summ)

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       if user_status == 'Player':
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
       if user_status == 'Vip':
          procent = '9%'
          i = 9
          stats_depozit = 'Вип'
       if user_status == 'Premium':
          procent = '13%'
          i = 13
          stats_depozit = 'Премиум'
       if user_status == 'Platina':
          procent = '17%'
          i = 17
          stats_depozit = 'Платина'
       if user_status == 'Helper':
          procent = '21%'
          i = 21
          stats_depozit = 'Хелпер'
       if user_status == 'Sponsor':
          procent = '24%'
          i = 24
          stats_depozit = 'Спонсор'
       if user_status == 'Osnovatel':
          procent = '27%'
          i = 27
          stats_depozit = 'Основатель'
       if user_status == 'Vladelec':
          procent = '29%'
          i = 29
          stats_depozit = 'Владелец'
       if user_status == 'Bog':
          procent = '32%'
          i = 32
          stats_depozit = 'Бог'
       if user_status == 'Vlaselin':
          procent = '36%'
          i = 36
          stats_depozit = 'Властелин'

       else:
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
          
          money_vivod = depozit / i
          money_vivod2 = int(money_vivod)
          money_vivod3 = '{:,}'.format(money_vivod2)
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i2 == 'снять':
          if summ <= money_vivod2 :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли проценты с депозита {summ2}$ 💵", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но снимать с процентов депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , 🙅‍♂️| нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
   
    if message.text.startswith('депозит'):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i = str(msg.text.split()[1])
       summ = int(msg.text.split()[2])
       summ2 = '{:,}'.format(summ)

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i == 'положить':
          if summ <= balance :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно положили на депозит {summ2}$ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя ложить отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
       if i == 'снять':
          if summ <= depozit :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли с депозита {summ2}$ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
          
    if message.text.startswith('Депозит'):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i = str(msg.text.split()[1])
       summ = int(msg.text.split()[2])
       summ2 = '{:,}'.format(summ)

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i == 'положить':
          if summ <= balance :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно положили на депозит {summ2}$ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя ложить отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
       if i == 'снять':
          if summ <= depozit :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли с депозита {summ2}$ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
          


    if message.text.startswith("Банк положить"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       bank_p = float(msg.text.split()[2])

       if bank_p >= 999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя ложить в банк больше лимита")
          return

       print(f"{name} положил в банк: {bank_p}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_p)
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       period = 180
       get = cursor.execute(f"SELECT stavka FROM time_bank WHERE user_id = {user_id}").fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if bank_p > 0:
             if balance >= bank_p:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно положили в банк {bank2}$ {rwin}",
                                        parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bank = {bank + bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE time_bank SET stavka = {time.time()} WHERE user_id = {user_id}')
                connect.commit()

             elif int(balance) < int(bank_p):
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств! {rloser}", parse_mode='html')

          if bank_p <= 0:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя положить в банк отрицательное число! {rloser}",
                                     parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ложить в банк можно раз в 3 минуты", parse_mode='html')
    if message.text.startswith("банк положить"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       bank_p = float(msg.text.split()[2])

       if bank_p >= 999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя ложить в банк больше лимита")
          return

       print(f"{name} положил в банк: {bank_p}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_p)
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       period = 180
       get = cursor.execute(f"SELECT stavka FROM time_bank WHERE user_id = {user_id}").fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if bank_p > 0:
             if balance >= bank_p:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно положили в банк {bank2}$ {rwin}",
                                        parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bank = {bank + bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE time_bank SET stavka = {time.time()} WHERE user_id = {user_id}')
                connect.commit()

             elif int(balance) < int(bank_p):
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств! {rloser}", parse_mode='html')

          if bank_p <= 0:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя положить в банк отрицательное число! {rloser}",
                                     parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🤷‍♂️ | <a href='tg://user?id={user_id}'>{user_name}</a>, ложить в банк можно раз в 3 минуты", parse_mode='html')

    if message.text.startswith("Банк снять"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       bank_s = float(msg.text.split()[2])
       print(f"{name} снял с банка: {bank_s}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_s)
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       if bank_s > 0:
          if bank >= bank_s:
             await bot.send_message(message.chat.id,
                                    f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли с банковского счёта {bank2}$ {rwin}",
                                    parse_mode='html')
             cursor.execute(f'UPDATE users SET bank = {bank - bank_s} WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance + bank_s} WHERE user_id = "{user_id}"')
             connect.commit()

          elif int(bank) < int(bank_s):
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств на банковском счету! {rloser}",
                                    parse_mode='html')

    if message.text.startswith("банк снять"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       bank_s = float(msg.text.split()[2])
       print(f"{name} снял с банка: {bank_s}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_s)
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       if bank_s > 0:
          if bank >= bank_s:
             await bot.send_message(message.chat.id,
                                    f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли с банковского счёта {bank2}$ {rwin}",
                                    parse_mode='html')
             cursor.execute(f'UPDATE users SET bank = {bank - bank_s} WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance + bank_s} WHERE user_id = "{user_id}"')
             connect.commit()

          elif int(bank) < int(bank_s):
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств на банковском счету! {rloser}",
                                    parse_mode='html')

###########################################АДМИН КОМАНДЫ###########################################
    if message.text.startswith("Поделить"):
       if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       perevod = float(msg.text.split()[1])
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod)
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       console = cursor.execute('SELECT user_id from users where user_status = "Owner"')
       console2 = cursor.execute('SELECT user_id from users where user_status = "Helper_Admin"')
       console3 = [console,console2]

       if int(balance2 / perevod) <= 0:
          await bot.send_message(message.chat.id, f"🙅‍♂️ | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя делить больше чем сам баланс", parse_mode='html')
          return

       if user_status[0] == 'Owner':
          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Деление баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 / perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Деление баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Деление баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 / perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Деление баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Деление баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Деление баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 /  perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       else:
          await message.reply(f"<a href='tg://user?id={user_id}'>{user_name}</a> ,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику {cash_owner_username} ⚠️", parse_mode='html')


    if message.text.startswith("поделить"):
       if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       perevod = float(msg.text.split()[1])
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod)
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 / perevod) <= 0:
          await bot.send_message(message.chat.id, f"🙅‍♂️ | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя делить больше чем сам баланс", parse_mode='html')
          return

       if user_status[0] == 'Owner':
          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Деление баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 / perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Деление баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Деление баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 / perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Деление баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Деление баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Деление баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 /  perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       else:
          await message.reply(f"<a href='tg://user?id={user_id}'>{user_name}</a> ,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику {cash_owner_username} ⚠️", parse_mode='html')

    
    if message.text.startswith('Выдать д'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])

       summ = float(message.text.split()[2])

       if user_status == 'Owner':
          await bot.send_message(message.chat.id, f"✅ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, вам было начислено {summ} Donate Coins 🪙", parse_mode='html')
          cursor.execute(f'UPDATE users SET donate_coins = {donate_coins + summ} WHERE user_id = {reply_user_id}')
          connect.commit()
       else:
          pass
    if message.text.startswith('Забрать д'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])

       summ = float(message.text.split()[2])

       if user_status == 'Owner':
          await bot.send_message(message.chat.id, f"✅ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, У вас было отнято {summ} Donate Coins 🪙", parse_mode='html')
          cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - summ} WHERE user_id = {reply_user_id}')
          connect.commit()          
       else:
          pass
    if message.text.startswith('Забрать рейтинг'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       rating = cursor.execute("SELECT rating from users where user_id = ?",(message.from_user.id,)).fetchone()
       rating = int(rating[0])

       summ = float(message.text.split()[2])

       if user_status == 'Owner':
          await bot.send_message(message.chat.id, f"✅ | <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, У вас было отнято {summ} Рейтинга 🪙", parse_mode='html')
          cursor.execute(f'UPDATE users SET rating = {rating - summ} WHERE user_id = {reply_user_id}')
          connect.commit()          
       else:
          pass          
    if message.text.startswith("Донат дать"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       ruser_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       ruser_name = ruser_name[0] 
       reply_user_id = msg.reply_to_message.from_user.id
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       perevod = int(msg.text.split()[1])
       perevod2 = '{0:,}'.format(perevod).replace(',', '.')

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?", (message.from_user.id,)).fetchone()
       donate_coins = round(int(donate_coins[0]))
       donate_coins2 = cursor.execute("SELECT donate_coins from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       donate_coins2 = round(donate_coins2[0])

       if not message.reply_to_message:
          await message.reply("ℹ | Эта команда должна быть ответом на сообщение!")
          return
       
       if reply_user_id == user_id:
          await message.reply_to_message.reply(f'ℹ | Вы не можете передать деньги сами себе! {rloser}', parse_mode='html')
          return

       
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       admin_id = 5535505563
       if perevod > 0:
          if donate_coins >= perevod: 
             if user_status[0] == "Admin":
                await message.reply_to_message.reply(f"💸 | Вы передали {perevod2} Доната🌑 игроку <a href='tg://user?id={reply_user_id}'>{ruser_name}</a> {rwin}", parse_mode='html')
                cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - perevod} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET donate_coins = {donate_coins2 + perevod} WHERE user_id = "{reply_user_id}"')
                connect.commit()  
                await bot.send_message(admin_id, f"🤝 | <a href='tg://user?id={user_id}'>{user_name}</a> передал {perevod2}$ игроку <a href='tg://user?id={reply_user_id}'>{ruser_name}</a> {rwin}", parse_mode='html')
             else:
                await message.reply_to_message.reply(f"🤝 | Вы передали {perevod2} Доната🌑 игроку <a href='tg://user?id={reply_user_id}'>{ruser_name}</a> {rwin}", parse_mode='html')
                cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - perevod} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET donate_coins = {donate_coins2 + perevod} WHERE user_id = "{reply_user_id}"')
                connect.commit()    
   
          elif int(balance) <= int(perevod):
             await message.reply( f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно Доната! {rloser}", parse_mode='html') 
             
       if perevod <= 0:
          await message.reply( f"ℹ | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя перевести отрицательное число! {rloser}", parse_mode='html') 
          
    if message.text.startswith("Изменить курс"):  

       user_id = message.from_user.id

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(user_id,)).fetchone()

       user_name = user_name[0]

       admin_id = 5197897742

       donate = cursor.execute("SELECT donate from users where user_id = ?",(admin_id,)).fetchone()

       donate_coins = round(int(donate[0]))

       summ = int(message.text.split()[2])

       summ2 = '{0:,}'.format(summ).replace(',', '.')

       win = ['🙂', '😋', '😄', '🤑', '😃']

       rwin = random.choice(win)

       loser = ['😔', '😕', '😣', '😞', '😢']

       rloser = random.choice(loser)

       if user_id == admin_id:        

          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно установили валютный курс равный {summ2}$", parse_mode='html')

          cursor.execute(f'UPDATE users SET donate_coins = {summ} WHERE user_id = "{admin_id}"')

          connect.commit()      

       else:

          return



    if message.text.startswith("купить валюту"):  

       user_id = message.from_user.id

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(user_id,)).fetchone()

       user_name = user_name[0]

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(user_id,)).fetchone()

       donate_coins = round(int(donate_coins[0]))

       balance = cursor.execute("SELECT balance from users where user_id = ?",(user_id,)).fetchone()

       balance = round(int(balance[0]))

       admin_id = 5197897742

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(admin_id,)).fetchone()

       donate_coins = round(int(donate_coins[0]))

       summ = int(message.text.split()[2])

       money = donate_coins * summ

       summ2 = '{0:,}'.format(summ).replace(',', '.')

       money2 = '{0:,}'.format(money).replace(',', '.')

       user_status = "Admin"

       win = ['🙂', '😋', '😄', '🤑', '😃']

       rwin = random.choice(win)

       loser = ['😔', '😕', '😣', '😞', '😢']

       rloser = random.choice(loser)

       if summ > 0:

          if donate_coins >= summ:

             await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили денег {money2}$ за  Донат коинов{summ2} 🌑! {rwin}", parse_mode='html')

             await bot.send_message(admin_id, f"🥳 | <a href='tg://user?id={user_id}'>{user_name}</a> купил {money2}$ на сумму {summ2} S-Coin! {rwin}", parse_mode='html')

             cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - summ} WHERE user_id = "{user_id}"')

             cursor.execute(f'UPDATE users SET balance = {balance + money} WHERE user_id = "{user_id}"')

             connect.commit() 

          elif donate_coins < summ:

             await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно донат-валюты! {rloser}", parse_mode='html')

       else:

          await bot.send_message(message.chat.id, f"ℹ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не можете купить отрицательное число валюты! {rloser}", parse_mode='html') 



    if message.text.startswith("Купить валюту"):  

       user_id = message.from_user.id

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(user_id,)).fetchone()

       user_name = user_name[0]

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(user_id,)).fetchone()

       donate_coins = round(int(donate_coins[0]))

       balance = cursor.execute("SELECT balance from users where user_id = ?",(user_id,)).fetchone()

       balance = round(int(balance[0]))

       admin_id = 5197897742

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(admin_id,)).fetchone()

       donate_coins = round(int(donate_coins[0]))

       summ = int(message.text.split()[2])

       money = donate_coins * summ

       summ2 = '{0:,}'.format(summ).replace(',', '.')

       money2 = '{0:,}'.format(money).replace(',', '.')

       user_status = "Admin"

       win = ['🙂', '😋', '😄', '🤑', '😃']

       rwin = random.choice(win)

       loser = ['😔', '😕', '😣', '😞', '😢']

       rloser = random.choice(loser)

       if summ > 0:

          if donate_coins >= summ:

             await bot.send_message(message.chat.id, f"🥳 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили денег {money2}$ за  Донат коинов{summ2} 🌑! {rwin}", parse_mode='html')

             await bot.send_message(admin_id, f"🥳 | <a href='tg://user?id={user_id}'>{user_name}</a> купил {money2}$ на сумму {summ2} S-Coin! {rwin}", parse_mode='html')

             cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - summ} WHERE user_id = "{user_id}"')

             cursor.execute(f'UPDATE users SET balance = {balance + money} WHERE user_id = "{user_id}"')

             connect.commit() 

          elif donate_coins < summ:

             await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно донат-валюты! {rloser}", parse_mode='html')

       else:

          await bot.send_message(message.chat.id, f"ℹ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не можете купить отрицательное число валюты! {rloser}", parse_mode='html') 
         
               
    if message.text.lower() == 'забрать права':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Owner':
          await message.reply(f"⛔️ |Разработчик: <a href='tg://user?id={user_id}'>{user_name}</a> забрал все права администрации у игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Player" WHERE user_id = {reply_user_id}')
          connect.commit()

       else:
          await message.reply(f"🆘 | Данная команда доступна только администрации с уровнем \"OWNER\"")
    if message.text.lower() == 'передать права':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Owner':
          await message.reply(f"⛔️ |Разработчик: <a href='tg://user?id={user_id}'>{user_name}</a> передал все права игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Owner" WHERE user_id = {reply_user_id}')
          connect.commit()

       else:
          await message.reply(f"🆘 | Данная команда доступна только администрации с уровнем \"OWNER\"")
    if message.text.lower() == 'выдать админа':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Owner':
          await message.reply(f"⛔️ |Разработчик: <a href='tg://user?id={user_id}'>{user_name}</a> выдал права администратора уровня \"ADMIN\" игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Admin" WHERE user_id = {reply_user_id}')
          connect.commit()

       else:
          await message.reply(f"🆘 | Данная команда доступна только администрации с уровнем \"OWNER\"")
    if message.text.lower() == 'выдать хелпера':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Owner':
          await message.reply(f"⛔️ |Разработчик: <a href='tg://user?id={user_id}'>{user_name}</a> выдал права администратора уровня \"HELPER ADMIN\" игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Helper_Admin" WHERE user_id = {reply_user_id}')
          connect.commit()

       else:
          await message.reply(f"🆘 | Данная команда доступна только администрации с уровнем \"OWNER\"")
    if message.text.lower() in ["админ", "Админ"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       admin_menu = InlineKeyboardMarkup(row_width=1)
       Admins_menu_up = InlineKeyboardButton(text='Войти ✅', callback_data='Admins_menu_up')
       admin_menu.add(Admins_menu_up)
       await bot.send_message(message.chat.id,f"<a href='tg://user?id={user_id}'>{user_name}</a>, войдите в админ меню🆘", reply_markup=admin_menu, parse_mode='html')
    if message.text.startswith("Умножить"):
       if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return
                
       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       perevod = float(msg.text.split()[1])
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 * perevod) >= 999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  Достигнул лимит баланса! 999 клаунд!", parse_mode='html')
          return

       if user_status[0] == 'Owner':

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       else:
          await message.reply(f"<a href='tg://user?id={user_id}'>{user_name}</a> ,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику {cash_owner_username} ⚠️", parse_mode='html')
    if message.text.startswith("умножить"):
       if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       perevod = float(msg.text.split()[1])
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod)
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 * perevod) >= 999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  Достигнул лимит баланса! 999 клаунд!", parse_mode='html')
          return

       if user_status[0] == 'Owner':
          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Умножение баланса\n💈 |Количество: {perevod2} раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 * perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return
       else:
          await message.reply(f"<a href='tg://user?id={user_id}'>{user_name}</a> ,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику {cash_owner_username} ⚠️", parse_mode='html')

    if message.text.startswith("выдать"):
       if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       perevod = float(msg.text.split()[1])
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod)
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 + perevod) >= 99999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  Достигнул лимит баланса! 9 гвинт!", parse_mode='html')
          return

       if user_status[0] == 'Owner':
          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Выдача денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Выдача денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Выдача денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Выдача денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Выдача денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Выдача денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Выдача денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()
          return 
       else:
          await message.reply(f"<a href='tg://user?id={user_id}'>{user_name}</a> ,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь владельцу ⚠️", parse_mode='html')

    if message.text.startswith("Хочу"):
       if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       perevod = float(msg.text.split()[1])
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod)
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 + perevod) >= 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  Достигнул лимит баланса!", parse_mode='html')
          return

       if user_status[0] == 'Player':
          await message.reply(f"⛔️ |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Захотел\n💈 |Деньги: {perevod2}$\n🤴 |Захотел: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Захотел\n💈 |Количество: {perevod2}$\n👨 |Игрок: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Захотел\n💈 |Количество: {perevod2}$\n👨 |Игрок: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Захотел\n💈 |Количество: {perevod2}$\n👨 |Игрок: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Захотел\n💈 |Количество: {perevod2}$\n👨 |Игрок: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Захотел\n💈 |Количество: {perevod2}$\n👨 |Игрок: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Захотел\n💈 |Количество: {perevod2}$\n👨 |Игрок: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       else:
          await message.reply(f"<a href='tg://user?id={user_id}'>{user_name}</a> ,Извините но вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к владельцу ⚠️", parse_mode='html') 

    if message.text.startswith("забрать"):
       if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       perevod = float(msg.text.split()[1])
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod)
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 - perevod) < 0:
         
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя заберать больше чем сам баланс игрока", parse_mode='html')
          return

       if user_status[0] == 'Owner':
          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       else:
          await message.reply(f"<a href='tg://user?id={user_id}'>{user_name}</a> ,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику {cash_owner_username} ⚠️", parse_mode='html')

    if message.text.startswith("Забрать"):
       if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       perevod = float(msg.text.split()[1])
       reply_user_id = msg.reply_to_message.from_user.id
       perevod2 = '{:,}'.format(perevod)
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if int(balance2 - perevod) < 0:
         
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя заберать больше чем сам баланс игрока", parse_mode='html')
          return

       if user_status[0] == 'Owner':

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Отбор денег\n💈 |Количество: {perevod2}$\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       else:
          await message.reply(f"<a href='tg://user?id={user_id}'>{user_name}</a> ,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику {cash_owner_username} ⚠️", parse_mode='html')

    if message.text.lower() in ["обнулить", "Обнулить"]:
       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       reply_user_id = msg.reply_to_message.from_user.id
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()

       if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return
       if user_status[0] == 'Owner':
          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Обнуление\n💈 |Количество: 1 раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET silver = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET gold = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE farm SET linen = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE farm SET cotton = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_games = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_pick = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_rake = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_craft = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_kit = {0} WHERE user_id = "{reply_user_id}"')
          

          connect.commit() 
          return
       if user_status[0] == 'Helper_Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Обнуление\n💈 |Количество: 1 раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Обнуление\n💈 |Количество: 1 раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Обнуление\n💈 |Количество: 1 раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET silver = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET gold = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE farm SET linen = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE farm SET cotton = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_games = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_pick = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_rake = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_craft = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_kit = {0} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       if user_status[0] == 'Admin':
          rows = cursor.execute('SELECT user_id FROM users where user_status = "Helper_Admin"').fetchall()
          for row in rows:
             await bot.send_message(row[0], f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Обнуление\n💈 |Количество: 1 раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await bot.send_message(5197897742, f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Обнуление\n💈 |Количество: 1 раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

          await message.reply(f"⛔️ |Администратор: <a href='tg://user?id={user_id}'>{user_name}</a> \n⚙️ |Действие: Обнуление\n💈 |Количество: 1 раз\n👨 |Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE users SET ethereum = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET iron = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET metall = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET silver = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET bronza = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE mine SET gold = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE farm SET linen = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE farm SET cotton = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_games = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_pick = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_rake = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_craft = {0} WHERE user_id = "{reply_user_id}"')
          cursor.execute(f'UPDATE bot_time SET time_kit = {0} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
          return
       else:
          await message.reply(f"<a href='tg://user?id={user_id}'>{user_name}</a> ,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику {cash_owner_username} ⚠️", parse_mode='html')
###########################################ПРАВИЛА###########################################
    if message.text.lower() in ["Правила", "правила"]:
       await bot.send_message(message.chat.id, f"""{pravilabota}""", parse_mode='html')
###########################################ПОМОЩЬ###########################################
    if message.text.lower() in ["помощь", "Помощь", "пм", "Пм"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       help2 = InlineKeyboardMarkup(row_width=2)
       Osn2 = InlineKeyboardButton(text='📝', callback_data='Osn2')
       game2 = InlineKeyboardButton(text=' 🎮', callback_data='game2')
       rabot2 = InlineKeyboardButton(text='💵', callback_data='rabot2')
       Im2 = InlineKeyboardButton(text='🕍 ', callback_data='Im2')
       Priv2 = InlineKeyboardButton(text='📖', callback_data='Priv2')
       Adm2 = InlineKeyboardButton(text='⛔️', callback_data='Admins_menu_up')
       help2.add(Osn2, game2, rabot2, Im2, Priv2, Adm2)
       await bot.send_message(message.chat.id, f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, виберите категории🔍

📝 | Основные
🎮 | Развлечения
🔨 | Зароботак
🏘 | Дома
📖 | Статусы
⛔️ | Для админов

Разработчик: @ptsub 💻
Наша беседа: <tg-spoiler>@ptsub</tg-spoiler> 💬 
    ''', reply_markup=help2, parse_mode='html')

###########################################СПИН#############################################
    if message.text.startswith("спин"):
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])

        balance2 = '{:,}'.format(balance).replace(',', '.')
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id
        rx = random.randint(0, 1001)
        msg = message
        user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
        user_name = str(user_name[0])
        name = msg.from_user.full_name
        d1 = float(message.text.split()[1])
        d2 = str(message.text.split()[2])

        if d2 == 'к':
           summ = int(f'{d1}000')
        if d2 == 'кк':
         summ = int(f'{d1}000000')
        if d2 == 'ккк':
           summ = int(f'{d1}000000000')
        if d2 == 'кккк':
           summ = int(f'{d1}000000000000')
        if d2 == 'ккккк':
           summ = int(f'{d1}000000000000000')
        if d2 == 'кккккк':
           summ = int(f'{d1}000000000000000000')
        if d2 == 'ккккккк':
           summ = int(f'{d1}000000000000000000000')
        if d2 == 'кккккккк':
           summ = int(f'{d1}000000000000000000000000')
        if d2 == 'ккккккккк':
           summ = int(f'{d1}000000000000000000000000000')
        if d2 == 'кккккккккк':
           summ = int(f'{d1}000000000000000000000000000000')
        if d2 == 'ккккккккккк':
           summ = int(f'{d1}000000000000000000000000000000000')
        if d2 == 'кккккккккккк':
           summ = int(f'{d1}000000000000000000000000000000000000')
        if d2 == 'ккккккккккккк':
           summ = int(f'{d1}000000000000000000000000000000000000000')
        if d2 == 'кккккккккккккк':
           summ = int(f'{d1}000000000000000000000000000000000000000000')
        if d2 == 'ккккккккккккккк':
           summ = int(f'{d1}000000000000000000000000000000000000000000000')
        if d2 == 'кккккккккккккккк':
           summ = int(f'{d1}000000000000000000000000000000000000000000000000')
        if d2 == 'ккккккккккккккккк':
           summ = int(f'{d1}000000000000000000000000000000000000000000000000000')
        if d2 == 'кккккккккккккккккк':
           summ = int(f'{d1}000000000000000000000000000000000000000000000000000000')
        if d2 == 'ккккккккккккккккккк':
           summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000')
        if d2 == 'кккккккккккккккккккк':
           summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000')
        if d2 == 'ккккккккккккккккккккк':
           summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000000')
        summ2 = '{:,}'.format(summ)
        print(f"{name} поставил в спин: {summ} и выиграл/проиграл: {rx}")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        period = 5 
        get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        loz = ['💩|👑|👑','💩|🖕|👑','💎|🖕|👑','💎|💣|🍌','👑|🍌|🖕','💎|🍓|💣']
        win = ['💎|🍓|🍌','👑|💎|🍓','🍓|👑|💎','💎|🍓|🍌','💎|🍓|🍓','🍌|🍌|💎']
        Twin = ['💎|💎|💎','🍓|🍓|🍓','👑|👑|👑','🍌|🍌|🍌']
        smtwin = ['🤯','🤩','😵','🙀']
        smwin = ['🙂', '😋', '😄', '🤑', '😃']
        loser = ['😔', '😕', '😣', '😞', '😢']
        rsmtwin = random.choice(smtwin)
        rsmtwin2 = random.choice(smtwin)
        rtwin = random.choice(Twin)
        rloser = random.choice(loser)
        rloser2 = random.choice(loser)
        rwin = random.choice(win)
        rloz = random.choice(loz)
        rsmwin = random.choice(smwin)
        rsmwin2 = random.choice(smwin)
        if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(0, 350):
                        c = Decimal(summ * 2)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)

                        await bot.send_message(chat_id,
                                               f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎰 | Игра: Спин\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {rwin} - {c2}$",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return

        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(351, 1000):
                        c = Decimal(summ * 0)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id,
                                               f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎰 | Игра: Спин\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {rloz} - {c2}$",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 0)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) == 1001:
                        c = Decimal(summ * 25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id,
                                               f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎰 | Игра: Спин\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {rwin} - {c2}$ - Джекпот",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 25)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return
                elif summ <= 1:
                    await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число! {rloser}",
                                           parse_mode='html')
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
        else:
            await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, извини. но играть можно только каждые 5️⃣ секунд. {rloser}",
                                       parse_mode='html')
    if message.text.startswith("Спин"):
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])

        balance2 = '{:,}'.format(balance)
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id
        rx = random.randint(0, 1001)
        msg = message
        user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
        user_name = str(user_name[0])
        name = msg.from_user.full_name
        summ = float(msg.text.split()[1])
        summ2 = '{:,}'.format(summ)
        print(f"{name} поставил в спин: {summ} и выиграл/проиграл: {rx}")
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        period = 5 
        get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        loz = ['💩|👑|👑','💩|🖕|👑','💎|🖕|👑','💎|💣|🍌','👑|🍌|🖕','💎|🍓|💣']
        win = ['💎|🍓|🍌','👑|💎|🍓','🍓|👑|💎','💎|🍓|🍌','💎|🍓|🍓','🍌|🍌|💎']
        Twin = ['💎|💎|💎','🍓|🍓|🍓','👑|👑|👑','🍌|🍌|🍌']
        smtwin = ['🤯','🤩','😵','🙀']
        smwin = ['🙂', '😋', '😄', '🤑', '😃']
        loser = ['😔', '😕', '😣', '😞', '😢']
        rsmtwin = random.choice(smtwin)
        rsmtwin2 = random.choice(smtwin)
        rtwin = random.choice(Twin)
        rloser = random.choice(loser)
        rloser2 = random.choice(loser)
        rwin = random.choice(win)
        rloz = random.choice(loz)
        rsmwin = random.choice(smwin)
        rsmwin2 = random.choice(smwin)
        if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(0, 350):
                        c = Decimal(summ * 2)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id,
                                               f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎰 | Игра: Спин\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {rwin} - {c2}$",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return

        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(351, 1000):
                        c = Decimal(summ * 0)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id,
                                               f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎰 | Игра: Спин\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {rloz} - {c2}$",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 0)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) == 1001:
                        c = Decimal(summ * 25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id,
                                               f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎰 | Игра: Спин\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {rwin} - {c2}$ - Джекпот",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 25)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return
                elif summ <= 1:
                    await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число! {rloser}",
                                           parse_mode='html')
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
        else:
            await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, извини. но играть можно только каждые 5️⃣ секунд. {rloser}",
                                       parse_mode='html')



################################################### GAME-VB ########################################


    if message.text.lower() in ['vb', "вб"]:
       msg = message
       user_id = msg.from_user.id
   
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот вся информация за игру "Game-VB" 🧊

📌 | Пример: /gamevb

⚠️ | ВАЖНО: Это игра, в которой нету ставки. В этой игре вы играете сразу на весь свой баланс

⚖️ | Шансы:
🟥 | 70% - LOSER - [0.1X]
🟩 | 30% - WIN - [1.5X]
       """, parse_mode='html')

#################################################### ФУТБОЛ ########################################

    if message.text.lower() in ['футбол', "фб"]:
       msg = message
       user_id = msg.from_user.id
   
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот вся информация за игру "Футбол" ⚽️

📌 | Пример: Футбол\Фб [ставка] | Футбол 1

⚖️ | Шансы:
🟥 | 29% - Промах - [0.2Х]
🟥 | 31% - Штанга - [0.4Х]
🟥 | 20% - Перекладина - [0.8X]
🟩 | 12% - Гол - [1.4X]
🟩 | 3% - Девятка - [2.3X]
🟩 | 1% - Крестовина - [4.3X]
""", parse_mode='html')





    if message.text.startswith('Фб'):
       msg = message
       user_id = msg.from_user.id

       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       summ = int(message.text.split()[1])
       summ2 = '{:,}'.format(summ)

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance)

       rx = random.randint(0,9550)
       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0,2900):
                   i = summ - summ * 0.2
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🧾 | Проигрыш: Промах! - {i3}$ [0.2X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(2901,6000):
                   i = summ - summ * 0.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🧾 | Проигрыш: Штанга! - {i3}$ [0.4X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(6001,8000):
                   i = summ - summ * 0.8
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🧾 | Проигрыш: Перекладина! - {i3}$ [0.8X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(8001,9200):
                   i = summ * 1.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🧾 | Выигрыш: Гол! - {i3}$ [1.4X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9201,9500):
                   i = summ * 2.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🧾 | Выигрыш: Девятка! - {i3}$ [2.3X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9501,9550):
                   i = summ * 4.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🧾 | Выигрыш: Крестовина! - {i3}$ [4.3X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств!", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд ", parse_mode='html')




    if message.text.startswith('Футбол'):
       msg = message
       user_id = msg.from_user.id

       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       summ = int(message.text.split()[1])
       summ2 = '{:,}'.format(summ)

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance)

       rx = random.randint(0,9550)
       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0,2900):
                   i = summ - summ * 0.2
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🧾 | Проигрыш: Промах! - {i3}$ [0.2X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(2901,6000):
                   i = summ - summ * 0.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🧾 | Проигрыш: Штанга! - {i3}$ [0.4X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(6001,8000):
                   i = summ - summ * 0.8
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🧾 | Проигрыш: Перекладина! - {i3}$ [0.8X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(8001,9200):
                   i = summ * 1.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🥳 | Выигрыш: Гол! - {i3}$ [1.4X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9201,9500):
                   i = summ * 2.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🥳 | Выигрыш: Девятка! - {i3}$ [2.3X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9501,9550):
                   i = summ * 4.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🥳 | Выигрыш: Крестовина! - {i3}$ [4.3X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств!", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд ", parse_mode='html')






    if message.text.startswith('фб'):
       msg = message
       user_id = msg.from_user.id

       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       d1 = float(message.text.split()[1])
       d2 = str(message.text.split()[2])

       if d2 == 'к':
          summ = int(f'{d1}000')
       if d2 == 'кк':
          summ = int(f'{d1}000000')
       if d2 == 'ккк':
          summ = int(f'{d1}000000000')
       if d2 == 'кккк':
          summ = int(f'{d1}000000000000')
       if d2 == 'ккккк':
          summ = int(f'{d1}000000000000000')
       if d2 == 'кккккк':
          summ = int(f'{d1}000000000000000000')
       if d2 == 'ккккккк':
          summ = int(f'{d1}000000000000000000000')
       if d2 == 'кккккккк':
          summ = int(f'{d1}000000000000000000000000')
       if d2 == 'ккккккккк':
          summ = int(f'{d1}000000000000000000000000000')
       if d2 == 'кккккккккк':
          summ = int(f'{d1}000000000000000000000000000000')
       if d2 == 'ккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000')
       if d2 == 'кккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000')
       if d2 == 'ккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000000')
       summ2 = '{:,}'.format(summ)

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance)

       rx = random.randint(0,9550)
       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0,2900):
                   i = summ - summ * 0.2
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🧾 | Проигрыш: Промах! - {i3}$ [0.2X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(2901,6000):
                   i = summ - summ * 0.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
💰 | Ставка: {summ2}$
🧾 | Проигрыш: Штанга! - {i3}$ [0.4X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(6001,8000):
                   i = summ - summ * 0.8
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
🎟 | Ставка: {summ2}$
🧾 | Проигрыш: Перекладина! - {i3}$ [0.8X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(8001,9200):
                   i = summ * 1.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: Гол! - {i3}$ [1.4X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9201,9500):
                   i = summ * 2.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: Девятка! - {i3}$ [2.3X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9501,9550):
                   i = summ * 4.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: Крестовина! - {i3}$ [4.3X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств!", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд ", parse_mode='html')


    if message.text.startswith('футбол'):
       msg = message
       user_id = msg.from_user.id

       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       d1 = int(message.text.split()[1])
       d2 = str(message.text.split()[2])

       if d2 == 'к':
          summ = int(f'{d1}000')
       if d2 == 'кк':
          summ = int(f'{d1}000000')
       if d2 == 'ккк':
          summ = int(f'{d1}000000000')
       if d2 == 'кккк':
          summ = int(f'{d1}000000000000')
       if d2 == 'ккккк':
          summ = int(f'{d1}000000000000000')
       if d2 == 'кккккк':
          summ = int(f'{d1}000000000000000000')
       if d2 == 'ккккккк':
          summ = int(f'{d1}000000000000000000000')
       if d2 == 'кккккккк':
          summ = int(f'{d1}000000000000000000000000')
       if d2 == 'ккккккккк':
          summ = int(f'{d1}000000000000000000000000000')
       if d2 == 'кккккккккк':
          summ = int(f'{d1}000000000000000000000000000000')
       if d2 == 'ккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000')
       if d2 == 'кккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000')
       if d2 == 'ккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000000')
       summ2 = '{:,}'.format(summ)

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance)

       rx = random.randint(0,9550)
       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0,2900):
                   i = summ - summ * 0.2
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
🎟 | Ставка: {summ2}$
🧾 | Проигрыш: Промах! - {i3}$ [0.2X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(2901,6000):
                   i = summ - summ * 0.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
🎟 | Ставка: {summ2}$
🧾 | Проигрыш: Штанга! - {i3}$ [0.4X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(6001,8000):
                   i = summ - summ * 0.8
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
🎟 | Ставка: {summ2}$
🧾 | Проигрыш: Перекладина! - {i3}$ [0.8X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(8001,9200):
                   i = summ * 1.4
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: Гол! - {i3}$ [1.4X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9201,9500):
                   i = summ * 2.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: Девятка! - {i3}$ [2.3X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(9501,9550):
                   i = summ * 4.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
⚽️ | Игра: Футбол
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: Крестовина! - {i3}$ [4.3X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств!", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд ", parse_mode='html')

##################################################КАЗИНО############################################
   
    if message.text.startswith("Охота"): 
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id

       win = ['🙂', '😋', '😄', '🗡', '😃']
       loser = ['😔', '😕', '😣', '😞', '😢']
       rx = random.randint(0,120)
       rand = random.randint(1,4)
       rwin = random.choice(win)
       rloser = random.choice(loser)

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       summ5 = message.text.split()[1]
       
       
       summ4 = (summ5).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '').replace("$", "").replace('м', '000000').replace('m', '000000').replace('т','000000000000')
       summ3 = float(summ4)
       summ = int(summ3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       rx = random.randint(0,10216)
       if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance)
       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0, 2500):
                   i = summ - summ * 0.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\nВы успешно пошли на охоту и выиграли\проиграли\n Проигрыш: {i3}$ [0.3X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(2501, 6500):
                   i = summ - summ * 0.5
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🥋 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n Вы успешно пошли на охотуи выиграли \проиграли\n🧾 | Проигрыш: {i3}$ [0.5X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(6500, 7500):
                   i = summ 
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\nВы никого не шали поэтому деньги остаються у вас [1X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(7501, 9500):
                   i = summ * 1.5
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\nВы успешно пршли на охоту и выиграли/проиграли\nВыигрыш: {i3}$ [1.5X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(9501, 10000):
                   i = summ * 2.8
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\nВы успешно пошли на охоту и выиграли/проиграли\nВыигрыш: {i3}$ [2.8X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(10001, 10200):
                   i = summ * 5
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\nВы успешно пошли на охоту  и выиграли/проиграли Выигрыш: {i3}$ [5X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(10201, 10210):
                   i = summ * 10
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(1571995529, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [10X]", parse_mode='html')

                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [10X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(10211, 10215):
                   i = summ * 41
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(1571995529, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [41X]", parse_mode='html')

                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [41X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) == 10216:
                   i = summ * 100
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(1571995529, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [100X]", parse_mode='html')

                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [100X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit()   
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств!", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд ", parse_mode='html') 







##################################################КАЗИНО############################################
   
    if message.text.startswith("казино"): 
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id

       win = ['🙂', '😋', '😄', '🤑', '😃']
       loser = ['😔', '😕', '😣', '😞', '😢']
       rx = random.randint(0,120)
       rand = random.randint(1,4)
       rwin = random.choice(win)
       rloser = random.choice(loser)

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       summ5 = message.text.split()[1]
       
       
       summ4 = (summ5).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '').replace("$", "").replace('м', '000000').replace('m', '000000').replace('т','000000000000').replace('д', '000000000000000000')
       summ3 = float(summ4)
       summ = int(summ3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       rx = random.randint(0,10216)
       if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance)
       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0, 2500):
                   i = summ - summ * 0.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Проигрыш: {i3}$ [0.3X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(2501, 6500):
                   i = summ - summ * 0.5
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Проигрыш: {i3}$ [0.5X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(6500, 7500):
                   i = summ 
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Деньги остаються при вас [1X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(7501, 9500):
                   i = summ * 1.5
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [1.5X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(9501, 10000):
                   i = summ * 2.8
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [2.8X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(10001, 10200):
                   i = summ * 5
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [5X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(10201, 10210):
                   i = summ * 10
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(1571995529, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [10X]", parse_mode='html')

                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [10X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(10211, 10215):
                   i = summ * 41
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(1571995529, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [41X]", parse_mode='html')

                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [41X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) == 10216:
                   i = summ * 100
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(1571995529, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [100X]", parse_mode='html')

                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🤵‍♀️ | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [100X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit()   
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств!", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд ", parse_mode='html') 







###########################################PLINKO###########################################
    
    
    if message.text.startswith("плинко"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id

       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       win = ['🙂', '😋', '😄', '😃']
       loser = ['😔', '😕', '😣', '😞', '😢']
       rx = random.randint(0,937)
       rwin = random.choice(win)
       rloser = random.choice(loser)

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       name = msg.from_user.full_name 

       d1 = int(message.text.split()[1])
       d2 = str(message.text.split()[2])

       if d2 == 'к':
          summ = int(f'{d1}000')
       if d2 == 'кк':
          summ = int(f'{d1}000000')
       if d2 == 'ккк':
          summ = int(f'{d1}000000000')
       if d2 == 'кккк':
          summ = int(f'{d1}000000000000')
       if d2 == 'ккккк':
          summ = int(f'{d1}000000000000000')
       if d2 == 'кккккк':
          summ = int(f'{d1}000000000000000000')
       if d2 == 'ккккккк':
          summ = int(f'{d1}000000000000000000000')
       if d2 == 'кккккккк':
          summ = int(f'{d1}000000000000000000000000')
       if d2 == 'ккккккккк':
          summ = int(f'{d1}000000000000000000000000000')
       if d2 == 'кккккккккк':
          summ = int(f'{d1}000000000000000000000000000000')
       if d2 == 'ккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000')
       if d2 == 'кккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000')
       if d2 == 'ккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000000')

       summ2 = '{:,}'.format(summ)
       print(f"{name} поставил в казино: {summ} и выиграл/проиграл: {rx}")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance)

       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if d1 > 0:
                if int(rx) in range(0,100):
                   c = Decimal(summ)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: 0$ [x0]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit()   
                   return                           
                if int(rx) in range(101,300):
                   c = Decimal(summ - summ * 0.25)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x0.25]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.75} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit()  
                   return   
                if int(rx) in range(301,600):
                   c = Decimal(summ * 0.5)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x0.5]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.5} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return  
                if int(rx) in range(601,850):
                   c = Decimal(summ - summ * 0.75)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x0.75]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.25} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return  
                if int(rx) in range(851,900):
                   c = Decimal(summ * 2)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x2]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return 
                if int(rx) in range(901,930):
                   c = Decimal(summ * 3)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x3]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 3)} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return
                if int(rx) in range(931,932):
                    c = Decimal(summ * 29)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2)
                    await bot.send_message(5493115949, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x29]", parse_mode='html')

                    await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x29]", parse_mode='html')
                    cursor.execute(
                        f'UPDATE users SET balance = {(balance - summ) + (summ * 29)} WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                    connect.commit()
                if int(rx) in range(933,937):
                   c = Decimal(summ * 10)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(5493115949, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x10]", parse_mode='html')

                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x10]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 10)} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return 
             elif summ <= 1:
                  await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число! {rloser}", parse_mode='html')                                      
          elif int(balance) <= int(summ):
               await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
       else:
        await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, извини. но играть можно только каждые 5️⃣ секунд. {rloser}", parse_mode='html')
        return











    if message.text.startswith("Плинко"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id

       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       win = ['🙂', '😋', '😄', '😃']
       loser = ['😔', '😕', '😣', '😞', '😢']
       rx = random.randint(0,937)
       rwin = random.choice(win)
       rloser = random.choice(loser)

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       name = msg.from_user.full_name 
       summ = int(msg.text.split()[1])
       summ2 = '{:,}'.format(summ)
       print(f"{name} поставил в казино: {summ} и выиграл/проиграл: {rx}")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance)
       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0,100):
                   c = Decimal(summ)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: 0$ [x0]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit()   
                   return                           
                if int(rx) in range(101,300):
                   c = Decimal(summ - summ * 0.25)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x0.25]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.75} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit()  
                   return   
                if int(rx) in range(301,600):
                   c = Decimal(summ * 0.5)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x0.5]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.5} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return  
                if int(rx) in range(601,850):
                   c = Decimal(summ - summ * 0.75)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x0.75]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ * 0.25} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return  
                if int(rx) in range(851,900):
                   c = Decimal(summ * 2)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x2]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return 
                if int(rx) in range(901,930):
                   c = Decimal(summ * 3)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x3]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 3)} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return
                if int(rx) in range(931,932):
                    c = Decimal(summ * 29)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2)
                    await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x29]", parse_mode='html')
                    cursor.execute(
                        f'UPDATE users SET balance = {(balance - summ) + (summ * 29)} WHERE user_id = "{user_id}"')
                    cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                    connect.commit()
                if int(rx) in range(933,937):
                   c = Decimal(summ * 10)
                   c2 = round(c)
                   c2 = '{:,}'.format(c2)
                   await bot.send_message(chat_id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n◾️ | Игра: Плинко\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {c2}$ [x10]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 10)} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                   cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                   connect.commit() 
                   return 
             elif summ <= 1:
                  await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число! {rloser}", parse_mode='html')                                      
          elif int(balance) <= int(summ):
               await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
       else:
        await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, извини. но играть можно только каждые 5️⃣ секунд. {rloser}", parse_mode='html')
        return
##################################################ЗВЕЗДА############################################
   
    if message.text.startswith("Звезда"): 
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id

       win = ['🙂', '😋', '😄', '🤑', '😃']
       loser = ['😔', '😕', '😣', '😞', '😢']
       rx = random.randint(0,120)
       rand = random.randint(1,4)
       rwin = random.choice(win)
       rloser = random.choice(loser)

       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       summ5 = message.text.split()[1]
       
       
       summ4 = (summ5).replace(' ', '').replace('k', '000').replace('е','е').replace('к', '000').replace(',', '').replace('.', '').replace("$", "").replace('м', '000000').replace('m', '000000').replace('т','000000000000')
       summ3 = float(summ4)
       summ = int(summ3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       rx = random.randint(0,10216)
       if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance)
       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0, 2500):
                   i = summ - summ * 0.3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🌟 | Игра: Звезда\n🎟 | Ставка: {summ2}$\n🧾 | Увы Проигрыш: {i3}$ [0.3X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(2501, 6500):
                   i = summ - summ * 0.5
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🌟 | Игра: Звезда\n🎟 | Ваша Ставка: {summ2}$\n🧾 | Увы Проигрыш: {i3}$ [0.5X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(6500, 7500):
                   i = summ 
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🌟 | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Звезда не долетела поэтому деньги остоються при вас [1X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(7501, 9500):
                   i = summ * 1.5
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🌟 | Игра: Звезда\n🎟 | Ваша Ставка: {summ2}$\n🧾 | Ваш Выигрыш: {i3}$ [1.5X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(9501, 10000):
                   i = summ * 2.8
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🌟 | Игра: Звезда\n🎟 | Ваша Ставка: {summ2}$\n🧾 | Ваш Выигрыш: {i3}$ [2.8X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(10001, 10200):
                   i = summ * 5
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🌟 | Игра: Звезда\n🎟 | Ставка: {summ2}$\n🧾 | Ваш Выигрыш: {i3}$ [5X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(10201, 10210):
                   i = summ * 10
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(1571995529, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🌟 | Игра: Звезда\n🎟 | Ваша Ставка: {summ2}$\n🧾 | Ваш Выигрыш: {i3}$ [10X]", parse_mode='html')

                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🌟 | Игра: Звезда\n🎟 | Ваша Ставка: {summ2}$\n🧾 | Ваш Выигрыш: {i3}$ [10X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) in range(10211, 10215):
                   i = summ * 41
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(1571995529, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🌟 | Игра: Звезда\n🎟 | Ваша ставка: {summ2}$\n🧾 | Ваш Выигрыш: {i3}$ [41X]", parse_mode='html')

                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🌟 | Игра: Звезда\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [41X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit() 
                if int(rx) == 10216:
                   i = summ * 100
                   i2 = int(i)
                   i3 = '{:,}'.format(i2)
                   await bot.send_message(1571995529, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🌟 | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [100X]", parse_mode='html')

                   await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🌟 | Игра: Казино\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {i3}$ [100X]", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   connect.commit()   
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств чтобы играть в звезду!", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд ", parse_mode='html') 







###########################################РЕЙТИНГ###########################################
    if message.text.lower() == 'рейтинг':
       msg = message
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",
                                    (message.from_user.id,)).fetchone()
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       bank = int(bank[0])
       rating = int(rating[0])
       rating2 = '{:,}'.format(rating)
       rey = ['👑','✨','✏️']
       ranrey = random.choice(rey)
       
      
       await bot.send_message(message.chat.id, f"💎 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш рейтинг - {rating2}", parse_mode='html')

    if message.text.startswith("рейтинг купить"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       d1 = float(message.text.split()[2])
       d2 = str(message.text.split()[3])

       if d2 == 'к':
          summ = int(f'{d1}000')
       if d2 == 'кк':
          summ = int(f'{d1}000000')
       if d2 == 'ккк':
          summ = int(f'{d1}000000000')
       if d2 == 'кккк':
          summ = int(f'{d1}000000000000')
       if d2 == 'ккккк':
          summ = int(f'{d1}000000000000000')
       if d2 == 'кккккк':
          summ = int(f'{d1}000000000000000000')
       if d2 == 'ккккккк':
          summ = int(f'{d1}000000000000000000000')
       if d2 == 'кккккккк':
          summ = int(f'{d1}000000000000000000000000')
       if d2 == 'ккккккккк':
          summ = int(f'{d1}000000000000000000000000000')
       if d2 == 'кккккккккк':
          summ = int(f'{d1}000000000000000000000000000000')
       if d2 == 'ккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000')
       if d2 == 'кккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000')
       if d2 == 'ккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000')

       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = int(rating[0])
       rating2 = '{:,}'.format(summ)
       c = summ * 150000000
       c2 = '{:,}'.format(c)

       if (summ + rating) >= 99999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя покупать рейтинг больше лимита")
          return

       if summ > 0:
          if int(balance) >= int(summ * 150000000):
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы повысили количество вашего рейтинга на {rating2}💎 за {c2}$! {rwin}", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance - c} WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET rating = {rating + summ} WHERE user_id = "{user_id}"')
             connect.commit()

 
       if int(balance) < int(summ * 150000000):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')

       if summ <= 0:
         await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя купить отрицательное число! {rloser}", parse_mode='html')
    
    if message.text.startswith("Рейтинг продать"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       summ = float(msg.text.split()[2])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = int(rating[0])
       c = summ * 100000000
       c2 = '{:,}'.format(c)
       rating2 = '{:,}'.format(summ)
       if summ > 0:
        if int(rating) >= int(summ):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы понизили количество вашего рейтинга на {rating2}💎 за {c2}$! {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + c} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE users SET rating = {rating - summ} WHERE user_id = "{user_id}"')
          connect.commit()

        if int(rating) < int(summ):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, у вас недостаточно рейтинга для его продажи! {rloser}", parse_mode='html')

       if summ <= 0:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя продать отрицательное число! {rloser}", parse_mode='html')

    if message.text.startswith("Рейтинг купить"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       summ = float(msg.text.split()[2])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = int(rating[0])
       rating2 = '{:,}'.format(summ)
       c = summ * 150000000

       if (summ + rating) >= 999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  нельзя покупать рейтинг больше лимита")
          return

       c2 = '{:,}'.format(c)
       if summ > 0:
        if int(balance) >= int(summ * 150000000):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы повысили количество вашего рейтинга на {rating2}💎 за {c2}$! {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance - c} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE users SET rating = {rating + summ} WHERE user_id = "{user_id}"')
          connect.commit()

 
        if int(balance) < int(summ * 150000000):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')

       if summ <= 0:
         await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя купить отрицательное число! {rloser}", parse_mode='html')
    
    if message.text.startswith("рейтинг продать"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       summ = float(msg.text.split()[2])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = int(rating[0])
       c = summ * 100000000
       c2 = '{:,}'.format(c)
       rating2 = '{:,}'.format(summ)
       if summ > 0:
        if int(rating) >= int(summ):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы понизили количество вашего рейтинга на {rating2}💎 за {c2}$! {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + c} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE users SET rating = {rating - summ} WHERE user_id = "{user_id}"')
          connect.commit()

        if int(rating) < int(summ):
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, у вас недостаточно рейтинга для его продажи! {rloser}", parse_mode='html')

       if summ <= 0:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя продать отрицательное число! {rloser}", parse_mode='html')

###########################################ПЕРЕВОДЫ###########################################
    if message.text.startswith("дать"):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name 
       rname =  msg.reply_to_message.from_user.last_name 
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply_user_id = msg.reply_to_message.from_user.id
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)



       perevod = int(msg.text.split()[1])
       perevod2 = '{:,}'.format(perevod)
       print(f"{name} | 💵Этот человек перевел:\n сумму: {perevod}\n Игроку {rname}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if not message.reply_to_message:
          await message.reply("❌ | Эта команда должна быть ответом на сообщение!")
          return
       
       if reply_user_id == user_id:
          await message.reply_to_message.reply(f'❌ | Вы не можете передать деньги сами себе! {rloser}', parse_mode='html')
          return

       if perevod > 0:
          if balance >= perevod:
             photopay = open('a/pay.jpg', 'rb')
             await message.reply_to_message.reply(f'[👤] Вы: {user_name}\n[💳] Действие передача денег.\n[💰] Сумма: {perevod2}$\n[💈] Получатель: {reply_user_name}.\n\n[❗️] {user_name}, с вашего баланса было списано {perevod2}$\n\n', photo=photopay, parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance - perevod} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
             connect.commit()    
   
          elif int(balance) <= int(perevod):
             await message.reply( f'{user_name},❌ | недостаточно средств! {rloser}', parse_mode='html')

       if perevod <= 0:
          await message.reply( f'{user_name},🤷‍♂️ | нельзя перевести отрицательное число! {rloser}', parse_mode='html')  

    if message.text.startswith("Дать"):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name 
       rname =  msg.reply_to_message.from_user.last_name 
       user_name = message.from_user.get_mention(as_html=True)
       reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
       reply_user_id = msg.reply_to_message.from_user.id
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)




       perevod = int(msg.text.split()[1])
       perevod2 = '{:,}'.format(perevod)
       print(f"{name} | 💵 Перевел:\n сумму: {perevod}\n Игроку {rname}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       if not message.reply_to_message:
          await message.reply("Эта команда должна быть ответом на сообщение!")
          return
       
       if reply_user_id == user_id:
          await message.reply_to_message.reply(f'❌ | Вы не можете передать деньги сами себе! {rloser}', parse_mode='html')
          return

       if perevod > 0:
          if balance >= perevod:  
             await message.reply_to_message.reply(f'[👤] Вы: {user_name}\n[💳] Действие передача денег.\n[💰] Сумма: {perevod2}$\n[💈] Получатель: {reply_user_name}.\n\n[❗️] {user_name}, с вашего баланса было списано {perevod2}$\n\n', parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance - perevod} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
             connect.commit()    
   
          elif int(balance) <= int(perevod):
             await message.reply( f'{user_name},❌ | недостаточно средств! {rloser}', parse_mode='html')

       if perevod <= 0:
          await message.reply( f'{user_name},❌ | нельзя перевести отрицательное число! {rloser}', parse_mode='html')  





       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])




       print(f"{name} перевел: {summ} игроку {rname}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])

       
       
       if reply_user_id == user_id:
          await message.reply_to_message.reply(f'Вы не можете передать деньги сами себе! {rloser}', parse_mode='html')
          return

       if summ > 0:
          if balance >= summ:  
             await bot.send_message(1887634547, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ | Действие: Передача денег\n💈 | Сумма: {perevod2}$\n👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
             await message.reply_to_message.reply(f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ | Действие: Передача денег\n💈 | Сумма: {perevod2}$\n👨 | Игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET balance = {balance2 + summ} WHERE user_id = "{reply_user_id}"')
             connect.commit()    
   
          elif int(balance) <= int(summ):
             await message.reply( f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')

       if summ <= 0:
          await message.reply( f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя перевести отрицательное число! {rloser}", parse_mode='html')  
 

###########################################ТОП###########################################
    if message.text.lower() in ["топ", "Топ"]:
       list = cursor.execute(f"SELECT * FROM users ORDER BY rating DESC").fetchmany(10)
       top_list = []
       user_id = message.from_user.id
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       num = 0

       

       for user in list:
           if user[7] >= 999999999999999999999999999999999999999999999999999999999999999999:
              c6 = 999999999999999999999999999999999999999999999999999999999999999999999999
           else:
              c6 = user[7]

           

           num += 1

           if num == 1:
              num2 = '1️⃣'
              num3 = ' <b>💎ТОП 1💎</b> |'
           if num == 2:
              num2 = '2️⃣'
              num3 = ''
           if num == 3:
              num2 = '3️⃣'
              num3 = ''
           if num == 4:
              num2 = '4️⃣'
              num3 = ''
           if num == 5:
              num2 = '5️⃣'
              num3 = ''
           if num == 6:
              num2 = '6️⃣'
              num3 = ''
           if num == 7:
              num2 = '7️⃣'
              num3 = ''
           if num == 8:
              num2 = '8️⃣'
              num3 = ''
           if num == 9:
              num2 = '9️⃣'
              num3 = ''
           if num == 10:
              num2 = '🔟'
              num3 = ''
           c = Decimal(c6)
           c2 = '{:,}'.format(c)

           if user[3] == 'Owner':
             stats = ' ✅<b>OWNER✅</b> '
           if user[3] == 'Admin':
             stats = ' 👮<b>АДМИН</b>👮 |'
           if user[3] == 'Helper_Admin':
             stats = ' 💻<b>HELPER</b>💻 |'
           if user[3] in ['Player', 'Vip', 'Premium', 'Platina', 'Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin']:
             stats = ''
           
           top_list.append(f"{num2}. {user[1]} |{stats}{num3} ID: <code>{user[0]}</code> |  — {c2}💎 ")
       top = "\n".join(top_list)
       photo = open('a/rat.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=photo, caption= f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот топ 10 игроков бота:\n" + top, parse_mode='html')
# Смена имени
    if message.text.startswith('Сменить ник'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       chat_id = message.chat.id
       user_id = message.from_user.id
       name = " ".join(message.text.split()[2:])

       if name in ['', ' ', '  ', '   ','    ', '     ', '      ', '       ','        ','         ','          ','           ','            ','              ','              ','               ','                ','            ']:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш ник не может быть пустым", parse_mode='html')
          return

       if len(name) <= 20:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно поменяли свое имя на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET user_name = \"{name}\" WHERE user_id = "{user_id}"')
          print(f"{user_name} сменил ник на {name}")
       else: 
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a> , ваш ник не может быть длинее 20 символов!", parse_mode='html')
    if message.text.startswith('сменить ник'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       chat_id = message.chat.id
       user_id = message.from_user.id
       name = " ".join(message.text.split()[2:])
       if len(name) <= 20:
          await bot.send_message(message.chat.id, f"🖊 | <a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно поменяли свое имя на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET user_name = \"{name}\" WHERE user_id = "{user_id}"')
          print(f"{user_name} сменил ник на {name}")
       else: 
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a> , ваш ник не может быть длинее 20 символов!", parse_mode='html')
    if message.text.lower() == 'Эфириум':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?", (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       await bot.send_message(message.chat.id,f"🟪 | <a href='tg://user?id={user_id}'>{user_name}</a>, количество эфириума: {ethereum}🟣")

    if message.text.lower() == 'эфириум курс':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       c = api.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']
       c2 = int(c)
       c3 = '{:,}'.format(c2)

       await bot.send_message(message.chat.id,f"🟪 | <a href='tg://user?id={user_id}'>{user_name}</a>, курс эфириума: {c3}🟣", parse_mode='html')
    if message.text.startswith('Эфириум'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       i = str(message.text.split()[1])
       d = int(message.text.split()[2])
       d2 = '{:,}'.format(d)
       c = api.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']
       c2 = int(c)
       c3 = '{:,}'.format(c2)

       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?", (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       summ = d * c2
       summ2 = '{:,}'.format(summ)

       if summ >= 999999999999999999999999999999999999999999999999999999999999999999999999:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>,  достигнул лимит, 99 клаунд")
          return

       if i == 'купить':
          if summ <= balance:
             if d > 0:
                await bot.send_message(message.chat.id, f" 💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {d2} эфириума 🟣 за {summ2}$", parse_mode='html')
                cursor.execute(f'UPDATE users SET ethereum = {ethereum + d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')
       if i == 'продать':
          if d <= ethereum:
             if d > 0:
                await bot.send_message(message.chat.id, f" 💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {d2} эфириума 🟣 за {summ2}$", parse_mode='html')
                cursor.execute(f'UPDATE users SET ethereum = {ethereum - d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')          
    
    
    if message.text.startswith('эфириум'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       i = str(message.text.split()[1])
       d = int(message.text.split()[2])
       d2 = '{:,}'.format(d)
       c = api.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']
       c2 = int(c)
       c3 = '{:,}'.format(c2)

       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?", (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       summ = d * c2
       summ2 = '{:,}'.format(summ)

       if i == 'купить':
          if summ <= balance:
             if d > 0:
                await bot.send_message(message.chat.id, f" 💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {d2} эфириума 🟣 за {summ2}$", parse_mode='html')
                cursor.execute(f'UPDATE users SET ethereum = {ethereum + d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')
       if i == 'продать':
          if d <= ethereum:
             if d > 0:
                await bot.send_message(message.chat.id, f" 💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {d2} эфириума 🟣 за {summ2}$", parse_mode='html')
                cursor.execute(f'UPDATE users SET ethereum = {ethereum - d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')          
#Ограбить банк
    if message.text.lower() == 'ограбить банк':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       x = random.randint(1,3)
       period = 86400 #86400 s 24h
       get = cursor.execute("SELECT stavka_bank FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       rx = random.randint(1000000,25000000)
       rx2 = '{:,}'.format(rx)
       if stavkatime > period:
          if int(x) in range(2,3):
             await bot.send_message(message.chat.id, f"🏦 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно ограбили банк на {rx2}$ ✅", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + rx} WHERE user_id ="{user_id}"')
             cursor.execute(f'UPDATE bot_time SET stavka_bank = {time.time()} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, вам не удалось ограбить банк", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ограбить банк можно раз в 24ч⏳", parse_mode='html')
# bonus 24h
    
    
    if message.text.lower() == 'ежедневный бонус':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       period = 86400 #86400 s = 24h
       get = cursor.execute("SELECT stavka_bonus FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       
       rx = random.randint(1000000,25000000)
       rx2 = '{:,}'.format(rx)

       if stavkatime > period:
          await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ежедневный бонус в сумме {rx2}$ 💵", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + rx}  WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE bot_time SET stavka_bonus = {time.time()} WHERE user_id = "{user_id}"')
          connect.commit()
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, получать ежедневный бонус можно раз в 24ч⏳", parse_mode='html') 


#####################################КУБИК##############################################################
    if message.text.startswith('Кубик'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         game = int(game[0])
         
         rx = random.randint(0,700)

         chil = int(message.text.split()[1])
         summ = int(message.text.split()[2])
         summ2 = '{:,}'.format(summ)
         
         
         
         summ_win = summ * 3
         summ_win2 = '{:,}'.format(summ_win)

         if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)

         period = 5
         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)
         if chil <= 6:
            if summ <= balance:
               if stavkatime > period:
                  if int(rx) in range(0,100):
                     if chil == 1:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲1 - {summ2}$\n🧾 | Выигрыш: 🎲1 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲1 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(101,200):
                     if chil == 2:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲2 - {summ2}$\n🧾 | Выигрыш: 🎲2 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲2 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(201,300):
                     if chil == 3:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲3 - {summ2}$\n🧾 | Выигрыш: 🎲3 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲3 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(401,500):
                     if chil == 4:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲4 - {summ2}$\n🧾 | Выигрыш: 🎲4 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲4 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(501,600):
                     if chil == 5:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲5 - {summ2}$\n🧾 | Выигрыш: 🎲5 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲5 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(601,700):
                     if chil == 6:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲6 - {summ2}$\n🧾 | Выигрыш: 🎲6 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲6 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
               else:
                  await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Играть можно раз в 5 секунд", parse_mode='html')
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средств!", parse_mode='html')
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, данного числа нету в кубике!", parse_mode='html')
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример Кубик 6 1000", parse_mode='html')

    if message.text.startswith('кубик'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         game = int(game[0])
         
         rx = random.randint(0,700)

         chil = int(message.text.split()[1])
         d1 = int(message.text.split()[2])
         d2 = str(message.text.split()[3])

         if d2 == 'к':
            summ = int(f'{d1}000')
         if d2 == 'кк':
            summ = int(f'{d1}000000')
         if d2 == 'ккк':
            summ = int(f'{d1}000000000')
         if d2 == 'кккк':
            summ = int(f'{d1}000000000000')
         if d2 == 'ккккк':
            summ = int(f'{d1}000000000000000')
         if d2 == 'кккккк':
            summ = int(f'{d1}000000000000000000')
         if d2 == 'ккккккк':
            summ = int(f'{d1}000000000000000000000')
         if d2 == 'кккккккк':
            summ = int(f'{d1}000000000000000000000000')
         if d2 == 'ккккккккк':
            summ = int(f'{d1}000000000000000000000000000')
         if d2 == 'кккккккккк':
            summ = int(f'{d1}000000000000000000000000000000')
         if d2 == 'ккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000')
         if d2 == 'кккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000')
         if d2 == 'ккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000')
         if d2 == 'кккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000')
         if d2 == 'ккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000')
         if d2 == 'кккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000')
         if d2 == 'ккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000')
         if d2 == 'кккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000000')
         if d2 == 'ккккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000')
         if d2 == 'кккккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000')
         if d2 == 'ккккккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000000')
         summ2 = '{:,}'.format(summ)
         
         
         if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)

         summ_win = summ * 3
         summ_win2 = '{:,}'.format(summ_win)

         period = 5
         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)
         if chil <= 6:
            if summ <= balance:
               if stavkatime > period:
                  if int(rx) in range(0,100):
                     if chil == 1:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲1 - {summ2}$\n🧾 | Выигрыш: 🎲1 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲1 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(101,200):
                     if chil == 2:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲2 - {summ2}$\n🧾 | Выигрыш: 🎲2 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲2 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(201,300):
                     if chil == 3:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲3 - {summ2}$\n🧾 | Выигрыш: 🎲3 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲3 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(401,500):
                     if chil == 4:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲4 - {summ2}$\n🧾 | Выигрыш: 🎲4 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲4 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(501,600):
                     if chil == 5:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲5 - {summ2}$\n🧾 | Выигрыш: 🎲5 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲5 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                  if int(rx) in range(601,700):
                     if chil == 6:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲6 - {summ2}$\n🧾 | Выигрыш: 🎲6 - {summ_win2}$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET balance = {balance + summ_win}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1}  WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
                     else:
                        await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Кубик\n🎟 | Ставка: 🎲{chil} - {summ2}$\n🧾 | Выигрыш: 🎲6 - 0$", parse_mode='html')
                        cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()}  WHERE user_id = "{user_id}"')
                        connect.commit()
               else:
                  await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Играть можно раз в 5 секунд", parse_mode='html')
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средств!", parse_mode='html')
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, данного числа нету в кубике!", parse_mode='html')
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример Кубик 6 1000", parse_mode='html')



#############################################################ЧЁТНОЕ \ НЕЧЁТНОЕ#########################################################



    if message.text.startswith('Нечётное'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         game = int(game[0])

         rx = random.randint(0,100)

         summ = int(message.text.split()[1])
         summ2 = '{:,}'.format(summ)

         if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)

         summ_win = summ * 2
         summ_win2 = '{:,}'.format(summ_win)

         period = 5
         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)

         if summ <= balance:
            if stavkatime > period:
               if int(rx) in range(0,65):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Нечётное - {summ2}$\n🧾 | Выигрыш: 🎲Чётное - 0$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
               if int(rx) in range(66,100):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Нечётное - {summ2}$\n🧾 | Выигрыш: 🎲Нечётное - {summ_win2}$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance + summ_win} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Играть можно раз в 5 секунд", parse_mode='html')
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Чётное 1000", parse_mode='html')

    if message.text.startswith('нечётное'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         game = int(game[0])

         rx = random.randint(0,100)

         d1 = int(message.text.split()[1])
         d2 = str(message.text.split()[2])

         if d2 == 'к':
            summ = int(f'{d1}000')
         if d2 == 'кк':
            summ = int(f'{d1}000000')
         if d2 == 'ккк':
            summ = int(f'{d1}000000000')
         if d2 == 'кккк':
            summ = int(f'{d1}000000000000')
         if d2 == 'ккккк':
            summ = int(f'{d1}000000000000000')
         if d2 == 'кккккк':
            summ = int(f'{d1}000000000000000000')
         if d2 == 'ккккккк':
            summ = int(f'{d1}000000000000000000000')
         if d2 == 'кккккккк':
            summ = int(f'{d1}000000000000000000000000')
         if d2 == 'ккккккккк':
            summ = int(f'{d1}000000000000000000000000000')
         if d2 == 'кккккккккк':
            summ = int(f'{d1}000000000000000000000000000000')
         if d2 == 'ккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000')
         if d2 == 'кккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000')
         if d2 == 'ккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000')
         if d2 == 'кккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000')
         if d2 == 'ккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000')
         if d2 == 'кккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000')
         if d2 == 'ккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000')
         if d2 == 'кккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000000')
         if d2 == 'ккккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000')
         if d2 == 'кккккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000')
         if d2 == 'ккккккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000000')
         summ2 = '{:,}'.format(summ)
         if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)
         summ_win = summ * 2
         summ_win2 = '{:,}'.format(summ_win)

         period = 5
         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)

         if summ <= balance:
            if stavkatime > period:
               if int(rx) in range(0,65):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Нечётное - {summ2}$\n🧾 | Выигрыш: 🎲Чётное - 0$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
               if int(rx) in range(66,100):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Нечётное - {summ2}$\n🧾 | Выигрыш: 🎲Нечётное - {summ_win2}$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance + summ_win} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Играть можно раз в 5 секунд", parse_mode='html')
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Чётное 1000", parse_mode='html')

    if message.text.startswith('Чётное'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         game = int(game[0])

         rx = random.randint(0,100)

         summ = int(message.text.split()[1])
         summ2 = '{:,}'.format(summ)

         summ_win = summ * 2
         summ_win2 = '{:,}'.format(summ_win)

         period = 5
         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)

         if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)

         if summ <= balance:
            if stavkatime > period:
               if int(rx) in range(0,65):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Чётное - {summ2}$\n🧾 | Выигрыш: 🎲Нечётное - 0$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
               if int(rx) in range(66,100):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Чётное - {summ2}$\n🧾 | Выигрыш: 🎲Чётное - {summ_win2}$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance + summ_win} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Играть можно раз в 5 секунд", parse_mode='html')
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Чётное 1000", parse_mode='html')

    if message.text.startswith('чётное'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         game = int(game[0])

         rx = random.randint(0,100)

         d1 = int(message.text.split()[1])
         d2 = str(message.text.split()[2])

         if d2 == 'к':
            summ = int(f'{d1}000')
         if d2 == 'кк':
            summ = int(f'{d1}000000')
         if d2 == 'ккк':
            summ = int(f'{d1}000000000')
         if d2 == 'кккк':
            summ = int(f'{d1}000000000000')
         if d2 == 'ккккк':
            summ = int(f'{d1}000000000000000')
         if d2 == 'кккккк':
            summ = int(f'{d1}000000000000000000')
         if d2 == 'ккккккк':
            summ = int(f'{d1}000000000000000000000')
         if d2 == 'кккккккк':
            summ = int(f'{d1}000000000000000000000000')
         if d2 == 'ккккккккк':
            summ = int(f'{d1}000000000000000000000000000')
         if d2 == 'кккккккккк':
            summ = int(f'{d1}000000000000000000000000000000')
         if d2 == 'ккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000')
         if d2 == 'кккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000')
         if d2 == 'ккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000')
         if d2 == 'кккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000')
         if d2 == 'ккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000')
         if d2 == 'кккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000')
         if d2 == 'ккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000')
         if d2 == 'кккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000000')
         if d2 == 'ккккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000')
         if d2 == 'кккккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000')
         if d2 == 'ккккккккккккккккккккк':
            summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000000')
         summ2 = '{:,}'.format(summ)

         if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
            balance = 999999999999999999999999999999999999999999999999999999999999999999
            cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)

         summ_win = summ * 2
         summ_win2 = '{:,}'.format(summ_win)

         period = 5
         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)

         if summ <= balance:
            if stavkatime > period:
               if int(rx) in range(0,65):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Чётное - {summ2}$\n🧾 | Выигрыш: 🎲Нечётное - 0$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
               if int(rx) in range(66,100):
                  await bot.send_message(message.chat.id, f"🤵‍♂ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🎲 | Игра: Чётное \ нечётное\n🎟 | Ставка: 🎲Чётное - {summ2}$\n🧾 | Выигрыш: 🎲Чётное - {summ_win2}$", parse_mode='html')
                  cursor.execute(f'UPDATE users SET balance = {balance + summ_win} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Играть можно раз в 5 секунд", parse_mode='html')
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Чётное 1000", parse_mode='html')



##################################################### WHEEL \ dice ##########################################################

    if message.text.startswith('dice'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = user_status[0]

       game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       game = int(game[0])

       black_red = str(message.text.split()[1])
       d1 = int(message.text.split()[2])
       d2 = str(message.text.split()[3])

       if d2 == 'к':
          summ = int(f'{d1}000')
       if d2 == 'кк':
          summ = int(f'{d1}000000')
       if d2 == 'ккк':
          summ = int(f'{d1}000000000')
       if d2 == 'кккк':
          summ = int(f'{d1}000000000000')
       if d2 == 'ккккк':
          summ = int(f'{d1}000000000000000')
       if d2 == 'кккккк':
          summ = int(f'{d1}000000000000000000')
       if d2 == 'ккккккк':
          summ = int(f'{d1}000000000000000000000')
       if d2 == 'кккккккк':
          summ = int(f'{d1}000000000000000000000000')
       if d2 == 'ккккккккк':
          summ = int(f'{d1}000000000000000000000000000')
       if d2 == 'кккккккккк':
          summ = int(f'{d1}000000000000000000000000000000')
       if d2 == 'ккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000')
       if d2 == 'кккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000')
       if d2 == 'ккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000')
       if d2 == 'кккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000')
       if d2 == 'ккккккккккккккккккккк':
          summ = int(f'{d1}000000000000000000000000000000000000000000000000000000000000000')

       summ2 = "{:,}".format(summ)

       if balance >= 999999999999999999999999999999999999999999999999999999999999999999:
          balance = 999999999999999999999999999999999999999999999999999999999999999999
          cursor.execute(f'UPDATE users SET balance = {999999999999999999999999999999999999999999999999999999999999999999}  WHERE user_id = ?', (user_id,))
          connect.commit()
          balance2 = '{:,}'.format(balance)

       if user_status in ['Bog','Vlaselin']:
          period = 2
       else:
          period = 5
       
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       if balance < summ:
          
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')
          return
       if stavkatime > period:
          if black_red in ['ч',"черный","Ч", "Черный"]:
             rx = random.randint(0,1000)

             if rx in range(0,850):
                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Проигрыш: 0$ [🔴]   
               """, parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()
             if rx in range(851, 999):
                summ3 = summ * 2
                summ4 = '{:,}'.format(summ3)

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [⚫️]                       
               """, parse_mode='html')  
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.exencute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()   
             if rx == 1000:
                summ3 = summ * 8
                summ4 = '{:,}'.format(summ3)

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [🟢]                        
               """, parse_mode='html')   
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit() 
          if black_red in ['к',"красный","К", "Красный"]:
             rx = random.randint(0,1000)

             if rx in range(0,850):
                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Проигрыш: 0$ [⚫️]   
               """, parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()
             if rx in range(851, 999):
                summ3 = summ * 2
                summ4 = '{:,}'.format(summ3)

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [🔴]                       
               """, parse_mode='html')  
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.exencute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()   
             if rx == 1000:
                summ3 = summ * 8
                summ4 = '{:,}'.format(summ3)

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [🟢]                        
               """, parse_mode='html')   
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()  
    if message.text.startswith('Dice'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = user_status[0]

       game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       game = int(game[0])

       black_red = str(message.text.split()[1])
       summ = int(message.text.split()[2])

       summ2 = "{:,}".format(summ)

       if user_status in ['Bog','Vlaselin']:
          period = 2
       else:
          period = 5

       if balance < summ:
          
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')
          return
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if black_red in ['ч',"черный","Ч", "Черный"]:
             rx = random.randint(0,1000)

             if rx in range(0,850):
                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Проигрыш: 0$ [🔴]   
               """, parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()
             if rx in range(851, 999):
                summ3 = summ * 2
                summ4 = '{:,}'.format(summ3)

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [⚫️]                       
               """, parse_mode='html')  
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.exencute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()   
             if rx == 1000:
                summ3 = summ * 8
                summ4 = '{:,}'.format(summ3)

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [🟢]                        
               """, parse_mode='html')   
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit() 
          if black_red in ['к',"красный","К", "Красный"]:
             rx = random.randint(0,1000)

             if rx in range(0,850):
                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Проигрыш: 0$ [⚫️]   
               """, parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()
             if rx in range(851, 999):
                summ3 = summ * 2
                summ4 = '{:,}'.format(summ3)

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [🔴]                       
               """, parse_mode='html')  
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.exencute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()   
             if rx == 1000:
                summ3 = summ * 8
                summ4 = '{:,}'.format(summ3)

                await bot.send_message(message.chat.id, f"""
🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🎱 | Игра: Wheel
🎟 | Ставка: {summ2}$
🧾 | Выигрыш: {summ4}$ [🟢]                        
               """, parse_mode='html')   
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()            

    if message.text.lower() in ['wheel','dice']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за игру Wheel 🎱

✒️ | Пример: dice [ч\к] [сумма]

⚙️ | ч - черный ⚫️
⚙️ | к - красный 🔴

⚖️ | Шансы: Черный ⚫️ - 50%, Красный 🔴 - 50%, Зерро 🟢 - 0.1%   
         """, parse_mode='html')

















############################################СИСТЕМА КРАФТА#############################
    if message.text.lower() == 'крафт':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
   
       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       menu_craft = InlineKeyboardMarkup(row_width=2)
       resurs1 = InlineKeyboardButton(text='🟥 Кирка Zerro ⛏', callback_data='resurs1')
       resurs2 = InlineKeyboardButton(text='🟥 Грабли Zerro 🌾', callback_data='resurs2')
       resurs3 = InlineKeyboardButton(text='🟨 Кирка Cherick ⛏', callback_data='resurs3')
       resurs4 = InlineKeyboardButton(text='🟨 Грабли Cherick 🌾', callback_data='resurs4')
       menu_craft.add(resurs1, resurs2, resurs3, resurs4)

       if basement == 1:
          basement_name = 'Standard'
          basement_period = 30
       
       if basement == 2:
          basement_name = 'Plus++'
          basement_period = 15
      
       if basement == 3:
          basement_name = 'Euro Plus++'
          basement_period = 4
       

       if basement > 0:
          await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, добро пожаловать в подвал🕋

👤 | Владелец: {user_name}
🕋 | Подвал: {basement_name}
⏳ | Ограничение по времени: {basement_period} секунд

↘️Выберите предмет какой хотите скрафтить       
""",reply_markup=menu_craft, parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! У вас нету подвала", parse_mode='html')
    if message.text.lower() == 'система крафта':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные о системе крафта⚒

▶️ | ⬜️ - обычные
▶️ | 🟩 - редкие
▶️ | 🟦 - сверх-редкие
▶️ | 🟪 - эпические
▶️ | 🟥 - мифические
▶️ | 🟨 - легендарные


📦 | Предметы:
⛏ | [🟥] [1] Кирка Zerro 
🌾 | [🟥] [2] Грабли Zerro 
⛏ | [🟨] [3] Кирка Cherick 
🌾 | [🟨] [4] Грабли Cherick 

⚖️ | Шансы крафта предметов:
⛏ | [🟥] [1] Кирка Zerro - 35%
🌾 | [🟥] [2] Грабли Zerro - 35%
⛏ | [🟨] [3] Кирка Cherick - 10%
🌾 | [🟨] [4] Грабли Cherick - 10%

⚒ | Чтобы начать крафтить введите команду \"Крафтить\"
ℹ️ | Крафтить можно только при наличии подвала
ℹ️ | У каждого подвала есть свои ограничение по времени на крафт""", parse_mode='html')
########################################ДОМА########################################
    if message.text.lower() == 'продать подвал':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
    
       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       if basement == 1:
          summ = 5000000
          summ2 = '{:,}'.format(summ)
          basement2 = 'Standard'

       if basement == 2:
          summ = 10000000
          summ2 = '{:,}'.format(summ)
          basement2 = 'Plus++'

       if basement == 3:
          summ = 20000000
          summ2 = '{:,}'.format(summ)
          basement2 = 'Euro plus++'

       if basement > 0:
          await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🕋 |Действие: Продажа подвала\n🕋 | Подвал: {basement2}\n💈 |Продано за: {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас уже есть подвал", parse_mode='html')
          return

    if message.text.startswith('купить подвал'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
    
       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       member = int(message.text.split()[2])
       
       if member == 1:
          summ = 5000000
          summ2 = '{:,}'.format(summ)
          basement2 = 'Standard'

       if member == 2:
          summ = 10000000
          summ2 = '{:,}'.format(summ)
          basement2 = 'Plus++'

       if member == 3:
          summ = 20000000
          summ2 = '{:,}'.format(summ)
          basement2 = 'Euro plus++'

       if member > 0:
          if member < 4:
             if house > 0:
                if basement == 0:
                   if balance >= summ:
                      await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🕋 |Действие: Покупка подвала\n🕋 | Подвал: {basement2}\n💈 |Стоимость: {summ2}$", parse_mode='html')
                      cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                      cursor.execute(f'UPDATE house SET basement = {member} WHERE user_id = {user_id}')
                      connect.commit()
                   else:
                      await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средтсв!", parse_mode='html')
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас уже есть подвал", parse_mode='html')
             else:
                 await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету дома! Подвал можно покупать только имея дом", parse_mode='html')
          else:
              await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! Нету такого номера подвала", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! Нету такого номера подвала", parse_mode='html')
    if message.text.startswith('Купить подвал'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
    
       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       member = int(message.text.split()[2])
       
       if member == 1:
          summ = 5000000
          summ2 = '{:,}'.format(summ)
          basement2 = 'Standard'

       if member == 2:
          summ = 10000000
          summ2 = '{:,}'.format(summ)
          basement2 = 'Plus++'

       if member == 3:
          summ = 20000000
          summ2 = '{:,}'.format(summ)
          basement2 = 'Euro plus++'

       if member > 0:
          if member < 4:
             if house > 0:
                if basement == 0:
                   if balance >= summ:
                      await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🕋 |Действие: Покупка подвала\n🕋 | Подвал: {basement2}\n💈 |Стоимость: {summ2}$", parse_mode='html')
                      cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                      cursor.execute(f'UPDATE house SET basement = {member} WHERE user_id = {user_id}')
                      connect.commit()
                   else:
                      await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средтсв!", parse_mode='html')
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас уже есть подвал", parse_mode='html')
             else:
                 await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету дома! Подвал можно покупать только имея дом", parse_mode='html')
          else:
              await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! Нету такого номера подвала", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! Нету такого номера подвала", parse_mode='html')



    if message.text.lower() in ['подвал', 'подвалы']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот список доступных подвалов 🕋

🕋 | [1] Standard - 5.000.000$
🕋 | [2] Plus++ - 10.000.000$
🕋 | [3] Euro Plus++ - 20.000.000$

🛒 Чтобы купить подвал себе в дом, введите команду \"Купить подвал [номер]\" """, parse_mode='html')
    
    
    
    
    if message.text.lower() == 'мой дом':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       if house == 1:
          house2 = 'Коробка'
       
       if house == 2:
          house2 = 'Сарай'

       if house == 3:
          house2 = 'Маленький домик'

       if house == 4:
          house2 = 'Квартира'

       if house == 5:
          house2 = 'Огромный дом'

       if house == 6:
          house2 = 'Коттедж'

       if house == 7:
          house2 = 'Вилла'

       if house == 8:
          house2 = 'Загородный дом'

       if basement == 1:
          basement2 = '\n🕋 | Подвал: Standard'


       if basement == 2:
          basement2 = '\n🕋 | Подвал: Plus++'
   

       if basement == 3:
          basement2 = '\n🕋 | Подвал: Euro Plus++'
      
       if basement == 0:
          basement2 = '\n🕋 | Подвал не имеиться'
         
       if house > 0:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш дом🏡\n\n👤 | Владелец: {user_name}\n🏠 | Дом: {house2}{basement2}\n\n🛒 Чтобы купить подвал , введите команду \"Подвалы\"\nℹ️ Чтобы продать подвал введите команду \"Продать подвал\"\nℹ️ Чтобы продать дом введите команду  \"Продать дом\"", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нету дома, что бы купить дом введите команду \"Дома\"", parse_mode='html')
    
    
    if message.text.lower() == 'продать дом':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       basement = cursor.execute("SELECT basement from house where user_id = ?", (message.from_user.id,)).fetchone()
       basement = int(basement[0])

       if basement == 1:
          basement2 = '\n🕋 | Подвал: Standard'
          summ_basement = 5000000

       if basement == 2:
          basement2 = '\n🕋 | Подвал: Plus++'
          summ_basement = 10000000

       if basement == 3:
          basement2 = '\n🕋 | Подвал: Euro Plus++'
          summ_basement = 20000000
       else:
          basement2 = ''
          summ_basement = 0

       if house == 1:
          house2 = 'Коробка'
          summ = 500000 + summ_basement
          summ2 = '{:,}'.format(summ)
          member_house = 1


       if house == 2:
          house2 = 'Сарай'
          summ = 3000000 + summ_basement
          summ2 = '{:,}'.format(summ)
          member_house = 2
      
       if house == 3:
          house2 = 'Маленький домик'
          summ = 5000000 + summ_basement
          summ2 = '{:,}'.format(summ)
          member_house = 3
      
       if house == 4:
          house2 = 'Квартира'
          summ = 7000000 + summ_basement
          summ2 = '{:,}'.format(summ)
          member_house = 4
      
       if house == 5:
          house2 = 'Огромный дом'
          summ = 10000000 + summ_basement
          summ2 = '{:,}'.format(summ)
          member_house = 5

       if house == 6:
          house2 = 'Коттедж'
          summ = 50000000 + summ_basement
          summ2 = '{:,}'.format(summ)
          member_house = 6

       if house == 7:
          house2 = 'Вилла'
          summ = 100000000 + summ_basement
          summ2 = '{:,}'.format(summ)
          member_house = 7

       if house == 8:
          house2 = 'Загородный дом'
          summ = 5000000000 + summ_basement
          summ2 = '{:,}'.format(summ)
          member_house = 8
      
          await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏡 |Действие: Продажа дома\n🏠 | Дом: {house2}{basement2}\n💈 |Продано за: {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ + summ_basement} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE house SET basement = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас и так нету дома! Что бы купить дом введите команду \"Дома\"", parse_mode='html')
          return

    if message.text.startswith('купить дом'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       member = int(message.text.split()[2])

       if member == 1:
          house2 = 'Коробка'
          summ = 500000
          summ2 = '{:,}'.format(summ)
          member_house = 1


       if member == 2:
          house2 = 'Сарай'
          summ = 3000000
          summ2 = '{:,}'.format(summ)
          member_house = 2
      
       if member == 3:
          house2 = 'Маленький домик'
          summ = 5000000
          summ2 = '{:,}'.format(summ)
          member_house = 3
      
       if member == 4:
          house2 = 'Квартира'
          summ = 7000000
          summ2 = '{:,}'.format(summ)
          member_house = 4
      
       if member == 5:
          house2 = 'Огромный дом'
          summ = 10000000
          summ2 = '{:,}'.format(summ)
          member_house = 5

       if member == 6:
          house2 = 'Коттедж'
          summ = 50000000
          summ2 = '{:,}'.format(summ)
          member_house = 6

       if member == 7:
          house2 = 'Вилла'
          summ = 100000000
          summ2 = '{:,}'.format(summ)
          member_house = 7

       if member == 8:
          house2 = 'Загородный дом'
          summ = 5000000000
          summ2 = '{:,}'.format(summ)
          member_house = 8

       if house == 0:
          if member > 0:
             if member < 9:
                if summ <= balance:
                   await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏡 |Действие: Покупка дома\n🏠 | Дом: {house2}\n💈 |Стоимость: {summ2}$", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE house SET house = {member_house} WHERE user_id = {user_id}')
                   connect.commit()
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средств!", parse_mode='html')               
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Нету такого номера дома!", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Нету такого номера дома!", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас уже есть дом, что бы продать дом введите команду \"Продать дом\"", parse_mode='html')



    if message.text.startswith('Купить дом'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       member = int(message.text.split()[2])

       if member == 1:
          house2 = 'Коробка'
          summ = 500000
          summ2 = '{:,}'.format(summ)
          member_house = 1


       if member == 2:
          house2 = 'Сарай'
          summ = 3000000
          summ2 = '{:,}'.format(summ)
          member_house = 2
      
       if member == 3:
          house2 = 'Маленький домик'
          summ = 5000000
          summ2 = '{:,}'.format(summ)
          member_house = 3
      
       if member == 4:
          house2 = 'Квартира'
          summ = 7000000
          summ2 = '{:,}'.format(summ)
          member_house = 4
      
       if member == 5:
          house2 = 'Огромный дом'
          summ = 10000000
          summ2 = '{:,}'.format(summ)
          member_house = 5

       if member == 6:
          house2 = 'Коттедж'
          summ = 50000000
          summ2 = '{:,}'.format(summ)
          member_house = 6

       if member == 7:
          house2 = 'Вилла'
          summ = 100000000
          summ2 = '{:,}'.format(summ)
          member_house = 7

       if member == 8:
          house2 = 'Загородный дом'
          summ = 5000000000
          summ2 = '{:,}'.format(summ)
          member_house = 8     
      
          if member > 0:
             if member < 9:
                if summ <= balance:
                   await bot.send_message(message.chat.id, f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏡 |Действие: Покупка дома\n🏠 | Дом: {house2}\n💈 |Стоимость: {summ2}$", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE house SET house = {member_house} WHERE user_id = {user_id}')
                   connect.commit()
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средств!", parse_mode='html')               
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Нету такого номера дома!", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Нету такого номера дома!", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас уже есть дом, что бы продать дом введите команду \"Продать дом\"", parse_mode='html')





    if message.text.lower() == 'дома':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, доступные дома:
🏠 1. Коробка - 500.000$
🏠 2. Сарай - 3.000.000$
🏠 3. Маленький домик - 5.000.000$
🏠 4. Квартира - 7.000.000$
🏠 5. Огромный дом - 10.000.000$
🏠 6. Коттедж - 50.000.000$
🏠 7. Вилла - 100.000.000$
🏠 8. Загородный дом - 5.000.000.000$
🏠9. Марс - 100.000.000.000.000.000

🛒 Для покупки дома введите "Купить дом [номер]"
       
       """, parse_mode='html')  




#########################################МАШИНЫ#######################################################
    if message.text.lower() == 'моя машина':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       hp = cursor.execute("SELECT hp from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       benz = cursor.execute("SELECT benz from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])
       if benz < 0:
             benz2 = 0
       else:
          benz2 = benz
       if cars == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       
       if hp in range(76,100):
          hp2 = 'Хорошое 🟩'

       if hp in range(51,75):
          hp2 = 'Среднее 🟧 '
         
       if hp in range(26,50):
          hp2 = 'Плохое 🟥'

       if hp in range(2,25):
          hp2 = 'Ужасное 🛑'

       if hp < 2:
          hp2 = 'Требуется ремонт ⛔️'

       else:
          if hp == 100:
             hp2 = 'Хорошое 🟩'
          if hp == 76:
             hp2 = 'Хорошое 🟩'
          if hp == 75:
             hp2 = 'Среднее 🟧'
          if hp == 51:
             hp2 = 'Среднее 🟧'
          if hp == 50:
             hp2 = 'Плохое 🟥'
          if hp == 26:
             hp2 = 'Плохое 🟥'
          if hp == 25:
             hp2 = 'Ужасное 🛑'
          if hp == 2:
             hp2 = 'Ужасное 🛑'

       if cars > 0:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш автомобиль🚘\n\n👤 | Владелец: {user_name}\n🚗 | Автомобиль: {cars_name}\n🚨 | Состояние: {hp2}\n⛽️ | Бензин: {benz2}%\n💰 | Стоимость: {cars_summ2}$\n\nℹ️ Чтобы продать машину введите команду \"Машину продать\"", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! У вас и так нету машины", parse_mode='html')
     


    if message.text.lower() == 'машину продать':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       if cars == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ)


       if cars > 0:
          await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Продажа машины\n🚘 | Машина: {cars_name}\n💈 |Проданно за: {cars_summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! У вас и так нету машины", parse_mode='html')
          return
      
    if message.text.startswith('Купить машину'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       member = int(message.text.split()[2])
       
       if member == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ)


       if member > 0:
          if member < 19:
             if cars == 0:
                if balance >= cars_summ:
                   await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Покупка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: {cars_summ2}$", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - cars_summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET cars = {member} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                   connect.commit()
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! У вас уже есть машина", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера машины", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера машины", parse_mode='html')

    if message.text.startswith('купить машину'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       member = int(message.text.split()[2])
       
       if member == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ)


       if member > 0:
          if member < 19:
             if cars == 0:
                if balance >= cars_summ:
                   await bot.send_message(message.chat.id, f"👨 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🚗 |Действие: Покупка машины\n🚘 | Машина: {cars_name}\n💈 |Стоимость: {cars_summ2}$", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - cars_summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET cars = {member} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                   connect.commit()
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! У вас уже есть машина", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера машины", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера машины", parse_mode='html')










    if message.text.lower() == 'машины':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, доступные машины:
🚗 1. Самокат - 10.000.000$
🚗 2. Велосипед - 15.000.000$
🚗 3. Гироскутер - 30.000.000$
🚗 4. Сегвей - 50.000.000$
🚗 5. Мопед - 90.000.000$
🚗 6. Мотоцикл - 100.000.000$
🚗 7. ВАЗ 2109 - 250.000.000$
🚗 8. Квадроцикл - 400.000.000$
🚗 9. Багги - 600.000.000$
🚗 10. Вездеход - 900.000.000$
🚗 11. Лада Xray - 1.400.000.000$
🚗 12. Audi Q7 - 2.500.000.000$
🚗 13. BMW X6 - 6.000.000.000$
🚗 14. Toyota FT-HS - 8.000.000.000$
🚗 15. BMW Z4 M - 10.000.000.000$
🚗 16. Subaru WRX STI - 40.000.000.000$
🚗 17. Lamborghini Veneno - 100.000.000.000$
🚗 18. Tesla Roadster - 300.000.000.000$

🛒 Для покупки машины введите "Купить машину [номер]"    
       
""", parse_mode='html')




    if message.text.lower() == 'самолёты':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, доступные машины:
✈️ 1. Гедра - 10.000$
✈️2. Xwer- 15.000$
✈️ 3. karbe - 30.000$
✈️4. color - 5.000.000.$
✈️ 5. Vig - 90.000.000$
✈️ 6. Zetr - 100.000.000$
✈️ 7. Nuix - 250.000.000$
✈️ 8. Merta - 400.000.000$
✈️ 9. Igherc - 600.000.000$
✈️ 10. Kipo - 900.000.000$
✈️ 11. Xray - 1.400.000.000$
✈️ 12. Q7 - 2.500.000.000$
✈️ 13. X6 - 6.000.000.000$
✈️ 14. FT-HS - 8.000.000.000$
✈️15. Z4 M - 10.000.000.000.000$
✈️ 16. WRX STI - 40.000.000.000.000$
✈️17. Veneno - 100.000.000.000.000.000$
✈️ 18. Roadster - 300.000.000.000.000.000.000$

🛒 Для покупки машины введите "Купить машину [номер]"    
       
""", parse_mode='html')





############################################################ШАХТА############################################################
    if message.text.lower() == 'шахта':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id,f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за шахту ⛏

⛏ | Руды на шахте:
      🪨 | Камень -  30%
      ⛓ | Железо - 28%
      🪙 | Серебро - 10%
      🎇 | Бронза - 6%
      ⚜️ | Золото - 3%

ℹ️ | Чтобы продать какую руду , воспользуйтесь командой \"Продать [Руда] [Количество]\"
ℹ️ | Чтобы копать руду воспользуйтесь командой \"Копать руду\"       
       """, parse_mode='html')
    if message.text.startswith('продать'):
      try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         # iron, silver, bronza, gold
         iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
         iron = int(iron[0])
         
         metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
         metall = int(metall[0])

         silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
         silver = int(silver[0])

         bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
         bronza = int(bronza[0])

         gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
         gold = int(gold[0])

         rud = str(message.text.split()[1])

         c = int(message.text.split()[2])

         summ = c * 25000
         summ2 = '{:,}'.format(summ)
         if rud == 'камень':
            if c <= iron:
               summ = c * 25000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} камень 🪨 за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET iron = {iron - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
         if rud == 'железо':
            if c <= metall:
               summ = c * 45000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} железо ⛓ за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET metall = {metall - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')

         if rud == 'серебро':
            if c <= silver:
               summ = c * 125000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} серебро 🪙 за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET silver = {silver - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
         if rud == 'бронзу':
            if c <= bronza:
               summ = c * 200000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} бронзы 🎇 за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET bronza = {bronza - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')

         if rud == 'золото':
            if c <= gold:
               summ = c * 500000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} золото ⚜️ за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET bronza = {bronza - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
      except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Продать [камень, железо, серебро, бронзу, золото, лён, хлопок] 1", parse_mode='html')

    if message.text.startswith('Продать'):
      try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         # iron, silver, bronza, gold
         iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
         iron = int(iron[0])
         
         metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
         metall = int(metall[0])

         silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
         silver = int(silver[0])

         bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
         bronza = int(bronza[0])

         gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
         gold = int(gold[0])

         rud = str(message.text.split()[1])

         c = int(message.text.split()[2])

         summ = c * 25000
         summ2 = '{:,}'.format(summ)
         if rud == 'камень':
            if c <= iron:
               summ = c * 25000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} камень 🪨 за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET iron = {iron - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
         if rud == 'железо':
            if c <= metall:
               summ = c * 45000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} железо ⛓ за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET metall = {metall - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')

         if rud == 'серебро':
            if c <= silver:
               summ = c * 125000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} серебро 🪙 за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET silver = {silver - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
         if rud == 'бронзу':
            if c <= bronza:
               summ = c * 200000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} бронзы 🎇 за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET bronza = {bronza - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')

         if rud == 'золото':
            if c <= gold:
               summ = c * 500000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} золото ⚜️ за {summ2}$", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET gold = {gold - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
      except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Продать [камень, железо, серебро, бронзу, золото, лён, хлопок] 1", parse_mode='html')

    if message.text.lower() == 'копать руду':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       pick = cursor.execute("SELECT pick from mine where user_id = ?", (message.from_user.id,)).fetchone()
       pick = pick[0]

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       rx = random.randint(0,100)

      # iron, silver, bronza, gold
       iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
       iron = int(iron[0])
       
       metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
       metall = int(metall[0])

       silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
       silver = int(silver[0])

       bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])

       gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       
       rx_iron = random.randint(15,20)
       rx_metall = random.randint(10,15)
       rx_silver = random.randint(5,10)
       rx_bronza = random.randint(0,5)
       
       if pick == 'Cherick':
          period = 3
       else:
          period = 5
       get = cursor.execute("SELECT time_pick FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)

       if pick == 'Cherick':
          if stavkatime > period:
             if int(rx) in range(0,40):
                await bot.send_message(message.chat.id, f"🪨 | Вы успешно выкопали {rx_iron * 2} камня", parse_mode='html')
                cursor.execute(f'UPDATE mine SET iron = {iron + rx_iron * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(41,70):
                await bot.send_message(message.chat.id, f"⛓ | Вы успешно выкопали {rx_metall * 2} железа", parse_mode='html')
                cursor.execute(f'UPDATE mine SET metall = {metall + rx_metall * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(71,85):
                await bot.send_message(message.chat.id, f"🪙 | Вы успешно выкопали {rx_silver * 2} серебра", parse_mode='html')
                cursor.execute(f'UPDATE mine SET silver = {silver + rx_silver * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(86,95):
                await bot.send_message(message.chat.id, f"🎇 | Вы успешно выкопали {rx_bronza * 2} бронзы", parse_mode='html')
                cursor.execute(f'UPDATE mine SET bronza = {bronza + rx_bronza * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(96,100):
                await bot.send_message(message.chat.id, f"⚜️ | Вы успешно выкопали 2 золото", parse_mode='html')
                cursor.execute(f'UPDATE mine SET gold = {gold + 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать руду можно раз в {period} секунд!", parse_mode='html')
             return

       if pick == 'Zerro':
          if stavkatime > period:
             if int(rx) in range(0,40):
                await bot.send_message(message.chat.id, f"🪨 | Вы успешно выкопали {rx_iron * 2} камня", parse_mode='html')
                cursor.execute(f'UPDATE mine SET iron = {iron + rx_iron * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(41,70):
                await bot.send_message(message.chat.id, f"⛓ | Вы успешно выкопали {rx_metall * 2} железа", parse_mode='html')
                cursor.execute(f'UPDATE mine SET metall = {metall + rx_metall * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(71,85):
                await bot.send_message(message.chat.id, f"🪙 | Вы успешно выкопали {rx_silver * 2} серебра", parse_mode='html')
                cursor.execute(f'UPDATE mine SET silver = {silver + rx_silver * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(86,95):
                await bot.send_message(message.chat.id, f"🎇 | Вы успешно выкопали {rx_bronza * 2} бронзы", parse_mode='html')
                cursor.execute(f'UPDATE mine SET bronza = {bronza + rx_bronza * 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(96,100):
                await bot.send_message(message.chat.id, f"⚜️ | Вы успешно выкопали 2 золото", parse_mode='html')
                cursor.execute(f'UPDATE mine SET gold = {gold + 2} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать руду можно раз в {period} секунд!", parse_mode='html')
             return

       if pick == 'on':
          if stavkatime > period:
             if int(rx) in range(0,40):
                await bot.send_message(message.chat.id, f"🪨 | Вы успешно выкопали {rx_iron} камня", parse_mode='html')
                cursor.execute(f'UPDATE mine SET iron = {iron + rx_iron} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(41,70):
                await bot.send_message(message.chat.id, f"⛓ | Вы успешно выкопали {rx_metall} железа", parse_mode='html')
                cursor.execute(f'UPDATE mine SET metall = {metall + rx_metall} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(71,85):
                await bot.send_message(message.chat.id, f"🪙 | Вы успешно выкопали {rx_silver} серебра", parse_mode='html')
                cursor.execute(f'UPDATE mine SET silver = {silver + rx_silver} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(86,95):
                await bot.send_message(message.chat.id, f"🎇 | Вы успешно выкопали {rx_bronza} бронзы", parse_mode='html')
                cursor.execute(f'UPDATE mine SET bronza = {bronza + rx_bronza} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(96,100):
                await bot.send_message(message.chat.id, f"⚜️ | Вы успешно выкопали 1 золото", parse_mode='html')
                cursor.execute(f'UPDATE mine SET gold = {gold + 1} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать руду можно раз в {period} секунд!", parse_mode='html')
             return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас нету кирки, что бы купить кирку введите команду \"Купить кирку\"", parse_mode='html')
          return
          




    if message.text.lower() == 'продать кирку':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       pick = cursor.execute("SELECT pick from mine where user_id = ?", (message.from_user.id,)).fetchone()
       pick = pick[0]

       if pick == 'Cherick':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! вы не можете продать кирку Cherick", parse_mode='html')

       if pick == 'Zerro':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! вы не можете продать кирку Zerro", parse_mode='html')

       if pick == 'off':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас и так нету кирки, что бы купить кирку введите команду \"Купить кирку\"", parse_mode='html')

       if pick == 'on':
          await bot.send_message(message.chat.id, f"⛏ | Вы продали кирку за 5.000$ ", parse_mode='html')
          cursor.execute(f'UPDATE mine SET pick = "off" WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE users SET balance = {balance + 5000} WHERE user_id = "{user_id}"')
          connect.commit()
    if message.text.lower() == 'купить кирку':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       pick = cursor.execute("SELECT pick from mine where user_id = ?", (message.from_user.id,)).fetchone()
       pick = pick[0]


       if pick == 'Cherick':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть кирка Cherick", parse_mode='html')

       if pick == 'Zerro':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть кирка Zerro", parse_mode='html')


       if pick == 'on':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть кирка, что бы продать кирку введите команду \"Продать кирку\"", parse_mode='html')

       if pick == 'off':
          if balance >= 5000:
             await bot.send_message(message.chat.id, f"⛏ | Вы купили кирку за 5.000$ ", parse_mode='html')
             cursor.execute(f'UPDATE mine SET pick = "on" WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance - 5000} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')



#################################################ФЕРМА#################################################
    if message.text.lower() in ['ферма', 'фермы']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за ферму 🌾

🌾 | Доступный урожай:
      🍃 | Лён =  5-10
      🌿 | Хлопок = 5-10

ℹ️ | Чтобы собрать какой то урожай, воспользуйтесь командой \"Собрать [лён\ хлопок]
ℹ️ | Чтобы продать какой-то урожай, воспользуйтесь командой \" Продать [лён\хлопок] [Количество]       
       """, parse_mode='html')
    if message.text.startswith('продать хлопок'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       cotton = cursor.execute("SELECT cotton from farm where user_id = ?", (message.from_user.id,)).fetchone()
       cotton = int(cotton[0])
       
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       c = int(message.text.split()[2])
       c2 = '{:,}'.format(c)
       
       summ = c * 150000
       summ2 = '{:,}'.format(summ)

       if c <= cotton:
          await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c2} хлопка 🌿 за {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE farm SET cotton = {cotton - с} WHERE user_id = "{user_id}"')
          connect.commit()
       else:
          await bot.send_message(message.chat.id,f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько ресурсов!", parse_mode='html')

    if message.text.startswith('Продать хлопок'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       cotton = cursor.execute("SELECT cotton from farm where user_id = ?", (message.from_user.id,)).fetchone()
       cotton = int(cotton[0])
       
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       c = int(message.text.split()[2])
       c2 = '{:,}'.format(c)
       
       summ = c * 150000
       summ2 = '{:,}'.format(summ)

       if c <= cotton:
          await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c2} хлопка 🌿 за {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE farm SET cotton = {cotton - с} WHERE user_id = "{user_id}"')
          connect.commit()
       else:
          await bot.send_message(message.chat.id,f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас недостаточно ресурсов!", parse_mode='html')


    if message.text.startswith('продать лён'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       linen = cursor.execute("SELECT linen from farm where user_id = ?", (message.from_user.id,)).fetchone()
       linen = int(linen[0])
       
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       c = int(message.text.split()[2])
       c2 = '{:,}'.format(c)
       
       summ = c * 150000
       summ2 = '{:,}'.format(summ)

       if c <= linen:
          await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c2} лён 🍃 за {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE farm SET linen = {linen - с} WHERE user_id = "{user_id}"')
          connect.commit()
       else:
          await bot.send_message(message.chat.id,f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас недостаточно ресурсов!", parse_mode='html')

    if message.text.startswith('Продать лён'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       linen = cursor.execute("SELECT linen from farm where user_id = ?", (message.from_user.id,)).fetchone()
       linen = int(linen[0])
       
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       colic = int(message.text.split()[2])
       c2 = '{:,}'.format(colic)
       
       summ = c * 150000
       summ2 = '{:,}'.format(summ)

       if colic <= linen:
          await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c2} лён 🍃 за {summ2}$", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE farm SET linen = {linen - colic} WHERE user_id = "{user_id}"')
          connect.commit()
       else:
          await bot.send_message(message.chat.id,f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько ресурсов!", parse_mode='html')
    
    
    if message.text.startswith('cобрать'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         rake = cursor.execute("SELECT rake from farm where user_id = ?", (message.from_user.id,)).fetchone()
         rake = rake[0]

         linen = cursor.execute("SELECT linen from farm where user_id = ?", (message.from_user.id,)).fetchone()
         linen = int(linen[0])

         cotton = cursor.execute("SELECT cotton from farm where user_id = ?", (message.from_user.id,)).fetchone()
         cotton = int(cotton[0])

         rud = str(message.text.split()[1])

         rx_linen = random.randint(5,10)

      
         if rake == 'Cherick':
             period = 2
         else:
            period = 5
         get = cursor.execute("SELECT time_rake FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)
         
         if stavkatime > period:
            if rake == 'Cherick':
               if rud == 'лён':
                  await bot.send_message(message.chat.id, f"🍃 | Вы успешно собрали {rx_linen * 2} лёна", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET linen = {linen + rx_linen * 2} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
               if rud == 'хлопок':
                  await bot.send_message(message.chat.id, f"🌿 | Вы успешно собрали {rx_linen} хлопка", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET cotton = {cotton + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
            if rake == 'Zerro':
               if rud == 'лён':
                  await bot.send_message(message.chat.id, f"🍃 | Вы успешно собрали {rx_linen * 2} лёна", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET linen = {linen + rx_linen * 2} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
               if rud == 'хлопок':
                  await bot.send_message(message.chat.id, f"🌿 | Вы успешно собрали {rx_linen} хлопка", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET cotton = {cotton + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
            if rake == 'on':
               if rud == 'лён':
                  await bot.send_message(message.chat.id, f"🍃 | Вы успешно собрали {rx_linen} лёна", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET linen = {linen + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
               if rud == 'хлопок':
                  await bot.send_message(message.chat.id, f"🌿 | Вы успешно собрали {rx_linen} хлопка", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET cotton = {cotton + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас нету граблей, что бы купить грабли введите команду \"Купить грабли\"", parse_mode='html')
               return
         
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать урожай можно раз в {period} секунд!", parse_mode='html')     
            return      
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Собрать [лён, хлопок]", parse_mode='html')

    if message.text.startswith('Собрать'):
       try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         rake = cursor.execute("SELECT rake from farm where user_id = ?", (message.from_user.id,)).fetchone()
         rake = rake[0]

         linen = cursor.execute("SELECT linen from farm where user_id = ?", (message.from_user.id,)).fetchone()
         linen = int(linen[0])

         cotton = cursor.execute("SELECT cotton from farm where user_id = ?", (message.from_user.id,)).fetchone()
         cotton = int(cotton[0])

         rud = str(message.text.split()[1])

         rx_linen = random.randint(5,10)

      

         if rake == 'Cherick':
             period = 2
         else:
            period = 5
         get = cursor.execute("SELECT time_rake FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = int(get[0])
         stavkatime = time.time() - float(last_stavka)
         
         if stavkatime > period:
            if rake == 'Cherick':
               if rud == 'лён':
                  await bot.send_message(message.chat.id, f"🍃 | Вы успешно собрали {rx_linen * 2} лёна", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET linen = {linen + rx_linen * 2} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
               if rud == 'хлопок':
                  await bot.send_message(message.chat.id, f"🌿 | Вы успешно собрали {rx_linen} хлопка", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET cotton = {cotton + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
            if rake == 'Zerro':
               if rud == 'лён':
                  await bot.send_message(message.chat.id, f"🍃 | Вы успешно собрали {rx_linen * 2} лёна", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET linen = {linen + rx_linen * 2} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
               if rud == 'хлопок':
                  await bot.send_message(message.chat.id, f"🌿 | Вы успешно собрали {rx_linen} хлопка", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET cotton = {cotton + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
            if rake == 'on':
               if rud == 'лён':
                  await bot.send_message(message.chat.id, f"🍃 | Вы успешно собрали {rx_linen} лёна", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET linen = {linen + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
               if rud == 'хлопок':
                  await bot.send_message(message.chat.id, f"🌿 | Вы успешно собрали {rx_linen} хлопка", parse_mode='html')
                  cursor.execute(f'UPDATE farm SET cotton = {cotton + rx_linen} WHERE user_id = "{user_id}"')
                  cursor.execute(f'UPDATE bot_time SET time_rake = {time.time()} WHERE user_id = "{user_id}"')
                  connect.commit()
                  return
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас нету граблей, что бы купить грабли введите команду \"Купить грабли\"", parse_mode='html')
               return
         
         else:
            await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать урожай можно раз в {period} секунд!", parse_mode='html')   
            return        
       except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: Собрать [лён, хлопок]", parse_mode='html')
          
    if message.text.lower() == 'продать грабли':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       rake = cursor.execute("SELECT rake from farm where user_id = ?", (message.from_user.id,)).fetchone()
       rake = rake[0]

       if rake == 'off':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас и так нету граблей, чтобы купить грабли введите команду \"Купить грабли\"", parse_mode='html')

       if rake == 'Zerro':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Но вы не можете продать грабли Zerro", parse_mode='html')

       if rake == 'Cherick':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Но вы не можете продать грабли Cherick", parse_mode='html')




       if rake == 'on':
         await bot.send_message(message.chat.id, f"⛏ | Вы продали грабли за 5.000$ ", parse_mode='html')
         cursor.execute(f'UPDATE farm SET rake = "off" WHERE user_id = "{user_id}"')
         cursor.execute(f'UPDATE users SET balance = {balance + 5000} WHERE user_id = "{user_id}"')
         connect.commit()

    if message.text.lower() == 'купить грабли':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       rake = cursor.execute("SELECT rake from farm where user_id = ?", (message.from_user.id,)).fetchone()
       rake = rake[0]

       if rake == 'on':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть грабли, что бы продать грабли введите команду \"Продать грабли\"", parse_mode='html')

       if rake == 'Zerro':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть грабли", parse_mode='html')
 
       if rake == 'Cherick':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть грабли", parse_mode='html')


       if rake == 'off':
          if balance >= 50000:
             await bot.send_message(message.chat.id, f"⛏ | Вы купили грабли за 50.000$ ", parse_mode='html')
             cursor.execute(f'UPDATE farm SET rake = "on" WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance - 5000} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')



###############################################ИНВЕНТАРЬ####################################################################

    if message.text.lower() == 'инвентарь':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       loser = ['😐', '😕','😟','😔','😓']
       rloser = random.choice(loser)

       farm = 0
       men = 0
       ob = 0

       linen = cursor.execute("SELECT linen from farm where user_id = ?", (message.from_user.id,)).fetchone()
       linen = int(linen[0])
       linen_f = '{:,}'.format(linen)

       cotton = cursor.execute("SELECT cotton from farm where user_id = ?", (message.from_user.id,)).fetchone()
       cotton = int(cotton[0])
       cotton_f = '{:,}'.format(cotton)

       iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
       iron = int(iron[0])
       iron_f = '{:,}'.format(iron)

       metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
       metall = int(metall[0])
       metall_f = '{:,}'.format(metall)

       silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
       silver = int(silver[0])
       silver_f = '{:,}'.format(silver)

       bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])
       bronza_f = '{:,}'.format(bronza)

       gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       gold_f = '{:,}'.format(gold)

       if iron > 0:
          iron2 = f'    🪨 | Камня: {iron_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          iron2 = ''

       if metall > 0:
          metall2 = f'    ⛓ | Железа: {metall_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          metall2 = ''
      
       if silver > 0:
          silver2 = f'    🪙 | Серебра: {silver_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          silver2 = ''

       if bronza > 0:
          bronza2 = f'    🎇 | Бронзы: {bronza_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          bronza2 = ''

       if gold > 0:
          gold2 = f'    ⚜️ | Золота: {gold_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          gold2 = ''

       if men > 0:
          men_2 = '\n⛏ | Шахта\n'
       else:
          men_2 = ''
       
       if linen > 0:
          linen2 = f'      🍃 | Лён: {linen_f} шт\n'
          farm = farm + 1
          ob = ob + 1
       else:
          linen2 = ''

       if cotton > 0:
          cotton2 = f'      🌿 | Хлопок: {cotton_f} шт\n'
          farm = farm + 1
          ob = ob + 1
       else:
          cotton2 = ''

       if farm > 0:
          farm2 = '🌾 | Ферма\n'
       else:
          farm2 = ''

       if ob == 0:
          ob2 = f'Вещи отсутствуют {rloser}'
       else:
          ob2 = ''
      
       await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот ваш инвентарь:\n{ob2}{men_2}{iron2}{metall2}{silver2}{bronza2}{gold2}\n{farm2}{linen2}{cotton2}", parse_mode='html')

    if message.text.startswith('гонка'):

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       loser = ['😐', '😕','😟','😔','😓']
       rloser = random.choice(loser)

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_id = ?", (message.from_user.id,)).fetchone()
       cars = cars[0]

       hp = cursor.execute("SELECT hp from cars where user_id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       benz = cursor.execute("SELECT benz from cars where user_id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])

       summ = int(message.text.split()[1]).replace(".", "")
       summ2 = '{0:,}'.format(summ).replace(".", "")

       if cars == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ)


       rx = random.randint(0,1000)
       rx2 = random.randint(1,25)
       summ3 = summ * 2
       summ4 = '{:,}'.format(summ3).replace(".", "")

       period = 5
       getе = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(getе[0])
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if summ <= balance:
             if cars > 0:
                if hp > 0:
                   if benz > 0:
                      if int(rx) in range(0,600):
                         await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏎 | Игра: Гонки\n🚘 | Машина: {cars_name}\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: 0$", parse_mode='html')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()
                      if int(rx) in range(601, 1000):
                         await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏎 | Игра: Гонки\n🚘 | Машина: {cars_name}\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {summ4}$", parse_mode='html')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance + summ * 2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()
                   else:
                      await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас закончился бензин в автомобиле", parse_mode='html')
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас поломался автомобиль , вы не можете участвовать в гонках", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Какие гонки без автомобиля? Купите автомобиль", parse_mode='html') 
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств", parse_mode='html') 
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! играй можно раз в {period} секунд", parse_mode='html') 


    if message.text.startswith('Гонка'):

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       loser = ['😐', '😕','😟','😔','😓']
       rloser = random.choice(loser)

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_id = ?", (message.from_user.id,)).fetchone()
       cars = cars[0]

       hp = cursor.execute("SELECT hp from cars where user_id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       benz = cursor.execute("SELECT benz from cars where user_id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])

       summ = int(message.text.split()[1]).replace(".", "")
       summ2 = '{0:,}'.format(summ)

       if cars == 1:
          cars_name = 'Самокат'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 2:
          cars_name = 'Велосипед'
          cars_summ = 15000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 3:
          cars_name = 'Гироскутер'
          cars_summ = 30000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 4:
          cars_name = 'Сегвей'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 5:
          cars_name = 'Мопед'
          cars_summ = 90000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 6:
          cars_name = 'Мотоцикл'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 7:
          cars_name = 'ВАЗ 2109'
          cars_summ = 250000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 8:
          cars_name = 'Квадроцикл'
          cars_summ = 400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 9:
          cars_name = 'Багги'
          cars_summ = 600000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 10:
          cars_name = 'Вездеход'
          cars_summ = 900000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 11:
          cars_name = 'Лада Xray'
          cars_summ = 1400000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 12:
          cars_name = 'Audi Q7'
          cars_summ = 2500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 13:
          cars_name = 'BMW X6'
          cars_summ = 6000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 14:
          cars_name = 'Toyota FT-HS'
          cars_summ = 8000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 15:
          cars_name = 'BMW Z4 M'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 16:
          cars_name = 'Subaru WRX STI'
          cars_summ = 40000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 17:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 18:
          cars_name = 'Tesla Roadster'
          cars_summ = 300000000000
          cars_summ2 = '{:,}'.format(cars_summ)


       rx = random.randint(0,1000)
       rx2 = random.randint(1,25)
       summ3 = summ * 2
       summ4 = '{:,}'.format(summ3).replace(".", "")

       period = 5
       getе = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(getе[0])
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if summ <= balance:
             if cars > 0:
                if hp > 0:
                   if benz > 0:
                      if int(rx) in range(0,600):
                         await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏎 | Игра: Гонки\n🚘 | Машина: {cars_name}\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: 0$", parse_mode='html')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()
                      if int(rx) in range(601, 1000):
                         await bot.send_message(message.chat.id, f"🤵‍♂️ | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n🏎 | Игра: Гонки\n🚘 | Машина: {cars_name}\n🎟 | Ставка: {summ2}$\n🧾 | Выигрыш: {summ4}$", parse_mode='html')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance + summ * 2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()
                   else:
                      await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас закончился бензин в автомобиле", parse_mode='html')
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас поломался автомобиль , вы не можете участвовать в гонках", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Какие гонки без автомобиля? Купите автомобиль", parse_mode='html') 
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств", parse_mode='html') 
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! играй можно раз в {period} секунд", parse_mode='html') 
        



######################################################Привилегии \ Донат меню##############################################
    if message.text.lower() == 'донат':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?", (message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])
       donate_coins2 = '{:,}'.format(donate_coins)

       donate_menu = InlineKeyboardMarkup(row_width=2)
       privilegii = InlineKeyboardButton(text='💵 Валюты', callback_data='privilegii')
       case = InlineKeyboardButton(text='🎁 Купить кейсы', callback_data='case')
       adms = InlineKeyboardButton(text='⛔️ Права администратора', callback_data='adms')
       donate_menu.add(privilegii, adms, case)
       await bot.send_message(message.chat.id, f'''<a href='tg://user?id={user_id}'>{user_name}</a>, донат был отправлен вам в лс''' , parse_mode='html')
       await bot.send_message(message.from_user.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, наш магазин:

🏆 Привилегии:
1️⃣ Вип | 15₽ 11₽
2️⃣ Легенда | 35₽ 26₽
3️⃣ Спонсор | 65₽ 48₽
4️⃣ Властелин | 80₽ 60₽
5️⃣ Администратор | 140₽ 105₽
6️⃣ Разработчик | 230₽ 172₽

📦 Кейсы:
7⃣ Временно недоступно

💸 Валюта:
8⃣ Валюта: 1 D-Coin - 2.000.000.000$

💹 Курс: 1 D-Coin - 1₽ 0.75₽

🔝Покупка: Напишите создателю {cash_owner_username}

💰Ваш баланс: (0,) D-Coin
⚡Пополнить баланс: Пополнить

🎃 Удачного хэллоуина   
       """, reply_markup=donate_menu, parse_mode='html')
    if message.text.lower() == 'властелин':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ВЛАСТЕЛИН 🤎

1️⃣ | Бонус-кит ВЛАСТЕЛИН
2️⃣ | Префикс ВЛАСТЕЛИН
3️⃣ | 1.000.000.000.000.000.000$
4️⃣ | 100.000.000 Рейтинга
5️⃣ | Money-case 5 шт.
6️⃣ | Donate-case 1 шт.
7️⃣ | Способность менять себе префикс
8️⃣ | Способность менять игрокам префикс
9️⃣ | Ограничение на время в играх становиться 2 секунды

🛒 Чтобы купить привилегию , войдите в Donate-menu с помощю команды \"Донат\"
       """, parse_mode='html') 


    if message.text.lower() == 'бог':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию БОГ 🤍

1️⃣ | Бонус-кит БОГ
2️⃣ | Префикс БОГ
3️⃣ | 500.000.000.000.000.000$
4️⃣ | 10.000.000 Рейтинга
5️⃣ | Money-case 5 шт.
6️⃣ | Donate-case 1 шт.
7️⃣ | Способность менять себе префикс
8️⃣ | Способность менять игрокам префикс
9️⃣ | Ограничение на время в играх становиться 2 секунды

🛒 Чтобы купить привилегию , войдите в Donate-menu с помощю команды \"Донат\"
       """, parse_mode='html') 


    if message.text.lower() == 'владелец':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ВЛАДЕЛЕЦ 🖤

1️⃣ | Бонус-кит ВЛАДЕЛЕЦ
2️⃣ | Префикс ВЛАДЕЛЕЦ
3️⃣ | 100.000.000.000.000.000$
4️⃣ | 1.000.000 Рейтинга
5️⃣ | Money-case 5 шт.
6️⃣ | Donate-case 1 шт.
7️⃣ | Способность менять себе префикс
8️⃣ | Способность менять игрокам префикс

🛒 Чтобы купить привилегию , войдите в Donate-menu с помощю команды \"Донат\"
       """, parse_mode='html') 


    if message.text.lower() == 'основатель':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ОСНОВАТЕЛЬ 💜

1️⃣ | Бонус-кит ОСНОВАТЕЛЬ
2️⃣ | Префикс ОСНОВАТЕЛЬ
3️⃣ | 20.000.000.000.000.000$
4️⃣ | 100.000 Рейтинга
5️⃣ | Money-case 5 шт.
6️⃣ | Donate-case 1 шт.
7️⃣ | Способность менять себе префикс

🛒 Чтобы купить привилегию , войдите в Donate-menu с помощю команды \"Донат\"
       """, parse_mode='html') 


    if message.text.lower() == 'спонсор':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию СПОНСОР 💙

1️⃣ | Бонус-кит СПОНСОР
2️⃣ | Префикс СПОНСОР
3️⃣ | 5.000.000.000.000.000$
4️⃣ | 10.000 Рейтинга
5️⃣ | Money-case 5 шт.
6️⃣ | Способность менять себе префикс

🛒 Чтобы купить привилегию , войдите в Donate-menu с помощю команды \"Донат\"   
       """, parse_mode='html') 


    if message.text.lower() == 'хелпер':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ХЕЛПЕР 💚

1️⃣ | Бонус-кит ХЕЛПЕР
2️⃣ | Префикс ХЕЛПЕР
3️⃣ | 700.000.000.000.000$
4️⃣ | 1.300 Рейтинга
5️⃣ | Money-case 3 шт.
6️⃣ | Способность менять себе префикс

🛒 Чтобы купить привилегию , войдите в Donate-menu с помощю команды \"Донат\"   
       """, parse_mode='html') 


    if message.text.lower() == 'платина':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ПЛАТИНА 💛

1️⃣ | Бонус-кит ПЛАТИНА
2️⃣ | Префикс ПЛАТИНА
3️⃣ | 400.000.000.000.000$
4️⃣ | 800 Рейтинга
5️⃣ | Money-case 1 шт.

🛒 Чтобы купить привилегию , войдите в Donate-menu с помощю команды \"Донат\"     
       """, parse_mode='html') 


    if message.text.lower() == '/premium':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, 
<b>BARAKA PREMIUM</b> 🤴
• X2 Добыча ресурсов на шахте
• X2 exp при выполнении ежедневных заданий 
• Статус <b>BARAKA Premium</b> 🤴 в топе игроков бота

• Префикс PREMIUM
• Выдать лимит до 100млн
📆 <b>1 месяц: 150 руб.</b>,    
       """, parse_mode='html')  
    if message.text.lower() == 'вип':

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id  

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ВИП ❤️

1️⃣ | Бонус-кит ВИП
2️⃣ | Префикс ВИП
3️⃣ | 10.000.000.000$
4️⃣ | 100 Рейтинга

🛒 Чтобы купить привилегию , войдите в Donate-menu с помощю команды \"Донат\"       
       """, parse_mode='html')  





###################################### КИТ-БОНУСЫ ##################################################
    if message.text.lower() == 'получить кит-бонус':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       user_status = cursor.execute('SELECT user_status from users where user_id = ?', (message.from_user.id,)).fetchone()
       user_status = user_status[0]

       balance = cursor.execute('SELECT balance from users where user_id = ?', (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       rating = cursor.execute('SELECT rating from users where user_id = ?', (message.from_user.id,)).fetchone()
       rating = int(rating[0])

       ethereum = cursor.execute('SELECT ethereum from users where user_id = ?', (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       metall = cursor.execute('SELECT metall from mine where user_id = ?', (message.from_user.id,)).fetchone()
       metall = int(metall[0])

       silver = cursor.execute('SELECT silver from mine where user_id = ?', (message.from_user.id,)).fetchone()
       silver = int(silver[0])

       bronza = cursor.execute('SELECT bronza from mine where user_id = ?', (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])

       gold = cursor.execute('SELECT gold from mine where user_id = ?', (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       period = 43200 #43200 s = 12h
       get = cursor.execute("SELECT time_kit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно получили свой кит-бонус", parse_mode='html')
          time.sleep(0.5)
          if user_status == 'Player':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⛓ 99 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 5 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 100🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 1000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 5} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET metall = {metall + 99} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 100} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Vip':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 5,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 57 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 15 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 200🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 5000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 15} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 57} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 200} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Premium':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 10,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 101 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 25 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 250🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 25} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 101} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 250} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Platina':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 15,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 125 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 300🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 15000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 125} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 300} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Helper':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 25,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🎇 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 100 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 500🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 25000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 100} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET bronza = {bronza + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Sponsor':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 150,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🎇 150 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 150000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET bronza = {bronza + 150} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Osnovatel':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 400,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 15 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 400000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 15} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Vladelec':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 700,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 700000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Bog':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 10.000,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 150 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 150} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return

          if user_status == 'Vlaselin':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 100.000,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 100000000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, администрация бота не может получать кит-бонус", parse_mode='html') 
             return   
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, получать кит-бонус можно раз в 10ч", parse_mode='html')


    if message.text.lower() == 'получить кит бонус':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       user_status = cursor.execute('SELECT user_status from users where user_id = ?', (message.from_user.id,)).fetchone()
       user_status = user_status[0]

       balance = cursor.execute('SELECT balance from users where user_id = ?', (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       rating = cursor.execute('SELECT rating from users where user_id = ?', (message.from_user.id,)).fetchone()
       rating = int(rating[0])

       ethereum = cursor.execute('SELECT ethereum from users where user_id = ?', (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       metall = cursor.execute('SELECT metall from mine where user_id = ?', (message.from_user.id,)).fetchone()
       metall = int(metall[0])

       silver = cursor.execute('SELECT silver from mine where user_id = ?', (message.from_user.id,)).fetchone()
       silver = int(silver[0])

       bronza = cursor.execute('SELECT bronza from mine where user_id = ?', (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])

       gold = cursor.execute('SELECT gold from mine where user_id = ?', (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       period = 40200 #43200 s = 10h
       get = cursor.execute("SELECT time_kit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно получили свой кит-бонус", parse_mode='html')
          time.sleep(0.5)
          if user_status == 'Player':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⛓ 99 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 5 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 100🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 1000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 5} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET metall = {metall + 99} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 100} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Vip':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 5,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 57 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 15 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 200🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 5000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 15} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 57} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 200} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Premium':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 10,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 101 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 25 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 250🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 25} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 101} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 250} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Platina':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 15,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🪙 125 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 300🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 15000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET silver = {silver + 125} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 300} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Helper':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 25,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🎇 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 100 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 500🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 25000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 100} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET bronza = {bronza + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Sponsor':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 150,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 🎇 150 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 150000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET bronza = {bronza + 150} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Osnovatel':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 400,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 15 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 400000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 15} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Vladelec':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 700,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 50 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 700000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 50} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          if user_status == 'Bog':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 10.000,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 150 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 150} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return

          if user_status == 'Vlaselin':
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 100.000,000,000,000,000$", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ⚜️ 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 💎 500 шт.", parse_mode='html')
             time.sleep(0.2)
             await bot.send_message(message.chat.id, f"🎁 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили 1.000🟪", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + 100000000000000000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET rating = {rating + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET gold = {gold + 500} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE users SET ethereum = {ethereum + 1000} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE bot_time SET time_kit = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, администрация бота не может получать кит-бонус", parse_mode='html') 
             return   
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, получать кит-бонус можно раз в 12ч", parse_mode='html')


    if message.text.lower() in ['кит-бонусы', 'кит бонусы', 'кит бонус', 'кит-бонус']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные о кит-бонусах 🎁

🎀 | Игрок:
      💰 | 1,000,000,000,000$
      ⛓ | 99 шт.
      💎 | 5 шт.
      🟣 | 100🟪

❤️ | Вип:
      💰 | 5,000,000,000,000$
      🪙 | 57 шт.
      💎 | 15 шт.
      🟣 | 200🟪

🧡 | Премиум:
      💰 | 10,000,000,000,000$
      🪙 | 101 шт.
      💎 |  25 шт.
      🟣 | 250🟪

💛 | Платина:
      💰 | 15,000,000,000,000$
      🪙 | 125 шт.
      💎 |  50 шт.
      🟣 | 300🟪

💚 | Хелпер:
      💰 | 25,000,000,000,000$
      🎇 | 50 шт.
      💎 |  100 шт.
      🟣 | 500🟪

💙 | Спонсор:
      💰 | 150,000,000,000,000$
      🎇 | 150 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

💜 | Основатель:
      💰 | 400,000,000,000,000$
      ⚜️ | 15 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

🖤 | ВЛАДЕЛЕЦ:
      💰 | 700,000,000,000,000$
      ⚜️ | 50 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

🤍 | БОГ:
      💰 | 10.000,000,000,000,000$
      ⚜️ | 150 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

🤎 | ВЛАСТЕЛИН:
      💰 | 100.000,000,000,000,000$
      ⚜️ | 500 шт.
      💎 |  500 шт.
      🟣 | 1.000🟪

ℹ️ Чтобы получить кит-бонус введите команду \"Получить кит-бонус\" 
ℹ️ Кит-бонус получить можно раз в 12ч      
       """, parse_mode='html')

####################################### ТОП Мажоров#######################################

    if message.text.lower() in ['топ багочей', 'топ мажоров', 'топ б']:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       list = cursor.execute(f"SELECT * FROM users ORDER BY balance DESC").fetchmany(15)
       top_list = []

       num = 0

       for user in list:
          if int(user[4]) < 0:
             balance3 = 0
          if int(user[4]) in range(1000, 999999):
             balance1 = user[4] / 1000
             balance2 = int(balance1)
             balance3 = f'{balance2} тыс'

          if int(user[4]) in range(1000000, 999999999):
             balance1 = user[4] / 1000000
             balance2 = int(balance1)
             balance3 = f'{balance2} млн'
 
          if int(user[4]) in range(1000000000, 999999999999):
             balance1 = user[4] / 1000000000
             balance2 = int(balance1)
             balance3 = f'{balance2} млрд'
 
          if int(user[4]) in range(1000000000000, 999999999999999):
             balance1 = user[4] / 1000000000000
             balance2 = int(balance1)
             balance3 = f'{balance2} трлн'

          if int(user[4]) in range(1000000000000000, 999999999999999999):
             balance1 = user[4] / 1000000000000000
             balance2 = int(balance1)
             balance3 = f'{balance2} квдр'

          if int(user[4]) in range(1000000000000000000, 999999999999999999999):
             balance1 = user[4] / 1000000000000000000
             balance2 = int(balance1)
             balance3 = f'{balance2} квнт'

          if int(user[4]) in range(1000000000000000000000, 999999999999999999999999):
             balance1 = user[4] / 1000000000000000000000
             balance2 = int(balance1)
             balance3 = f'{balance2} скст' 
          if int(user[4]) in range(1000000000000000000000000, 999999999999999999999999):
             balance1 = user[4] / 1000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} трикс'
          if int(user[4]) >= 1000000000000000000000000000:
             balance1 = user[4] / 1000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} твинкс'  
          if int(user[4]) in range(1000000000000000000000000000000, 999999999999999999999999999999999):
             balance1 = user[4] / 1000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} септ'
          if int(user[4]) in range(1000000000000000000000000000000000, 999999999999999999999999999999999999):
             balance1 = user[4] / 1000000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} октл'
          if int(user[4]) in range(1000000000000000000000000000000000000, 999999999999999999999999999999999999999):
             balance1 = user[4] / 1000000000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} нонл'
          if int(user[4]) in range(1000000000000000000000000000000000000000, 999999999999999999999999999999999999999999):
             balance1 = user[4] / 1000000000000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} декал'
          if int(user[4]) in range(1000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999):
             balance1 = user[4] / 1000000000000000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} эндк'
          if int(user[4]) in range(1000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999):
             balance1 = user[4] / 1000000000000000000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} доктл'
          if int(user[4]) in range(1000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999) :
             balance1 = user[4] / 1000000000000000000000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} гугл'
          if int(user[4]) in range(1000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999) :
             balance1 = user[4] / 1000000000000000000000000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} кинд'
          if int(user[4]) in range(1000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999999) :
             balance1 = user[4] / 1000000000000000000000000000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} трипт'
          if int(user[4]) in range(1000000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999999999) :
             balance1 = user[4] / 1000000000000000000000000000000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} срист'
          if int(user[4]) in range(1000000000000000000000000000000000000000000000000000000000000, 999999999999999999999999999999999999999999999999999999999999999):
             balance1 = user[4] / 1000000000000000000000000000000000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} манит'
          if int(user[4]) >= 1000000000000000000000000000000000000000000000000000000000000000:
             balance1 = user[4] / 100000000000000000000000000000000000000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} гвинт'
          if int(user[4]) >= 100000000000000000000000000000000000000000000000000000000000000000000000000:
             balance1 = user[4] / 100000000000000000000000000000000000000000000000000000000000000000000000000
             balance2 = round(balance1)
             balance3 = f'{balance2} клаунд'

            
          num += 1

          if num == 1:
             num2 = '1️⃣'
             num3 = ' <b>💰ТОП 1💰</b> |'
          if num == 2:
             num2 = '2️⃣'
             num3 = ''
          if num == 3:
             num2 = '3️⃣'
             num3 = ''
          if num == 4:
             num2 = '4️⃣'
             num3 = ''
          if num == 5:
             num2 = '5️⃣'
             num3 = ''
          if num == 6:
             num2 = '6️⃣'
             num3 = ''
          if num == 7:
             num2 = '7️⃣'
             num3 = ''
          if num == 8:
             num2 = '8️⃣'
             num3 = ''
          if num == 9:
             num2 = '9️⃣'
             num3 = ''
          if num == 10:
             num2 = '🔟'
             num3 = ''
          if num == 11:
             num2 = '1⃣1⃣'
             num3 = ''
          if num == 12:
             num2 = '1⃣2⃣'
             num3 = ''
          if num == 13:
             num2 = '1⃣3⃣'
             num3 = ''
          if num == 14:
             num2 = '1⃣4⃣'
             num3 = ''
          if num == 15:
             num2 = '1⃣5⃣'
             num3 = ''
          
          if user[3] == 'Owner':
             stats = ' 🤠<b>OWNER</b>🤠 '
          if user[3] == 'Admin':
             stats = ' 👮<b>АДМИН</b>👮 |'
          if user[3] == 'Helper_Admin':
             stats = ' ⚠️<b>HELPER АДМИН</b>⚠️ |'
          if user[3] in ['Player', 'Vip', 'Premium', 'Platina', 'Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin']:
             stats = ''


          top_list.append(f"{num2} {user[1]} |{stats}{num3} 🔎 ID: <code>{user[0]}</code> | ${balance3} ")

       top = "\n".join(top_list)
       await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот топ 15 богачей в боте:\n" + top, parse_mode='html')

############################## СИСТЕМА СООБЩЕНИЙ ####################################

    if message.text.lower() in ['система с', "система сообщений", "с сообщений", "с сообщение", "сс", "с с"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за систему сообщений 💬

ℹ️ | Пример команды: /m [ID] [сообщение]

⚠️ | Система сообщений была разработана для связи с игроками, у которых SMS SPAM BAN TELEGRAM        
       """, parse_mode='html')








##############################СИСТЕМА "E" ########################################

    if message.text.lower() in ['система е', 'е']:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за систему "Е" ⚙️

🕹 | Информация:
<code>1e3</code> - 1.000$ - тыщ.
<code>1e6</code> - 1.000.000$ - млн.
<code>1e9</code> - 1.000.000.000$ - млрд.
<code>1e12</code> - 1.000.000.000.000$ - трлн.
<code>1e15</code> - 1.000.000.000.000.000$ - кврд.
<code>1e18</code> - 1.000.000.000.000.000.000$ - квнт.
<code>1e21</code> - 1.000.000.000.000.000.000.000$ - скст.
<code>1e24</code> - 1.000.000.000.000.000.000.000.000$ трикс.
<code>1e27</code> - 1.000.000.000.000.000.000.000.000.000$ твинкс.
<code>1e30</code> - 1.000.000.000.000.000.000.000.000.000.000$ септ.
<code>1e33</code> - 1.000.000.000.000.000.000.000.000.000.000.000$ октл.
<code>1e36</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000$ нонл.
<code>1e39</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000$ декал.
<code>1e42</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ эндк.
<code>1e45</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ доктл.
<code>1e48</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ гугл.
<code>1e51</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ кинд.
<code>1e54</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ трипт.
<code>1e57</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ срист.
<code>1e60</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ манит.
<code>1e63</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000$ гвинт. 
<code>1e66</code> - 1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000 клаунд

ℹ️ | <b>Система "e" , работает только на командах с маленькой буквы, с маленькой, вы можете водит точные цифры ставки, передачи и так далее ...</b>
    """, parse_mode='html')




###################################### аватарки #######################################
    if message.text.lower() in ['убрать скин', "убрать скины", "удалить скин", "-скин"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0]) 

       await bot.send_message(message.chat.id, f"🪣 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно удалили свой скин", parse_mode='html')
       cursor.execute(f'UPDATE avatarka SET avatarka = "none" WHERE user_id = {user_id}')
       connect.commit()


    if message.text.lower() in ['скины', 'скин', "скрин", "скун"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       strach_photo = open('a/страж.jpg', 'rb')

       cheat_photo = open('a/cheat.jpg', 'rb')

       apper_photo = open('a/apper.jpg', 'rb')

       dyp_photo = open('a/дюп.jpg', 'rb')

       girl_photo = open('a/girl.jpg', 'rb')

       admin_photo = open('a/админ.jpg', 'rb')

       ava_strach = InlineKeyboardMarkup(row_width=1)
       ava_strach2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_strach')
       ava_strach.add(ava_strach2)

       ava_cheat = InlineKeyboardMarkup(row_width=1)
       ava_cheat2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_cheat')
       ava_cheat.add(ava_cheat2)

       ava_apper = InlineKeyboardMarkup(row_width=1)
       ava_apper2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_apper')
       ava_apper.add(ava_apper2)

       ava_dyp = InlineKeyboardMarkup(row_width=1)
       ava_dyp2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_dyp')
       ava_dyp.add(ava_dyp2)

       ava_girl = InlineKeyboardMarkup(row_width=1)
       ava_girl2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_girl')
       ava_girl.add(ava_girl2)

       ava_admin = InlineKeyboardMarkup(row_width=1)
       ava_admin2 = InlineKeyboardButton(text='ПОСТАВИТЬ 🖼', callback_data='ava_admin')
       ava_admin.add(ava_admin2)

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, добро пожаловать в меню скинов 🗾

ℹ️ | Всего скинов: 6

ℹ️ | Доступные аватарки: ДЮППЕР, СТРАЖ, АППЕР, ЧИТЕР, ДЕВУШКА

⛔️ | Админ: АДМИН

ℹ️ | Каждый скин имеет свой дизайн, и на балансе будет виден красивое оформление профиля (баланса)

↘️ | Виберите один скин ниже 
       """, parse_mode='html')
       await bot.send_photo(message.chat.id, strach_photo, '', reply_markup=ava_strach)
       await bot.send_photo(message.chat.id, cheat_photo, '', reply_markup=ava_cheat)
       await bot.send_photo(message.chat.id, apper_photo, '', reply_markup=ava_apper)
       await bot.send_photo(message.chat.id, dyp_photo, '', reply_markup=ava_dyp)
       await bot.send_photo(message.chat.id, girl_photo, '', reply_markup=ava_girl)
       await bot.send_photo(message.chat.id, admin_photo, '', reply_markup=ava_admin)




###################################### РЕПУТАЦИЯ + ###################################

    if message.text.lower() in ['+', '++', '+++', 'кросс', "молодец", "имба"]:
       user_id = message.from_user.id

       reply_user_id = message.reply_to_message.from_user.id
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = user_name[0]

       reput = cursor.execute("SELECT reput from reput where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reput = int(reput[0])

       if reply_user_id == user_id:
          await bot.send_message(message.chat.id, f"📝 Не голосуй пидор", parse_mode='html')
          return

       await bot.send_message(message.chat.id, f"📊 | Вы успешно повысили репутацию  <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> . Теперь его репутация: {reput + 1}", parse_mode='html')
       cursor.execute(f'UPDATE reput SET reput = {reput + 1} WHERE user_id = {reply_user_id}')
       connect.commit()


###################################### РП КОМАНДЫ ####################################

    if message.text.lower() in ['Обнять', 'обнять', 'ОБНЯТЬ', "имба"]:
        friend_name = message.reply_to_message.from_user.username
        friend_id = message.reply_to_message.from_user.id
        # await message.delete()
        await message.answer(f'[{your_name}](tg://user?id={str(your_id)}) обнял-приподнял [{friend_name}](tg://user?id={str(friend_id)})', parse_mode="Markdown")     
        await message.answer(f'[{your_name}](tg://user?id={str(your_id)}) обнял-приподнял всех друзей', parse_mode="Markdown")
 
########################################PROMO#########################################
    if message.text.startswith('Создать промо'):  
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       
       name = str(message.text.split()[2])
       dengi = int(message.text.split()[3])
       imya = str(message.text.split()[4])
       kol = int(message.text.split()[5])
       if user_status == 'Owner':
           if imya == 'деньги':
               await bot.send_message(message.chat.id, f'Вы успешно создали промо под названием: {name} | количество: {dengi} | валюта: {imya} | количество активаций: {kol}', parse_mode='html')
               cursor.execute(f'UPDATE promo1 SET name = \"{name}\"')
               cursor.execute(f'UPDATE promo1 SET members = {0}')
               cursor.execute(f'UPDATE promo1 SET ob_members = {0}')
               cursor.execute(f'UPDATE promo1 SET dengi = {dengi}')
               cursor.execute(f'UPDATE promo1 SET val = \"{imya}\"')
               cursor.execute(f'UPDATE promo1 SET akt = {kol}')
           if imya == 'донат':
               await bot.send_message(message.chat.id, f'Вы успешно создали промо под названием: {name} | количество: {dengi} | валюта: {imya} | количество активаций: {kol}', parse_mode='html')
               cursor.execute(f'UPDATE promo1 SET name = "{name}"')
               cursor.execute(f'UPDATE promo1 SET members = {0}')
               cursor.execute(f'UPDATE promo1 SET ob_members = {0}')
               cursor.execute(f'UPDATE promo1 SET dengi = {dengi}')
               cursor.execute(f'UPDATE promo1 SET val = "{imya}"')
               cursor.execute(f'UPDATE promo1 SET akt = {kol}')
       else:
           await bot.send_message(message.chat.id, f'Вы не создатель бота.', parse_mode='html')

    if message.text.startswith('Промокод'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       
       text = str(message.text.split()[1])

       members = cursor.execute(f"SELECT members from promo1 where user_id = {user_id}").fetchone()
       members = int(members[0])
       
       dengi = cursor.execute(f"SELECT dengi from promo1 where user_id = {user_id}").fetchone()
       dengi = int(dengi[0])
       dengi2 = '{:,}'.format(dengi).replace(',', '.')
       
       akt = cursor.execute(f"SELECT akt from promo1 where user_id = {user_id}").fetchone()
       akt = int(akt[0])
       
       name = cursor.execute(f"SELECT name from promo1 where user_id = {user_id}").fetchone()
       name = str(name[0])

       val = cursor.execute(f"SELECT val from promo1 where user_id = {user_id}").fetchone()
       val = str(val[0])
       
       balance = cursor.execute(f"SELECT balance from users where user_id = {user_id}").fetchone()
       balance = int(balance[0])
       
       ecoins = cursor.execute(f"SELECT ecoins from users where user_id = {user_id}").fetchone()
       ecoins = int(ecoins[0])

       ob_members = cursor.execute("SELECT ob_members from promo1").fetchone()
       ob_members = int(ob_members[0])
       if text == name:
           if ob_members < akt:
               if members == 0:
                   if val == 'деньги':
                       await bot.send_message(message.chat.id, f"🖲 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно воспользовались промокодом {text} ", parse_mode='html')
                       await bot.send_message(message.chat.id, f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вам было зачислено <code>{dengi2}</code>$ ✅", parse_mode='html')
                       cursor.execute(f'UPDATE users SET balance = {balance + dengi} where user_id = {user_id}')
                       cursor.execute(f'UPDATE promo1 SET members = {1} where user_id = {user_id}')
                       cursor.execute(f'UPDATE promo1 SET ob_members = {ob_members + 1}')
                       connect.commit()
                       return
                   if val == 'донат':
                       await bot.send_message(message.chat.id, f"🖲 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно воспользовались промокодом {text} ", parse_mode='html')
                       await bot.send_message(message.chat.id, f"🪙 | <a href='tg://user?id={user_id}'>{user_name}</a>, вам было зачислено {dengi2} -коинов 🪙", parse_mode='html')
                       cursor.execute(f'UPDATE users SET dcoins = {ecoins + dengi} where user_id = {user_id}')
                       cursor.execute(f'UPDATE promo1 SET members = {1} where user_id = {user_id}')
                       cursor.execute(f'UPDATE promo1 SET ob_members = {ob_members + 1}')
                       connect.commit()
                       return
               else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы уже воспользовались этим промокодом", parse_mode='html')
                   return
           else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, данный промокод больше не действителен", parse_mode='html')
               return
       else:
           await bot.send_message(message.chat.id, f'{user_name}, похоже такого промокода не существует...', parse_mode='html')                 






########################################        Смена префикса          ######################################
    if message.text.startswith('Поменять префикс'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       prefix = ' '.join(message.text.split()[2:])
       if len(prefix) <= 20:
          if user_status in ['Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin', 'Admin', 'Helper_Admin', 'Owner']:
             await bot.send_message(message.chat.id, f"🔒 | Вы успешно сменили свой префикс на {prefix}")
             cursor.execute(f'UPDATE users SET pref = "{prefix}" WHERE user_id = {user_id}')
             connect.commit()
             return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять префикс можно только от привилегии \"ХЕЛПЕР\"", parse_mode='html')
             return
       else:
          await bot.send_message(message.chat.id, f"🆘 | Игрок, менять префикс не может быть более 20 символов!", parse_mode='html')
          return

    if message.text.startswith('поменять префикс'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       prefix = ' '.join(message.text.split()[2:])
       if len(prefix) <= 20:
          if user_status in ['Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin', 'Admin', 'Helper_Admin', 'Owner']:
             await bot.send_message(message.chat.id, f"🔒 | Вы успешно сменили свой префикс на {prefix}")
             cursor.execute(f'UPDATE users SET pref = "{prefix}" WHERE user_id = {user_id}')
             connect.commit()
             return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять префикс можно только от привилегии \"ХЕЛПЕР\"", parse_mode='html')
             return
       else:
          await bot.send_message(message.chat.id, f"🆘 | Игрок, менять префикс не может быть более 20 символов!", parse_mode='html')
          return

    if message.text.startswith('Cменить игроку префикс'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_id = message.reply_to_message.from_user.id
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       prefix = ' '.join(message.text.split()[3:])
       if len(prefix) <= 20:
          period = 900
          get = cursor.execute("SELECT stavka FROM time_prefix WHERE user_id = ?", (message.from_user.id,)).fetchone()
          last_stavka = f"{int(get[0])}"
          stavkatime = time.time() - float(last_stavka)
          if stavkatime > period:
             if user_status in ['Vladelec', 'Bog', 'Vlaselin', 'Admin', 'Helper_Admin', 'Owner']:
                await bot.send_message(message.chat.id, f"🔒 | Вы успешно сменили игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> префикс на {prefix}", parse_mode='html')
                cursor.execute(f'UPDATE users SET pref = "{prefix}" WHERE user_id = {reply_user_id}')
                cursor.execute(f'UPDATE time_prefix SET stavka = "{time.time()}" WHERE user_id = {reply_user_id}')
                connect.commit()
                return
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять префикс можно только от привилегии \"ВЛАДЕЛЕЦ\"", parse_mode='html')
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять игроку ник можно раз в 15 минут", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | Игрок, менять префикс не может быть более 20 символов!", parse_mode='html')
          return
    
    if message.text.startswith('cменить игроку префикс'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_id = message.reply_to_message.from_user.id
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       prefix = ' '.join(message.text.split()[3:])
       if len(prefix) <= 20:
          period = 900
          get = cursor.execute("SELECT stavka FROM time_prefix WHERE user_id = ?", (message.from_user.id,)).fetchone()
          last_stavka = f"{int(get[0])}"
          stavkatime = time.time() - float(last_stavka)
          if stavkatime > period:
             if user_status in ['Vladelec', 'Bog', 'Vlaselin', 'Admin', 'Helper_Admin', 'Owner']:
                await bot.send_message(message.chat.id, f"🔒 | Вы успешно сменили игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> префикс на {prefix}", parse_mode='html')
                cursor.execute(f'UPDATE users SET pref = "{prefix}" WHERE user_id = {reply_user_id}')
                cursor.execute(f'UPDATE time_prefix SET stavka = "{time.time()}" WHERE user_id = {reply_user_id}')
                connect.commit()
                return
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять префикс можно только от привилегии \"ВЛАДЕЛЕЦ\"", parse_mode='html')
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять игроку ник можно раз в 15 минут", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | Игрок, менять префикс не может быть более 20 символов!", parse_mode='html')
          return
         
    
    if message.text.startswith('cменить префикс'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       prefix = ' '.join(message.text.split()[2:])
       if len(prefix) <= 20:
          if user_status in ['Helper', 'Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin', 'Admin', 'Helper_Admin', 'Owner']:
             await bot.send_message(message.chat.id, f"🔒 | Вы успешно сменили свой префикс на {prefix}")
             cursor.execute(f'UPDATE users SET pref = "{prefix}" WHERE user_id = {user_id}')
             connect.commit()
             return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять префикс можно только от привилегии \"ХЕЛПЕР\"", parse_mode='html')
             return
       else:
          await bot.send_message(message.chat.id, f"🆘 | Игрок, менять префикс не может быть более 20 символов!", parse_mode='html')
          return

    if message.text.startswith('Сменить префикс'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       prefix = ' '.join(message.text.split()[2:])
       if len(prefix) <= 20:
          if user_status in ['Sponsor', 'Osnovatel', 'Vladelec', 'Bog', 'Vlaselin', 'Admin', 'Helper_Admin', 'Owner']:
             await bot.send_message(message.chat.id, f"🔒 | Вы успешно сменили свой префикс на {prefix}")
             cursor.execute(f'UPDATE users SET pref = "{prefix}" WHERE user_id = {user_id}')
             connect.commit()
             return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, менять префикс можно только от привилегии \"СПОНСОР\"", parse_mode='html')
             return
       else:
          await bot.send_message(message.chat.id, f"🆘 | Игрок, менять префикс не может быть более 10 символов!", parse_mode='html')
          return









#####################################################      КЕЙСЫ             ####################################################
    if message.text.lower() in ["открыть кейсы", "открыть дроп"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       
       

       money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
       money_case = int(money_case[0])

       donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
       donate_case = int(donate_case[0])

       ob_member = 0

       if money_case > 0:
          ob_member += 1
       else:
          pass

       if donate_case > 0:
          ob_member += 1
       else:
          pass

       if ob_member < 1:
          photo = open('a/k.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"""
🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету не каких дропов что бы купить дроп напишите донат
          """,parse_mode='html')
          return


       photo = open('a/k.jpg', 'rb')
       await bot.send_photo(message.chat.id, photo=photo)
       case_shop1 = InlineKeyboardMarkup(row_width=2)
       money_case1 = InlineKeyboardButton(text='Открыть Money-Drop 💸', callback_data='up_money_case')
       donate_case2 = InlineKeyboardButton(text='Открыть Donate-Drop 🧧', callback_data='up_donate_case')
       case_shop1.add(money_case1, donate_case2)


       photo = open('a/k.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот ваши дропы 🎁

💸 | Money-Drop - {money_case} шт.
🧧 | Donate-Drop - {donate_case} шт.

↘️ Виберите один из дропов, который хотите открыть 
       """,reply_markup=case_shop1, parse_mode='html')

    if message.text.lower() in ['Кейсы', 'дропы']:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])


       

       money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
       money_case = int(money_case[0])

       donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
       donate_case = int(donate_case[0])
      
       ob_members = 0

       if donate_case > 0:
          ob_members += 1
          donate_case2 = f'      🧧 | Donate-Drop - {donate_case} шт.\n'
       else:
          donate_case2 = ''

       if money_case > 0:
          ob_members += 1
          money_case2 = f'      💸 | Money-Drop - {money_case} шт.\n'
       else:
          money_case2 = ''

       if ob_members > 0:
          casee = '🎁 | Ваши дропы:\n'
       else:
          casee = '😟 | У вас нету дропов...'

          photo = open('a/k.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, хочешь задонатить? Если хочешь задонить то напиши разработчику✅"
       """, parse_mode='html')    




#####################################################      BOXSЫ             ####################################################
    if message.text.lower() in ["открыть боксы", "открыть бокс"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       
       

       money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
       money_case = int(money_case[0])

       donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
       donate_case = int(donate_case[0])

       ob_member = 0

       if money_case > 0:
          ob_member += 1
       else:
          pass

       if donate_case > 0:
          ob_member += 1
       else:
          pass

       if ob_member < 1:
          photo = open('a/kl.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"""
🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету не каких боксов что бы купить дроп напишите донат
          """,parse_mode='html')
          return


       photo = open('a/ke.jpg', 'rb')
       await bot.send_photo(message.chat.id, photo=photo)
       case_shop1 = InlineKeyboardMarkup(row_width=2)
       money_case1 = InlineKeyboardButton(text='Открыть Мегаящик 🎁', callback_data='up_money_case')
       donate_case2 = InlineKeyboardButton(text='Открыть Ящик 📦', callback_data='up_donate_case')
       case_shop1.add(money_case1, donate_case2)


       photo = open('a/ke.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот ваши боксы 🎁

💸 | Мегаящик - {money_case} шт.
🧧 | Ящик - {donate_case} шт.

↘️ Виберите один из боксы, который хотите открыть 
       """,reply_markup=case_shop1, parse_mode='html')

    if message.text.lower() in ['Кейсы', 'дропы']:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])


       

       money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
       money_case = int(money_case[0])

       donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
       donate_case = int(donate_case[0])
      
       ob_members = 0

       if donate_case > 0:
          ob_members += 1
          donate_case2 = f'      🧧 | Ящик - {donate_case} шт.\n'
       else:
          donate_case2 = ''

       if money_case > 0:
          ob_members += 1
          money_case2 = f'      💸 | Мегаящик - {money_case} шт.\n'
       else:
          money_case2 = ''

       if ob_members > 0:
          casee = '🎁 | Ваши дропы:\n'
       else:
          casee = '😟 | У вас нету дропов...'

          photo = open('a/k.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, хочешь задонатить? Если хочешь задонить то напиши разработчику✅"
       """, parse_mode='html')    





#################################################### !канал ################################
    if message.text.lower() in ['канал', "!канал", "channel"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       channel_pov = cursor.execute("SELECT members from channel_pov where user_id = ?", (message.from_user.id,)).fetchone()
       channel_pov = int(channel_pov[0])

       if channel_pov > 0:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы уже получили деньги за подписку")
          return
       
       sub_pov = InlineKeyboardMarkup(row_width=1)
       channel_push = InlineKeyboardButton(text='КАНАЛ 🔈', url='https://t.me/dlot_bb')
       channel_poverk = InlineKeyboardButton(text='ПРОВЕРИТЬ ✅', callback_data='channel_poverk')
       sub_pov.add(channel_push, channel_poverk)

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>,, вот условия задание 💠

🔈 | Подписаться на канал

💰 | Приз: 500.000.000.000.000.000$

↘️ Выберите одну кнопку ниже...       
       """, reply_markup=sub_pov, parse_mode='html')
       user_channel_status = await bot.get_chat_member(chat_id="@dlot_bb", user_id=message.from_user.id)
       if user_channel_status['status'] != 'left':
          print('GOOD')
       else:
          print('Luser')


@dp.callback_query_handler(text='gamevb')
async def craft_resurs3(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
   balance = int(balance[0])

   game = cursor.execute("SELECT game from users where user_id = ?",(callback.from_user.id,)).fetchone()
   game = int(game[0])

   balance2 = '{:,}'.format(balance)


   rx = random.randint(0, 10000)

   period = 5
   get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
   last_stavka = f"{int(get[0])}"
   stavkatime = time.time() - float(last_stavka)
   if stavkatime > period:
      if balance > 0:
         if int(rx) in range(0, 7000):
            i = balance - balance * 0.1
            i2 = int(i)
            i3 = '{:,}'.format(i2)
            await callback.message.answer(  f"""
👤 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🧊 | Игра: GAME-VB
🎟 | Ставка: {balance2}$
🕹 | Вы проиграли: {i3}$ [0.1X]            
""", parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
            connect.commit()
            return
         if int(rx) in range(7001, 10000):
            i = balance * 1.5
            i2 = int(i)
            i3 = '{:,}'.format(i2)
            await callback.message.answer( f"""
👤 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>
🧊 | Игра: GAME-VB
🎟 | Ставка: {balance2}$
👾 | Выигрыш состовляет: {i3}$ [1.5X]            
""", parse_mode='html')
            cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
            connect.commit()
            return
      else:
         await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас недостаточно средств! ", parse_mode='html')
   else:
      await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд", parse_mode='html')         




@dp.callback_query_handler(text='ava_admin')
async def craft_resurs3(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_status = str(user_status[0])

   if user_status in ['Player', 'Helper_Admin', 'Owner']:
      await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"IRON MASK\"", parse_mode='html')
      cursor.execute(f'UPDATE avatarka SET avatarka = "admin" WHERE user_id = {user_id}')
      connect.commit()
      return
   else:
      await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику {cash_owner_username} ️", parse_mode='html')

@dp.callback_query_handler(text='ava_girl')
async def craft_resurs3(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили скин \"REDSHARK\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "girl" WHERE user_id = {user_id}')
   connect.commit()

@dp.callback_query_handler(text='ava_dyp')
async def craft_resurs3(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили скин \"ИТАЧИ\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "dyp" WHERE user_id = {user_id}')
   connect.commit()

@dp.callback_query_handler(text='ava_apper')
async def craft_resurs3(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"ANIME\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "apper" WHERE user_id = {user_id}')
   connect.commit()

@dp.callback_query_handler(text='ava_cheat')
async def craft_resurs3(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"ЧИТЕР\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "cheat" WHERE user_id = {user_id}')
   connect.commit()

@dp.callback_query_handler(text='ava_strach')
async def craft_resurs3(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   await callback.message.answer( f"🖼 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили аватарку \"СТРАЖ\"", parse_mode='html')
   cursor.execute(f'UPDATE avatarka SET avatarka = "strach" WHERE user_id = {user_id}')
   connect.commit()

@dp.callback_query_handler(text='channel_poverk')
async def craft_resurs3(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
   balance = int(balance[0])
   user_channel_status = await bot.get_chat_member(chat_id="@dlot_bb", user_id=callback.from_user.id)

   channel_pov = cursor.execute("SELECT members from channel_pov where user_id = ?", (callback.from_user.id,)).fetchone()
   channel_pov = int(channel_pov[0])

   if channel_pov > 0:
      await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы уже получили деньги за подписку", parse_mode='html')
      return

   if user_channel_status['status'] != 'left':
      await callback.message.answer( f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно подписались на канал ✅", parse_mode='html')
      await callback.message.answer( f"💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили приз в размере  500.000.000.000.000.000$", parse_mode='html')
      cursor.execute(f'UPDATE channel_pov SET members = {1} WHERE user_id = {user_id}')
      cursor.execute(f'UPDATE users SET balance = {balance + 500000000000000000} WHERE user_id = {user_id}')
      connect.commit()
   else:
      await callback.message.answer( f"❌ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не подписались на канал, попробуйте снова", parse_mode='html')

@dp.callback_query_handler(text='owner_cash')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за OWNER ⛔️

1️⃣ | Выдача валюты
2️⃣ | Отбор валюты
3️⃣ | Умножение валюты
4️⃣ | Обнуление
5️⃣ | Выдача бана
6️⃣ | Выдача разбана
7️⃣ |Поделить баланс
8️⃣ | Выдача прав администратора "ADMIN"
9️⃣ | Выдача прав администратора "HELPER-ADMIN"
🔟 | Выдача Donate-Coins
1️⃣1️⃣ | МАССОВОЕ ОБНУЛЕНИЕ
1️⃣2️⃣ | Выдача бана по ID
1️⃣3️⃣ | Выдача разбана по ID
1️⃣4️⃣ | Выдача варна
1️⃣5️⃣ | Отбор варна 
1️⃣6️⃣ | Выдача варна по ID
1️⃣7️⃣ | Отбор варна по ID
1️⃣8️⃣ | Возможность посмотреть профиль игрока
1️⃣9️⃣ | Возможность посмотреть профиль игрока по ID
2️⃣0️⃣ | Возможность выдать права администратора "OWNER"
2️⃣1️⃣ | ДОСТУП К КОНСОЛИ БОТА
2️⃣2️⃣ | ДОСТУП К РЕПОРТАМ

🛒 Для покупки администраторских прав , обратитесь к Владельцу бота - {cash_owner_username}
    """,  parse_mode='html' )


@dp.callback_query_handler(text='helper_admins_cash')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за HELPER-ADMIN ⛔️

1️⃣ | Выдача валюты
2️⃣ | Отбор валюты
3️⃣ | Умножение валюты
4️⃣ | Обнуление
5️⃣ | Выдача бана
6️⃣ | Выдача разбана
7️⃣ | Поделить баланс
8️⃣ | Просмотр профила 
9️⃣ | Просмотр профиля по ID 
🔟 | Выдача варна 
1️⃣1️⃣ | Отбор варна
1️⃣2️⃣ | Выдача бана по ID
1️⃣3️⃣ | Выдача разбана по ID
1️⃣4️⃣ | Выдача варна по ID
1️⃣5️⃣ | Отбор варна по ID
1️⃣6️⃣ | Обнуление по ID
1️⃣7️⃣ | ДОСТУП К КОНСОЛИ БОТА
1️⃣8️⃣ | ДОСТУП К РЕПОРТАМ

🛒 Для покупки администраторских прав , обратитесь к Владельцу бота - {cash_owner_username}
    """,  parse_mode='html' )

@dp.callback_query_handler(text='admins_cash')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ADMIN ⛔️

1️⃣ | Выдача валюты
2️⃣ | Отбор валюты
3️⃣ | Умножение валюты
4️⃣ | Обнуление
5️⃣ | Просмотр профиля игрока
6️⃣ | Поделить баланс

🛒 Для покупки администраторских прав , обратитесь к Владельцу бота - {cash_owner_username}
    """,  parse_mode='html' )

@dp.callback_query_handler(text='adms')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    admins_menu_cash = InlineKeyboardMarkup(row_width=2)
    admins_cash = InlineKeyboardButton(text='⛔️ ADMIN', callback_data='admins_cash')
    helper_admins_cash = InlineKeyboardButton(text='⛔️ HELPER-ADMIN', callback_data='helper_admins_cash')
    owner_cash = InlineKeyboardButton(text='⛔️ OWNER', callback_data='owner_cash')
    admins_menu_cash.add(admins_cash, helper_admins_cash, owner_cash)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за статусы администраторов⛔️

1️⃣ | ADMIN - 400Р
4️⃣ | HELPER-ADMIN - 1.500Р
5️⃣ | OWNER - 5.000Р

↘️ Чтобы посмотреть возможности , выберите статус ниже   
    """,reply_markup=admins_menu_cash,  parse_mode='html' )
  
@dp.callback_query_handler(text='cash_vlaselin')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    case_donate = cursor.execute("SELECT case_donate from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_donate = int(case_donate[0])

    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 300000000000000000:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили привилегию ВЛАСТЕЛИН ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Vlaselin" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 5} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {case_donate + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 10000000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 500000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВЛАСТЕЛИН 🤎" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 300} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Donate-coins", parse_mode='html' )

@dp.callback_query_handler(text='vlastelin')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    vlaselin_menu = InlineKeyboardMarkup(row_width=1)
    cash_vlaselin = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_vlaselin')
    
    vlaselin_menu.add(cash_vlaselin)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за привилегию ВЛАСТЕЛИН 🤎

1️⃣ | Бонус-кит ВЛАСТЕЛИН
2️⃣ |Префикс ВЛАСТЕЛИН
3️⃣ |1.000.000.000.000.000.000$
4️⃣ | 100.000.000 Рейтинга
5️⃣ | Money-case 5 шт.
6️⃣ | Donate-case 1 шт.
7️⃣ | Способность менять себе префикс
8️⃣ | Способность менять игрокам префикс
9️⃣ | Ограничение на время в играх становиться 2 секунды

🛒 Чтобы купить привилегию , выберите кнопку купить ниже
    """, reply_markup=vlaselin_menu,  parse_mode='html')


@dp.callback_query_handler(text='cash_bog')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    case_donate = cursor.execute("SELECT case_donate from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_donate = int(case_donate[0])

    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 300000000000:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили валюту", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Bog" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 5000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {case_donate + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 10000000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 50000000000000000000000000000000000000000000000000000000000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "БОГ 🤍" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 300} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает Денег", parse_mode='html' )

@dp.callback_query_handler(text='bog')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    bog_menu = InlineKeyboardMarkup(row_width=1)
    cash_bog = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_bog')
    
    bog_menu.add(cash_bog)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за валюту

1️⃣ | Бонус-кит БОГ
2️⃣ |Префикс БОГ
3️⃣ |160 ДОНАТ КОИНОВ
4️⃣ | 10.000.000 Рейтинга
5️⃣ | Money-case 5.000.000шт.
6️⃣ | Donate-case 1 шт.
7️⃣ | Способность менять себе префикс
8️⃣ | Способность менять игрокам префикс
9️⃣ | Ограничение на время в играх становиться 2 секунды

🛒 Чтобы купить привилегию , выберите кнопку купить ниже
    """, reply_markup=bog_menu,  parse_mode='html')


@dp.callback_query_handler(text='cash_vladelec')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    case_donate = cursor.execute("SELECT case_donate from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_donate = int(case_donate[0])

    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 250:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили валюту  ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Vladelec" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 700} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {case_donate + 700} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 10000000000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 40000000000000000000000000000000000000000000000000000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ТЫ ЛУЧШИЙ 💖" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 250} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает денег", parse_mode='html' )

@dp.callback_query_handler(text='vladelec')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    vladelec_menu = InlineKeyboardMarkup(row_width=1)
    cash_vladelec = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_vladelec')
    
    vladelec_menu.add(cash_vladelec)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> ,  вот данные за валюту

ЗА ПОКУПКУ ТЫ ПОЛУЧИШЬ

1️⃣ | ШАНС В ФУТБОЛЕ
2️⃣ | АДМИН
3️⃣ | 5000000 ДОНАТ КОИНОВ
4️⃣ | 1.000.000.000.000 РЕЙТИНГА
5️⃣ | Money-case 800 шт.
6️⃣ | Donate-case 700 шт.
7️⃣ | Способность менять себе префикс

🛒 Чтобы купить валюту , выберите кнопку купить ниже
    """, reply_markup=vladelec_menu,  parse_mode='html')


@dp.callback_query_handler(text='cash_osnovatel')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    
    case_donate = cursor.execute("SELECT case_donate from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_donate = int(case_donate[0])
    
    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 17000000000000:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили валюту ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Osnovatel" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 500} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {case_donate + 100} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 10000000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 49000000000000000000000000000000000000000000000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "СПАСИБО ЗА ДОНАТ 💖" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 70000} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает денег", parse_mode='html' )

@dp.callback_query_handler(text='osnovatel')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    osnovatel_menu = InlineKeyboardMarkup(row_width=1)
    cash_osnovatel = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_osnovatel')
    
    osnovatel_menu.add(cash_osnovatel)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за валюту

ЗА ПОКУПКУ ВЫ ПОЛУЧИТЕ

1️⃣ | 1.000.000.000 РЕЙТИНГА
2️⃣ | АДМИН
3️⃣ | 1000000 ДОНАТ КОИНОВ
4️⃣ | Шанс в казино
5️⃣ | Money-case 100 штук

🛒 Чтобы купить валюту , выберите кнопку купить ниже
    """, reply_markup=osnovatel_menu,  parse_mode='html')


@dp.callback_query_handler(text='cash_sponsor')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    
    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 150000000005:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили валюту 5⃣", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Sponsor" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 30} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 10000} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 40000000000000000000000000000000000000000000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ДОНАТЕР ГОДА 💝" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 155} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас нехватает денег", parse_mode='html' )

@dp.callback_query_handler(text='sponsor')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    sponsor_menu = InlineKeyboardMarkup(row_width=1)
    cash_sponsor = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_sponsor')
    
    sponsor_menu.add(cash_sponsor)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за покупку валюты

ЗА ПОКУПКУ ВЫ ПОЛУЧИТЕ

1️⃣ | Х30 КЕЙСОВ
2️⃣ | 4000 ДОНАТ КОИНОВ
3️⃣ | ШАНС В СПИНЕ

🛒 Чтобы купить валюту , выберите кнопку купить ниже
    """, reply_markup=sponsor_menu,  parse_mode='html')



@dp.callback_query_handler(text='cash_helper')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    
    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 1000000000:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили валюту 4⃣", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Helper" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 30} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 1300} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SETbalance = {balance + 400000000000000000000000000000000000000000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ЛУЧШИЙ 💖" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 100} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас недостаточно денег!", parse_mode='html' )

@dp.callback_query_handler(text='helper')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    helper_menu = InlineKeyboardMarkup(row_width=1)
    cash_helper = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_helper')
    
    helper_menu.add(cash_helper)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за валюту 4⃣

ЗА ПОКУПКУ ТЫ ПОЛУЧИШЬ

1️⃣ | 200 донат коинов
2️⃣ | Шансы Х2 в казино 

🤝 Чтобы купить валюту , выберите кнопку купить ниже
    """, reply_markup=helper_menu,  parse_mode='html')


@dp.callback_query_handler(text='cash_platina')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    
    case_money = cursor.execute("SELECT case_money from user_case where user_id = ?",(callback.from_user.id,)).fetchone()
    case_money = int(case_money[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 5000:
       await callback.message.answer( f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили валюту 2⃣ ", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Platina" where user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_money = {case_money + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 800} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 1000000000000000000000000000000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ДОНАТЕР 💖" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 50} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"😞 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас недостаточно средств на балансе!", parse_mode='html' )

@dp.callback_query_handler(text='platina')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    platina_menu = InlineKeyboardMarkup(row_width=1)
    cash_platina = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_platina')
    
    platina_menu.add(cash_platina)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> вы собераетесь купить валюту 3⃣, чтобы купить нажми на кнопку снизу 🔽
    """, reply_markup=platina_menu,  parse_mode='html')


@dp.callback_query_handler(text='cash_premium')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 300000000000:
       await callback.message.answer( f"😞 | <a href='tg://user?id={user_id}'>{user_name}</a>,  У вас недостаточно средств ",         parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Premium" where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 300} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 500000000000000000000000000000000000.000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ЛУЧШИЙ ❤" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 30} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! У вас на балансе 0", parse_mode='html' )

@dp.callback_query_handler(text='premium')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    premium_menu = InlineKeyboardMarkup(row_width=1)
    cash_premium = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_premium')
    
    premium_menu.add(cash_premium)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы хотите купить валюту 2⃣?

🛒 Чтобы купить валюту , выберите кнопку купить ниже
    """, reply_markup=premium_menu,  parse_mode='html')


@dp.callback_query_handler(text='cash_vip')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    pref = cursor.execute("SELECT pref from users where user_id = ?",(callback.from_user.id,)).fetchone()
    pref = pref[0]
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    if donate_coins >= 1000000000000:
       await callback.message.answer( f"😞 | <a href='tg://user?id={user_id}'>{user_name}</a>,  на вашем балансе 0₽", parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Vip" where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 100} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 10000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВИП ❤️" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 10} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! На вашем балансе недостаточно средтсв!", parse_mode='html' )

@dp.callback_query_handler(text='vip')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])



    vip_menu = InlineKeyboardMarkup(row_width=1)
    cash_vip = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_vip')
    
    vip_menu.add(cash_vip)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы собераетесь купить валюту 10е29 чтобы преобрести нажмите на кнопку купить 🔽
    """, reply_markup=vip_menu,  parse_mode='html')

@dp.callback_query_handler(text='privilegii')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    privilegii_inline = InlineKeyboardMarkup(row_width=3)
    vip = InlineKeyboardButton(text='1⃣', callback_data='vip')
    premium = InlineKeyboardButton(text='2⃣', callback_data='premium')
    platina = InlineKeyboardButton(text='3⃣', callback_data='platina')
    helper = InlineKeyboardButton(text='4⃣', callback_data='helper')
    sponsor = InlineKeyboardButton(text='5⃣', callback_data='sponsor')
    osnovatel = InlineKeyboardButton(text='6⃣', callback_data='osnovatel')
    vladelec = InlineKeyboardButton(text='7⃣', callback_data='vladelec')
    bog = InlineKeyboardButton(text='8⃣', callback_data='bog')
    vlastelin = InlineKeyboardButton(text='9⃣', callback_data='vlastelin')
    privilegii_inline.add(vip, premium, platina, helper, sponsor, osnovatel, vladelec, bog, vlastelin)
    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот доступные валюты 🤝 
🛒 Чтобы купить валюту , виберите её ниже
все доступные валюты📝

1⃣ | 10e29 = 15₽
2⃣ | 500е34 = 35₽ 
3⃣ | 100е39 = 49₽
4⃣ | 20е42 = 59₽ 
5⃣ | 40е49 = 70₽ 
6⃣ | 60е56 = 100₽ 
7⃣ | 40е60 = 125₽
8⃣ | 60е63 = 200₽
9⃣ | 45е64 = 500₽ 

ℹ️ Чтобы купить валюту, выберите кнопку ниже 😉   
    """, reply_markup=privilegii_inline,  parse_mode='html')

@dp.callback_query_handler(text='money_case_cash1')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
    money_case = int(money_case[0])

    if donate_coins >= 50:
       await callback.message.answer(f"💸 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купил 1 Money-Case", parse_mode='html')
       cursor.execute(f'UPDATE user_case SET case_money = {money_case + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 50} WHERE user_id = {user_id}')
       connect.commit()
       return
    else:
       await callback.message.answer(f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не достаточно Donate-Coins 🪙", parse_mode='html')




@dp.callback_query_handler(text='money_case')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    money_case_cash = InlineKeyboardMarkup(row_width=2)
    money_case_cash1 = InlineKeyboardButton(text='🛒 Купить кейс', callback_data='money_case_cash1')
    money_case_cash.add(money_case_cash1)

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за Money-Case 💸

ℹ️ | В 1 Money-Case выпадает от 0$ и до 999гугл.

🛒 Чтобы купить нажмите кнопку ниже 🔽
    """, reply_markup=money_case_cash,  parse_mode='html')


@dp.callback_query_handler(text='up_money_case')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
    money_case = int(money_case[0])

    balance = cursor.execute(f'SELECT balance from users where user_id = {user_id}').fetchone()
    balance = int(balance[0])

    if money_case < 1:
       await callback.message.answer( f"🆘 | Игрок, у вас нету Money кейсов", parse_mode='html')
       return
       
    rx = random.randint(0, 100000000000000000000000000000)
    rx2 = '{:,}'.format(rx)

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вы открыли Money-Case 💸

🔎 | Результат: {rx2}$    
    """, parse_mode='html')
    cursor.execute(f'UPDATE users SET balance = {balance + rx} WHERE user_id = {user_id}')
    cursor.execute(f'UPDATE user_case SET case_money = {money_case - 1} WHERE user_id = {user_id}')
    connect.commit()

@dp.callback_query_handler(text='up_donate_case')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
    donate_case = int(donate_case[0])

    if donate_case < 1:
       await callback.message.answer( f"🆘 | Игрок, у вас нету Донат кейсов", parse_mode='html')
       return
   
    rx = random.randint(0, 935)

    if int(rx) in range(0,500):
       await callback.message.answer( f"""
⏳ | <i>Кейс открывается .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>💚 ХЕЛПЕР</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Helper" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ХЕЛПЕР 💚" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(501,750):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>💙 СПОНСОР</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Sponsor" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "СПОНСОР 💙" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(751,850):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>💜 ОСНОВАТЕЛЬ</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Osnovatel" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ОСНОВАТЕЛЬ 💜" WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(851,900):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>🖤 ВЛАДЕЛЕЦ</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Vladelec" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВЛАДЕЛЕЦ 🖤" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(901,925):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>🤍 БОГ</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Bog" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "БОГ 🤍" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
    if int(rx) in range(925,935):
       await callback.message.answer( f"""
⏳ | <i>Открытия кейса .....</i>      
       """, parse_mode='html')
       time.sleep(2)
       await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно выбили с донат кейса - <b>🤎 ВЛАСТЕЛИН</b>    
       """, parse_mode='html')
       cursor.execute(f'UPDATE users SET user_status = "Vlaselin" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET pref = "ВЛАСТЕЛИН 🤎" WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case - 1} WHERE user_id = {user_id}')
       connect.commit()
@dp.callback_query_handler(text='donate_case_cash1')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
    donate_case = int(donate_case[0])

    if donate_coins >= 100:
       await callback.message.answer(f"🧧 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купил 1 Donate-Case", parse_mode='html')
       cursor.execute(f'UPDATE user_case SET case_donate = {donate_case + 1} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 100} WHERE user_id = {user_id}')
       connect.commit()
       return
    else:
       await callback.message.answer(f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не достаточно Donate-Coins 🪙", parse_mode='html')


@dp.callback_query_handler(text='donate_case')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    donate_case_cash = InlineKeyboardMarkup(row_width=2)
    donate_case_cash1 = InlineKeyboardButton(text='🛒 Купить кейс', callback_data='donate_case_cash1')
    donate_case_cash.add(donate_case_cash1)

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за Donate-Case 🧧

ℹ️ | В 1 Donate-Case падает рандомно случайная привилегия!

🛒 Чтобы купить нажмите кнопку ниже 🔽
    """, reply_markup=donate_case_cash,  parse_mode='html')

@dp.callback_query_handler(text='case')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    case_shop = InlineKeyboardMarkup(row_width=2)
    money_case1 = InlineKeyboardButton(text='💸 Money-Case', callback_data='money_case')
    donate_case2 = InlineKeyboardButton(text='🧧 Donate-Case', callback_data='donate_case')
    case_shop.add(money_case1, donate_case2)

    money_case = cursor.execute(f'SELECT case_money from user_case where user_id = {user_id}').fetchone()
    money_case = int(money_case[0])

    donate_case = cursor.execute(f'SELECT case_donate from user_case where user_id = {user_id}').fetchone()
    donate_case = int(donate_case[0])
    
    ob_members = 0

    if donate_case > 0:
       ob_members += 1
       donate_case2 = f'      🧧 | Donate-Case - {donate_case} шт.\n'
    else:
       donate_case2 = ''

    if money_case > 0:
       ob_members += 1
       money_case2 = f'      💸 | Money-Case - {money_case} шт.\n'
    else:
       money_case2 = ''
   
    if ob_members > 0:
       casee = '🎁 | Ваши кейсы:\n'
    else:
       casee = '😟 | У вас нету кейсов...'

    await callback.message.answer( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот данные за кейсы 🎁

💸 | Money-Case - 50 Hepy-Coins 👻
🧧 | Donate-Case - 100 Hepy-Coins 👻
👑 | Reting-Case - 250 Hepy-Coins 👻 
{casee}{money_case2}{donate_case2}{reting_case2}

🛒 Чтобы купить\посмотреть информацию, выберите кнопку ниже ⬇️  
    """, reply_markup=case_shop,  parse_mode='html')
 

@dp.callback_query_handler(text='resurs4')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    basement = cursor.execute("SELECT basement from house where user_id = ?",(callback.from_user.id,)).fetchone()
    basement = int(basement[0])

    iron = cursor.execute("SELECT iron from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    iron = int(iron[0])

    metall = cursor.execute("SELECT metall from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    metall = int(metall[0])

    linen = cursor.execute("SELECT linen from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    linen = int(linen[0])

    cotton = cursor.execute("SELECT cotton from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    cotton = int(cotton[0])


    #rake, pick
    rake = cursor.execute("SELECT rake from farm where user_id = ?", (callback.from_user.id,)).fetchone()
    rake = rake[0]

    pick = cursor.execute("SELECT pick from mine where user_id = ?", (callback.from_user.id,)).fetchone()
    pick = pick[0]
    
    if basement == 1:
       basement_period = 30
   
    if basement == 2:
       basement_period = 15

    if basement == 3:
       basement_period = 4
    
    rx = random.randint(0,1000)

    getе = cursor.execute("SELECT time_craft FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(getе[0])
    stavkatime = time.time() - float(last_stavka)
    if basement > 0:
       if stavkatime > basement_period:
          if int(rx) in range(0,900):
             await callback.message.answer( f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Грабли Cherick 🌾\n💈 |Результат: Провал ❌", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
          if int(rx) in range(901,1000):
             await callback.message.answer(  f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Грабли Cherick 🌾\n💈 |Результат: Успешно ✅", parse_mode='html')
             await callback.message.answer(  f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы получили предмет: Грабли Cherick 🌾\n🔱 | Уникальность: Х2 Добыча ресурсов, Ограничение на время снимаеться на 50%", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE farm SET rake = "Cherick" WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
       else:
          await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! С вашим подвалом можно крафтить раз в {basement_period} секунд", parse_mode='html')
          await bot.answer_callback_query(callback.id)
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Крафтить можно только с подвалом", parse_mode='html')
       await bot.answer_callback_query(callback.id)


@dp.callback_query_handler(text='resurs3')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    basement = cursor.execute("SELECT basement from house where user_id = ?",(callback.from_user.id,)).fetchone()
    basement = int(basement[0])

    iron = cursor.execute("SELECT iron from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    iron = int(iron[0])

    metall = cursor.execute("SELECT metall from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    metall = int(metall[0])

    linen = cursor.execute("SELECT linen from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    linen = int(linen[0])

    cotton = cursor.execute("SELECT cotton from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    cotton = int(cotton[0])


    #rake, pick
    rake = cursor.execute("SELECT rake from farm where user_id = ?", (callback.from_user.id,)).fetchone()
    rake = rake[0]

    pick = cursor.execute("SELECT pick from mine where user_id = ?", (callback.from_user.id,)).fetchone()
    pick = pick[0]
    
    if basement == 1:
       basement_period = 30
   
    if basement == 2:
       basement_period = 15

    if basement == 3:
       basement_period = 4
    
    rx = random.randint(0,1000)

    getе = cursor.execute("SELECT time_craft FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(getе[0])
    stavkatime = time.time() - float(last_stavka)
    if basement > 0:
       if stavkatime > basement_period:
          if int(rx) in range(0,900):
             await callback.message.answer( f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Кирка Cherick ⛏\n💈 |Результат: Провал ❌", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
          if int(rx) in range(901,1000):
             await callback.message.answer(  f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Кирка Cherick ⛏\n💈 |Результат: Успешно ✅", parse_mode='html')
             await callback.message.answer(  f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы получили предмет: Кирка Cherick ⛏\n🔱 | Уникальность: Х2 Добыча ресурсов, Ограничение на время снимаеться на 50%", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET pick = "Cherick" WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
       else:
          await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! С вашим подвалом можно крафтить раз в {basement_period} секунд", parse_mode='html')
          await bot.answer_callback_query(callback.id)
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Крафтить можно только с подвалом", parse_mode='html')
       await bot.answer_callback_query(callback.id)


@dp.callback_query_handler(text='resurs2')
async def craft_resurs2(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    basement = cursor.execute("SELECT basement from house where user_id = ?",(callback.from_user.id,)).fetchone()
    basement = int(basement[0])

    iron = cursor.execute("SELECT iron from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    iron = int(iron[0])

    metall = cursor.execute("SELECT metall from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    metall = int(metall[0])

    linen = cursor.execute("SELECT linen from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    linen = int(linen[0])

    cotton = cursor.execute("SELECT cotton from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    cotton = int(cotton[0])


    #rake, pick
    rake = cursor.execute("SELECT rake from farm where user_id = ?", (callback.from_user.id,)).fetchone()
    rake = rake[0]

    pick = cursor.execute("SELECT pick from mine where user_id = ?", (callback.from_user.id,)).fetchone()
    pick = pick[0]
    
    if basement == 1:
       basement_period = 30
   
    if basement == 2:
       basement_period = 15

    if basement == 3:
       basement_period = 4
    
    rx = random.randint(0,1000)

    getе = cursor.execute("SELECT time_craft FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(getе[0])
    stavkatime = time.time() - float(last_stavka)
    if basement > 0:
       if stavkatime > basement_period:
          if int(rx) in range(0,750):
             await callback.message.answer( f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Грабли Zerro 🌾\n💈 |Результат: Провал ❌", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
          if int(rx) in range(751,1000):
             await callback.message.answer(  f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Грабли Zerro 🌾\n💈 |Результат: Успешно ✅", parse_mode='html')
             await callback.message.answer(  f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы получили предмет: Грабли Zerro 🌾\n🔱 | Уникальность: Х2 Добыча ресурсов", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE farm SET rake = "Zerro" WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
       else:
          await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! С вашим подвалом можно крафтить раз в {basement_period} секунд", parse_mode='html')
          await bot.answer_callback_query(callback.id)
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Крафтить можно только с подвалом", parse_mode='html')
       await bot.answer_callback_query(callback.id)


@dp.callback_query_handler(text='resurs1')
async def craft_resurs1(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    basement = cursor.execute("SELECT basement from house where user_id = ?",(callback.from_user.id,)).fetchone()
    basement = int(basement[0])

    iron = cursor.execute("SELECT iron from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    iron = int(iron[0])

    metall = cursor.execute("SELECT metall from mine where user_id = ?",(callback.from_user.id,)).fetchone()
    metall = int(metall[0])

    linen = cursor.execute("SELECT linen from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    linen = int(linen[0])

    cotton = cursor.execute("SELECT cotton from farm where user_id = ?",(callback.from_user.id,)).fetchone()
    cotton = int(cotton[0])


    #rake, pick
    rake = cursor.execute("SELECT rake from farm where user_id = ?", (callback.from_user.id,)).fetchone()
    rake = rake[0]

    pick = cursor.execute("SELECT pick from mine where user_id = ?", (callback.from_user.id,)).fetchone()
    pick = pick[0]
    
    if basement == 1:
       basement_period = 30
   
    if basement == 2:
       basement_period = 15

    if basement == 3:
       basement_period = 4
    
    rx = random.randint(0,1000)

    getе = cursor.execute("SELECT time_craft FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(getе[0])
    stavkatime = time.time() - float(last_stavka)
    if basement > 0:
       if stavkatime > basement_period:
          if int(rx) in range(0,750):
             await callback.message.answer( f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Кирка Zerro ⛏\n💈 |Результат: Провал ❌", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
          if int(rx) in range(751,1000):
             await callback.message.answer(  f"👨 |Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>\n⚙️ |Действие: Крафт предмета\n📦 | Предмет: Кирка Zerro ⛏\n💈 |Результат: Успешно ✅", parse_mode='html')
             await callback.message.answer(  f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы получили предмет: Кирка Zerro⛏\n🔱 | Уникальность: Х2 Добыча ресурсов", parse_mode='html')
             cursor.execute(f'UPDATE bot_time SET time_craft = {time.time()} WHERE user_id = {user_id}')
             cursor.execute(f'UPDATE mine SET pick = "Zerro" WHERE user_id = {user_id}')
             connect.commit()
             await bot.answer_callback_query(callback.id)
       else:
          await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! С вашим подвалом можно крафтить раз в {basement_period} секунд", parse_mode='html')
          await bot.answer_callback_query(callback.id)
    else:
       await callback.message.answer( f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Крафтить можно только с подвалом", parse_mode='html')
       await bot.answer_callback_query(callback.id)


@dp.callback_query_handler(text='Priv2')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.answer(f'''
а ок пон

ℹ️ Что бы использовать команду , напишите команду сообщением
    ''', parse_mode='html')

@dp.callback_query_handler(text='Im2')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.answer(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот все команды на имущество📝

🏠 | Дома
         🏡 Мой дом 
         🏡 Купить подвал [номер]
         🏡 Продать подвал 
         🏡 Крафтить
         🏡 Система крафта 

🚘 | Машины
        🚗 Моя машина
        🚗 Заправить 
        🚗 Поченить
        🚗 Продать машину

✈️ | Самолёт
        ✈️ Мои самолёт
        ✈️ Купить самолёт [номер]
        ✈️ Заправить
        ✈️ Продать сомалёт

 ⛴️ l Яхта 
         ⛴️ мои яхта 
         ⛴️ купить яхту [номер]
         ⛴️ подарить яхту игроку
         ⛴️ продать яхту

ℹ️ Что бы использовать команду , напишите команду сообщением
    ''', parse_mode='html')

@dp.callback_query_handler(text='rabot2')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.answer(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот список работних команд📝

⛏ | Шахта
      Купить кирку ⛏
      Копать руду ⛏
      Продать [название руды] [количество] ⛏
      
🌾 | Ферма 
      Купить грабли 🌾
      Собрать [название урожая] 🌾
      Продать [название урожая] [количество] 🌾
      
ℹ️ Что бы использовать команду , напишите команду сообщением
    ''', parse_mode='html')

@dp.callback_query_handler(text='game2')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.answer(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, <b>вот список игровых команд 📝

🧊 /gamevb | вб - игра на весь баланс, выводит информацию за игру
⚽️ Футбол  1 | Фб 1 - Азартная игра футбол
🎱 Dice ч 1 | Dice к 1 | Wheel - Азартная игра , со ставкой на чёрный цвет, ставка на красный цвет, выводит информацию за игру
🤵‍♀️ Казино 1 - Азартная игра казино
◾️ Плинко 1 -  Азартная игра Плинко
🎰 | Спин 1 - Азартная игра Спин
🎲 Кубик 1 [до 7] 1 - Азартная игра Кубик
🎲 Чётное 1 | нечётное 1 - Азартная игра Чётное нечётное со ставкой на чётное , со ставкой на нечётное
⭐ Звезда бросить [ставка] - Азартная игра Звезда

ℹ️ Что бы использовать команду </b>, напишите команду сообщением
    ''', parse_mode='html')

@dp.callback_query_handler(text='admins_comands')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0]) 
    if user_status == 'Owner':
       commands = '''
1️⃣ | Выдать [сумма]
2️⃣ | Забрать [сумма]
3️⃣ | Умножить [количество]
4️⃣ | Обнулить
5️⃣ | /ban
6️⃣ | /unban
7️⃣ |Выдать админа
8️⃣ | Выдать хелпера
9️⃣ | Передать права
🔟 | Забрать права
1️⃣1️⃣ | /reset
1️⃣2️⃣ | /warn
1️⃣3️⃣ | reset_id [ID]
1️⃣4️⃣ | /info
1️⃣5️⃣ | /info_id [ID]
1️⃣6️⃣ | Поделить [количество]
1️⃣7️⃣ | /ban_id [ID]
1️⃣8️⃣ | /unban_id [ID]
1️⃣9️⃣ | /warn_id [ID]
2️⃣0️⃣ | /unwarn_id [ID]
2️⃣1️⃣ | Забрать донат
2️⃣2️⃣ | Забрать рейтинг

       '''
    if user_status == 'Helper_Admin':
       commands = '''
1️⃣ | Выдать [сумма]
2️⃣ | Забрать [сумма]
3️⃣ | Умножить [количество]
4️⃣ | Обнулить
5️⃣ | /ban
6️⃣ | /unban
7️⃣ | /warn
8️⃣ | reset_id [ID]
9️⃣ | /info
🔟 | /info_id [ID]
1️⃣1️⃣ | Поделить [количество]
1️⃣2️⃣ | /ban_id [ID]
1️⃣3️⃣ | /unban_id [ID]
1️⃣4️⃣ | /warn_id [ID]
1️⃣5️⃣ | /unwarn_id [ID]


       '''
    if user_status == 'Admin':
       commands = '''
1️⃣ | Выдать [сумма]
2️⃣ | Забрать [сумма]
3️⃣ | Умножить [количество]
4️⃣ | Обнулить
5️⃣ | /info
6️⃣ | Поделить [количество]
       '''
    if user_status == 'Admin':
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот список администраторских команд 📝\n{commands}", parse_mode='html')
       return
    if user_status == 'Helper_Admin':
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот список администраторских команд 📝\n{commands}", parse_mode='html')
       return
    if user_status == 'Owner':
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот список администраторских команд 📝\n{commands}", parse_mode='html')
       return
    else:
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику {cash_owner_username} ⚠️", parse_mode='html')

@dp.callback_query_handler(text='stats222')
async def ob_Statisyik(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = user_status[0]

    sqlite_select_query21 = """SELECT * from users where user_status = \"Vip\""""
    cursor.execute(sqlite_select_query21)
    vip = cursor.fetchall()

    sqlite_select_query22 = """SELECT * from users where user_status = \"Premium\""""
    cursor.execute(sqlite_select_query22)
    premium = cursor.fetchall()

    sqlite_select_query23 = """SELECT * from users where user_status = \"Platina\""""
    cursor.execute(sqlite_select_query23)
    platina = cursor.fetchall()

    sqlite_select_query24 = """SELECT * from users where user_status = \"Helper\""""
    cursor.execute(sqlite_select_query24)
    helper = cursor.fetchall()

    sqlite_select_query25 = """SELECT * from users where user_status = \"Sponsor\""""
    cursor.execute(sqlite_select_query25)
    sponsor = cursor.fetchall()

    sqlite_select_query26 = """SELECT * from users where user_status = \"Osnovatel\""""
    cursor.execute(sqlite_select_query26)
    osnovatel = cursor.fetchall()

    sqlite_select_query27 = """SELECT * from users where user_status = \"Vladelec\""""
    cursor.execute(sqlite_select_query27)
    vladelec = cursor.fetchall()

    sqlite_select_query28 = """SELECT * from users where user_status = \"Bog\""""
    cursor.execute(sqlite_select_query28)
    bog = cursor.fetchall()

    sqlite_select_query29 = """SELECT * from users where user_status = \"Vlaselin\""""
    cursor.execute(sqlite_select_query29)
    vlaselin = cursor.fetchall()

    sqlite_select_query = """SELECT * from users"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Admin\""""
    cursor.execute(sqlite_select_query2)
    records2 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Helper_Admin\""""
    cursor.execute(sqlite_select_query2)
    records3 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Owner\""""
    cursor.execute(sqlite_select_query2)
    records4 = cursor.fetchall()

    if user_status == 'Owner':
       await callback.message.answer(f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот общая статистика бота 🔎

🔓 | Основная
         👤 | Игроков: {len(records)}

🔰 | Привилегии
         ❤️ | ВИП: {len(vip)}
         🧡 | ПРЕМИУМ: {len(premium)}
         💛 | ПЛАТИНА: {len(platina)}
         💚 | ХЕЛПЕР: {len(helper)}
         💙 | СПОНСОР: {len(sponsor)}
         💜 | ОСНОВАТЕЛЬ: {len(osnovatel)}
         🖤 | ВЛАДЕЛЕЦ: {len(vladelec)}
         🤍 | БОГ: {len(bog)}
         🤎 | ВЛАСТЕЛИН: {len(vlaselin)}

🛑 | Администрация
         ⛔️ | ADMIN: {len(records2)}
         ⚠️ | HELPER-ADMIN: {len(records3)}
         ✅ | OWNER: {len(records4)}        
       """, parse_mode='html')
    else:
       await callback.message.answer(f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, статистика бота доступна только от прав администратора \"HELPER-ADMINS\" ", parse_mode='html')


@dp.callback_query_handler(text='statistic')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    
    sqlite_select_query = """SELECT * from users"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Admin\""""
    cursor.execute(sqlite_select_query2)
    records2 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Helper_Admin\""""
    cursor.execute(sqlite_select_query2)
    records3 = cursor.fetchall()

    sqlite_select_query2 = """SELECT * from users where user_status = \"Owner\""""
    cursor.execute(sqlite_select_query2)
    records4 = cursor.fetchall()

    stats222 = InlineKeyboardMarkup(row_width=1)
    ob_statistik2 = InlineKeyboardButton(text='Общая статистика 🔎', callback_data='ob_statistik2')
    
    stats222.add(ob_statistik2)

    if user_status == "Admin":
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот статистика бота  📊\n🤵 | Игроков:{len(records)}\n👨‍⚖️ | OWNER: {len(records4)}\n👮‍♀️ | HELPER-ADMINS: {len(records3)}\n🤠 | ADMIN: {len(records2)}",reply_markup=stats222, parse_mode='html')
       return
    if user_status == "Helper_Admin":
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот статистика бота  📊\n🤵 | Игроков:{len(records)}\n👨‍⚖️ | OWNER: {len(records4)}\n👮‍♀️ | HELPER-ADMINS: {len(records3)}\n🤠 | ADMIN: {len(records2)}",reply_markup=stats222 , parse_mode='html')
       return

    if user_status == "Owner":
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вот статистика бота  📊\n🤵| Игроков: {len(records)}\n👨‍⚖️ | OWNER: {len(records4)}\n👮‍♀️ | HELPER-ADMINS: {len(records3)}\n🤠 | ADMIN: {len(records2)}",reply_markup=stats222 , parse_mode='html')
       return
    else:
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику ⚠️ ", parse_mode='html')
@dp.callback_query_handler(text='Admins_menu_up')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0])

    admins_menu = InlineKeyboardMarkup(row_width=2)
    statistic = InlineKeyboardButton(text='Статистика 👥', callback_data='statistic')
    admins_comands = InlineKeyboardButton(text='Админ команды 📝', callback_data='admins_comands')
    admins_menu.add(statistic, admins_comands)
    if user_status == 'Owner':
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно вошли в админ меню ✅\n\n⛔️ | Права администратора: OWNER\n\n🔐 | Категории:\n     👥 | Статистика бота\n     📝 | Админ команды\n\n↘️ Выбери одну из категорий", reply_markup=admins_menu , parse_mode='html')
       return

    if user_status == 'Helper_Admin':
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно вошли в админ меню ✅\n\n⛔️ | Права администратора: HELPER ADMINS\n\n🔐 | Категории:\n     👥 | Статистика бота\n     📝 | Админ команды\n\n↘️ Выбери одну из категорий", reply_markup=admins_menu , parse_mode='html')
       return
    if user_status == 'Admin':
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно вошли в админ меню ✅\n\n⛔️ | Права администратора: ADMINS\n\n🔐 | Категории:\n     👥 | Статистика бота\n     📝 | Админ команды\n\n↘️ Выбери одну из категорий", reply_markup=admins_menu , parse_mode='html')
       return
    else:
       await callback.message.answer(f"<a href='tg://user?id={user_id}'>{user_name}</a>,Вы не являетесь администратором бота 👮. Для получение прав администратора обратитесь к разработчику {cash_owner_username} ⚠️ ", parse_mode='html')
@dp.callback_query_handler(text='Osn2')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    await callback.message.answer(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, <b>вот список основных команд📝

🕴 Профиль - выводит ваш игровой профиль
🔎 Ник  | Сменить ник  - Выводит ваш ник, и так же его меняет 
⚙️ Сменить префикс  | +игроку префикс  - меняет префикс себе, меняет префикс игроку.
👝 Б  | Баланс  - выводит ваш игровой баланс
🏦 Банк  | Банк положить 1  | Банк снять 1  - выводит ваш игровой банк с депозитом , позволяет положить в банк сумму, позволяет снять с банка сумму
🏛 Депозит положить 1  | Депозит снять 1  | Процент снять 1  - Позволяет положить на депозит , позволяет снять с депозита , позволяет снять накапанный процент с депозита 
🟣 Эфириум курс  | Эфириум купить 1  | Эфириум продать  1  - Выводит курс эфириума, позволяет купить эфириум, позволяет продать эфириум
💎  Рейтинг | Рейтинг купить 1 | Рейтинг продать 1 - Выводит ваш игровой рейтинг, позволяет купить рейтинг, позволяет продать рейтинг
🤝 Дать 1e30  | Передать 1  [ID] - Позволяет передать деньги игроку, позволяет передать деньги игроку по ID
👑 Топ  | Топ б  - Выводит топ по рейтингу игроков, выводит топ по игровому балансу игроков
👮‍♂️ Репорт  - Выводит информацию за систему репортов</b>
🎁 Розыгрыш - Выводит список розыгрышей 
🎁Розыгрышпд - Выводит информацию за систему розыгрыша

ℹ️ Что бы использовать команду , напишите команду сообщением
    ''', parse_mode='html')

@dp.callback_query_handler(text='register_help')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help2 = InlineKeyboardMarkup(row_width=2)
    Osn2 = InlineKeyboardButton(text='Основные 📝', callback_data='Osn2')
    game2 = InlineKeyboardButton(text='Игры 🎮', callback_data='game2')
    rabot2 = InlineKeyboardButton(text='Работы 🔨', callback_data='rabot2')
    Im2 = InlineKeyboardButton(text='Имущество 🏘 ', callback_data='Im2')
    Priv2 = InlineKeyboardButton(text='Привилегии 📖', callback_data='Priv2')
    Adm2 = InlineKeyboardButton(text='Admins menu ⛔️', callback_data='Admins_menu_up')
    Priv = InlineKeyboardButton(text='❕ Остальные ', callback_data='Priv')
    Org = InlineKeyboardButton(text='Организации 🏰 ', callback_data='Org')
    help2.add(Osn2, game2, rabot2, Im2, Priv2, Adm2,Priv,Org)
    await bot.send_message(message.chat.id, f'''
<a href='tg://user?id={user_id}'>{user_name}</a> , Вот информация о боте 🔎

💬 скоро | Игровой чат #1 - Игровой чат
👨‍💻 {owner_bot_name}- Разработчик

➖➖➖➖➖➖➖➖➖➖➖

📖 Доступные категории:

📝 Основные
🎮 Игры 
🔨 Работы
🏘 Имущество
📖 Привилегии
⛔️ Admins menu 
❕ Остальные 

➖➖➖➖➖➖➖➖➖➖➖
↘️Выберите одну из доступных категорий
    ''', reply_markup=help2, parse_mode='html')


@dp.message_handler(lambda message: message.text.lower() == 'кнб')
async def process_command_1(message: types.Message):
    
    button1 = InlineKeyboardButton('🗿Камень', callback_data = '1')
    button2 = InlineKeyboardButton('✂️Ножницы', callback_data = '2')
    button3 = InlineKeyboardButton('📄Бумага', callback_data = '3')
    buttons = InlineKeyboardMarkup().add(button1, button2, button3)
    await bot.send_message(message.chat.id, "🤚 Я готов играть!\n Выбери предмет, чтобы со мной сыграть 🎭", reply_markup= buttons)

@dp.callback_query_handler(lambda c: c.data == '1')
async def process_callback_yes(callback: types.CallbackQuery):
    rand = random.choice(["🪨 Камень", "✂️Ножницы", "📄Бумага"])

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer("Я выбрал " + rand + "\nА ты выбрал 🗿Камень")
    if rand == '🗿Камень':
        await callback.message.answer("У нас ничья🤝")
    elif rand == '✂️Ножницы':
        await callback.message.answer("Ты выиграл🥇")
    else:
        await callback.message.answer("Я победил🥇")

@dp.callback_query_handler(lambda c: c.data == '2')
async def process_callback_yes(callback: types.CallbackQuery):
    rand = random.choice(["🪨 Камень", "✂️Ножницы", "📄Бумага"])

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer("Я выбрал " + rand + "\nА ты выбрал ✂️Ножницы")
    if rand == '🗿Камень':
        await callback.message.answer("Я победил🥇")
    elif rand == '✂️Ножницы':
        await callback.message.answer("У нас ничья🤝")
    else:
        await callback.message.answer("Ты победил🥇")

@dp.callback_query_handler(lambda c: c.data == '2')
async def process_callback_yes(callback: types.CallbackQuery):
    rand = random.choice(["🪨 Камень", "✂️Ножницы", "📄Бумага"])

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer("Я выбрал " + rand + "\nА ты выбрал ✂️Ножницы")
    if rand == '🗿Камень':
        await callback.message.answer("Я победил🥇")
    elif rand == '✂️Ножницы':
        await callback.message.answer("У нас ничья🤝")
    else:
        await callback.message.answer("Ты победил🥇")

@dp.callback_query_handler(lambda c: c.data == '2')
async def process_callback_yes(callback: types.CallbackQuery):
    rand = random.choice(["🗿Камень", "✂️Ножницы", "📄Бумага"])

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer("Я выбрал " + rand + "\nА ты выбрал ✂️Ножницы")
    if rand == '🗿Камень':
        await callback.message.answer("Я победил🥇")
    elif rand == '✂️Ножницы':
        await callback.message.answer("У нас ничья🤝")
    else:
        await callback.message.answer("Ты победил🥇")

@dp.callback_query_handler(lambda c: c.data == '3')
async def process_callback_yes(callback: types.CallbackQuery):
    rand = random.choice(["🗿Камень", "✂️Ножницы", "📄Бумага"])

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer("Я выбрал " + rand + "\nА ты выбрал 📄Бумага")
    if rand == '🗿Камень':
        await callback.message.answer("Ты победил🥇")
    elif rand == '✂️Ножницы':
        await callback.message.answer("Я победил🥇")
    else:
        await callback.message.answer("У нас ничья🤝")

#развлечения
































if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)