import time
import ctypes

def get_active_window_details():
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        
        # Get class name
        class_buffer = ctypes.create_unicode_buffer(260)
        ctypes.windll.user32.GetClassNameW(hwnd, class_buffer, 260)
        
        # Get title
        title_length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        title_buffer = ctypes.create_unicode_buffer(title_length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, title_buffer, title_length + 1)
        
        return class_buffer.value, title_buffer.value
    except Exception as e:
        return "Error", str(e)

print("==================================================")
print("3초 뒤에 현재 활성화된 창의 Class와 Title을 출력합니다.")
print("포트나이트 창을 마우스로 클릭하여 켜주세요...")
print("==================================================")
time.sleep(3)
cls, title = get_active_window_details()
print(f"▶ 감지된 클래스: '{cls}'")
print(f"▶ 감지된 타이틀: '{title}'")
print("==================================================")
