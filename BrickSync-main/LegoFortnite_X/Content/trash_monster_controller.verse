using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { /UnrealEngine.com/Temporary/SpatialMath }

trash_monster_controller := class(creative_device):
    # 대상 레고 블록 (위턱)
    @editable TopJaw : creative_prop = creative_prop{}
    
    # H키와 J키를 입력받을 인풋 트리거 2개
    @editable OpenTrigger : input_trigger_device = input_trigger_device{}
    @editable CloseTrigger : input_trigger_device = input_trigger_device{}

    # [추가] 플레이어 진입을 감지할 뮤테이터 존
    @editable MutatorZone : mutator_zone_device = mutator_zone_device{}
    
    # 턱관절 회전 방향과 각도 설정
    @editable RotationAxis : vector3 = vector3{X := 0.0, Y := 1.0, Z := 0.0}
    @editable RotateAngleDegrees : float = 45.0
    
    # 입 벌어지는 속도 (몇 초 만에 열릴지)
    @editable DurationSeconds : float = 1.0

    var OriginalTransform : transform = transform{}

    OnBegin<override>()<suspends>:void=
        # 게임 시작 시 턱이 닫혀있는 "원래 위치"를 영구 기억함
        set OriginalTransform = TopJaw.GetTransform()
        
        # H와 J키가 눌리면 함수 발동!
        OpenTrigger.PressedEvent.Subscribe(OnOpenPressed)
        CloseTrigger.PressedEvent.Subscribe(OnClosePressed)

        # 뮤테이터 존 진입/퇴장 이벤트 연결
        MutatorZone.AgentEntersEvent.Subscribe(OnPlayerEntered)
        MutatorZone.AgentExitsEvent.Subscribe(OnPlayerExited)

        # 시작 시 이미 구역 내에 있는 플레이어 즉시 등록
        for (Player : GetPlayspace().GetPlayers()):
            if (MutatorZone.IsInVolume[Player]):
                OnPlayerEntered(Player)

    # 구역 진입 시 트리거 작동 활성화
    OnPlayerEntered(Agent : agent):void=
        OpenTrigger.Register(Agent)
        CloseTrigger.Register(Agent)
        Print("플레이어가 제어 영역에 진입했습니다. 단축키 활성화.")

    # 구역 퇴장 시 트리거 작동 비활성화
    OnPlayerExited(Agent : agent):void=
        OpenTrigger.Unregister(Agent)
        CloseTrigger.Unregister(Agent)
        Print("플레이어가 제어 영역을 벗어났습니다. 단축키 비활성화.")

    OnOpenPressed(Agent : agent):void=
        spawn{ OpenJaw() }

    OnClosePressed(Agent : agent):void=
        spawn{ CloseJaw() }

    # [시소 파괴 메커니즘 1: 절대 좌표 강제 45도 이동]
    OpenJaw()<suspends>:void=
        RadianAngle := DegreesToRadians(RotateAngleDegrees)
        LocalRotation := MakeRotation(RotationAxis, RadianAngle)
        
        # 이곳이 컴파일 에러를 일으킨 수학 기호 수정본입니다!
        TargetRotation := OriginalTransform.Rotation.RotateBy(LocalRotation)
        
        TopJaw.MoveTo(OriginalTransform.Translation, TargetRotation, DurationSeconds)

    # [시소 파괴 메커니즘 2: 원점 강제 복귀]
    CloseJaw()<suspends>:void=
        TopJaw.MoveTo(OriginalTransform.Translation, OriginalTransform.Rotation, DurationSeconds)
