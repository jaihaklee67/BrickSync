using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /Fortnite.com/Characters }
using { /UnrealEngine.com/Temporary/SpatialMath }

ferris_wheel_controller := class(creative_device):

    @editable
    WheelProp : creative_prop = creative_prop{}

    # 아까 지정하신 커스텀 키 번호 (예: 11번, 12번, 13번 트리거 장치 연결)
    @editable
    TriggerLeft_CCW : input_trigger_device = input_trigger_device{}  # '[' 키
    
    @editable
    TriggerRight_CW : input_trigger_device = input_trigger_device{}  # ']' 키
    
    @editable
    TriggerStop : input_trigger_device = input_trigger_device{}      # '\' 키

    @editable
    RotateSpeed : float = 45.0 # 1초당 도는 각도 (에디터 조절 가능)
    
    @editable
    MutatorZone : mutator_zone_device = mutator_zone_device{}

    var CurrentDir : float = 0.0
    var IsRotating : logic = false
    var CurrentDriver : ?agent = false

    OnBegin<override>()<suspends>:void=
        TriggerLeft_CCW.PressedEvent.Subscribe(OnTurnLeft)
        TriggerRight_CW.PressedEvent.Subscribe(OnTurnRight)
        TriggerStop.PressedEvent.Subscribe(OnStop)
        
        MutatorZone.AgentEntersEvent.Subscribe(OnPlayerEntered)
        MutatorZone.AgentExitsEvent.Subscribe(OnPlayerExited)

    OnPlayerEntered(Agent : agent):void=
        set CurrentDriver = option{Agent}
        TriggerLeft_CCW.Register(Agent)
        TriggerRight_CW.Register(Agent)
        TriggerStop.Register(Agent)

    OnPlayerExited(Agent : agent):void=
        set CurrentDriver = false
        TriggerLeft_CCW.Unregister(Agent)
        TriggerRight_CW.Unregister(Agent)
        TriggerStop.Unregister(Agent)

    OnTurnLeft(Agent:agent):void=
        if (Driver := CurrentDriver?, Driver = Agent):
            set CurrentDir = -1.0
            if (not IsRotating?):
                spawn{ RotateLoop() }

    OnTurnRight(Agent:agent):void=
        if (Driver := CurrentDriver?, Driver = Agent):
            set CurrentDir = 1.0
            if (not IsRotating?):
                spawn{ RotateLoop() }

    OnStop(Agent:agent):void=
        if (Driver := CurrentDriver?, Driver = Agent):
            set IsRotating = false

    # 1초마다 지속적으로 부드럽게 회전시키는 엔진
    RotateLoop()<suspends>:void=
        set IsRotating = true
        loop:
            if (IsRotating?):
                CurrentTF := WheelProp.GetTransform()
                # 관람차의 축(Roll) 방향으로 회전. 모형에 따라 X, Y, Z축 변경이 필요할 수 있습니다.
                RotationDelta := MakeRotation(vector3{X:=1.0, Y:=0.0, Z:=0.0}, DegreesToRadians(RotateSpeed * CurrentDir))
                WheelProp.MoveTo(CurrentTF.Translation, CurrentTF.Rotation.RotateBy(RotationDelta), 1.0)
            else:
                break
