using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /Fortnite.com/Characters }
using { /UnrealEngine.com/Temporary/SpatialMath }

lego_car_controller := class(creative_device):

    @editable
    CarRoot : creative_prop = creative_prop{}

    @editable
    VehicleChair : chair_device = chair_device{}

    # Input Trigger (포트나이트 설정에서 다음 키로 바인딩하세요):
    # 전진 = Y / 후진 = L / 좌회전 = U / 우회전 = O
    @editable
    TriggerForward : input_trigger_device = input_trigger_device{}
    @editable
    TriggerBackward : input_trigger_device = input_trigger_device{}
    @editable
    TriggerLeft : input_trigger_device = input_trigger_device{}
    @editable
    TriggerRight : input_trigger_device = input_trigger_device{}

    @editable
    MoveDistance : float = 512.0

    @editable
    MoveTime : float = 0.9

    @editable
    ForwardMultiplier : float = -1.0

    @editable
    RotateAngle : float = 45.0
    @editable
    RotateTime : float = 0.5

    var IsTranslating : logic = false
    var IsRotating : logic = false
    var CurrentDriver : ?agent = false

    OnBegin<override>()<suspends>:void=
        TriggerForward.PressedEvent.Subscribe(OnForward)
        TriggerBackward.PressedEvent.Subscribe(OnBackward)
        TriggerLeft.PressedEvent.Subscribe(OnLeft)
        TriggerRight.PressedEvent.Subscribe(OnRight)

        VehicleChair.SeatedEvent.Subscribe(OnPlayerSeated)
        VehicleChair.ExitedEvent.Subscribe(OnPlayerExited)

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

    OnForward(Agent:agent):void=
        if (not IsTranslating?, Driver := CurrentDriver?, Driver = Agent):
            spawn{ MoveCarSafe(1.0) }

    OnBackward(Agent:agent):void=
        if (not IsTranslating?, Driver := CurrentDriver?, Driver = Agent):
            spawn{ MoveCarSafe(-1.0) }

    OnLeft(Agent:agent):void=
        if (not IsRotating?, Driver := CurrentDriver?, Driver = Agent):
            spawn{ RotateCarSafe(-1.0) }

    OnRight(Agent:agent):void=
        if (not IsRotating?, Driver := CurrentDriver?, Driver = Agent):
            spawn{ RotateCarSafe(1.0) }

    MoveCarSafe(Direction:float)<suspends>:void=
        set IsTranslating = true
        MoveCar(Direction)
        set IsTranslating = false

    RotateCarSafe(Direction:float)<suspends>:void=
        set IsRotating = true
        RotateCar(Direction)
        set IsRotating = false

    # === 전진/후진 ===
    # 현재 회전의 로컬 앞방향(Forward)을 기준으로 이동합니다
    MoveCar(Direction:float)<suspends>:void=
        CurrentTransform := CarRoot.GetTransform()
        ForwardVector := CurrentTransform.Rotation.GetLocalForward()
        NewPosition := CurrentTransform.Translation + (ForwardVector * (MoveDistance * Direction * ForwardMultiplier))
        CarRoot.MoveTo(NewPosition, CurrentTransform.Rotation, MoveTime)

    # === 좌우 회전 ===
    # 현재 회전을 기준으로 지정된 각도만큼 회전합니다 (YawPitchRoll 기반 상대회전 적용)
    RotateCar(Direction:float)<suspends>:void=
        CurrentTransform := CarRoot.GetTransform()
        AngleDegrees := RotateAngle * Direction
        YawRotation := MakeRotationFromYawPitchRollDegrees(AngleDegrees, 0.0, 0.0)
        NewRotation := CurrentTransform.Rotation.RotateBy(YawRotation)
        CarRoot.MoveTo(CurrentTransform.Translation, NewRotation, RotateTime)
