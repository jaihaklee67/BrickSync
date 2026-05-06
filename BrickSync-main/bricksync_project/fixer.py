import codecs

path = 'web_app/lesson.html'
with codecs.open(path, 'r', 'utf-8') as f:
    content = f.read()

startMarker = "            if (window.parent.connectionType === 'BLE') {"
endMarker = "            try {\n                await writeToHub('\\x03\\x03');"

startIndex = content.find(startMarker)
endIndex = content.find(endMarker)

if startIndex == -1 or endIndex == -1:
    print("Markers not found")
    exit(1)

cleanBLELogic = """            if (window.parent.connectionType === 'BLE') {
                // ===============================================
                // BLE ENGINE (Virtual Machine)
                // ===============================================
                window.bleEngineRunCounter = (window.bleEngineRunCounter || 0) + 1;
                const currentRunId = window.bleEngineRunCounter;

                console.log(`🚀 [BLE_ENGINE] Starting ${validStacks.length} concurrent block stacks (RunID: ${currentRunId})`);

                let maxGlobalDelay = 0;
                let anySequenceFound = false;

                validStacks.forEach((stack) => {
                    const stackBlocks = Array.from(stack.querySelectorAll('.workspace-item'));
                    if (stackBlocks.length === 0) return;
                    
                    anySequenceFound = true;
                    const firstAction = stackBlocks[0].getAttribute('data-action');
                    const isEventLoop = firstAction !== 'start';

                    let currentBleDelay = 0;
                    let bleGlobalMotorSpeed = 40;
                    const bleQueue = [];

                    stackBlocks.forEach((block) => {
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

                        if (paramVal === -1) paramVal = Math.floor(Math.random() * 3) + 1;
                        if (timeVal === -1) timeVal = Math.floor(Math.random() * 3) + 1;

                        switch (action) {
                            case 'motor_speed_set':
                                bleGlobalMotorSpeed = paramVal === -1 ? 40 : paramVal;
                                break;
                            case 'motor_cw':
                                bleQueue.push({ action: 'motor', speed: bleGlobalMotorSpeed, delay: currentBleDelay });
                                currentBleDelay += (timeVal * 1000);
                                bleQueue.push({ action: 'motor', speed: 0, delay: currentBleDelay });
                                currentBleDelay += 300;
                                break;
                            case 'motor_ccw':
                                bleQueue.push({ action: 'motor', speed: -bleGlobalMotorSpeed, delay: currentBleDelay });
                                currentBleDelay += (timeVal * 1000);
                                bleQueue.push({ action: 'motor', speed: 0, delay: currentBleDelay });
                                currentBleDelay += 300;
                                break;
                            case 'motor_stop':
                                bleQueue.push({ action: 'motor', speed: 0, delay: currentBleDelay });
                                currentBleDelay += 300;
                                break;
                            case 'sound_note':
                            case 'sound_animal':
                            case 'sound_play':
                                currentBleDelay += 5000;
                                break;
                            case 'event_color_sensor':
                                bleQueue.push({ action: 'wait_color', targetColor: paramVal, delay: currentBleDelay });
                                break;
                            case 'flow_wait':
                                currentBleDelay += (paramVal * 1000);
                                break;
                            case 'matrix_image':
                            case 'matrix_pixel':
                                let freshMatEl = block.querySelector('.param-unified') || block.querySelector('.block-param:not(.param-time)');
                                let matrixArrBLE = freshMatEl ? (freshMatEl.getAttribute('data-matrix') || JSON.stringify([0, 6, 0, 0, 0, 0, 6, 0, 6])) : JSON.stringify([0, 6, 0, 0, 0, 0, 6, 0, 6]);
                                let mBleTime = freshMatEl ? (parseFloat(freshMatEl.getAttribute('data-val')) || 2) : 2;

                                bleQueue.push({ action: 'matrix', colors: JSON.parse(matrixArrBLE), delay: currentBleDelay });
                                currentBleDelay += (mBleTime * 1000);
                                bleQueue.push({ action: 'matrix_clear', delay: currentBleDelay });
                                break;
                            case 'matrix_clear':
                                bleQueue.push({ action: 'matrix_clear', delay: currentBleDelay });
                                break;
                        }
                    });

                    if (currentBleDelay > maxGlobalDelay) {
                        maxGlobalDelay = currentBleDelay;
                    }

                    const executeBleQueue = async () => {
                        let lastExecutionTime = 0;
                        for (const cmd of bleQueue) {
                            if (window.bleEngineRunCounter !== currentRunId) return; 
                            try {
                                const waitTime = cmd.delay - lastExecutionTime;
                                
                                if (waitTime > 0 && cmd.action !== 'wait_color') {
                                    await new Promise(r => setTimeout(r, waitTime));
                                    lastExecutionTime = cmd.delay;
                                }

                                if (cmd.action === 'motor') {
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev === 64 || dev === 61 || dev === 62 || dev === 63 || dev === 57 || dev === 59) continue;

                                        let speedInt = Math.round(cmd.speed);
                                        let speedHex = speedInt < 0 ? (256 + speedInt) : speedInt;
                                        await window.parent.writeToHub(new Uint8Array([7, 0, 0x81, p, 0x10, 0x01, speedHex]));
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                } else if (cmd.action === 'matrix') {
                                    let encodedColors = cmd.colors.map(c => c > 0 ? c + 160 : 0);
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev !== undefined && dev !== 64) continue;

                                        let payload = [16, 0, 0x81, p, 0x10, 0x51, 0x02, ...encodedColors];
                                        await window.parent.writeToHub(new Uint8Array(payload));
                                        await new Promise(r => setTimeout(r, 30));
                                    }
                                } else if (cmd.action === 'matrix_clear') {
                                    for (let p = 0; p < 6; p++) {
                                        const dev = window.parent.hubDevices ? window.parent.hubDevices[p] : undefined;
                                        if (dev !== undefined && dev !== 64) continue;

                                        let payload = [16, 0, 0x81, p, 0x10, 0x51, 0x02, 0, 0, 0, 0, 0, 0, 0, 0, 0];
                                        await window.parent.writeToHub(new Uint8Array(payload));
                                        await new Promise(r => setTimeout(r, 20));
                                    }
                                    await window.parent.writeToHub(new Uint8Array([8, 0, 0x81, 50, 0x10, 0x51, 0x00, 0]));
                                } else if (cmd.action === 'wait_color') {
                                    let matched = false;
                                    while (!matched && window.bleEngineRunCounter === currentRunId) {
                                        if (window.parent.sensorData) {
                                            for (let p = 0; p < 6; p++) {
                                                if (window.parent.hubDevices && window.parent.hubDevices[p] === 61) {
                                                    if (window.parent.sensorData[p] === cmd.targetColor) {
                                                        matched = true;
                                                        break;
                                                    }
                                                }
                                            }
                                        }
                                        if (!matched) await new Promise(r => setTimeout(r, 100));
                                    }
                                    if (!matched) return;
                                    
                                    lastExecutionTime = cmd.delay; 
                                }
                            } catch (e) {
                                console.error("BLE Command Error:", e);
                            }
                        }
                    };

                    if (isEventLoop) {
                        (async () => {
                            while (window.bleEngineRunCounter === currentRunId) {
                                await executeBleQueue();
                                await new Promise(r => setTimeout(r, 500));
                            }
                        })();
                    } else {
                        executeBleQueue();
                    }
                });

                setTimeout(() => {
                    if (blockCount > 1 && anySequenceFound && window.bleEngineRunCounter === currentRunId) {
                        triggerSuccessConfetti();
                        try { window.parent.sendWebSocketAction({ action: "CAT_FEED_REWARD" }); } catch (e) { }
                    }
                }, maxGlobalDelay + 1000);

                return;
            }

"""

newContent = content[:startIndex] + cleanBLELogic + content[endIndex:]
with codecs.open(path, 'w', 'utf-8') as f:
    f.write(newContent)
print("done")
