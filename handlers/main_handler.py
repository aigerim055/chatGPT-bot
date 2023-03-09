from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import Message

from api.api import Api
from decouple import config

router = Router()
api = Api(config('API'))

@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>")


@router.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward received message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker and etc.)
    """
    print(await api.get_response(message))
    try:
        # Send copy of the received message
        await message.answer(await api.get_response(message.text))
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
