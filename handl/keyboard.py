from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import  InlineKeyboardBuilder
from db.dbMod import get_all_modpacks #get_all_categories

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='мод-паки🖥')],
    [KeyboardButton(text='аддоны📱')],
    [KeyboardButton(text='обо мне📜'),KeyboardButton(text='поддержать❤️')]
],
resize_keyboard=True,
input_field_placeholder='выберите что вы хотите скачать!')

#async def categories_kb():
    #categories = await get_all_categories()
    #keyboard = InlineKeyboardBuilder()
    #if not categories:
       # return None

   # for category in categories:
       # cat_name = category
       # cat_code = category
       # keyboard.add(InlineKeyboardButton(
          #  text=f"📂 {cat_name.capitalize()}",
          #  callback_data=f"cat_{cat_code}"
      #  ))
   # return keyboard.adjust(2).as_markup()

donate = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='donationalerts', url='https://www.donationalerts.com/r/timye')],
    [InlineKeyboardButton(text='5⭐️', callback_data='donate_5'),
     InlineKeyboardButton(text='10⭐️', callback_data='donate_10')],
    [InlineKeyboardButton(text='25⭐️', callback_data='donate_25'),
     InlineKeyboardButton(text='40⭐️', callback_data='donate_40')],
    [InlineKeyboardButton(text='50⭐️', callback_data='donate_50')],
])

async def all_modpack(prefix="download"):
    keyboard = InlineKeyboardBuilder()
    modpacks = await get_all_modpacks()
    for modpack in modpacks:
        btn_text = f"{modpack['name']} | v{modpack['version']}"
        btn_callback = f"{prefix}_{modpack['id']}"
        keyboard.add(InlineKeyboardButton(text=btn_text, callback_data=btn_callback))
    return keyboard.adjust(1).as_markup()
