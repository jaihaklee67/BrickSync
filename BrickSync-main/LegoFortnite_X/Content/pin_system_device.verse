using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/UI }
using { /Fortnite.com/UI }
using { /UnrealEngine.com/Temporary/SpatialMath }
using { /Verse.org/Colors }

pin_system_device := class(creative_device):

    @editable OpenUI_Button : button_device = button_device{}
    
    
    @editable WindmillSeq_CW : cinematic_sequence_device = cinematic_sequence_device{}
    @editable WindmillSeq_CCW : cinematic_sequence_device = cinematic_sequence_device{}
    
    @editable SkipHUD : hud_message_device = hud_message_device{}
    
    @editable PIN_Clockwise : string = "7241"
    @editable PIN_CounterClock : string = "9988"

    var InputString : string = ""
    var MyCanvas : ?canvas = false
    var DisplayText : text_block = text_block{}

    TextToMsg<localizes>(S:string) : message = "{S}"

    OnBegin<override>()<suspends>:void=
        OpenUI_Button.InteractedWithEvent.Subscribe(HandleOpen)

    HandleOpen(Agent:agent):void=
        if (Player := player[Agent], PlayerUI := GetPlayerUI[Player]):
            CloseUI(Player) 
            set InputString = ""
            NewCanvas := MakeCanvas(Player)
            set MyCanvas = option{NewCanvas}
            PlayerUI.AddWidget(NewCanvas, player_ui_slot{InputMode := ui_input_mode.All})
            UpdateDisplay()

    CloseUI(Player:player):void=
        if (PlayerUI := GetPlayerUI[Player], ActiveCanvas := MyCanvas?):
            PlayerUI.RemoveWidget(ActiveCanvas)
            set MyCanvas = false

    HandleCloseBtn(WM:widget_message):void=
        CloseUI(WM.Player)

    Add0(WM:widget_message):void= AddNum("0")
    Add1(WM:widget_message):void= AddNum("1")
    Add2(WM:widget_message):void= AddNum("2")
    Add3(WM:widget_message):void= AddNum("3")
    Add4(WM:widget_message):void= AddNum("4")
    Add5(WM:widget_message):void= AddNum("5")
    Add6(WM:widget_message):void= AddNum("6")
    Add7(WM:widget_message):void= AddNum("7")
    Add8(WM:widget_message):void= AddNum("8")
    Add9(WM:widget_message):void= AddNum("9")

    AddNum(Num:string):void=
        set InputString = InputString + Num
        UpdateDisplay()

    ClearInput(WM:widget_message):void=
        set InputString = ""
        UpdateDisplay()

    SubmitInput(WM:widget_message):void=
        if (InputString = PIN_Clockwise):
            set InputString = "CW MOTOR ON!"
            UpdateDisplay()
            WindmillSeq_CW.Play()           
            spawn{ DelayedClose(WM.Player) }
            
        else if(InputString = PIN_CounterClock):
            set InputString = "CCW MOTOR ON!"
            UpdateDisplay()
            
            WindmillSeq_CCW.Play()    
            spawn{ DelayedClose(WM.Player) }
            
        else:
            set InputString = "ERROR"
            UpdateDisplay()
            spawn{ DelayedClear() }

    DelayedClose(Player:player)<suspends>:void=
        Sleep(0.1)
        CloseUI(Player)

    DelayedClear()<suspends>:void=
        Sleep(1.0)
        set InputString = ""
        UpdateDisplay()

    UpdateDisplay():void=
        DisplayText.SetText(TextToMsg("PIN: " + InputString))

    MakeCanvas(Player:player):canvas=
        set DisplayText = text_block{DefaultText := TextToMsg("PIN: "), DefaultTextColor := NamedColors.White}
        
        B1 := button_regular{DefaultText:=TextToMsg(" 1 ")}
        B1.OnClick().Subscribe(Add1)
        B2 := button_regular{DefaultText:=TextToMsg(" 2 ")}
        B2.OnClick().Subscribe(Add2)
        B3 := button_regular{DefaultText:=TextToMsg(" 3 ")}
        B3.OnClick().Subscribe(Add3)
        B4 := button_regular{DefaultText:=TextToMsg(" 4 ")}
        B4.OnClick().Subscribe(Add4)
        B5 := button_regular{DefaultText:=TextToMsg(" 5 ")}
        B5.OnClick().Subscribe(Add5)
        B6 := button_regular{DefaultText:=TextToMsg(" 6 ")}
        B6.OnClick().Subscribe(Add6)
        B7 := button_regular{DefaultText:=TextToMsg(" 7 ")}
        B7.OnClick().Subscribe(Add7)
        B8 := button_regular{DefaultText:=TextToMsg(" 8 ")}
        B8.OnClick().Subscribe(Add8)
        B9 := button_regular{DefaultText:=TextToMsg(" 9 ")}
        B9.OnClick().Subscribe(Add9)
        B0 := button_regular{DefaultText:=TextToMsg(" 0 ")}
        B0.OnClick().Subscribe(Add0)
        
        BSub := button_regular{DefaultText:=TextToMsg("ENT")}
        BSub.OnClick().Subscribe(SubmitInput)
        BClr := button_regular{DefaultText:=TextToMsg("CLR")}
        BClr.OnClick().Subscribe(ClearInput)
        BExt := button_quiet{DefaultText:=TextToMsg(" X ")}
        BExt.OnClick().Subscribe(HandleCloseBtn)

        Row1 := stack_box{Orientation := orientation.Horizontal, Slots := array{
            stack_box_slot{Widget:=B1, Padding:=margin{Right:=10.0}},
            stack_box_slot{Widget:=B2, Padding:=margin{Right:=10.0}},
            stack_box_slot{Widget:=B3}
        }}
        Row2 := stack_box{Orientation := orientation.Horizontal, Slots := array{
            stack_box_slot{Widget:=B4, Padding:=margin{Right:=10.0}},
            stack_box_slot{Widget:=B5, Padding:=margin{Right:=10.0}},
            stack_box_slot{Widget:=B6}
        }}
        Row3 := stack_box{Orientation := orientation.Horizontal, Slots := array{
            stack_box_slot{Widget:=B7, Padding:=margin{Right:=10.0}},
            stack_box_slot{Widget:=B8, Padding:=margin{Right:=10.0}},
            stack_box_slot{Widget:=B9}
        }}
        Row4 := stack_box{Orientation := orientation.Horizontal, Slots := array{
            stack_box_slot{Widget:=BClr, Padding:=margin{Right:=10.0}},
            stack_box_slot{Widget:=B0, Padding:=margin{Right:=10.0}},
            stack_box_slot{Widget:=BSub}
        }}

        PadContainer := stack_box{Orientation := orientation.Vertical, Slots := array{
            stack_box_slot{Widget:=BExt, HorizontalAlignment := horizontal_alignment.Right, Padding:=margin{Bottom:=20.0}},
            stack_box_slot{Widget:=DisplayText, Padding:=margin{Bottom:=20.0}},
            stack_box_slot{Widget:=Row1, Padding:=margin{Bottom:=10.0}},
            stack_box_slot{Widget:=Row2, Padding:=margin{Bottom:=10.0}},
            stack_box_slot{Widget:=Row3, Padding:=margin{Bottom:=10.0}},
            stack_box_slot{Widget:=Row4}
        }}
        
        ColorBlock := color_block{DefaultColor := color{R:=0.05, G:=0.05, B:=0.1}, DefaultOpacity := 0.9}
        
        BgOverlay := overlay{Slots:=array{
            overlay_slot{Widget:=ColorBlock},
            overlay_slot{Widget:=PadContainer, Padding:=margin{Left:=30.0, Right:=30.0, Top:=30.0, Bottom:=30.0}}
        }}

        NewCanvas := canvas{Slots:=array{
            canvas_slot{
                Widget := BgOverlay
                Anchors := anchors{Minimum:=vector2{X:=0.5,Y:=0.5}, Maximum:=vector2{X:=0.5,Y:=0.5}}
                Alignment := vector2{X:=0.5, Y:=0.5}
            }
        }}
        return NewCanvas
