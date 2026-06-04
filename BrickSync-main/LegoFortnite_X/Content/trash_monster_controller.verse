using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { /UnrealEngine.com/Temporary/SpatialMath }

trash_monster_controller := class(creative_device):
    # 대상 레고 블록 (위턱)
    @editable TopJaw : creative_prop = creative_prop{}
    
    # Z키와 X키를 입력받을 인풋 트리거 2개
    @editable OpenTrigger : input_trigger_device = input_trigger_device{}
    @editable CloseTrigger : input_trigger_device = input_trigger_device{}
    
    # 턱관절 회전 방향과 각도 설정
    @editable RotationAxis : vector3 = vector3{X := 0.0, Y := 1.0, Z := 0.0}
    @editable RotateAngleDegrees : float = 45.0
    
    # 입 벌어지는 속도 (몇 초 만에 열릴지)
    @editable DurationSeconds : float = 1.0

    var OriginalTransform : transform = transform{}

    OnBegin<override>()<suspends>:void=
        # 게임 시작 시 턱이 닫혀있는 "원래 위치"를 영구 기억함
        set OriginalTransform = TopJaw.GetTransform()
        
        # Z와 X키가 눌리면 함수 발동!
        OpenTrigger.PressedEvent.Subscribe(OnOpenPressed)
        CloseTrigger.PressedEvent.Subscribe(OnClosePressed)

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
