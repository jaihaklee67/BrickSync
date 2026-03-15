using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }

# 스낵 매점(자판기) 시스템을 관리하는 마법의 장치입니다.
snack_stand_device := class(creative_device):

    # -------------------------------------------------------------
    # [1] 매점 테이블에 숨겨둘 3개의 입력 트리거 장치 (색상별로 인식)
    # -------------------------------------------------------------
    @editable GreenButton : input_trigger_device = input_trigger_device{}   # 초록색 블록 인식용 트리거
    @editable YellowButton : input_trigger_device = input_trigger_device{}  # 황색 블록 인식용 트리거
    @editable RedButton : input_trigger_device = input_trigger_device{}     # 빨간색 블록 인식용 트리거

    # -------------------------------------------------------------
    # [2] 간식을 쏟아낼 3개의 아이템 지급 장치 (Item Granter)
    # -------------------------------------------------------------
    @editable GreenGranter : item_granter_device = item_granter_device{}   # 초록색 보상 (사과)
    @editable YellowGranter : item_granter_device = item_granter_device{}  # 황색 보상 (피자)
    @editable RedGranter : item_granter_device = item_granter_device{}     # 빨간색 보상 (포션)

    # -------------------------------------------------------------
    # [3] 게임이 시작될 때 장치들을 준비시키는(귀를 여는) 단계
    # -------------------------------------------------------------
    OnBegin<override>()<suspends>:void=
        # 누군가(혹은 파이썬 브릿지가) 트리거를 작동시키면, 정해진 함수로 연결!
        GreenButton.PressedEvent.Subscribe(OnGreenTriggered)
        YellowButton.PressedEvent.Subscribe(OnYellowTriggered)
        RedButton.PressedEvent.Subscribe(OnRedTriggered)


    # -------------------------------------------------------------
    # [4] 조건문(If-Then) 로직 : "만약 (If) 이 색상 버튼이 눌리면, 그러면 (Then) 이 간식을 주어라!"
    # -------------------------------------------------------------
    
    # 만약(If) 초록색 블록(버튼)이 인식된다면?
    OnGreenTriggered(Player:agent):void=
        # 그러면(Then) 초록색에 맞는 사과를 쏟아내라!
        GreenGranter.GrantItem(Player)

    # 만약(If) 황색 블록(버튼)이 인식된다면?
    OnYellowTriggered(Player:agent):void=
        # 그러면(Then) 황색에 맞는 피자를 쏟아내라!
        YellowGranter.GrantItem(Player)

    # 만약(If) 빨간색 블록(버튼)이 인식된다면?
    OnRedTriggered(Player:agent):void=
        # 그러면(Then) 빨간색에 맞는 포션을 쏟아내라!
        RedGranter.GrantItem(Player)
