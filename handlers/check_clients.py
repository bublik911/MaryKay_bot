from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Text

router = Router()


@router.message(
    Text("📕Проверить клиентскую базу")
)
async def check_base(message: Message):
    pass
