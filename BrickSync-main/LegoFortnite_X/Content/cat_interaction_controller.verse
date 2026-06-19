using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/SpatialMath }

cat_interaction_controller := class(creative_device):

    @editable
    CatProp : creative_prop = creative_prop{}

    @editable
    CondButton : conditional_button_device = conditional_button_device{}

    @editable
    JumpHeight : float = 40.0

    @editable
    JumpDuration : float = 0.2

    var IsRunning : logic = false

    OnBegin<override>()<suspends>:void=
        CondButton.ActivatedEvent.Subscribe(OnCatInteracted)

    OnCatInteracted(Agent : agent):void=
        if (not IsRunning?):
            spawn{ JumpSequence() }

    JumpSequence()<suspends>:void=
        set IsRunning = true
        
        InitialTransform := CatProp.GetTransform()
        
        # 위로 점프 (Z축) - X, Y 값을 명시하여 컴파일 에러 방지
        JumpPos := InitialTransform.Translation + vector3{X := 0.0, Y := 0.0, Z := JumpHeight}
        CatProp.MoveTo(JumpPos, InitialTransform.Rotation, JumpDuration)
        
        # 다시 아래로 내려옴
        CatProp.MoveTo(InitialTransform.Translation, InitialTransform.Rotation, JumpDuration)
        
        set IsRunning = false

