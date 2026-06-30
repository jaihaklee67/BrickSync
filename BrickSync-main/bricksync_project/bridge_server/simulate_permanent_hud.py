class MockHUDController:
    def __init__(self, controller_name, use_permanent_hud=False):
        self.controller_name = controller_name
        self.use_permanent_hud = use_permanent_hud
        self.hud_visible = False
        self.coin_count = 0

    def on_player_added(self):
        # 게임 시작 또는 플레이어 입장 시 HUD 생성
        self.hud_visible = True
        print(f"[{self.controller_name}] 1. OnPlayerAdded - HUD 화면 생성 완료! (Score: {self.coin_count})")

    def on_player_seated(self):
        # 의자 탑승 시 (현재 이미 켜져 있으므로 상태 유지 확인)
        print(f"[{self.controller_name}] 2. OnPlayerSeated - 탑승 상태 HUD 감지 (Score: {self.coin_count}, Visible: {self.hud_visible})")

    def on_player_exited(self):
        # 의자 하차 시 시뮬레이션
        if self.use_permanent_hud:
            # 신규 로직: 하차 시 제거 생략
            print(f"[{self.controller_name}] 3. OnPlayerExited - (영구 노출 모드) HUD 화면 유지! (Visible: {self.hud_visible})")
        else:
            # 기존 로직: 하차 시 즉시 제거
            self.hud_visible = False
            print(f"[{self.controller_name}] 3. OnPlayerExited - (기본 모드) HUD 화면 강제 제거! (Visible: {self.hud_visible})")

    def on_item_picked_up(self):
        # 코인 수집 시 시뮬레이션
        self.coin_count += 1
        print(f"[{self.controller_name}] 4. OnItemPickedUp - 코인 수집 성공! (Score: {self.coin_count})")
        
        # 5초 뒤 자동 삭제 스레드 동작 시뮬레이션
        if self.use_permanent_hud:
            print(f"[{self.controller_name}]    -> (영구 노출 모드) 5초 자동 삭제 루틴 스킵! 화면 상시 유지.")
        else:
            self.hud_visible = False
            print(f"[{self.controller_name}]    -> (기본 모드) 5초 후 HUD 화면 자동 삭제! (Visible: {self.hud_visible})")

# 5개 단원 컨트롤러 시뮬레이션 목록
units = ["1단원 보트", "2단원 잠수함", "3단원 관람차", "4단원 카트", "5단원 동굴카"]

print("==================================================")
print("1. [기존 Verse 로직] 의자에서 내리거나 코인 수집 시 UI가 사라지는 경우")
print("==================================================")
for unit in units:
    sim_old = MockHUDController(unit, use_permanent_hud=False)
    sim_old.on_player_added()
    sim_old.on_player_seated()
    sim_old.on_player_exited()
    sim_old.on_item_picked_up()

print("\n==================================================")
print("2. [수정 Verse 로직] 게임 종료 전까지 UI가 항상 떠있고 수집 수치만 갱신되는 경우")
print("==================================================")
for unit in units:
    sim_new = MockHUDController(unit, use_permanent_hud=True)
    sim_new.on_player_added()
    sim_new.on_player_seated()
    sim_new.on_player_exited()
    sim_new.on_item_picked_up()
print("==================================================")
