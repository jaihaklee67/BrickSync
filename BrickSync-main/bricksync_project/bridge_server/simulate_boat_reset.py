class MockBoatProp:
    def __init__(self, position):
        self.position = position

    def teleport_to(self, target_pos):
        self.position = target_pos
        return True

class MockBoatController:
    def __init__(self, use_reset_logic=False):
        self.use_reset_logic = use_reset_logic
        self.boat_prop = MockBoatProp((0, 0, 0)) # 에디터 배치 위치: (0, 0, 0)
        self.starting_position = (0, 0, 0)

    def on_begin(self):
        print("\n[OnBegin] Start Game Session.")
        if self.use_reset_logic:
            # 신규 로직: 시작 좌표로 강제 텔레포트 리셋
            success = self.boat_prop.teleport_to(self.starting_position)
            if success:
                print(f"  -> Reset boat to starting position: {self.boat_prop.position}")
        else:
            # 기존 로직: 그냥 현재 위치에서 그대로 시작
            print(f"  -> Start boat from last session position: {self.boat_prop.position}")

    def execute_move(self, steps):
        prev_pos = self.boat_prop.position
        new_x = prev_pos[0] + (steps * 100)
        self.boat_prop.position = (new_x, prev_pos[1], prev_pos[2])
        print(f"[Move] Forward {steps} times. Position changed: {prev_pos} -> {self.boat_prop.position}")

# 세션 진행 테스트 (게임을 켜서 이동하고, 끄고, 다시 켰을 때)
print("==================================================")
print("1. [Old Logic] Boat position persists across games")
print("==================================================")
controller_old = MockBoatController(use_reset_logic=False)

# 매치 1
controller_old.on_begin()
controller_old.execute_move(3) # 앞으로 3번 이동
print("--> Match 1 Ended")

# 매치 2 (종료 후 재시작)
controller_old.on_begin()
print(f"--> Final Start Position: {controller_old.boat_prop.position} (Error: Started from last session's ending position)")

print("\n==================================================")
print("2. [New Logic] Boat auto-teleports back on restart")
print("==================================================")
controller_new = MockBoatController(use_reset_logic=True)

# 매치 1
controller_new.on_begin()
controller_new.execute_move(3) # 앞으로 3번 이동
print("--> Match 1 Ended")

# 매치 2 (종료 후 재시작)
controller_new.on_begin()
print(f"--> Final Start Position: {controller_new.boat_prop.position} (Success: Correctly reset to original position)")
print("==================================================")
