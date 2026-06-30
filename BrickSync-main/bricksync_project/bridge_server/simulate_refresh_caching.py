class SimulatedBrowserCache:
    def __init__(self):
        self.cached_files = {
            "lesson.html": {
                "version": "v1_old",
                "top_bar_z_index": 10,
                "home_btn_clickable": False
            }
        }
        self.network_hung = True # 새로고침이 로딩창에서 막힘 (Socket Lock)

    def force_refresh_attempt(self, new_server_file):
        print(f"\n[새로고침 시도] Ctrl + F5 또는 F5 실행")
        if self.network_hung:
            # 네트워크가 막혀 있으면 새 파일을 받아오지 못하고 이전 캐시 파일을 강제 재사용함
            print("  -> [경고] 네트워크 대기 상태(Socket Lock)로 인해 새 파일을 받아오지 못함!")
            print("  -> [유지] 브라우저가 기존에 메모리에 들고 있던 구버전(v1_old) 캐시를 계속 실행합니다.")
        else:
            # 네트워크가 뚫리면 새 파일로 업데이트
            self.cached_files["lesson.html"] = new_server_file
            print("  -> [성공] 새 버전(v2_new) 파일이 브라우저에 성공적으로 로드되었습니다!")

    def get_current_state(self, stage):
        file_info = self.cached_files["lesson.html"]
        print(f"  -> [{stage} 결과] 버전: {file_info['version']}, top-bar z-index: {file_info['top_bar_z_index']}, 클릭 가능 여부: {file_info['home_btn_clickable']}")
        return file_info["home_btn_clickable"]

# 새롭게 서버에 패치된 파일 정보 (z-index 3010)
new_server_file = {
    "version": "v2_new",
    "top_bar_z_index": 3010,
    "home_btn_clickable": True
}

print("==================================================")
print("1. [오류 발생 상황] 새로고침이 막혀서 기존 캐시가 유지되는 경우")
print("==================================================")
browser_old = SimulatedBrowserCache()
browser_old.network_hung = True # 소켓 락으로 네트워크 대기 발생

# 새로고침을 시도했으나 서버 대기로 실패
browser_old.force_refresh_attempt(new_server_file)

# 모든 스테이지에서 클릭 여부 검증
stages = ["STAGE 1", "STAGE 2", "STAGE 3", "STAGE 4", "STAGE 5"]
for stage in stages:
    browser_old.get_current_state(stage)

print("\n==================================================")
print("2. [오류 해결 상황] 서버 재부팅 및 주소창 Enter 입력 후")
print("==================================================")
browser_new = SimulatedBrowserCache()
browser_new.network_hung = False # 소켓 정체 해소 완료

# 새로고침 성공
browser_new.force_refresh_attempt(new_server_file)

# 모든 스테이지에서 클릭 여부 검증
for stage in stages:
    browser_new.get_current_state(stage)
print("==================================================")
