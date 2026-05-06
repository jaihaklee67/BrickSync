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

    var TargetDir : float = 0.0
    var IsMoving : logic = false
    var CurrentDriver : ?agent = false
    var TargetAngle : float = 0.0

    # 누적 오차(관람차 찌그러짐)를 막기 위한 절대 기준점 변수
    var InitialRotation : rotation = rotation{}
    var InitialPosition : vector3 = vector3{}
    var CurrentAngle : float = 0.0

    OnBegin<override>()<suspends>:void=
        # 처음 시작할 때의 관람차 위치와 기울기를 '성역'으로 영구 저장
        set InitialRotation = WheelProp.GetTransform().Rotation
        set InitialPosition = WheelProp.GetTransform().Translation

        TriggerLeft_CCW.PressedEvent.Subscribe(OnTurnLeft)
        TriggerRight_CW.PressedEvent.Subscribe(OnTurnRight)
        TriggerStop.PressedEvent.Subscribe(OnStop)
        
        MutatorZone.AgentEntersEvent.Subscribe(OnPlayerEntered)
        MutatorZone.AgentExitsEvent.Subscribe(OnPlayerExited)
        
        # 단일 안전 엔진 시동
        spawn{ SafeDriveLoop() }

    OnPlayerEntered(Agent : agent):void=
        set CurrentDriver = option{Agent}
        TriggerLeft_CCW.Register(Agent)
        TriggerRight_CW.Register(Agent)
        TriggerStop.Register(Agent)

    OnPlayerExited(Agent : agent):void=
        # 플레이어가 튕겨나가도 조종 권한(h,j,k 등)을 뺏지 않음!
        # set CurrentDriver = false
        # TriggerLeft_CCW.Unregister(Agent) 등 주석 처리
        set TargetAngle = TargetAngle

    OnTurnLeft(Agent:agent):void=
        if (Driver := CurrentDriver?, Driver = Agent):
            set TargetDir = -1.0
            set IsMoving = true
            set TargetAngle = CurrentAngle - 99999.0 # 정확히 1바퀴 족쇄를 풀고 무한대 역회전 개방

    OnTurnRight(Agent:agent):void=
        if (Driver := CurrentDriver?, Driver = Agent):
            set TargetDir = 1.0
            set IsMoving = true
            set TargetAngle = CurrentAngle + 99999.0 # 정확히 1바퀴 족쇄를 풀고 무한대 회전 개방

    OnStop(Agent:agent):void=
        if (Driver := CurrentDriver?, Driver = Agent):
            set IsMoving = false
            set TargetAngle = CurrentAngle # K키 즉시 정지용

    # 절대 방어 회전 엔진: 1바퀴 정밀 회전 후 자동 브레이크 작동
    SafeDriveLoop()<suspends>:void=
        loop:
            if (IsMoving?):
                # 1. 0.5초 동안 돌아갈 스텝 각도 누적 계산
                var Step : float = RotateSpeed * TargetDir * 0.5
                var NewAngle : float = CurrentAngle + Step
                
                # 2. 이번 단계에서 목표치(360도)에 도달했는지 검사하여 자동차 멈추듯 자동 브레이크
                if (TargetDir > 0.0 and NewAngle >= TargetAngle):
                    set NewAngle = TargetAngle
                    set IsMoving = false
                else if (TargetDir < 0.0 and NewAngle <= TargetAngle):
                    set NewAngle = TargetAngle
                    set IsMoving = false
                    
                set CurrentAngle = NewAngle
                
                # 3. 누적(Current)이 아닌 초기 상태(Initial)에서 매번 새롭게 절대 회전값 산출
                LocalDeltaRot := MakeRotation(vector3{X:=1.0, Y:=0.0, Z:=0.0}, DegreesToRadians(CurrentAngle))
                NewRotation := InitialRotation.RotateBy(LocalDeltaRot)
                
                # 5. 처음 위치한 좌표 절대 고정! 관람차 탈선(시소 이펙트) 물리적 절대 불가
                WheelProp.MoveTo(InitialPosition, NewRotation, 0.5)

                # 6. [불사조 패치] MoveTo 취소로 인한 먹통 엔진 폭주 방어 쿨타임
                Sleep(0.01)
            else:
                Sleep(0.1)
                # 엔진이 완전히 멈춰서 휴식 중일 때만 남몰래 각도 정리 (-360도 깎기로 인한 역주행 버그 원천 차단!!)
                if (CurrentAngle >= 360.0):
                    set CurrentAngle -= 360.0
                    set TargetAngle -= 360.0
                if (CurrentAngle <= -360.0):
                    set CurrentAngle += 360.0
                    set TargetAngle += 360.0
