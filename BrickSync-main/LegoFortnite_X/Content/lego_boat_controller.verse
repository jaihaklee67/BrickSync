using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /Fortnite.com/Characters }
using { /UnrealEngine.com/Temporary/SpatialMath }

lego_boat_controller := class(creative_device):

    @editable
    BoatRoot : creative_prop = creative_prop{}

    @editable
    VehicleChair : chair_device = chair_device{}

    # 키보드/브릭싱크 연동 입력 트리거
    @editable TriggerForward : input_trigger_device = input_trigger_device{}
    @editable TriggerBackward : input_trigger_device = input_trigger_device{}
    @editable TriggerLeft : input_trigger_device = input_trigger_device{}
    @editable TriggerRight : input_trigger_device = input_trigger_device{}

    # 월드 내 배치되는 물리 버튼 4개
    @editable ButtonForward : button_device = button_device{}
    @editable ButtonBackward : button_device = button_device{}
    @editable ButtonLeft : button_device = button_device{}
    @editable ButtonRight : button_device = button_device{}

    # 함정 구역 디바이스 (배열 형태로 변경)
    @editable BouncerZones : []mutator_zone_device = array{}
    @editable ChillerZones : []mutator_zone_device = array{}

    @editable MoveDistance : float = 512.0
    @editable MoveTime : float = 0.9
    @editable ForwardMultiplier : float = 1.0
    
    @editable RotateAngle : float = 45.0
    @editable RotateTime : float = 0.5

    @editable ForwardAxisX : float = 0.0
    @editable ForwardAxisY : float = 0.0
    @editable ForwardAxisZ : float = -1.0

    @editable SteerAxisX : float = 0.0
    @editable SteerAxisY : float = 1.0
    @editable SteerAxisZ : float = 0.0

    # 바운서 충돌 설정
    @editable BounceDistance : float = 400.0
    @editable BounceHeight : float = 150.0
    @editable BounceDuration : float = 0.4

    var IsMoving : logic = false
    var CurrentDriver : ?agent = false
    
    # 상태 제어 플래그
    var IsStunned : logic = false
    var IsFrozen : logic = false

    OnBegin<override>()<suspends>:void=
        # 입력 트리거 이벤트 구독
        TriggerForward.PressedEvent.Subscribe(OnForward)
        TriggerBackward.PressedEvent.Subscribe(OnBackward)
        TriggerLeft.PressedEvent.Subscribe(OnLeft)
        TriggerRight.PressedEvent.Subscribe(OnRight)

        # 물리 버튼 이벤트 구독
        ButtonForward.InteractedWithEvent.Subscribe(OnBtnForward)
        ButtonBackward.InteractedWithEvent.Subscribe(OnBtnBackward)
        ButtonLeft.InteractedWithEvent.Subscribe(OnBtnLeft)
        ButtonRight.InteractedWithEvent.Subscribe(OnBtnRight)

        # 의자 탑승 이벤트 구독
        VehicleChair.SeatedEvent.Subscribe(OnPlayerSeated)
        VehicleChair.ExitedEvent.Subscribe(OnPlayerExited)

        # 물리 함정 감지 영역 배열 바인딩
        for (Zone : BouncerZones):
            Zone.AgentEntersEvent.Subscribe(OnBouncerTriggered)

        for (Zone : ChillerZones):
            Zone.AgentEntersEvent.Subscribe(OnChillerEntered)
            Zone.AgentExitsEvent.Subscribe(OnChillerExited)

    # --- 의자 탑승 핸들러 ---
    OnPlayerSeated(Agent : agent):void=
        set CurrentDriver = option{Agent}
        TriggerForward.Register(Agent)
        TriggerBackward.Register(Agent)
        TriggerLeft.Register(Agent)
        TriggerRight.Register(Agent)

    OnPlayerExited(Agent : agent):void=
        set CurrentDriver = false
        TriggerForward.Unregister(Agent)
        TriggerBackward.Unregister(Agent)
        TriggerLeft.Unregister(Agent)
        TriggerRight.Unregister(Agent)

    # --- 입력 트리거 (키보드/브릭싱크) 조종 핸들러 ---
    OnForward(Agent:agent):void=
        if (not IsMoving?, not IsStunned?, Driver := CurrentDriver?, Driver = Agent):
            spawn{ MoveBoatSafe(1.0) }

    OnBackward(Agent:agent):void=
        if (not IsMoving?, not IsStunned?, Driver := CurrentDriver?, Driver = Agent):
            spawn{ MoveBoatSafe(-1.0) }

    OnLeft(Agent:agent):void=
        if (not IsMoving?, not IsStunned?, Driver := CurrentDriver?, Driver = Agent):
            spawn{ RotateBoatSafe(-1.0) }

    OnRight(Agent:agent):void=
        if (not IsMoving?, not IsStunned?, Driver := CurrentDriver?, Driver = Agent):
            spawn{ RotateBoatSafe(1.0) }

    # --- 월드 물리 버튼 조종 핸들러 ---
    OnBtnForward(Agent:agent):void=
        if (not IsMoving?, not IsStunned?):
            spawn{ MoveBoatSafe(1.0) }

    OnBtnBackward(Agent:agent):void=
        if (not IsMoving?, not IsStunned?):
            spawn{ MoveBoatSafe(-1.0) }

    OnBtnLeft(Agent:agent):void=
        if (not IsMoving?, not IsStunned?):
            spawn{ RotateBoatSafe(-1.0) }

    OnBtnRight(Agent:agent):void=
        if (not IsMoving?, not IsStunned?):
            spawn{ RotateBoatSafe(1.0) }

    # --- 안전 제어 및 실제 이동/회전 처리 ---
    MoveBoatSafe(Direction:float)<suspends>:void=
        set IsMoving = true
        MoveBoat(Direction)
        set IsMoving = false

    RotateBoatSafe(Direction:float)<suspends>:void=
        set IsMoving = true
        RotateBoat(Direction)
        set IsMoving = false

    MoveBoat(Direction:float)<suspends>:void=
        CurrentTransform := BoatRoot.GetTransform()
        VecX := CurrentTransform.Rotation.GetLocalForward() * ForwardAxisX
        VecY := CurrentTransform.Rotation.GetLocalRight() * ForwardAxisY
        VecZ := CurrentTransform.Rotation.GetLocalUp() * ForwardAxisZ
        ActualForward := VecX + VecY + VecZ
        
        # 칠러(빙판) 감지 시 슬라이딩 가속
        Multiplier := if (IsFrozen?) then ForwardMultiplier * 1.3 else ForwardMultiplier
        
        NewPosition := CurrentTransform.Translation + (ActualForward * (MoveDistance * Direction * Multiplier))
        BoatRoot.MoveTo(NewPosition, CurrentTransform.Rotation, MoveTime)

    RotateBoat(Direction:float)<suspends>:void=
        CurrentTransform := BoatRoot.GetTransform()
        
        # 칠러(빙판) 감지 시 선회 각도 축소 (30%)
        ActualAngle := if (IsFrozen?) then RotateAngle * 0.3 else RotateAngle
        AngleDegrees := ActualAngle * Direction
        
        RotationDelta := MakeRotationFromYawPitchRollDegrees(
            Yaw   := AngleDegrees * SteerAxisZ, 
            Pitch := AngleDegrees * SteerAxisY, 
            Roll  := AngleDegrees * SteerAxisX
        )
        
        NewRotation := CurrentTransform.Rotation.RotateBy(RotationDelta)
        
        if (IsFrozen?):
            # 빙판 관성으로 전진 드리프트
            VecX := CurrentTransform.Rotation.GetLocalForward() * ForwardAxisX
            VecY := CurrentTransform.Rotation.GetLocalRight() * ForwardAxisY
            VecZ := CurrentTransform.Rotation.GetLocalUp() * ForwardAxisZ
            ActualForward := VecX + VecY + VecZ
            
            DriftPosition := CurrentTransform.Translation + (ActualForward * 200.0)
            BoatRoot.MoveTo(DriftPosition, NewRotation, RotateTime)
        else:
            BoatRoot.MoveTo(CurrentTransform.Translation, NewRotation, RotateTime)

    # --- 바운서 넉백 및 스턴 처리 ---
    OnBouncerTriggered(Agent : agent):void=
        if (Driver := CurrentDriver?, Driver = Agent, not IsStunned?):
            spawn{ BounceSequence() }

    BounceSequence()<suspends>:void=
        set IsStunned = true
        set IsMoving = true
        
        CurrentTransform := BoatRoot.GetTransform()
        VecX := CurrentTransform.Rotation.GetLocalForward() * ForwardAxisX
        VecY := CurrentTransform.Rotation.GetLocalRight() * ForwardAxisY
        VecZ := CurrentTransform.Rotation.GetLocalUp() * ForwardAxisZ
        ActualForward := VecX + VecY + VecZ
        
        BackwardVec := ActualForward * -1.0
        UpwardVec := CurrentTransform.Rotation.GetLocalUp()
        
        BounceTarget := CurrentTransform.Translation + (BackwardVec * BounceDistance) + (UpwardVec * BounceHeight)
        
        # 넉백 물리 모션
        BoatRoot.MoveTo(BounceTarget, CurrentTransform.Rotation, BounceDuration)
        Sleep(0.4)
        
        set IsMoving = false
        set IsStunned = false

    # --- 칠러 상태 감지 ---
    OnChillerEntered(Agent : agent):void=
        if (Driver := CurrentDriver?, Driver = Agent):
            set IsFrozen = true

    OnChillerExited(Agent : agent):void=
        if (Driver := CurrentDriver?, Driver = Agent):
            set IsFrozen = false
