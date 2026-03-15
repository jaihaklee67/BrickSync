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

print("Starting Fortnite Bridge Server (Discrete Block Movement Mode)...")

steering_state = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False}
active_threads = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False}
keys = {"UP": 'y', "DOWN": 'l', "LEFT": 'u', "RIGHT": 'o'}

def steering_worker(direction):
    print(f"[{direction}] 1타일 이동 신호 발송 (키: {keys[direction]}) - 다중 스레드 폭주 스팸 차단 완료")
    
    # 꾹 누르지 않고 짧게 탁! 쳐서 언리얼 캐릭터가 의자에서 달리는 모션 발생을 원천 차단
    # (반복루프를 빼버려서 "1타일 이동 블록 = 정확히 1번만 키 입력" 하도록 강제 패치)
    if steering_state[direction]:
        pydirectinput.keyDown(keys[direction]); time.sleep(0.1); pydirectinput.keyUp(keys[direction])
        
        # 1.05초 동안 추가 입력(다른 방향의 동일 지시) 방어 쿨타임 (이 쿨타임 중 중지 명령이 오면 즉시 종료)
        wait_time = 0.0
        while wait_time < 1.05 and steering_state[direction]:
            time.sleep(0.05)
            wait_time += 0.05
            
    # 일꾼이 역할(1타일 이동)을 끝마치면 스레드 종료 보고
    active_threads[direction] = False

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
                        steering_state["UP"] = True
                        if not active_threads["UP"]:
                            active_threads["UP"] = True
                            threading.Thread(target=steering_worker, args=("UP",), daemon=True).start()
                    elif action == "STEER_DOWN":
                        steering_state["DOWN"] = True
                        if not active_threads["DOWN"]:
                            active_threads["DOWN"] = True
                            threading.Thread(target=steering_worker, args=("DOWN",), daemon=True).start()
                    elif action == "STEER_LEFT":
                        steering_state["LEFT"] = True
                        if not active_threads["LEFT"]:
                            active_threads["LEFT"] = True
                            threading.Thread(target=steering_worker, args=("LEFT",), daemon=True).start()
                    elif action == "STEER_RIGHT":
                        steering_state["RIGHT"] = True
                        if not active_threads["RIGHT"]:
                            active_threads["RIGHT"] = True
                            threading.Thread(target=steering_worker, args=("RIGHT",), daemon=True).start()
                    
                    elif action == "STOP_UP":
                        steering_state["UP"] = False
                    elif action == "STOP_DOWN":
                        steering_state["DOWN"] = False
                    elif action == "STOP_LEFT":
                        steering_state["LEFT"] = False
                    elif action == "STOP_RIGHT":
                        steering_state["RIGHT"] = False

                    elif action == "MWHEEL_LEFT":
                        print("▶ 관람차 (단일모터) 좌회전 발송 (h키 한번 탁 쳐서 가동)")
                        threading.Thread(target=lambda: [pydirectinput.keyDown('h'), time.sleep(0.3), pydirectinput.keyUp('h')], daemon=True).start()
                    elif action == "MWHEEL_RIGHT":
                        print("▶ 관람차 (단일모터) 우회전 발송 (j키 한번 탁 쳐서 가동)")
                        threading.Thread(target=lambda: [pydirectinput.keyDown('j'), time.sleep(0.3), pydirectinput.keyUp('j')], daemon=True).start()
                    elif action in ["STOP_MWHEEL_LEFT", "STOP_MWHEEL_RIGHT"]:
                        print("▶ 관람차 (단일모터) 정지 스위치 발송 (k키 한 번 탁 쳐서 정지)")
                        threading.Thread(target=lambda: [pydirectinput.keyDown('k'), time.sleep(0.3), pydirectinput.keyUp('k')], daemon=True).start()

                    elif action in ["SPEED_1", "SPEED_2", "SPEED_3", "SPEED_4"]:
                        print(f"▶ 속도 변속 {action} 수신 (포트나이트 T키 전송 차단 - 물리 모터 속도만 조절됨)")
                        # pydirectinput.keyDown('t'); time.sleep(0.1); pydirectinput.keyUp('t')
                    elif action == "ACTION_LIGHT":
                        print("▶ 네온사인 조명 대표 ON (i키 전송)")
                        pydirectinput.keyDown('i'); time.sleep(0.1); pydirectinput.keyUp('i')
                    elif action == "ACTION_SOUND":
                        print("▶ 사운드 재생 (p키 전송)")
                        pydirectinput.keyDown('p'); time.sleep(0.1); pydirectinput.keyUp('p')
                        
                    elif action == "CAT_FEED_REWARD":
                        print("[REWARD] 보상 발동! E키")
                        pydirectinput.keyDown('e'); time.sleep(0.1); pydirectinput.keyUp('e')
                except Exception as e:
                    pass
    except Exception as e:
        pass
    finally:
        for d in steering_state: steering_state[d] = False
        print("연결 종료됨")
        
    return ws

async def index_handler(request):
    return web.FileResponse(os.path.join(web_app_dir, 'app.html'))

def init_app():
    app = web.Application()
    app.router.add_get('/ws', handle_websocket)
    app.router.add_get('/', index_handler)
    app.router.add_static('/', web_app_dir)
    return app

if __name__ == "__main__":
    app = init_app()
    web.run_app(app, host="0.0.0.0", port=8000)
