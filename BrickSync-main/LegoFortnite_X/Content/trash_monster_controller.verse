using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { /UnrealEngine.com/Temporary/SpatialMath }
using { /Fortnite.com/Characters }
using { /Verse.org/Assets }
using { /UnrealEngine.com/Temporary/UI }
using { /Verse.org/Colors }
using { /Fortnite.com/UI }

trash_monster_controller := class(creative_device):
    # 대상 레고 블록 (위턱)
    @editable TopJaw : creative_prop = creative_prop{}
    
    # H키와 J키를 입력받을 인풋 트리거 2개
    @editable OpenTrigger : input_trigger_device = input_trigger_device{}
    @editable CloseTrigger : input_trigger_device = input_trigger_device{}

    # 플레이어 진입을 감지할 뮤테이터 존
    @editable MutatorZone : mutator_zone_device = mutator_zone_device{}

    # [일반유저] 인게임 상호작용 물리 버튼 장치 연결
    @editable InGameButton_Open : button_device = button_device{}
    @editable InGameButton_Close : button_device = button_device{}

    # [수정] 6단원 연동 스포너 및 트래커 장치 연결 (보상용 인풋 트리거 제거)
    @editable BrickSyncSpawner : item_spawner_device = item_spawner_device{} # 브릭싱크 코인 스포너
    @editable ComboSpawner : item_spawner_device = item_spawner_device{}     # 인게임 버튼 콤보 코인 스포너
    @editable LessonTracker : tracker_device = tracker_device{}              # 단원 완료 점수 트래커

    @editable PanelBGTexture : ?texture = false
    @editable BarBGTexture : ?texture = false
    @editable BarFillTexture : ?texture = false
    @editable CoinTexture : ?texture = false
    
    # 턱관절 회전 방향과 각도 설정
    @editable RotationAxis : vector3 = vector3{X := 0.0, Y := 1.0, Z := 0.0}
    @editable RotateAngleDegrees : float = 45.0
    
    # 입 벌어지는 속도 (몇 초 만에 열릴지)
    @editable DurationSeconds : float = 1.0

    var OriginalTransform : transform = transform{}

    # 상태 관리 변수
    var IsCoinCollected : logic = false
    var IsCoinSpawned : logic = false
    var HasOpenedCombo : logic = false
    var WasTriggeredByKeyboard : logic = false # 브릭싱크 vs 수동 버튼 판별용
    var IsLessonCompleted : logic = false # 단원 완료 점수 중복 카운트 방지용

    var CanvasMap : [agent]canvas = map{}

    OnBegin<override>()<suspends>:void=
        # 게임 시작 시 턱이 닫혀있는 "원래 위치"를 영구 기억함
        set OriginalTransform = TopJaw.GetTransform()
        
        # H와 J키가 눌리면 함수 발동!
        OpenTrigger.PressedEvent.Subscribe(OnOpenPressed)
        CloseTrigger.PressedEvent.Subscribe(OnClosePressed)

        # 인게임 물리 버튼이 눌리면 함수 발동!
        InGameButton_Open.InteractedWithEvent.Subscribe(OnOpenPressedInGame)
        InGameButton_Close.InteractedWithEvent.Subscribe(OnClosePressedInGame)

        # 코인 줍기 이벤트 연결
        BrickSyncSpawner.ItemPickedUpEvent.Subscribe(OnCoinPickedUp)
        ComboSpawner.ItemPickedUpEvent.Subscribe(OnCoinPickedUp)

        # 시작 시 모든 플레이어에게 트리거 할당 (존 감지 버그 우회 및 오작동 차단)
        for (Player : GetPlayspace().GetPlayers()):
            OnPlayerAdded(Player)
        GetPlayspace().PlayerAddedEvent().Subscribe(OnPlayerAdded)

    OnPlayerAdded(Player : player):void=
        OpenTrigger.Register(Player)
        CloseTrigger.Register(Player)
        LessonTracker.Assign(Player) # 트래커 활성 할당
        ShowCollectionUI(Player, LessonTracker.GetValue(Player))
        Print("새로운 플레이어 등록 완료: H/J 단축키 활성화.")

    # 플레이어가 쓰레기통 근처에 있는지 검사하는 함수 (안전 거리 4000.0)
    IsPlayerInRange(Agent : agent) : logic =
        if (PlayerCharacter := Agent.GetFortCharacter[]):
            PlayerPos := PlayerCharacter.GetTransform().Translation
            MonsterPos := TopJaw.GetTransform().Translation
            Dist := Distance(PlayerPos, MonsterPos)
            if (Dist <= 4000.0): # 약 8타일 반경 이내에 있을 때만
                return true
        return false

    OnOpenPressed(Agent : agent):void=
        if (PlayerCharacter := Agent.GetFortCharacter[]):
            PlayerPos := PlayerCharacter.GetTransform().Translation
            MonsterPos := TopJaw.GetTransform().Translation
            Dist := Distance(PlayerPos, MonsterPos)
            Print("Open Input Detected! Distance: {Dist} (Limit: 4000.0)")

        InRange := IsPlayerInRange(Agent)
        if (InRange = true):
            set WasTriggeredByKeyboard = true
            spawn{ OpenJaw() }

    OnClosePressed(Agent : agent):void=
        if (PlayerCharacter := Agent.GetFortCharacter[]):
            PlayerPos := PlayerCharacter.GetTransform().Translation
            MonsterPos := TopJaw.GetTransform().Translation
            Dist := Distance(PlayerPos, MonsterPos)
            Print("Close Input Detected! Distance: {Dist} (Limit: 4000.0)")

        InRange := IsPlayerInRange(Agent)
        if (InRange = true):
            spawn{ CloseJaw() }

    # --- [인게임 물리 버튼 조작부] ---
    OnOpenPressedInGame(Agent : agent):void=
        set WasTriggeredByKeyboard = false
        spawn{ OpenJaw() }

    OnClosePressedInGame(Agent : agent):void=
        spawn{ CloseJaw() }

    # [시소 파악 메커니즘 1: 절대 좌표 강제 45도 이동]
    OpenJaw()<suspends>:void=
        set IsCoinCollected = false
        set IsCoinSpawned = false
        set HasOpenedCombo = true
        RadianAngle := DegreesToRadians(RotateAngleDegrees)
        LocalRotation := MakeRotation(RotationAxis, RadianAngle)
        
        TargetRotation := OriginalTransform.Rotation.RotateBy(LocalRotation)
        
        TopJaw.MoveTo(OriginalTransform.Translation, TargetRotation, DurationSeconds)

    # [시소 파악 메커니즘 2: 원점 강제 복귀]
    CloseJaw()<suspends>:void=
        TopJaw.MoveTo(OriginalTransform.Translation, OriginalTransform.Rotation, DurationSeconds)

        # 동작 완료 시 콤보 코인 생성 체크
        if (HasOpenedCombo?):
            set HasOpenedCombo = false
            if (not IsCoinCollected?, not IsCoinSpawned?):
                if (WasTriggeredByKeyboard?):
                    # 키보드(브릭싱크) 연동 시: 쓰레기통 입 앞 스포너만 1개 작동
                    BrickSyncSpawner.Enable()
                    BrickSyncSpawner.SpawnItem()
                    set IsCoinSpawned = true
                    Print("★ [BrickSync Block Success] Coin spawned successfully.")
                else:
                    # 인게임 수동 버튼 작동 시: 수동 조작 스포너만 1개 작동
                    ComboSpawner.Enable()
                    ComboSpawner.SpawnItem()
                    set IsCoinSpawned = true
                    Print("★ [Manual Combo] Coin spawned successfully.")

    # 코인 수집 시 트래커 1회 증가 및 보상 기능 잠금
    OnCoinPickedUp(Agent : agent):void=
        if (not IsCoinCollected?):
            set IsCoinCollected = true
            set IsCoinSpawned = false
            
            # 스포너 잠금(추가 스폰 원천 차단)
            BrickSyncSpawner.Disable()
            ComboSpawner.Disable()
            
            # 한 단원(레슨) 내에서 트래커는 최초 1회만 증가하도록 제어
            if (not IsLessonCompleted?):
                set IsLessonCompleted = true
                # 코인 획득 시 Assign을 호출하면 점수가 0으로 강제 초기화되는 버그 방지를 위해 Increment만 안전하게 실행
                LessonTracker.Increment(Agent) # 트래커 카운트 1 증가
                spawn { UpdateHUDWithDelay(Agent) }
                Print("🎯 Coin collected. Lesson Tracker incremented.")
            else:
                Print("🎯 Coin collected, but tracker was already incremented for this lesson.")

    UpdateHUDWithDelay(Agent : agent)<suspends>:void=
        Sleep(0.2)
        CurrentCount := LessonTracker.GetValue(Agent)
        ShowCollectionUI(Agent, CurrentCount)

    # --- [실시간 미션 진행 상황 HUD UI 시스템] ---
    ShowCollectionUI(Agent : agent, CurrentCount : int):void=
        if (Player := player[Agent], PlayerUI := GetPlayerUI[Player]):
            # 기존 캔버스가 존재하면 제거하여 글씨 겹침 현상 원천 차단
            if (OldCanvas := CanvasMap[Agent]):
                PlayerUI.RemoveWidget(OldCanvas)
                
            # 1) 전체 HUD 배경 패널
            var HUDBacking : widget = color_block:
                DefaultColor := MakeColorFromSRGB(0.35, 0.65, 0.90)
                DefaultOpacity := 0.8
                DefaultDesiredSize := vector2{X := 720.0, Y := 115.0}

            if (PTexture := PanelBGTexture?):
                set HUDBacking = texture_block:
                    DefaultImage := PTexture
                    DefaultDesiredSize := vector2{X := 720.0, Y := 115.0}

            # 2) 진행율 게이지 배경
            var ProgressBarBG : widget = color_block:
                DefaultColor := MakeColorFromSRGB(0.1, 0.1, 0.15)
                DefaultOpacity := 0.8
                DefaultDesiredSize := vector2{X := 300.0, Y := 18.0}
            
            if (BGTexture := BarBGTexture?):
                set ProgressBarBG = texture_block:
                    DefaultImage := BGTexture
                    DefaultDesiredSize := vector2{X := 300.0, Y := 18.0}

            # 3) 진행율 채우기 게이지
            CountFloat := CurrentCount * 1.0
            ProgressWidth := 300.0 * (CountFloat / 8.0)
            
            var ProgressBarFill : widget = color_block:
                DefaultColor := MakeColorFromSRGB(1.0, 0.75, 0.0)
                DefaultOpacity := 1.0
                DefaultDesiredSize := vector2{X := ProgressWidth, Y := 14.0}

            if (FillTexture := BarFillTexture?):
                set ProgressBarFill = texture_block:
                    DefaultImage := FillTexture
                    DefaultDesiredSize := vector2{X := ProgressWidth, Y := 14.0}

            ProgressBarOverlay := overlay:
                Slots := array:
                    overlay_slot:
                        Widget := ProgressBarBG
                        HorizontalAlignment := horizontal_alignment.Left
                        VerticalAlignment := vertical_alignment.Center
                    overlay_slot:
                        Widget := ProgressBarFill
                        HorizontalAlignment := horizontal_alignment.Left
                        VerticalAlignment := vertical_alignment.Center
                        Padding := margin{Left := 2.0}

            # 4) 코인 아이콘 및 스코어 텍스트 배치
            var HUDLeftWidget : ?widget = false
            if (Texture := CoinTexture?):
                set HUDLeftWidget = option{texture_block{DefaultImage := Texture, DefaultDesiredSize := vector2{X := 36.0, Y := 36.0}}}

            ScoreTextBlock := text_block:
                DefaultText := MyMonsterScoreMessage(CurrentCount)
                DefaultTextColor := NamedColors.Yellow

            var SlotsArray : []stack_box_slot = array{}
            
            if (LeftWidget := HUDLeftWidget?):
                set SlotsArray = SlotsArray + array:
                    stack_box_slot:
                        Widget := LeftWidget
                        VerticalAlignment := vertical_alignment.Center
                        Padding := margin{Right := 12.0}
            
            set SlotsArray = SlotsArray + array:
                stack_box_slot:
                    Widget := ProgressBarOverlay
                    VerticalAlignment := vertical_alignment.Center
            
            set SlotsArray = SlotsArray + array:
                stack_box_slot:
                    Widget := ScoreTextBlock
                    VerticalAlignment := vertical_alignment.Center
                    Padding := margin{Left := 12.0}

            HUDContentStack := stack_box:
                Orientation := orientation.Horizontal
                Slots := SlotsArray

            # 5) 미션 타이틀 텍스트 설정
            RewardTextBlock := text_block:
                DefaultText := MyMonsterRewardMessage()
                DefaultTextColor := NamedColors.White
                DefaultTextSize := 18.0

            # 6) 레이아웃 수직 스택박스 조립
            HUDVerticalStack := stack_box:
                Orientation := orientation.Vertical
                Slots := array:
                    stack_box_slot:
                        Widget := RewardTextBlock
                        HorizontalAlignment := horizontal_alignment.Center
                        Padding := margin{Bottom := 8.0}
                    stack_box_slot:
                        Widget := HUDContentStack
                        HorizontalAlignment := horizontal_alignment.Center

            # 7) 백 패널 및 레이아웃 합성
            FinalHUDWidget := overlay:
                Slots := array:
                    overlay_slot:
                        Widget := HUDBacking
                        HorizontalAlignment := horizontal_alignment.Center
                        VerticalAlignment := vertical_alignment.Center
                    overlay_slot:
                        Widget := HUDVerticalStack
                        HorizontalAlignment := horizontal_alignment.Center
                        VerticalAlignment := vertical_alignment.Center

            # 8) 캔버스 슬롯 화면 상단 고정 배치
            MyCanvas := canvas:
                Slots := array:
                    canvas_slot:
                        Anchors := anchors{Minimum := vector2{X := 0.5, Y := 0.05}, Maximum := vector2{X := 0.5, Y := 0.05}}
                        Offsets := margin{Top := 0.0, Left := 0.0, Right := 720.0, Bottom := 130.0}
                        Alignment := vector2{X := 0.5, Y := 0.5}
                        Widget := FinalHUDWidget
                        
            PlayerUI.AddWidget(MyCanvas)
            if (set CanvasMap[Agent] = MyCanvas) {}

    RemoveCollectionUI(Agent : agent):void=
        if (Player := player[Agent], PlayerUI := GetPlayerUI[Player]):
            if (OldCanvas := CanvasMap[Agent]):
                PlayerUI.RemoveWidget(OldCanvas)

    MyMonsterScoreMessage<localizes>(Count : int) : message = "{Count} / 8"
    MyMonsterRewardMessage<localizes>() : message = "황금 동전 모으기 / Collect Golden Coins"
