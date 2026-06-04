using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /Fortnite.com/Characters }
using { /UnrealEngine.com/Temporary/SpatialMath }

lego_car_controller := class(creative_device):

    @editable
    CarRoot : creative_prop = creative_prop{}

    @editable
    VehicleChair : chair_device = chair_device{}

    @editable TriggerForward : input_trigger_device = input_trigger_device{}
    @editable TriggerBackward : input_trigger_device = input_trigger_device{}
    @editable TriggerLeft : input_trigger_device = input_trigger_device{}
    @editable TriggerRight : input_trigger_device = input_trigger_device{}

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

    var IsMoving : logic = false
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
        if (not IsMoving?, Driver := CurrentDriver?, Driver = Agent):
            spawn{ MoveCarSafe(1.0) }

    OnBackward(Agent:agent):void=
        if (not IsMoving?, Driver := CurrentDriver?, Driver = Agent):
            spawn{ MoveCarSafe(-1.0) }

    OnLeft(Agent:agent):void=
        if (not IsMoving?, Driver := CurrentDriver?, Driver = Agent):
            spawn{ RotateCarSafe(-1.0) }

    OnRight(Agent:agent):void=
        if (not IsMoving?, Driver := CurrentDriver?, Driver = Agent):
            spawn{ RotateCarSafe(1.0) }

    MoveCarSafe(Direction:float)<suspends>:void=
        set IsMoving = true
        MoveCar(Direction)
        set IsMoving = false

    RotateCarSafe(Direction:float)<suspends>:void=
        set IsMoving = true
        RotateCar(Direction)
        set IsMoving = false

    MoveCar(Direction:float)<suspends>:void=
        CurrentTransform := CarRoot.GetTransform()
        
        # 설정한 축을 로컬 벡터로 변환 (현재 자동차가 쳐다보는 방향 기준)
        VecX := CurrentTransform.Rotation.GetLocalForward() * ForwardAxisX
        VecY := CurrentTransform.Rotation.GetLocalRight() * ForwardAxisY
        VecZ := CurrentTransform.Rotation.GetLocalUp() * ForwardAxisZ
        ActualForward := VecX + VecY + VecZ
        
        NewPosition := CurrentTransform.Translation + (ActualForward * (MoveDistance * Direction * ForwardMultiplier))
        CarRoot.MoveTo(NewPosition, CurrentTransform.Rotation, MoveTime)

    RotateCar(Direction:float)<suspends>:void=
        CurrentTransform := CarRoot.GetTransform()
        
        AngleDegrees := RotateAngle * Direction
        
        RotationDelta := MakeRotationFromYawPitchRollDegrees(
            Yaw   := AngleDegrees * SteerAxisZ, 
            Pitch := AngleDegrees * SteerAxisY, 
            Roll  := AngleDegrees * SteerAxisX
        )
        
        NewRotation := CurrentTransform.Rotation.RotateBy(RotationDelta)
        CarRoot.MoveTo(CurrentTransform.Translation, NewRotation, RotateTime)

