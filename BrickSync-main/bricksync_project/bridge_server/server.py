import asyncio
from aiohttp import web
import json
import os
import threading
import time

try:
    import pydirectinput
except ImportError:
    print("pydirectinput is not installed. Run: pip install pydirectinput")
    pass

web_app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web_app")

print("Starting Fortnite Bridge Server (Discrete Block Movement Mode with Global Lock)...")

# 글로벌 스레드 동기화 락 (멀티스레드에서 SendInput 동시 호출로 인한 키 씹힘 및 락 현상 완벽 방지)
pydirectinput_lock = threading.Lock()

def safe_press(key):
    with pydirectinput_lock:
        try:
            pydirectinput.keyDown(key)
            time.sleep(0.05)
            pydirectinput.keyUp(key)
        except Exception:
            pass

def safe_key_down(key):
    with pydirectinput_lock:
        try:
            pydirectinput.keyDown(key)
        except Exception:
            pass

def safe_key_up(key):
    with pydirectinput_lock:
        try:
            pydirectinput.keyUp(key)
        except Exception:
            pass

steering_state = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False}
active_threads = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False}
keys = {"UP": 'y', "DOWN": 'l', "LEFT": 'u', "RIGHT": 'o'}

def click_loop_worker(direction, key):
    print(f"▶ [AUTO-FIRE START] {direction} ({key}키 연사 루프 가동)")
    while steering_state[direction]:
        safe_press(key)
        
        # 1.05초 대기 (총 간격 1.10초 = 0.05 + 1.05)
        wait_time = 0.0
        while wait_time < 1.05 and steering_state[direction]:
            time.sleep(0.05)
            wait_time += 0.05
    # [Failsafe] 루프를 빠져나왔을 때 확실히 키를 한 번 더 떼어 줌
    safe_key_up(key)
    active_threads[direction] = False
    print(f"■ [AUTO-FIRE STOP] {direction} ({key}키 연사 루프 종료)")

def release_all_steering_keys():
    print("🧹 [FAILSAFE] 4방향 모든 키 강제 해제 실행!")
    safe_key_up('y')
    safe_key_up('l')
    safe_key_up('u')
    safe_key_up('o')

async def handle_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("웹브라우저(브릭싱크)가 연결되었습니다!")
    
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    action = data.get("action")
                    
                    if action == "STEER_UP":
                        if not steering_state["UP"] and not active_threads["UP"]:
                            steering_state["UP"] = True
                            active_threads["UP"] = True
                            threading.Thread(target=click_loop_worker, args=("UP", 'y'), daemon=True).start()
                    elif action == "STEER_DOWN":
                        if not steering_state["DOWN"] and not active_threads["DOWN"]:
                            steering_state["DOWN"] = True
                            active_threads["DOWN"] = True
                            threading.Thread(target=click_loop_worker, args=("DOWN", 'l'), daemon=True).start()
                    elif action == "STEER_LEFT":
                        if not steering_state["LEFT"] and not active_threads["LEFT"]:
                            steering_state["LEFT"] = True
                            active_threads["LEFT"] = True
                            threading.Thread(target=click_loop_worker, args=("LEFT", 'u'), daemon=True).start()
                    elif action == "STEER_RIGHT":
                        if not steering_state["RIGHT"] and not active_threads["RIGHT"]:
                            steering_state["RIGHT"] = True
                            active_threads["RIGHT"] = True
                            threading.Thread(target=click_loop_worker, args=("RIGHT", 'o'), daemon=True).start()
                    
                    elif action == "STOP_UP":
                        steering_state["UP"] = False
                        release_all_steering_keys()
                    elif action == "STOP_DOWN":
                        steering_state["DOWN"] = False
                        release_all_steering_keys()
                    elif action == "STOP_LEFT":
                        steering_state["LEFT"] = False
                        release_all_steering_keys()
                    elif action == "STOP_RIGHT":
                        steering_state["RIGHT"] = False
                        release_all_steering_keys()

                    elif action == "MWHEEL_LEFT":
                        print("▶ 관람차 (단일모터) 좌회전 발송 (h키 한번 탁 쳐서 가동)")
                        threading.Thread(target=lambda: safe_press('h'), daemon=True).start()
                    elif action == "MWHEEL_RIGHT":
                        print("▶ 관람차 (단일모터) 우회전 발송 (k키 한번 탁 쳐서 가동)")
                        threading.Thread(target=lambda: safe_press('k'), daemon=True).start()
                    elif action in ["STOP_MWHEEL_LEFT", "STOP_MWHEEL_RIGHT"]:
                        print("▶ 관람차 (단일모터) 정지 스위치 발송 (j키 한 번 탁 쳐서 정지)")
                        threading.Thread(target=lambda: safe_press('j'), daemon=True).start()

                    elif action in ["SPEED_1", "SPEED_2", "SPEED_3", "SPEED_4"]:
                        speed_durations = {
                            "SPEED_1": 0.2,
                            "SPEED_2": 0.5,
                            "SPEED_3": 0.9,
                            "SPEED_4": 1.3
                        }
                        duration = speed_durations[action]
                        print(f"▶ 속도 변속 {action} 수신 (포트나이트 T키 {duration}초 입력 전송)")
                        def press_speed_key(dur):
                            safe_key_down('t')
                            time.sleep(dur)
                            safe_key_up('t')
                        threading.Thread(target=press_speed_key, args=(duration,), daemon=True).start()

                    elif action == "CLEANUP_KEYS":
                        print("🧹 [CLEANUP] 모든 조작 가상 키 강제 해제 실행")
                        release_all_steering_keys()

                    elif action == "ACTION_LIGHT":
                        print("▶ 네온사인 조명 대표 ON ([키 전송)")
                        threading.Thread(target=lambda: safe_press('['), daemon=True).start()
                    elif action == "ACTION_SOUND":
                        print("▶ 사운드 재생 (p키 전송)")
                        threading.Thread(target=lambda: safe_press('p'), daemon=True).start()
                        
                    elif action == "CAT_FEED_REWARD":
                        print("[REWARD] 보상 발동! E키")
                        threading.Thread(target=lambda: safe_press('e'), daemon=True).start()
                        
                    elif action == "MONSTER_ALERT":
                        print("[ALERT] 몬스터 감지 경보 발동! G키")
                        threading.Thread(target=lambda: safe_press('g'), daemon=True).start()
                        
                    elif action == "SWING_CONTROL":
                        direction = data.get("dir")
                        turns = data.get("val", 1)
                        key = 'j' if direction == "FORWARD" else 'h'
                        print(f"▶ [SWING_CONTROL] {direction} {turns}바퀴 수신 ({key}키 {turns}회 반복 연사)")
                        def press_swing_key(k, count):
                            for _ in range(count):
                                safe_key_down(k)
                                time.sleep(0.05)
                                safe_key_up(k)
                                time.sleep(1.2) # 1바퀴 도는 시간(1.11초) + 안전 마진 대기
                        threading.Thread(target=press_swing_key, args=(key, turns), daemon=True).start()
                        
                    elif action == "motor_cw":
                        print("▶ 쓰레기 괴물 입 열기 (H키 전송)")
                        threading.Thread(target=lambda: [safe_key_down('h'), time.sleep(0.3), safe_key_up('h')], daemon=True).start()
                        
                    elif action == "motor_ccw":
                        print("▶ 쓰레기 괴물 입 닫기 (J키 전송)")
                        threading.Thread(target=lambda: [safe_key_down('j'), time.sleep(0.3), safe_key_up('j')], daemon=True).start()

                    elif action in ["motor_stop", "motor_stop_cw", "motor_stop_ccw", "motor_stop_generic"]:
                        print("▶ 쓰레기 괴물 동작 정지 (K키 전송)")
                        threading.Thread(target=lambda: [safe_key_down('k'), time.sleep(0.3), safe_key_up('k')], daemon=True).start()
                except Exception as e:
                    pass
    except Exception as e:
        pass
    finally:
        for d in steering_state: steering_state[d] = False
        try:
            with pydirectinput_lock:
                for k in ['y', 'l', 'u', 'o', 'h', 'k', 'j', 't', '[', 'p', 'e', 'g', 'n']:
                    pydirectinput.keyUp(k)
        except Exception:
            pass
        print("연결 종료됨")
        
    return ws

@web.middleware
async def no_cache_middleware(request, handler):
    try:
        response = await handler(request)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except web.HTTPException as ex:
        ex.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        ex.headers['Pragma'] = 'no-cache'
        ex.headers['Expires'] = '0'
        raise ex

async def index_handler(request):
    return web.FileResponse(os.path.join(web_app_dir, 'app.html'))

def init_app():
    app = web.Application(middlewares=[no_cache_middleware])
    app.router.add_get('/ws', handle_websocket)
    app.router.add_get('/', index_handler)
    app.router.add_static('/', web_app_dir)
    return app

if __name__ == "__main__":
    app = init_app()
    web.run_app(app, host="0.0.0.0", port=8000)
