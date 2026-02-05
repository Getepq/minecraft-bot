from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.types import PreCheckoutQuery
import handl.keyboard as kb
from db.dbMOD import get_modpack

rt = Router()

@rt.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAOJaYNDGahNdCiOVnbrt48qMYLDb_4AAmUUaxvYzAABSFO9o3XpjZnYAQADAgADeQADOAQ',
                               caption='👋 *Добро пожаловать*\!\n\n🎮 Этот бот создан *игроком для игроков*\!\nЗдесь ты найдешь лучший контент для своей игры:\n▫️ *Мод\-паки* для Minecraft Java ☕️\n▫️ *Аддоны* для Minecraft Bedrock 📱\n\n✨ Наша библиотека обновляется специально для *вас*\!\nМы добавляем именно то, что любят пользователи, и какие сборки вы ждете\.\n\n🚀 _Чтобы посмотреть нашу библеотеку модпаков кнопку ниже\!_',
                               parse_mode="MarkdownV2",
                               reply_markup=kb.main)

@rt.message(F.text == 'мод-паки🖥')
async def ls_modpack(message: Message):
    await message.reply('Тут ниже прикреплены все сборки на данный момент!',
                         reply_markup=await kb.all_modpack())

@rt.message(F.text == 'обо мне📜')
async def about_me(message: Message):
    await message.reply('Я обычный начинающий програмист решивший обучиться фреймворку aiogram.\nЕсли вам понравился мой бот и вы хотите поддержать его работу,то можете пожертвовать копеечку с помощью звёзд или же на DonationAlerts.\nМожете со мной связаться в личные сообщение и предложить свои новооведение в бота или же новые мод паки.\n\nМой тг:@Timye\nМой тгк:https://t.me/progouME')

@rt.message(F.text == 'аддоны📱')
async def addon(message: Message):
    await message.reply('Извините мобайл плееры,я пока что не знаю какие аддоны вам нужны,но вы можете порекомендовать их в мом тгк под постом на эту тему.')

@rt.message(F.text == 'поддержать❤️')
async def donate(message: Message):
    await message.reply('Способы поддержать бота снизу.',
                        reply_markup=kb.donate)

@rt.callback_query(F.data.startswith('donate_'))
async def send_donate(callback: CallbackQuery):
    amount = callback.data.split("_")[1]
    prices = [LabeledPrice(label='XTR', amount=amount)]

    await callback.message.answer_invoice(
        title='Поддержать автора',
        description = f"Донат на развитие проектов в размере {amount} звезд! Спасибо!",
        prices = prices,
        provider_token = "",
        payload = f"donate_payload_{amount}",
        currency = "XTR",
    )
    await callback.answer()

@rt.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@rt.message(F.successful_payment)
async def success_payment_handler(message: Message):
    payment_info = message.successful_payment
    await message.answer(f"Спасибо за донат {payment_info.total_amount} звезд! 🥳")

@rt.callback_query(F.data.startswith("download_"))
async def send_pack_file(callback: CallbackQuery):
    pack_id = callback.data.split("_")[1]

    pack = await get_modpack(pack_id)

    if pack:
        if pack['photo_id']:
            await callback.message.answer_photo(
                photo=pack['photo_id'],
                caption=f"📦 {pack['name']}\n\nℹ️ {pack['description']}\nVersion: {pack['version']}"
            )
        await callback.message.answer_document(document=pack['file_id'])
        await callback.answer()
    else:
        await callback.answer("Ошибка: Модпак не найден", show_alert=True)



