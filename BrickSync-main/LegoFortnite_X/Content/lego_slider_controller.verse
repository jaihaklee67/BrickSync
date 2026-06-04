using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/SpatialMath }

lego_slider_controller := class(creative_device):

    @editable
    TargetProp : creative_prop = creative_prop{}

    @editable
    PlayButton : button_device = button_device{}

    @editable
    MoveAxisX : float = 1.0
    
    @editable
    MoveAxisY : float = 0.0
    
    @editable
    MoveAxisZ : float = 0.0

    @editable
    MoveDistance : float = 300.0

    @editable
    MoveTime : float = 2.0

    var IsRunning : logic = false

    OnBegin<override>()<suspends>:void=
        PlayButton.InteractedWithEvent.Subscribe(OnPlayButtonPressed)

    OnPlayButtonPressed(Agent : agent):void=
        if (not IsRunning?):
            spawn{ RunMotorSequence() }

    RunMotorSequence()<suspends>:void=
        set IsRunning = true
        
        InitialTransform := TargetProp.GetTransform()
        
        ForwardVec := InitialTransform.Rotation.GetLocalForward() * MoveAxisX
        RightVec   := InitialTransform.Rotation.GetLocalRight() * MoveAxisY
        UpVec      := InitialTransform.Rotation.GetLocalUp() * MoveAxisZ
        
        WorldDirection := ForwardVec + RightVec + UpVec
        
        # 버튼을 누르면 여러 번 반복하지 않고 딱 "한 번만" 갔다가 되돌아오도록 수정했습니다.
        ForwardPos := InitialTransform.Translation + (WorldDirection * MoveDistance)
        TargetProp.MoveTo(ForwardPos, InitialTransform.Rotation, MoveTime)
        
        TargetProp.MoveTo(InitialTransform.Translation, InitialTransform.Rotation, MoveTime)
            
        set IsRunning = false
