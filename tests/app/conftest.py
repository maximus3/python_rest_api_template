import datetime
from unittest.mock import AsyncMock, Mock

import pytest
from aiogram import types


@pytest.fixture(name='bot')
async def bot_fixture():
    """Bot fixture"""
    _bot = Mock()
    _bot.send_document = AsyncMock()
    _bot.send_message = AsyncMock()
    _bot.send_message.return_value = types.Message(
        message_id=46456,
        chat=types.Chat(id=1, type='type'),
        date=datetime.datetime.now(),
    )
    _bot.send_media_group = AsyncMock()
    _bot.pin_chat_message = AsyncMock()
    _bot.edit_message_text = AsyncMock()
    yield _bot


@pytest.fixture
async def mock_bot(mocker, bot):
    """Mock bot fixture"""
    mock = mocker.patch('app.bot_helper.bot.bot', bot)
    return mock


@pytest.fixture
def mock_message_id(mocker):
    """Mock message id fixture"""
    mock = mocker.patch(
        'app.bot_helper.send.ping_status.MESSAGE_ID',
        types.Message(
            message_id=453534,
            chat=types.Chat(id=1, type='type'),
            date=datetime.datetime.now(),
        ),
    )
    return mock
