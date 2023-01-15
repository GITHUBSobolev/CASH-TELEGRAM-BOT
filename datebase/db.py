import sqlite3
from aiogram import Bot, Dispatcher, executor, types

connect = sqlite3.connect("datebase/users.db")
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id BIGINT NOT NULL,
    level INT NOT NULL,
    balance NUMERIC,
    bank NUMERIC NOT NULL,
    fantom NUMERIC NOT NULL,
    ecoins NUMERIC NOT NULL,
    energy INT NOT NULL,
    expe NUMERIC NOT NULL,
    games INT NOT NULL,
    user_name text NOT NULL,
    user_status text NOT NULL,
    rating NUMERIC NOT NULL,
    work INT NOT NULL,
    pet1 INT NOT NULL,
    pet2 INT NOT NULL,
    pet3 INT NOT NULL,
    pet4 INT NOT NULL,
    pet5 INT NOT NULL,
    pet6 INT NOT NULL,
    pet7 INT NOT NULL,
    pet8 INT NOT NULL,
    pet9 INT NOT NULL,
    pet10 INT NOT NULL,
    pet_name text NOT NULL,
    pet_hp INT NOT NULL,
    pet_eat INT NOT NULL,
    pet_mood INT NOT NULL,
    checking INT NOT NULL,
    checking1 INT NOT NULL,
    checking2 INT NOT NULL,
    checking3 INT NOT NULL,
    status_block text NOT NULL,
    cards INT NOT NULL,
    ferma NUMERIC NOT NULL ,
    ferma_money NUMERIC NOT NULL ,
    Farm INT NOT NULL ,
    case1 NUMERIC,
    case2 NUMERIC,
    case3 NUMERIC,
    case4 NUMERIC,
    limitpered NUMERIC,
    bonus INT,
    cardslimit NUMERIC,
    limitbank NUMERIC,
    bonusvip INT,
    bonusprem INT,
    limitvidach NUMERIC,
    limitvidach2 NUMERIC,
    bal INT,
    referrer_id NUMERIC,
    countref NUMERIC,
    game NUMERIC,
    warn INT,
    marry NUMERIC,
    marry_time NUMERIC,
    marry_date timestamp,
    stavka INT,
    num_lose INT,
    num_win INT
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS ferma(
    user_id NUMERIC NOT NULL ,
    user_name text NOT NULL ,
    ferma INT NOT NULL ,
    balance NUMERIC NOT NULL 
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS cooldown(
            cd_ferma INT,
            kurs INT,
            cd_bank INT,
            cd_energy INT,
            cd_limit NUMERIC,
            cd_bonus INT,
            cd_clan NUMERIC
            )""")
cursor.execute("""CREATE TABLE IF NOT EXISTS mine(
    user_id NUMERIC NOT NULL,
    user_name text NOT NULL,
    iron NUMERIC NOT NULL,
    gold NUMERIC NOT NULL,
    diamonds NUMERIC NOT NULL,
    amethysts NUMERIC NOT NULL,
    aquamarine NUMERIC NOT NULL,
    emeralds NUMERIC NOT NULL

)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS workshop(
    user_id NUMERIC NOT NULL,
    user_name text NOT NULL,
    work_shop INT NOT NULL,
    workshop_c INT NOT NULL
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS property(
    user_id NUMERIC NOT NULL,
    user_name text NOT NULL,
    have text NOT NULL,
    yacht INT NOT NULL,
    cars INT NOT NULL,
    plane INT NOT NULL,
    helicopter INT NOT NULL,
    house INT NOT NULL,
    phone INT NOT NULL

)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS business(
    user_id NUMERIC NOT NULL ,
    user_name text NOT NULL ,
    business INT NOT NULL ,
    balance NUMERIC NOT NULL ,
    workers NUMERIC,
    have text NOT NULL
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS bot(
    chat_id NUMERIC NOT NULL,
    last_stavka NUMERIC NOT NULL

)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS bot_bonus(
    user_id NUMERIC NOT NULL,
    last_stavka NUMERIC NOT NULL
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS bot_work(
    user_id NUMERIC NOT NULL,
    last_stavka NUMERIC NOT NULL
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS ban_list(
    user_id NUMERIC NOT NULL,
    user_name text NOT NULL,
    Cause text NOT NULL,
    time NUMERIC
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS fzve(
    user_id NUMERIC ,
    money NUMERIC ,
    bill_id text NOT NULL
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS kurs(
    valut NUMERIC ,
    valut2 NUMERIC ,
    valut3 NUMERIC,
    valut4 NUMERIC
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS wdzy(
    summ NUMERIC,
    wdz text
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS cars(
    user_id NUMERIC,
    user_name text,
    hp INT,
    benz INT
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS promo(
    user_id NUMERIC,
    user_name text,
    activ NUMERIC,
    summ NUMERIC,
    name text,
    comment text
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS promold(
    user_id NUMERIC,
    user_name text,
    name text
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS clan(
    user_id NUMERIC,
    user_name text,
    status text,
    clan_id NUMERIC,
    clan_name text)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS clans(
    members NUMERIC,
    clan_id NUMERIC,
    clan_name text,
    kazna NUMERIC,
    type_clan INT,
    new_clan_id NUMERIC,
    power NUMERIC,
    win NUMERIC,
    lose NUMERIC,
    last_stavka NUMERIC NOT NULL
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS clans_id(
    new_clan_id NUMERIC
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS city(
    citizens NUMERIC,
    user_id NUMERIC,
    user_name text,
    kazna NUMERIC,
    city_name text,
happynes NUMERIC,
    electricity NUMERIC,
    water NUMERIC,
    factory NUMERIC,
    road NUMERIC NOT NULL,
    houses NUMERIC,
    work_place NUMERIC,
    taxes NUMERIC,
    material NUMERIC

)
""")

marry_me = []
marry_rep = []
divorce_me = []
divorce_rep = []
first_p=[]
second_p=[]
summ_stavka=[]
def add_check(user_id, money, bill_id):
    cursor.execute("INSERT INTO fzve VALUES(%s, %s ,%s)",
                   (user_id, money, bill_id,))
    connect.commit()


def get_check(bill_id):
    result = cursor.execute("SELECT * FROM fzve WHERE bill_id =%s", (bill_id,))
    result = cursor.fetchone()
    if not bool(len(result)):
        return False
    return result[0]



def is_number(_str):
    try:
        int(_str)
    except ValueError:
        return False

async def get_marry(message: types.Message):
    user = message.from_user
    marry = cursor.execute("SELECT marry FROM users WHERE user_id=%s", (user.id,))
    marry=cursor.fetchall()
    return marry

async def get_rang(message: types.Message):
    user = message.from_user
    cursor.execute("SELECT * FROM users WHERE user_id=%s", (user.id,))
    data = cursor.fetchone()
    return data

async def reply_get_rang(message: types.Message):
    reply = message.reply_to_message
    replyuser = reply.from_user
    cursor.execute("SELECT * FROM users WHERE user_id=%s", (replyuser.id,))
    data = cursor.fetchone()
    return data
async def get_clan(message: types.Message):
    user = message.from_user
    cursor.execute("SELECT * FROM clan WHERE user_id=%s", (user.id,))
    data_c = cursor.fetchone()
    return data_c