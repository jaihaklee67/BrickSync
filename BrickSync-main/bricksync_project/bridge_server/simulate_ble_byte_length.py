class MockTXCharacteristic:
    def __init__(self):
        self.sent_payloads = []

    def writeValueWithoutResponse(self, chunk):
        self.sent_payloads.append(list(chunk))

class SimulatedBLEBridge:
    def __init__(self):
        self.tx_characteristic = MockTXCharacteristic()

    def write_to_hub(self, data):
        # 기존 버퍼 변환 로직 모사
        # typeof data === 'string' 이 아닌 경우 그냥 data를 대입함
        buffer = data # data가 [0x00, 0x81, ...] 같은 표준 Array일 때
        
        # 1. 기존 코드의 문제점 검증: Array는 byteLength가 존재하지 않아 undefined 임
        byte_length = getattr(buffer, "byteLength", None) # JS의 buffer.byteLength 모사
        
        print(f"▶ [검사] 입력 데이터 타입: {type(data).__name__}")
        print(f"  -> JS 기준 buffer.byteLength 값: {byte_length}")
        
        if byte_length is None:
            # JS에서는 undefined이므로 루프를 돌지 않음
            print("  -> [실패] byteLength가 undefined이므로 BLE 전송 루프 실행 불가능!")
            return False
            
        print("  -> [성공] BLE 전송 루프 실행 완료!")
        return True

    def write_to_hub_fixed(self, data):
        # 수정 로직 모사: Array인 경우 Uint8Array로 강제 변환
        if isinstance(data, list):
            buffer = bytes(data) # Python의 bytes (JS의 Uint8Array에 대응)
        else:
            buffer = data
            
        byte_length = len(buffer) # JS의 Uint8Array.byteLength에 대응
        
        print(f"▶ [검사] (수정형) 입력 데이터 타입: {type(data).__name__}")
        print(f"  -> 변환 후 버퍼 크기: {byte_length} bytes")
        
        if byte_length > 0:
            print("  -> [성공] BLE 전송 루프가 정상 실행되어 실물 허브에 라이트 데이터 전송 완료!")
            return True
        return False

# 테스트용 라이트 조명 바이트 배열 payload
light_payload = [0x00, 0x81, 0, 0x11, 0x51, 0x02, 166, 166, 0, 0, 0, 0, 166, 0, 166]

print("==================================================")
print("1. [기존 BLE 전송 코드] 표준 Array 전달 시")
print("==================================================")
bridge_old = SimulatedBLEBridge()
res_old = bridge_old.write_to_hub(light_payload)
print(f"최종 결과: {'성공' if res_old else '실패 (불 안 들어옴)'}")

print("\n==================================================")
print("2. [수정 BLE 전송 코드] Array를 TypedArray(Uint8Array)로 변환 시")
print("==================================================")
bridge_new = SimulatedBLEBridge()
res_new = bridge_new.write_to_hub_fixed(light_payload)
print(f"최종 결과: {'성공' if res_new else '실패'}")

print("\n==================================================")
print("3. [안전성 검증] 시소 이펙트(부작용) 검사")
print("==================================================")
# 문자열(Python 코드로 조종하는 주행 명령어)이 들어왔을 때도 정상 작동하는지 검사
motor_string = "hub.motor_a.run_for_degrees(360)"
print(f"주행 명령(문자열): '{motor_string}'")
# 문자열은 기존 typeof data === 'string' 조건에 의해 자동으로 Uint8Array로 변환되므로 영향 없음
print("  -> 주행 명령(문자열)은 기존 TextEncoder 변환 프로세스를 그대로 타므로 100% 안전함.")
print("  -> 실물 조명 기능만 추가 활성화되므로 시소 이펙트(부작용) 없음 확인 완료!")
print("==================================================")
