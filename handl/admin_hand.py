from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from db.dbMOD import add_modpack, delete_modpack
import handl.keyboard as kb

ADMIN_ID = [8467563699]

rt = Router()

class AddModpackState(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_version = State()
    waiting_for_category = State()
    waiting_for_photo = State()
    waiting_for_file = State()


def is_admin(user_id):
    return user_id in ADMIN_ID

@rt.message(Command('del'))
async def process_del(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer(
        'МОДПАК УДАЛЯЕТСЯ СРАЗУ ПРИ НАЖАТИИ!\nНажмите на кнопку, чтобы удалить модпак:',
        reply_markup=await kb.all_modpack(prefix="delete")
    )

@rt.callback_query(F.data.startswith("delete_"))
async def delete_pack_handler(callback: CallbackQuery):
    pack_id = callback.data.split("_")[1]
    try:
        await delete_modpack(pack_id)
        await callback.message.edit_text("Модпак удален.")
        await callback.answer("Удалено")
    except Exception as e:
        await callback.answer(f"Ошибка: {e}", show_alert=True)

@rt.message(Command("add"))
async def start_add(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await message.answer("Добавление модпака.\n\nВведите название:")
    await state.set_state(AddModpackState.waiting_for_name)

@rt.message(AddModpackState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание:")
    await state.set_state(AddModpackState.waiting_for_description)

@rt.message(AddModpackState.waiting_for_description)
async def process_desc(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите для какой версии и загрузчик:")
    await state.set_state(AddModpackState.waiting_for_version)

@rt.message(AddModpackState.waiting_for_version)
async def process_version(message: types.Message, state: FSMContext):
    await state.update_data(version=message.text)
    await message.answer("Введите категорию:")
    await state.set_state(AddModpackState.waiting_for_category)

@rt.message(AddModpackState.waiting_for_category)
async def process_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Теперь отправь мне фото для модпака:")
    await state.set_state(AddModpackState.waiting_for_photo)

@rt.message(AddModpackState.waiting_for_photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await message.answer("Теперь скинь ZIP-файл с модпаком:")
    await state.set_state(AddModpackState.waiting_for_file)

@rt.message(AddModpackState.waiting_for_file, F.document)
async def process_file(message: types.Message, state: FSMContext):
    if 'zip' not in message.document.mime_type and not message.document.file_name.endswith('.zip'):
        await message.answer("Отправьте именно ZIP архив!")
        return

    file_id = message.document.file_id
    data = await state.get_data()

    try:
        await add_modpack(
            name=data['name'],
            description=data['description'],
            version=data['version'],
            category=data['category'],
            photo_id=data['photo_id'],
            file_id=file_id
        )
        await message.answer(f"Модпак {data['name']} добавлен!")
    except Exception as e:
        await message.answer(f"Ошибка при сохранении: {e}")

    await state.clear()



