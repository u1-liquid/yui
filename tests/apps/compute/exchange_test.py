import re

import pytest

from yui.apps.compute.exchange import exchange
from yui.utils import json

from ...util import FakeBot

YEN_PATTERN = re.compile(
    r'100 JPY == (?:\.?\d+,?)+ KRW \(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\)'
)


@pytest.mark.asyncio
async def test_exchange_command():
    bot = FakeBot()
    bot.add_channel('C1', 'test')
    bot.add_user('U1', 'tester')
    event = bot.create_message('C1', 'U1')

    await exchange(bot, event, '100엔')

    said = bot.call_queue.pop(0)
    assert said.method == 'chat.postMessage'
    assert said.data['channel'] == 'C1'
    assert YEN_PATTERN.match(said.data['text'])

    await exchange(bot, event, '100 JPY to KRW')

    said = bot.call_queue.pop(0)
    assert said.method == 'chat.postMessage'
    assert said.data['channel'] == 'C1'
    assert YEN_PATTERN.match(said.data['text'])

    await exchange(bot, event, '100원')

    said = bot.call_queue.pop(0)
    assert said.method == 'chat.postMessage'
    assert said.data['channel'] == 'C1'
    assert said.data['text'] == '변환하려는 두 화폐가 같은 단위에요!'

    await exchange(bot, event, '100 BTC')

    said = bot.call_queue.pop(0)
    assert said.method == 'chat.postMessage'
    assert said.data['channel'] == 'C1'
    assert said.data['text'] == '지원되는 통화기호가 아니에요!'

    await exchange(bot, event, '아무말 대잔치')

    said = bot.call_queue.pop(0)
    assert said.method == 'chat.postMessage'
    assert said.data['channel'] == 'C1'
    assert said.data['text'] == '주문을 이해하는데에 실패했어요!'


@pytest.mark.asyncio
async def test_exchange_error(response_mock):
    response_mock.get(
        'https://api.manana.kr/exchange/rate.json?base=KRW&code=JPY',
        body=json.dumps([False]),
        headers={'Content-Type': 'application/json'},
    )
    bot = FakeBot()
    bot.add_channel('C1', 'test')
    bot.add_user('U1', 'tester')
    event = bot.create_message('C1', 'U1')

    await exchange(bot, event, '100엔')

    said = bot.call_queue.pop(0)
    assert said.method == 'chat.postMessage'
    assert said.data['channel'] == 'C1'
    assert said.data['text'] == '알 수 없는 에러가 발생했어요! 아빠에게 문의해주세요!'
