from ...box import box
from ...command import C
from ...event import TeamJoin

box.assert_channel_required('welcome')


@box.on(TeamJoin)
async def welcome_item4(bot, event: TeamJoin):
    await bot.say(
        C.welcome.get(),
        f'<@{event.user.id}>님 item4 개인 Slack에 오신걸 환영합니다! :tada:\n'
        f'갑자기 알림이 울려서 놀라셨죠? 저는 Slack 봇 유이라고 해요. '
        f'제 도움이 필요하면 언제든지 `{bot.config.PREFIX}도움`을 입력해서 '
        f'도움말을 확인해주세요!\n\n'
        f'먼저, 다른 참가자분들과 구분하기 쉽도록 프로필 사진 설정을 부탁드립니다.\n\n'
        f'item4 개인 슬랙에는 다음과 같은 채널들이 있으니 참가해보셔도 좋을 것 같아요!\n\n'
        f'- #_general - 일상적인 대화는 여기서 하면 돼요.\n'
        f'- #_notice - 공지사항이 올라오는 곳이에요. 여기는 읽기만 가능해요.\n'
        f'- #dev - 개발/개발자에 대한 이야기를 하는 곳이에요.\n'
        f'- #gender - 성별 이슈, 성 소수자 등에 대한 주제들을 위한 특별 채널이에요.\n'
        f'- #subculture - 서브컬쳐 덕질은 여기서 하면 됩니다.\n'
        f'- #suggest - 슬랙 운영에 대한 건의는 여기서 해주세요\n'
        f'- #test - 제게 이것저것 시켜보고 싶으실 땐 이곳에서 해주세요!\n\n'
        f'이 외에도 채널들이 있으니 천천히 찾아보세요! '
        f'그럼 즐거운 Slack 이용이 되셨으면 좋겠습니다! 잘 부탁드려요!',
    )
