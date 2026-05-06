import re

file_path = r"c:\Users\PC\Desktop\anti_2\bricksync_project\web_app\lesson.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add 'car_forward', 'car_backward' block to HTML Palette
insertion_point = "<!-- NEW 모터 시계방향 작동 블록 -->"

car_blocks = """
        <!-- NEW 자동차 앞으로 이동 블록 -->
        <div class="spike-block bg-pink" draggable="true" data-action="car_forward" style="background: #f472b6;">
            <div class="block-icon" style="display:flex; align-items:center; justify-content:center;">
                <i class="fas fa-arrow-up" style="color: white; font-size: 32px;"></i>
            </div>
            <div class="block-param param-time" style="border-radius:16px; min-width:32px; padding:2px 8px;">1</div>
        </div>

        <!-- NEW 자동차 뒤로 이동 블록 -->
        <div class="spike-block bg-pink" draggable="true" data-action="car_backward" style="background: #f472b6;">
            <div class="block-icon" style="display:flex; align-items:center; justify-content:center;">
                <i class="fas fa-arrow-down" style="color: white; font-size: 32px;"></i>
            </div>
            <div class="block-param param-time" style="border-radius:16px; min-width:32px; padding:2px 8px;">1</div>
        </div>
"""
if "car_forward" not in html:
    html = html.replace(insertion_point, car_blocks + "\n" + insertion_point)

# 2. Add parser to block condition
html = html.replace("if (action === 'motor_cw' || action === 'motor_ccw') {",
                    "if (action === 'motor_cw' || action === 'motor_ccw' || action === 'car_forward' || action === 'car_backward') {")
html = html.replace("action === 'motor_cw' || action === 'motor_ccw'", "action === 'motor_cw' || action === 'motor_ccw' || action === 'car_forward' || action === 'car_backward'")

# 3. Add to python generator
py_car_fwd_case = """
                        case 'car_forward':
                        case 'car_backward':
                            let p0_sign = (action === 'car_forward') ? '-' : '';
                            let p1_sign = (action === 'car_forward') ? '' : '-';
                            pyCode += `${indent}try:\\n${indent}  import motor\\n${indent}  for p in range(6):\\n${indent}    spd = int(${p0_sign}global_motor_speed if p==0 else ${p1_sign}global_motor_speed) * 100\\n${indent}    try: motor.set_duty_cycle(p, spd)\\n${indent}    except:\\n${indent}      try: motor.run(p, spd)\\n${indent}      except: pass\\n${indent}except: pass\\n${indent}utime.sleep_ms(int(${pythonTimeVal} * 1000)) \\n${indent}sm() \\n`;
                            cumulativeDelayMs += (timeVal * 1000);
                            break;"""
if "case 'car_forward':" not in html:
    html = html.replace("case 'motor_cw':", py_car_fwd_case.strip() + "\n                        case 'motor_cw':", 1)


# 4. Add to BLE parser
ble_car_fwd_case = """
                            case 'car_forward':
                            case 'car_backward':
                                bleQueue.push({ action: action, speed: bleGlobalMotorSpeed, delay: currentBleDelay });
                                currentBleDelay += (timeVal * 1000);
                                bleQueue.push({ action: 'car_stop', speed: 0, dir: action, delay: currentBleDelay });
                                currentBleDelay += 300;
                                break;"""
if "case 'car_forward':\n                            case 'car_backward':" not in html:
    html = html.replace("case 'motor_cw':\n                                bleQueue", ble_car_fwd_case.strip() + "\n                            case 'motor_cw':\n                                bleQueue", 1)


# 5. Add to BLE engine queue runner
ble_runner_case = """} else if (cmd.action.startsWith('car_') && cmd.action !== 'car_speed_set' && cmd.action !== 'car_stop') {
                                    let fws = cmd.action === 'car_forward' ? 'UP' : cmd.action === 'car_backward' ? 'DOWN' : 'UP';
                                    try { window.parent.sendWebSocketAction({ action: 'STEER_' + fws }); } catch (e) { }
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev === 64 || dev === 61 || dev === 62 || dev === 63 || dev === 57 || dev === 59) continue;
                                        
                                        let p0_s = (cmd.action === 'car_forward') ? -1 : 1;
                                        let p1_s = (cmd.action === 'car_forward') ? 1 : -1;
                                        let spd = p === 0 ? (cmd.speed * p0_s) : (cmd.speed * p1_s);
                                        let speedInt = Math.round(spd);
                                        let speedHex = speedInt < 0 ? (256 + speedInt) : speedInt;
                                        await window.parent.writeToHub(new Uint8Array([8, 0, 0x81, p, 0x10, 0x51, 0x00, speedHex]));
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                } else if (cmd.action === 'car_stop') {
                                    let fws = cmd.dir === 'car_forward' ? 'UP' : cmd.dir === 'car_backward' ? 'DOWN' : 'UP';
                                    try { window.parent.sendWebSocketAction({ action: 'STOP_' + fws }); } catch (e) { }
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev === 64 || dev === 61 || dev === 62 || dev === 63 || dev === 57 || dev === 59) continue;
                                        await window.parent.writeToHub(new Uint8Array([8, 0, 0x81, p, 0x10, 0x51, 0x00, 0]));
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                """ 
if "cmd.action === 'car_stop'" not in html:
    html = html.replace("} else if (cmd.action === 'matrix') {", ble_runner_case + "} else if (cmd.action === 'matrix') {", 1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
print("patch successful")
