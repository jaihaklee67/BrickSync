import ctypes

def get_windows():
    windows = []
    def callback(hwnd, extra):
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                title = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, title, length + 1)
                windows.append((hwnd, title.value))
        return True

    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    EnumWindows(EnumWindowsProc(callback), 0)
    return windows

if __name__ == "__main__":
    wins = get_windows()
    with open("windows_list.txt", "w", encoding="utf-8") as f:
        for hwnd, title in wins:
            f.write(f"HWND: {hwnd} | TITLE: '{title}'\n")
    print("Done enum windows.")
