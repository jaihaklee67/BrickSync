const fs = require('fs');

let html = fs.readFileSync('web_app/lesson.html', 'utf8');

const pyStart = html.indexOf('            let blockCount = 0;');
const pyEnd = html.indexOf('            buildPyCode(rootBlocks, "");');

if (pyStart > -1 && pyEnd > -1) {
    let pyNew = `            let blockCount = 0;
            // 브라우저 로컬 사운드 동기화 큐 (명령 시간 지연 연산)
            const localSoundsQueue = [];
            let cumulativeDelayMs = 0;

            function buildPyCode(blockArray, indent) {
                // 부모 컨테이너(루프 등) 내부일 때도 정확한 순차 실행
                blockArray.forEach((block) => {
                    const action = block.getAttribute('data-action');
                    blockCount++;
                    
                    let paramVal = 1;
                    let timeVal = 1;
                    let paramEl = null;

                    if (action === 'motor_cw' || action === 'motor_ccw') {
                        const timeEl = block.querySelector('.block-param');
                        if (timeEl) {
                            if (timeEl.hasAttribute('data-val')) timeVal = parseFloat(timeEl.getAttribute('data-val'));
                            else {
                                const textVal = timeEl.innerText.trim();
                                if (!isNaN(textVal) && textVal !== "") timeVal = parseFloat(textVal);
                            }
                        }
                    } else {
                        paramEl = block.querySelector('.block-param:not(.param-time)');
                        if (paramEl) {
                            if (paramEl.hasAttribute('data-val')) paramVal = parseFloat(paramEl.getAttribute('data-val'));
                            else {
                                const textVal = paramEl.innerText.trim();
                                if (!isNaN(textVal) && textVal !== "") paramVal = parseFloat(textVal);
                            }
                        }

                        const timeEl = block.querySelector('.param-time');
                        if (timeEl) {
                            if (timeEl.hasAttribute('data-val')) timeVal = parseFloat(timeEl.getAttribute('data-val'));
                            else {
                                const textVal = timeEl.innerText.trim();
                                if (!isNaN(textVal) && textVal !== "") timeVal = parseFloat(textVal);
                            }
                        }
                    }

                    let pythonVal = paramVal === -1 ? 'math.urandom.getrandbits(3)' : paramVal;
                    let pythonTimeVal = timeVal === -1 ? 'math.urandom.getrandbits(3)' : timeVal;

                    switch (action) {
                        case 'start': break;

                        case 'motor_speed_set':
                            pyCode += \`\${indent}global_motor_speed = \${pythonVal} \\n\${indent}print("Global Motor Speed Set:", global_motor_speed, "%") \\n\`;
                            break;
                        case 'motor_speed':
                            pyCode += \`\${indent}print("Motor Speed Block Triggered") \\n\`;
                            break;
                        case 'motor_cw':
                            pyCode += \`\${indent}try:\\n\${indent}  import motor\\n\${indent}  for p in range(6):\\n\${indent}    try: motor.run_for_degrees(p, int(\${pythonTimeVal} * 360), global_motor_speed)\\n\${indent}    except: pass\\n\${indent}except:\\n\${indent}  for p in [getattr(hub.port, x, None) for x in ['A','B','C','D','E','F']]:\\n\${indent}    try:\\n\${indent}      if p and hasattr(p, 'motor'): p.motor.run_for_degrees(int(\${pythonTimeVal} * 360), global_motor_speed)\\n\${indent}    except: pass\\n\`;
                            cumulativeDelayMs += (timeVal * 1500); // 근사치 (블로킹이므로 브라우저쪽 애니메이션 싱크용)
                            break;
                        case 'motor_ccw':
                            pyCode += \`\${indent}try:\\n\${indent}  import motor\\n\${indent}  for p in range(6):\\n\${indent}    try: motor.run_for_degrees(p, -int(\${pythonTimeVal} * 360), global_motor_speed)\\n\${indent}    except: pass\\n\${indent}except:\\n\${indent}  for p in [getattr(hub.port, x, None) for x in ['A','B','C','D','E','F']]:\\n\${indent}    try:\\n\${indent}      if p and hasattr(p, 'motor'): p.motor.run_for_degrees(-int(\${pythonTimeVal} * 360), global_motor_speed)\\n\${indent}    except: pass\\n\`;
                            cumulativeDelayMs += (timeVal * 1500);
                            break;
                        case 'motor_stop':
                            pyCode += \`\${indent}sm() \\n\`;
                            break;

                        case 'matrix_image':
                        case 'matrix_pixel':
                            const matEl = block.querySelector('.param-unified') || block.querySelector('.block-param:not(.param-time)') || paramEl;
                            let matrixArr = matEl ? (matEl.getAttribute('data-matrix') || JSON.stringify([0, 6, 0, 0, 0, 0, 6, 0, 6])) : JSON.stringify([0, 6, 0, 0, 0, 0, 6, 0, 6]);
                            let lightDuration = matEl ? (parseFloat(matEl.getAttribute('data-val')) || 2) : 2;

                            if (matrixArr) {
                                try {
                                    const arr = JSON.parse(matrixArr);
                                    pyCode += \`\${indent}try:\\n\`;
                                    const nextIndent = indent + "  ";
                                    pyCode += \`\${nextIndent}m = \${JSON.stringify(arr)}\\n\`;
                                    pyCode += \`\${nextIndent}try:\\n\${nextIndent}  import color_matrix\\n\${nextIndent}  for p in range(6):\\n\${nextIndent}    try: color_matrix.show(p, m)\\n\${nextIndent}    except:\\n\${nextIndent}      try:\\n\${nextIndent}        for y in range(3):\\n\${nextIndent}          for x in range(3):\\n\${nextIndent}            color_matrix.set_pixel(p, x, y, m[y*3+x])\\n\${nextIndent}      except: pass\\n\${nextIndent}except: pass\\n\`;
                                    pyCode += \`\${nextIndent}try:\\n\${nextIndent}  for y in range(3):\\n\${nextIndent}    for x in range(3):\\n\${nextIndent}      try: hub.display.pixel(x+1, y+1, 9 if m[y*3+x]>0 else 0)\\n\${nextIndent}      except: pass\\n\${nextIndent}      try: hub.light_matrix.set_pixel(x+1, y+1, 100 if m[y*3+x]>0 else 0)\\n\${nextIndent}      except: pass\\n\${nextIndent}      try:\\n\${nextIndent}        import light_matrix\\n\${nextIndent}        light_matrix.set_pixel(x+1, y+1, 100 if m[y*3+x]>0 else 0)\\n\${nextIndent}      except: pass\\n\${nextIndent}except: pass\\n\`;
                                    pyCode += \`\${indent}except:\\n\${indent}  pass\\n\`;
                                } catch (e) { }
                            }

                            pyCode += \`\${indent}utime.sleep_ms(int(\${lightDuration} * 1000)) \\n\`;
                            cumulativeDelayMs += (lightDuration * 1000);

                            pyCode += \`\${indent}try:\\n\${indent}  hub.led(0)\\n\${indent}  import light_matrix; light_matrix.clear()\\n\${indent}except:\\n\${indent}  try: hub.display.clear()\\n\${indent}  except: pass\\n\`;
                            break;
                        case 'matrix_clear':
                            pyCode += \`\${indent}try:\\n\${indent}  hub.led(0)\\n\${indent}  import light_matrix; light_matrix.clear()\\n\${indent}except:\\n\${indent}  try: hub.display.clear()\\n\${indent}  except: pass\\n\`;
                            break;

                        case 'flow_wait':
                            pyCode += \`\${indent}utime.sleep_ms(int(\${pythonVal} * 1000)) \\n\`;
                            cumulativeDelayMs += (paramVal * 1000);
                            break;

                        case 'control_repeat':
                        case 'control_forever':
                            let maxIter = (action === 'control_forever') ? 'True' : \`range(int(\${pythonVal}))\`;
                            let loopStmt = (action === 'control_forever') ? 'while' : 'for i in';
                            pyCode += \`\${indent}\${loopStmt} \${maxIter}: \\n\`;

                            const innerStack = block.querySelector(':scope > .loop-inner-stack');
                            if (innerStack) {
                                const innerBlocks = Array.from(innerStack.children).filter(b => b.classList.contains('workspace-item') && !b.classList.contains('placeholder'));
                                if (innerBlocks.length > 0) {
                                    buildPyCode(innerBlocks, indent + "  ");
                                } else {
                                    pyCode += \`\${indent}  pass\\n\`;
                                }
                            } else {
                                pyCode += \`\${indent}  pass\\n\`;
                            }
                            break;

                        case 'event_color_sensor':
                            pyCode += \`\${indent}print("Waiting for color", \${pythonVal}) \\n\${indent}wait_sensor = True\\n\${indent}while wait_sensor:\\n\${indent}  try:\\n\${indent}    import color_sensor\\n\${indent}    for p in range(6):\\n\${indent}      try:\\n\${indent}        if color_sensor.color(p) == \${pythonVal}:\\n\${indent}          wait_sensor = False\\n\${indent}          break\\n\${indent}      except: pass\\n\${indent}  except: pass\\n\${indent}  utime.sleep_ms(50)\\n\`;
                            break;

                        case 'sound_note':
                        case 'sound_animal':
                        case 'sound_play':
                            const soundTrack = paramVal === -1 ? Math.floor(Math.random() * 8) + 1 : paramVal;
                            localSoundsQueue.push({ track: soundTrack, delay: cumulativeDelayMs });
                            pyCode += \`\${indent}utime.sleep_ms(5000) \\n\`;
                            cumulativeDelayMs += 5000;
                            break;

                        default:
                            pyCode += \`\${indent}print("Action: \${action}, Param: \${pythonVal}") \\n\`;
                    }
                });
            }
`;
    html = html.substring(0, pyStart) + pyNew + '\n' + html.substring(pyEnd);
}

const bleStart = html.indexOf("            if (window.parent.connectionType === 'BLE') {");
const bleEndStr = '                    setTimeout(() => {\n                        if (blockCount > 1 && anySequenceFound && window.bleEngineRunCounter === currentRunId) {\n                            triggerSuccessConfetti();\n                            try { window.parent.sendWebSocketAction({ action: "CAT_FEED_REWARD" }); console.log("포트나이트 연동 신호(CAT_FEED_REWARD) 전송 완료 [BLE]"); } catch (e) { }\n                        }\n                    }, maxGlobalDelay + 1000);\n\n                    return;\n                }';

const bleEndIdx = html.indexOf(bleEndStr);

if (bleStart > -1 && bleEndIdx > -1) {
    let bleNew = `            if (window.parent.connectionType === 'BLE') {
                window.bleEngineRunCounter = (window.bleEngineRunCounter || 0) + 1;
                const currentRunId = window.bleEngineRunCounter;
                console.log(\`🚀 [BLE_ENGINE] Starting \${validStacks.length} concurrent block stacks (RunID: \${currentRunId})\`);

                let anySequenceFound = false;

                const executeStack = async (stack) => {
                    const stackBlocks = Array.from(stack.querySelectorAll('.workspace-item'));
                    if (stackBlocks.length === 0) return;
                    anySequenceFound = true;

                    const parseBlock = (block) => {
                        const action = block.getAttribute('data-action');
                        let paramVal = 1; let timeVal = 1; let paramEl = null;

                        if (action === 'motor_cw' || action === 'motor_ccw') {
                            const timeEl = block.querySelector('.block-param');
                            if (timeEl) {
                                if (timeEl.hasAttribute('data-val')) timeVal = parseFloat(timeEl.getAttribute('data-val'));
                                else { const tv = timeEl.innerText.trim(); if (!isNaN(tv) && tv !== "") timeVal = parseFloat(tv); }
                            }
                        } else {
                            paramEl = block.querySelector(':scope > .block-param:not(.param-time)') || block.querySelector('.block-param:not(.param-time)');
                            if (paramEl) {
                                if (paramEl.hasAttribute('data-val')) paramVal = parseFloat(paramEl.getAttribute('data-val'));
                                else { const tv = paramEl.innerText.trim(); if (!isNaN(tv) && tv !== "") paramVal = parseFloat(tv); }
                            }
                            const timeEl = block.querySelector(':scope > .param-time') || block.querySelector('.param-time');
                            if (timeEl) {
                                if (timeEl.hasAttribute('data-val')) timeVal = parseFloat(timeEl.getAttribute('data-val'));
                                else { const tv = timeEl.innerText.trim(); if (!isNaN(tv) && tv !== "") timeVal = parseFloat(tv); }
                            }
                        }
                        if (paramVal === -1) paramVal = Math.floor(Math.random() * 3) + 1;
                        if (timeVal === -1) timeVal = Math.floor(Math.random() * 3) + 1;
                        return { action, paramVal, timeVal, paramEl, block };
                    };

                    let bleGlobalMotorSpeed = 40;

                    const runBlocksSeq = async (blocksArray) => {
                        for (const block of blocksArray) {
                            if (window.bleEngineRunCounter !== currentRunId) return;
                            const parsed = parseBlock(block);
                            blockCount++;

                            switch (parsed.action) {
                                case 'motor_speed_set':
                                    bleGlobalMotorSpeed = parsed.paramVal;
                                    break;
                                case 'motor_cw':
                                case 'motor_ccw':
                                    let speed = bleGlobalMotorSpeed;
                                    if (parsed.action === 'motor_ccw') speed = -speed;
                                    let deg = Math.floor(parsed.timeVal * 360);
                                    let d1 = deg & 0xFF; let d2 = (deg >> 8) & 0xFF; let d3 = (deg >> 16) & 0xFF; let d4 = (deg >> 24) & 0xFF;
                                    let speedHex = speed < 0 ? (256 + speed) : speed;
                                    // Start Speed For Degrees Command (LWP3)
                                    // msg_len, hub, 0x81, port, 0x11, 0x0B, D1..D4, Speed, MaxPower, EndState, Profile
                                    for (let p=0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev === 64 || dev === 61 || dev === 62 || dev === 63 || dev === 57 || dev === 59) continue;
                                        let payload = [14, 0x00, 0x81, p, 0x11, 0x0B, d1, d2, d3, d4, speedHex, 100, 127, 3];
                                        await window.parent.writeToHub(new Uint8Array(payload));
                                        await new Promise(r => setTimeout(r, 20)); // wait for msg to digest
                                    }
                                    // Block delay calculation (approximate)
                                    let estTimeMs = (deg / Math.max(10, Math.abs(speed))) * 100; 
                                    if (estTimeMs < 100) estTimeMs = 100;
                                    await new Promise(r => setTimeout(r, estTimeMs + 200)); 
                                    break;
                                case 'motor_stop':
                                    for (let p=0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev === 64 || dev === 61 || dev === 62 || dev === 63 || dev === 57 || dev === 59) continue;
                                        await window.parent.writeToHub(new Uint8Array([7, 0, 0x81, p, 0x10, 0x01, 0])); // power 0
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                    break;
                                case 'sound_note':
                                case 'sound_animal':
                                case 'sound_play':
                                    await new Promise(r => setTimeout(r, 4000));
                                    break;
                                case 'event_color_sensor':
                                    console.log(\`⏱️ [BLE] Waiting for color: \${parsed.paramVal}\`);
                                    let matched = false;
                                    while (!matched && window.bleEngineRunCounter === currentRunId) {
                                        if (window.parent.sensorData) {
                                            for (let p = 0; p < 6; p++) {
                                                if (window.parent.hubDevices && window.parent.hubDevices[p] === 61) {
                                                    if (window.parent.sensorData[p] === parsed.paramVal) {
                                                        matched = true; break;
                                                    }
                                                }
                                            }
                                        }
                                        await new Promise(r => setTimeout(r, 100));
                                    }
                                    console.log(\`✅ [BLE] Color \${parsed.paramVal} detected!\`);
                                    break;
                                case 'flow_wait':
                                    await new Promise(r => setTimeout(r, parsed.paramVal * 1000));
                                    break;
                                case 'matrix_image':
                                case 'matrix_pixel':
                                    let matEl = parsed.block.querySelector('.param-unified') || parsed.block.querySelector('.block-param:not(.param-time)');
                                    let matrixArrBLE = matEl ? (matEl.getAttribute('data-matrix') || JSON.stringify([0,6,0,0,0,0,6,0,6])) : JSON.stringify([0,6,0,0,0,0,6,0,6]);
                                    let mBleTime = matEl ? (parseFloat(matEl.getAttribute('data-val')) || 2) : 2;
                                    let mArr = JSON.parse(matrixArrBLE);
                                    let encodedColors = mArr.map(c => c > 0 ? c + 160 : 0);
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev !== undefined && dev !== 64) continue;
                                        let payload = [16, 0, 0x81, p, 0x10, 0x51, 0x02, ...encodedColors];
                                        await window.parent.writeToHub(new Uint8Array(payload));
                                        await new Promise(r => setTimeout(r, 30));
                                    }
                                    await new Promise(r => setTimeout(r, mBleTime * 1000));
                                    
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev !== undefined && dev !== 64) continue;
                                        let payload = [16, 0, 0x81, p, 0x10, 0x51, 0x02, 0,0,0,0, 0,0,0,0, 0];
                                        await window.parent.writeToHub(new Uint8Array(payload));
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                    await window.parent.writeToHub(new Uint8Array([8, 0, 0x81, 50, 0x10, 0x51, 0x00, 0]));
                                    break;
                                case 'matrix_clear':
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev !== undefined && dev !== 64) continue;
                                        let payload = [16, 0, 0x81, p, 0x10, 0x51, 0x02, 0,0,0,0, 0,0,0,0, 0];
                                        await window.parent.writeToHub(new Uint8Array(payload));
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                    await window.parent.writeToHub(new Uint8Array([8, 0, 0x81, 50, 0x10, 0x51, 0x00, 0]));
                                    break;
                                case 'control_repeat':
                                case 'control_forever':
                                    let iters = parsed.action === 'control_forever' ? Infinity : parsed.paramVal;
                                    const innerStack = parsed.block.querySelector(':scope > .loop-inner-stack');
                                    let children = [];
                                    if (innerStack) children = Array.from(innerStack.children).filter(b => b.classList.contains('workspace-item'));
                                    
                                    for (let i = 0; i < iters; i++) {
                                        if (window.bleEngineRunCounter !== currentRunId) break;
                                        await runBlocksSeq(children);
                                    }
                                    break;
                            }
                        }
                    };
                    
                    // Top-level execution, extract only roots of the given stack (we don't flatten anymore! nested blocks handled recursively)
                    let rootBlocks = Array.from(stack.children).filter(b => b.classList.contains('workspace-item') && !b.classList.contains('placeholder'));
                    
                    const firstAction = rootBlocks[0] ? rootBlocks[0].getAttribute('data-action') : '';
                    if (firstAction.startsWith('event_')) {
                        // Event loop continuously monitors the stack
                        while (window.bleEngineRunCounter === currentRunId) {
                            await runBlocksSeq(rootBlocks);
                            await new Promise(r => setTimeout(r, 100)); // debounce
                        }
                    } else {
                        // Standard sequential run
                        await runBlocksSeq(rootBlocks);
                    }
                };

                // Execute all stacks concurrently, and wait for all non-event stacks to finish before rewarding
                Promise.all(validStacks.map(stack => executeStack(stack))).then(() => {
                    // Only trigger if no new run replaced it AND there were actually valid blocks
                    if (window.bleEngineRunCounter === currentRunId && anySequenceFound && blockCount > 1) {
                        triggerSuccessConfetti();
                        try { window.parent.sendWebSocketAction({ action: "CAT_FEED_REWARD" }); console.log("포트나이트 연동 신호(CAT_FEED_REWARD) 전송 완료 [BLE]"); } catch (e) { }
                    }
                });
                
                return;
            }`;

    html = html.substring(0, bleStart) + bleNew + '\n' + html.substring(bleEndIdx + bleEndStr.length);
}

fs.writeFileSync('web_app/lesson.html', html, 'utf8');
console.log('done javascript overwrite');
