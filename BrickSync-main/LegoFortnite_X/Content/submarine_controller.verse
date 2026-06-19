using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /Fortnite.com/Characters }
using { /UnrealEngine.com/Temporary/SpatialMath }

# submarine_controller: 해저 탐사 잠수함(Submarine)을 위한 벌스 기기 장치
# 조립된 레고 잠수함의 4방향 조작(키보드/물리버튼) 및 타 차량과의 조작 간섭 방지 필터링을 탑재하고 있습니다.
# 추가로 바운서/칠러 물리 함정 연동 기능이 내장되어 있습니다.
submarine_controller := class(creative_device):

    @editable
    SubmarineRoot : creative_prop = creative_prop{}

    @editable
    VehicleChair : chair_device = chair_device{}

    # 브릭싱크 키보드 매핑 통신용 입력 트리거
    @editable TriggerForward : input_trigger_device = input_trigger_device{}
    @editable TriggerBackward : input_trigger_device = input_trigger_device{}
    @editable TriggerLeft : input_trigger_device = input_trigger_device{}
    @editable TriggerRight : input_trigger_device = input_trigger_device{}

    # 인게임 상호작용용 버튼 디바이스
    @editable ButtonForward : button_device = button_device{}
    @editable ButtonBackward : button_device = button_device{}
    @editable ButtonLeft : button_device = button_device{}
    @editable ButtonRight : button_device = button_device{}

    # 가로막힘 없는 개별 조작을 위한 트랙 감지 구역 (뮤테이터 존 배열)
    @editable TrackZones : []mutator_zone_device = array{}

    # 함정 구역 디바이스 (배열 형태로 변경)
    @editable BouncerZones : []mutator_zone_device = array{}
    @editable ChillerZones : []mutator_zone_device = array{}

    # 플레이어가 연동된 도로 구역 중 하나에라도 속해 있는지 확인하는 검사 함수
    # (등록된 구역이 없을 때는 정상 작동하도록 예외 우회 처리 포함)
    IsPlayerInTrack(Agent : agent)<decides><transacts>:void=
        if (TrackZones.Length > 0):
            var InZone : logic = false
            for (Zone : TrackZones):
                if (Zone.IsInVolume[Agent]):
                    set InZone = true
            InZone = true

    # 이동 감도 및 설정 파라미터
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
        # 키보드 입력 트리거 구독
        TriggerForward.PressedEvent.Subscribe(OnForward)
        TriggerBackward.PressedEvent.Subscribe(OnBackward)
        TriggerLeft.PressedEvent.Subscribe(OnLeft)
        TriggerRight.PressedEvent.Subscribe(OnRight)

        # 인게임 버튼 입력 구독
        ButtonForward.InteractedWithEvent.Subscribe(OnBtnForward)
        ButtonBackward.InteractedWithEvent.Subscribe(OnBtnBackward)
        ButtonLeft.InteractedWithEvent.Subscribe(OnBtnLeft)
        ButtonRight.InteractedWithEvent.Subscribe(OnBtnRight)

        # 의자 탑승/하차 이벤트 구독
        VehicleChair.SeatedEvent.Subscribe(OnPlayerSeated)
        VehicleChair.ExitedEvent.Subscribe(OnPlayerExited)

        # 물리 함정 감지 영역 배열 바인딩
        for (Zone : BouncerZones):
            Zone.AgentEntersEvent.Subscribe(OnBouncerTriggered)

        for (Zone : ChillerZones):
            Zone.AgentEntersEvent.Subscribe(OnChillerEntered)
            Zone.AgentExitsEvent.Subscribe(OnChillerExited)

    # 플레이어 의자 탑승 시
    OnPlayerSeated(Agent : agent):void=
        set CurrentDriver = option{Agent}
        TriggerForward.Register(Agent)
        TriggerBackward.Register(Agent)
        TriggerLeft.Register(Agent)
        TriggerRight.Register(Agent)

    # 플레이어 의자 하차 시
    OnPlayerExited(Agent : agent):void=
        set CurrentDriver = false
        TriggerForward.Unregister(Agent)
        TriggerBackward.Unregister(Agent)
        TriggerLeft.Unregister(Agent)
        TriggerRight.Unregister(Agent)

    # --- 키보드 입력 콜백 (의자 탑승 상태 검증 및 도로 영역 검증 포함) ---
    OnForward(Agent:agent):void=
        if (not IsMoving?, not IsStunned?, Driver := CurrentDriver?, Driver = Agent, IsPlayerInTrack[Agent]):
            spawn{ MoveSubmarineSafe(1.0) }

    OnBackward(Agent:agent):void=
        if (not IsMoving?, not IsStunned?, Driver := CurrentDriver?, Driver = Agent, IsPlayerInTrack[Agent]):
            spawn{ MoveSubmarineSafe(-1.0) }

    OnLeft(Agent:agent):void=
        if (not IsMoving?, not IsStunned?, Driver := CurrentDriver?, Driver = Agent, IsPlayerInTrack[Agent]):
            spawn{ RotateSubmarineSafe(-1.0) }

    OnRight(Agent:agent):void=
        if (not IsMoving?, not IsStunned?, Driver := CurrentDriver?, Driver = Agent, IsPlayerInTrack[Agent]):
            spawn{ RotateSubmarineSafe(1.0) }

    # --- 물리 버튼 클릭 콜백 (의자 미탑승 시에도 작동 가능) ---
    OnBtnForward(Agent:agent):void=
        if (not IsMoving?, not IsStunned?):
            spawn{ MoveSubmarineSafe(1.0) }

    OnBtnBackward(Agent:agent):void=
        if (not IsMoving?, not IsStunned?):
            spawn{ MoveSubmarineSafe(-1.0) }

    OnBtnLeft(Agent:agent):void=
        if (not IsMoving?, not IsStunned?):
            spawn{ RotateSubmarineSafe(-1.0) }

    OnBtnRight(Agent:agent):void=
        if (not IsMoving?, not IsStunned?):
            spawn{ RotateSubmarineSafe(1.0) }

    # --- 실제 이동 제어 구현 ---
    MoveSubmarineSafe(Direction:float)<suspends>:void=
        set IsMoving = true
        MoveSubmarine(Direction)
        set IsMoving = false

    RotateSubmarineSafe(Direction:float)<suspends>:void=
        set IsMoving = true
        RotateSubmarine(Direction)
        set IsMoving = false

    MoveSubmarine(Direction:float)<suspends>:void=
        CurrentTransform := SubmarineRoot.GetTransform()
        
        VecX := CurrentTransform.Rotation.GetLocalForward() * ForwardAxisX
        VecY := CurrentTransform.Rotation.GetLocalRight() * ForwardAxisY
        VecZ := CurrentTransform.Rotation.GetLocalUp() * ForwardAxisZ
        ActualForward := VecX + VecY + VecZ
        
        # 칠러(빙판) 감지 시 슬라이딩 가속
        Multiplier := if (IsFrozen?) then ForwardMultiplier * 1.3 else ForwardMultiplier
        
        NewPosition := CurrentTransform.Translation + (ActualForward * (MoveDistance * Direction * Multiplier))
        SubmarineRoot.MoveTo(NewPosition, CurrentTransform.Rotation, MoveTime)

    RotateSubmarine(Direction:float)<suspends>:void=
        CurrentTransform := SubmarineRoot.GetTransform()
        
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
            SubmarineRoot.MoveTo(DriftPosition, NewRotation, RotateTime)
        else:
            SubmarineRoot.MoveTo(CurrentTransform.Translation, NewRotation, RotateTime)

    # --- 바운서 넉백 및 스턴 처리 ---
    OnBouncerTriggered(Agent : agent):void=
        if (Driver := CurrentDriver?, Driver = Agent, not IsStunned?):
            spawn{ BounceSequence() }

    BounceSequence()<suspends>:void=
        set IsStunned = true
        set IsMoving = true
        
        CurrentTransform := SubmarineRoot.GetTransform()
        VecX := CurrentTransform.Rotation.GetLocalForward() * ForwardAxisX
        VecY := CurrentTransform.Rotation.GetLocalRight() * ForwardAxisY
        VecZ := CurrentTransform.Rotation.GetLocalUp() * ForwardAxisZ
        ActualForward := VecX + VecY + VecZ
        
        BackwardVec := ActualForward * -1.0
        UpwardVec := CurrentTransform.Rotation.GetLocalUp()
        
        BounceTarget := CurrentTransform.Translation + (BackwardVec * BounceDistance) + (UpwardVec * BounceHeight)
        
        # 넉백 물리 모션
        SubmarineRoot.MoveTo(BounceTarget, CurrentTransform.Rotation, BounceDuration)
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
