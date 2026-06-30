class MockBoatProp:
    def __init__(self, editor_placement):
        self.position = editor_placement # 실제 에디터에 배치된 월드 좌표 (예: 12500, -850, 150)
        self.editor_placement = editor_placement

    def teleport_to(self, target_pos):
        self.position = target_pos
        return True

class MockBoatController:
    def __init__(self, starting_position, use_safe_filter=False):
        self.starting_position = starting_position
        self.use_safe_filter = use_safe_filter
        self.boat_prop = MockBoatProp((12500, -850, 150)) # 실제 에디터 배치 위치

    def on_begin(self):
        print(f"\n[OnBegin] Start game session (Boat default coordinates: {self.boat_prop.editor_placement})")
        print(f"  - Input StartingPosition value: {self.starting_position}")
        
        if self.use_safe_filter:
            # 신규 로직: (0, 0, 0)인 경우 텔레포트 차단 필터 가동
            if self.starting_position[0] == 0.0 and self.starting_position[1] == 0.0 and self.starting_position[2] == 0.0:
                print("  -> [Safe Filter] StartingPosition is (0,0,0) default. Skip teleport to protect boat.")
            else:
                success = self.boat_prop.teleport_to(self.starting_position)
                if success:
                    print(f"  -> [Teleport] Reset boat to coordinate: {self.boat_prop.position}")
        else:
            # 기존 로직: 조건 없이 무조건 순간이동
            success = self.boat_prop.teleport_to(self.starting_position)
            if success:
                print(f"  -> [Teleport] Teleport boat to coordinate: {self.boat_prop.position}")

        # 최종 보트의 위치 진단
        if self.boat_prop.position == (0, 0, 0):
            print("  -> [Diagnostic] Warning: Boat teleported to (0,0,0) and is missing! [FAIL]")
        else:
            print(f"  -> [Diagnostic] Success: Boat is active at coordinate {self.boat_prop.position}! [PASS]")

# 시뮬레이션 테스트
print("==================================================")
print("1. [Old Logic] StartingPosition is default (0,0,0)")
print("==================================================")
sim_old = MockBoatController(starting_position=(0.0, 0.0, 0.0), use_safe_filter=False)
sim_old.on_begin()

print("\n==================================================")
print("2. [New Logic] StartingPosition is default (0,0,0)")
print("==================================================")
sim_new_zero = MockBoatController(starting_position=(0.0, 0.0, 0.0), use_safe_filter=True)
sim_new_zero.on_begin()

print("\n==================================================")
print("3. [New Logic] StartingPosition is configured with valid coordinates")
print("==================================================")
sim_new_valid = MockBoatController(starting_position=(12500.0, -850.0, 150.0), use_safe_filter=True)
sim_new_valid.on_begin()
print("==================================================")
