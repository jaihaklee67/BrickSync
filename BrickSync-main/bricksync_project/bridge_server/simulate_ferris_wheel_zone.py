class MockMutatorZone:
    def __init__(self, player_in_zone=False):
        self.player_in_zone = player_in_zone

    def is_in_volume(self, player):
        return self.player_in_zone

class MockFerrisWheelController:
    def __init__(self, use_global_registration=False):
        self.use_global_registration = use_global_registration
        self.zone = MockMutatorZone(player_in_zone=False)
        self.triggers_registered = False
        self.rotation_command_executed = False

    def on_begin(self, player):
        print("\n[OnBegin] 게임 세션 시작.")
        if self.use_global_registration:
            # 신규 로직: 구역 여부 상관없이 시작 시점에 상시 등록
            self.triggers_registered = True
            print(f"  -> [성공] 플레이어 {player}에게 대관람차 단축키 트리거(h,j,k) 상시 감지 등록 완료!")
        else:
            # 기존 로직: 시작 시점에는 대기, 구역 진입 시 등록
            print("  -> [대기] 대관람차 영역 진입 대기 중...")

    def player_movement_tick(self, player, in_zone):
        self.zone.player_in_zone = in_zone
        print(f"\n[이동 정보] 플레이어가 대관람차 구역 내부에 있습니까? : {in_zone}")
        
        if not self.use_global_registration:
            # 기존 로직: 구역 진입 여부 실시간 체크하여 등록/해제
            if self.zone.is_in_volume(player):
                if not self.triggers_registered:
                    self.triggers_registered = True
                    print("  -> [감지] 구역 진입 ➔ 단축키(h,j,k) 등록 성공!")
            else:
                if self.triggers_registered:
                    self.triggers_registered = False
                    print("  -> [감지] 구역 이탈 ➔ 단축키(h,j,k) 등록 해제!")

    def press_turn_left(self, player):
        print(f"\n[이벤트] 서버에서 h키(관람차 좌회전)를 수신했습니다.")
        if self.triggers_registered:
            # 동작 검사
            if self.use_global_registration:
                self.rotation_command_executed = True
                print("  -> [성공] 대관람차 좌회전 동작을 안전하게 가동합니다! (상시 작동)")
            else:
                # 기존 로직: 구역 내 운전자 등록 체크
                if self.zone.is_in_volume(player):
                    self.rotation_command_executed = True
                    print("  -> [성공] 대관람차 좌회전 동작 가동 성공! (구역 내부 감지됨)")
                else:
                    print("  -> [실패] 구역 외부에 서 있어 조작 신호가 무시되었습니다!")
        else:
            print("  -> [실패] 키 트리거가 등록되지 않아 신호 자체가 유실되었습니다!")

# 시뮬레이션 테스트
print("==================================================")
print("1. [기존 영역 감지 로직] 대관람차 구역 밖에서 테스트할 때")
print("==================================================")
sim_old = MockFerrisWheelController(use_global_registration=False)
sim_old.on_begin("Player1")

# 대관람차에서 멀리 떨어져서 (예: 보트 구역) 테스트 진행
sim_old.player_movement_tick("Player1", in_zone=False)
sim_old.press_turn_left("Player1")

print("\n==================================================")
print("2. [수정 상시 감지 로직] 대관람차 구역 밖에서 테스트할 때")
print("==================================================")
sim_new = MockFerrisWheelController(use_global_registration=True)
sim_new.on_begin("Player1")

# 대관람차에서 멀리 떨어져서 (예: 보트 구역) 테스트 진행
sim_new.player_movement_tick("Player1", in_zone=False)
sim_new.press_turn_left("Player1")
print("==================================================")
