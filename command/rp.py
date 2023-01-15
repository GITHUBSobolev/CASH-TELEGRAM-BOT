from collections import namedtuple
from email import message
from numpy import number
#РП КОМАНДЫ ОТ CASH
@dp.message_handler(commands="обнять")
async def send_hug(message: types.Message):
    your_id = message.from_id
    your_name = message.from_user.username
    try:
        friend_name = message.reply_to_message.from_user.username
        friend_id = message.reply_to_message.from_user.id
        # await message.delete()
        await message.answer(f'[{your_name}](tg://user?id={str(your_id)}) обнял-приподнял [{friend_name}](tg://user?id={str(friend_id)})', parse_mode="Markdown")
    except:
        # await message.delete()
        await message.answer(f'[{your_name}](tg://user?id={str(your_id)}) обнял-приподнял всех друзей', parse_mode="Markdown")