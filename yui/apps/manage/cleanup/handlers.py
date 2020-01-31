from .models import EventLog
from ....box import box
from ....command import Cs
from ....event import Message


@box.on(Message)
@box.on(Message, subtype='message_replied')
@box.on(Message, subtype='bot_message')
@box.on(Message, subtype='channel_join')
@box.on(Message, subtype='channel_leave')
async def make_log(bot, event: Message, sess):
    try:
        channels = Cs.auto_cleanup_targets.gets()
    except KeyError:
        return True

    if event.channel in channels:
        log = EventLog(channel=event.channel.id, ts=event.ts)
        with sess.begin():
            sess.add(log)
    return True