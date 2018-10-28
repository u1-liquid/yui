from ...box import box
from ...event import Message


@box.command('help', ['도움', '도움말'])
async def help(bot, event: Message, raw: str):
    """
    봇 명령어들의 도움말 모음

    `{PREFIX}help` (전체 명령어 목록)
    `{PREFIX}help quit` (개별 명령어 도움말)

    """
    p = bot.config.PREFIX
    if raw == '':
        await bot.say(
            event.channel,
            '\n'.join(
                a.get_short_help(p)
                for a in bot.box.apps if a.has_short_help
            ),
            thread_ts=event.ts,
        )
    else:
        apps = [
            h for h in bot.box.apps
            if h.has_short_help and raw in h.names
        ]

        if apps:
            if len(apps) == 1:
                a = apps[0]
                try:
                    help = a.get_full_help(p)
                except NotImplementedError:
                    help = a.get_short_help(p)

                await bot.say(
                    event.channel,
                    help,
                    thread_ts=event.ts,
                )
            else:
                await bot.say(
                    event.channel,
                    '\n'.join(a.get_short_help(p) for a in apps),
                    thread_ts=event.ts,
                )
        else:
            await bot.say(
                event.channel,
                '그런 명령어는 없어요!',
                thread_ts=event.ts,
            )
