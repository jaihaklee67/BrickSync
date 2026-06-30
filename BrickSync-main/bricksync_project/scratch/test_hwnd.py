import time
import ctypes

def diag():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    print(f"diag: hwnd = {hwnd}")
    if hwnd == 0:
        print("diag: hwnd is NULL (no active foreground window).")
        return
        
    class_buffer = ctypes.create_unicode_buffer(260)
    res_cls = ctypes.windll.user32.GetClassNameW(hwnd, class_buffer, 260)
    print(f"diag: GetClassNameW result = {res_cls}, buffer value = '{class_buffer.value}'")
    
    title_length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    print(f"diag: GetWindowTextLengthW result = {title_length}")
    
    title_buffer = ctypes.create_unicode_buffer(title_length + 1)
    res_title = ctypes.windll.user32.GetWindowTextW(hwnd, title_buffer, title_length + 1)
    print(f"diag: GetWindowTextW result = {res_title}, buffer value = '{title_buffer.value}'")
    
    err = ctypes.windll.kernel32.GetLastError()
    print(f"diag: LastError = {err}")

print("Sleeping 3 seconds. Remain focused on Chrome...")
time.sleep(3)
diag()
