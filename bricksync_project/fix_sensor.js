const fs = require('fs');

let appH = fs.readFileSync('web_app/app.html', 'utf8');

// fix app.html handleBLEData
appH = appH.replace(
    '                else if (portID < 6 && window.hubDevices && window.hubDevices[portID] === 61 && value.byteLength >= 5) {',
    '                else if (portID < 6 && value.byteLength === 5) {'
);

// add aggressive subscribe
let connectHook = `            await window.txCharacteristic.startNotifications();
            window.txCharacteristic.addEventListener('characteristicvaluechanged', handleBLEData);`;

if (appH.indexOf(connectHook) > -1) {
    let connectNew = `            await window.txCharacteristic.startNotifications();
            window.txCharacteristic.addEventListener('characteristicvaluechanged', handleBLEData);
            
            // 모든 포트를 무조건 센서 감지 모드(Mode 0)로 강제 구독
            for(let p=0; p<6; p++) {
                const subscribeMsg = new Uint8Array([10, 0, 0x41, p, 0, 1, 0, 0, 0, 1]);
                try { await window.txCharacteristic.writeValueWithoutResponse(subscribeMsg); } catch(e){}
                await new Promise(r => setTimeout(r, 30));
            }`;
    appH = appH.replace(connectHook, connectNew);
} else {
    console.log("Could not find connectHook in appH");
}

fs.writeFileSync('web_app/app.html', appH, 'utf8');


let les = fs.readFileSync('web_app/lesson.html', 'utf8');

// fix Python color sensor Wait code
const pyOld = /case 'event_color_sensor':([\s\S]*?)break;/;
if (pyOld.test(les)) {
    let newPy = `case 'event_color_sensor':
                            pyCode += \`\${indent}print("Waiting for color", \${pythonVal}) \\n\${indent}wait_sensor = True\\n\${indent}while wait_sensor:\\n\${indent}  for pnt in ['A','B','C','D','E','F']:\\n\${indent}    try:\\n\${indent}      p = getattr(hub.port, pnt)\\n\${indent}      if p.device.get()[0] == \${pythonVal}:\\n\${indent}        wait_sensor = False\\n\${indent}        break\\n\${indent}    except: pass\\n\${indent}  try:\\n\${indent}    import color_sensor\\n\${indent}    for p in range(6):\\n\${indent}      try:\\n\${indent}        if color_sensor.color(p) == \${pythonVal}: wait_sensor = False\\n\${indent}      except: pass\\n\${indent}  except: pass\\n\${indent}  utime.sleep_ms(50)\\n\`;
                            break;`;
    les = les.replace(pyOld, newPy);
} else {
    console.log("Could not find pyOld in les");
}


// fix BLE motor block Color wait code
// From lesson.html:
// if (window.parent.hubDevices && window.parent.hubDevices[p] === 61) {
//     if (window.parent.sensorData[p] === parsed.paramVal) {

les = les.replace(
    'if (window.parent.hubDevices && window.parent.hubDevices[p] === 61) {',
    'if (true) { // 센서타입 61 검사를 무시하고 들어오는 Data가 조건과 맞는지만 봅니다.'
);

fs.writeFileSync('web_app/lesson.html', les, 'utf8');
console.log('done fixing');
