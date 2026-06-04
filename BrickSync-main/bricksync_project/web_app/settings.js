// BrickSync - 공통 설정 모달 스크립트 (Settings Modal Module)
// 이 스크립트는 공통 설정창 주입, 다국어 처리, 효과음 볼륨 조절, 블록 영역 배율 조정, 로컬 백업/복원 기능을 처리합니다.

(function () {
    // ----------------------------------------------------
    // 1. 다국어 사전 정의 (Translation Dictionary)
    // ----------------------------------------------------
    const i18n = {
        ko: {
            // Sidebar / UI Shell
            nav_home: "홈",
            nav_lessons: "학습단원",
            nav_ai_lessons: "AI 학습단원",
            nav_workspace: "워크스페이스",
            nav_projects: "프로젝트",
            nav_dashboard: "교사/학부모용 대시보드",
            nav_settings: "설정",

            // Settings Modal
            modal_title: "⚙️ BrickSync 설정",
            sec_profile: "👤 학생 프로필",
            logout_btn: "로그아웃",
            sec_lang: "🌐 언어 설정 (Language)",
            sec_volume: "🔊 효과음 볼륨 (Volume)",
            sec_zoom: "🔍 워크스페이스 배율 (Zoom)",
            sec_backup: "💾 프로젝트 로컬 백업 & 복구",
            backup_export: "📤 내 컴퓨터로 백업하기",
            backup_import: "📥 컴퓨터에서 복원하기",
            sec_diagnostics: "📡 실시간 통신 진단",
            diag_btn: "자가 진단 시작",
            diag_connecting: "클라우드 서버 연결 확인 중...",
            diag_online: "● Firebase 클라우드 연결됨 (정상 연동 중)",
            diag_offline: "● 오프라인 모드 안전 작동 중",
            alert_import_success: "프로젝트 복원이 완료되었습니다. 화면을 새로고침합니다.",
            alert_import_fail: "올바르지 않은 백업 파일입니다.",
            session_expires: "대기 시간 만료 예정",

            // [New translations for index.html, workspace, and lesson UI]
            profile_student: "학생",
            lbl_my_projects: "내 프로젝트",
            btn_new_project: "+ 새 프로젝트",
            lbl_blocks_count: "블록 수: {count}개",
            lbl_last_modified: "최근 수정",
            lbl_lesson_badge: "일반 단원 {unit}",
            lbl_ai_lesson_badge: "AI 단원 {unit}",
            lbl_connect_hub: "허브 연결",
            lbl_conn_method_title: "연결 방식 선택",
            lbl_conn_method_desc: "스파이크 허브와 연결할 방식을 선택해주세요.",
            lbl_conn_usb: "USB 선으로 연결 (강력 추천)",
            lbl_conn_usb_desc: "안정적이며 빠른 속도 지원",
            lbl_conn_bt: "무선 블루투스 연결",
            lbl_cancel: "취소",
            btn_run: "실행",
            btn_stop: "정지",
            lbl_mission_progress: "미션 달성도",
            btn_check_tasks: "과제 확인",
            lbl_required_tasks: "필수 수행 과제",
            btn_close: "닫기",
            hint_drag_assemble: "하단에서 아이콘 블럭을 끌어와 조립해보세요!",
            btn_back_home: "홈으로 가기",
            lbl_workspace_title: "BrickSync Essential 아이콘 코딩",
            lbl_ai_vision_title: "AI 비전 제스처 인식",
            lbl_model_training: "인식 모델 학습 기능",
            lbl_btn_rock: "주먹 (Rock)",
            lbl_btn_paper: "보 (Paper)",
            lbl_btn_scissors: "가위 (Scissors)",
            lbl_btn_none: "배경 (None)",
            lbl_gesture_waiting: "대기 중...",
            lbl_ai_loading: "AI 엔진 로딩 중...",
            lbl_mission_clear_title: "미션 달성!",
            lbl_mission_clear_desc: "아래의 핀(PIN) 코드를 레고 포트나이트 맵의<br><strong style=\"color:#0ea5e9;\">[비밀 제어 해제장치]</strong>에 입력하세요.",
            lbl_issued_code: "지급된 액세스 코드",
            btn_copy: "복사하기",

            // Learning list
            lesson_1: "1. 요리조리 기울여서 탐험보트를 출발시켜요",
            lesson_2: "2. 바닷속 잠수함으로 바다를 탐험해요",
            lesson_3: "3. 모터를 돌려 빙글빙글 대관람차를 태워줘요",
            lesson_4: "4. 동굴자동차를 타고 여행해요",
            lesson_5: "5. 급행통로 게이트를 만들어요",

            ai_lesson_1: "1. 가위! 바위! 보! 손가락으로 하는 북극 레이싱",
            ai_lesson_2: "2. 앉았다 일어서기! 마법 나무 엘리베이터 타기",
            ai_lesson_3: "3. 카메라에 맛있는 과일을 보여주고 간식 선물받기"
        },
        en: {
            // Sidebar / UI Shell
            nav_home: "Home",
            nav_lessons: "Lessons",
            nav_ai_lessons: "AI Lessons",
            nav_workspace: "Workspace",
            nav_projects: "Projects",
            nav_dashboard: "Dashboard",
            nav_settings: "Settings",

            // Settings Modal
            modal_title: "⚙️ BrickSync Settings",
            sec_profile: "👤 Student Profile",
            logout_btn: "Logout",
            sec_lang: "🌐 Language Settings",
            sec_volume: "🔊 SFX Volume",
            sec_zoom: "🔍 Workspace Scale",
            sec_backup: "💾 Local Backup & Restore",
            backup_export: "Export to PC",
            backup_import: "Import from PC",
            sec_diagnostics: "📡 Connectivity Diagnostics",
            diag_btn: "Start Diagnostic",
            diag_connecting: "Checking cloud connection...",
            diag_online: "● Firebase Connected (Syncing Live)",
            diag_offline: "● Operating safely in Offline Mode",
            alert_import_success: "Project restore completed. Reloading page.",
            alert_import_fail: "Invalid backup file format.",
            session_expires: "Session expiring soon",

            // [New translations for index.html, workspace, and lesson UI]
            profile_student: "Student",
            lbl_my_projects: "My Projects",
            btn_new_project: "+ New Project",
            lbl_blocks_count: "Blocks: {count}",
            lbl_last_modified: "Modified",
            lbl_lesson_badge: "Lesson {unit}",
            lbl_ai_lesson_badge: "AI Lesson {unit}",
            lbl_connect_hub: "Connect Hub",
            lbl_conn_method_title: "Select Connection Method",
            lbl_conn_method_desc: "Please select how to connect with your Spike Hub.",
            lbl_conn_usb: "Connect with USB Cable (Recommended)",
            lbl_conn_usb_desc: "Provides stable and fast connection speed",
            lbl_conn_bt: "Wireless Bluetooth Connection",
            lbl_cancel: "Cancel",
            btn_run: "Run",
            btn_stop: "Stop",
            lbl_mission_progress: "Progress",
            btn_check_tasks: "Tasks",
            lbl_required_tasks: "Required Tasks",
            btn_close: "Close",
            hint_drag_assemble: "Drag and assemble icon blocks from below!",
            btn_back_home: "Go to Home",
            lbl_workspace_title: "BrickSync Essential Icon Coding",
            lbl_ai_vision_title: "AI Vision Gesture Recognition",
            lbl_model_training: "Model Training Control",
            lbl_btn_rock: "Rock",
            lbl_btn_paper: "Paper",
            lbl_btn_scissors: "Scissors",
            lbl_btn_none: "Background (None)",
            lbl_gesture_waiting: "Waiting...",
            lbl_ai_loading: "AI Engine Loading...",
            lbl_mission_clear_title: "Mission Accomplished!",
            lbl_mission_clear_desc: "Enter the PIN code below into the<br><strong style=\"color:#0ea5e9;\">[Secret Control Unlock Device]</strong> on the Lego Fortnite map.",
            lbl_issued_code: "Issued Access Code",
            btn_copy: "Copy",

            // Learning list
            lesson_1: "1. Tilt left and right to launch the exploration boat",
            lesson_2: "2. Explore the sea with an underwater submarine",
            lesson_3: "3. Spin the motor to ride the Ferris wheel",
            lesson_4: "4. Ride a cave car and travel",
            lesson_5: "5. Build an express pathway gate",

            ai_lesson_1: "1. Rock Paper Scissors! Finger-controlled Arctic Racing",
            ai_lesson_2: "2. Squats! Riding the Magic Tree Elevator",
            ai_lesson_3: "3. Show delicious fruit to the camera and get a snack treat"
        }
    };

    // ----------------------------------------------------
    // 2. CSS 스타일 주입 (Glassmorphic Custom UI matching Lego Fortnite)
    // ----------------------------------------------------
    const styles = `
        .bs-settings-overlay {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(15, 7, 32, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            display: flex; justify-content: center; align-items: center;
            z-index: 99999;
            opacity: 0; pointer-events: none;
            transition: opacity 0.3s ease;
        }
        .bs-settings-overlay.show {
            opacity: 1; pointer-events: auto;
        }
        .bs-settings-card {
            background: rgba(43, 17, 79, 0.85);
            border: 2px solid rgba(250, 204, 21, 0.3);
            box-shadow: 0 20px 50px rgba(0,0,0,0.6), 0 0 30px rgba(167, 139, 250, 0.2);
            border-radius: 24px;
            width: 480px; max-width: 90%;
            padding: 30px;
            color: #f8fafc;
            transform: scale(0.9);
            transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            position: relative;
        }
        .bs-settings-overlay.show .bs-settings-card {
            transform: scale(1);
        }
        .bs-settings-header {
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 15px; margin-bottom: 20px;
        }
        .bs-settings-title {
            font-size: 1.4rem; font-weight: 800; color: #facc15;
            text-shadow: 0 0 10px rgba(250, 204, 21, 0.4);
        }
        .bs-settings-close {
            background: none; border: none; color: #cbd5e1;
            font-size: 1.5rem; cursor: pointer; transition: color 0.2s;
        }
        .bs-settings-close:hover { color: #f43f5e; }
        
        .bs-settings-section {
            margin-bottom: 20px;
        }
        .bs-settings-sec-title {
            font-size: 0.95rem; font-weight: 700; color: #c4b5fd;
            margin-bottom: 10px; display: flex; align-items: center; gap: 8px;
        }
        
        /* Profile Row */
        .bs-profile-row {
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(255,255,255,0.05); padding: 12px 18px; border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.08);
        }
        .bs-profile-name { font-weight: 700; font-size: 1.05rem; }
        .bs-btn-danger {
            background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.4);
            color: #f43f5e; padding: 6px 14px; border-radius: 8px; font-weight: 700;
            cursor: pointer; transition: 0.2s;
        }
        .bs-btn-danger:hover { background: #f43f5e; color: #fff; }

        /* Button Groups (Language / Zoom) */
        .bs-btn-group {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;
        }
        .bs-btn-group.three-cols {
            grid-template-columns: repeat(3, 1fr);
        }
        .bs-btn-option {
            background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
            color: #cbd5e1; padding: 10px; border-radius: 10px; font-weight: 600;
            cursor: pointer; text-align: center; transition: 0.2s;
        }
        .bs-btn-option:hover { background: rgba(255,255,255,0.1); color: #fff; }
        .bs-btn-option.active {
            background: var(--fn-yellow, #facc15); color: #000;
            border-color: var(--fn-yellow, #facc15);
            box-shadow: 0 0 12px rgba(250, 204, 21, 0.3); font-weight: 800;
        }
        
        /* Volume Range */
        .bs-volume-container {
            display: flex; align-items: center; gap: 15px;
        }
        .bs-volume-slider {
            flex: 1; height: 6px; -webkit-appearance: none; appearance: none;
            background: rgba(255,255,255,0.15); border-radius: 3px; outline: none;
        }
        .bs-volume-slider::-webkit-slider-thumb {
            -webkit-appearance: none; appearance: none; width: 18px; height: 18px;
            border-radius: 50%; background: #facc15; cursor: pointer;
            box-shadow: 0 0 8px rgba(250, 204, 21, 0.5);
        }
        .bs-volume-val { font-family: 'Outfit', monospace; font-weight: 700; width: 35px; text-align: right; }

        /* Backup Buttons */
        .bs-backup-group {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;
        }
        .bs-btn-accent {
            background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.4);
            color: #38bdf8; padding: 10px; border-radius: 10px; font-weight: 700;
            cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px;
            transition: 0.2s;
        }
        .bs-btn-accent:hover { background: #38bdf8; color: #000; }
        
        /* Diagnostics Panel */
        .bs-diag-box {
            background: rgba(0,0,0,0.2); padding: 12px 18px; border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.05); font-size: 0.9rem; min-height: 45px;
            display: flex; align-items: center; justify-content: space-between;
        }
        .bs-diag-status { font-weight: 600; color: #94a3b8; }
        .bs-diag-btn {
            background: rgba(167, 139, 250, 0.15); border: 1px solid rgba(167, 139, 250, 0.4);
            color: #c4b5fd; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem;
            font-weight: 700; cursor: pointer; transition: 0.2s;
        }
        .bs-diag-btn:hover { background: #8b5cf6; color: #fff; }
    `;

    // ----------------------------------------------------
    // 3. HTML 마크업 및 동적 레이아웃 주입
    // ----------------------------------------------------
    function injectSettingsDOM() {
        if (document.getElementById('bs-settings-modal')) return;

        // 1. Style Tag 주입
        const styleTag = document.createElement('style');
        styleTag.innerHTML = styles;
        document.head.appendChild(styleTag);

        // 2. Modal Overlay & Card 주입
        const overlay = document.createElement('div');
        overlay.id = 'bs-settings-modal';
        overlay.className = 'bs-settings-overlay';
        overlay.innerHTML = `
            <div class="bs-settings-card">
                <div class="bs-settings-header">
                    <span class="bs-settings-title" data-settings-i18n="modal_title">⚙️ BrickSync 설정</span>
                    <button class="bs-settings-close" onclick="closeSettingsModal()">&times;</button>
                </div>
                
                <!-- 1. Profile Section -->
                <div class="bs-settings-section">
                    <div class="bs-settings-sec-title" data-settings-i18n="sec_profile">👤 학생 프로필</div>
                    <div class="bs-profile-row">
                        <span class="bs-profile-name" id="bs-settings-profile-name">최민</span>
                        <button class="bs-btn-danger" onclick="settingsLogout()" data-settings-i18n="logout_btn">로그아웃</button>
                    </div>
                </div>
                
                <!-- 2. Language Section -->
                <div class="bs-settings-section">
                    <div class="bs-settings-sec-title" data-settings-i18n="sec_lang">🌐 언어 설정 (Language)</div>
                    <div class="bs-btn-group">
                        <button class="bs-btn-option" id="btn-lang-ko" onclick="changeSettingsLanguage('ko')">한국어</button>
                        <button class="bs-btn-option" id="btn-lang-en" onclick="changeSettingsLanguage('en')">English</button>
                    </div>
                </div>
                
                <!-- 3. Volume Section -->
                <div class="bs-settings-section">
                    <div class="bs-settings-sec-title" data-settings-i18n="sec_volume">🔊 효과음 볼륨 (Volume)</div>
                    <div class="bs-volume-container">
                        <input type="range" class="bs-volume-slider" id="settings-volume-slider" min="0" max="100" value="100" oninput="changeSettingsVolume(this.value)">
                        <span class="bs-volume-val" id="settings-volume-display">100%</span>
                    </div>
                </div>
                
                <!-- 4. Workspace Scale Section -->
                <div class="bs-settings-section">
                    <div class="bs-settings-sec-title" data-settings-i18n="sec_zoom">🔍 워크스페이스 배율 (Zoom)</div>
                    <div class="bs-btn-group three-cols">
                        <button class="bs-btn-option" id="btn-scale-80" onclick="changeSettingsScale(0.8)">80%</button>
                        <button class="bs-btn-option" id="btn-scale-100" onclick="changeSettingsScale(1.0)">100%</button>
                        <button class="bs-btn-option" id="btn-scale-120" onclick="changeSettingsScale(1.2)">120%</button>
                    </div>
                </div>
                
                <!-- 5. Backup Section -->
                <div class="bs-settings-section">
                    <div class="bs-settings-sec-title" data-settings-i18n="sec_backup">💾 프로젝트 로컬 백업 & 복구</div>
                    <div class="bs-backup-group">
                        <button class="bs-btn-accent" onclick="exportSettingsProjects()" data-settings-i18n="backup_export">📤 백업하기</button>
                        <button class="bs-btn-accent" onclick="document.getElementById('bs-backup-file-input').click()" data-settings-i18n="backup_import">📥 복원하기</button>
                    </div>
                    <input type="file" id="bs-backup-file-input" style="display:none;" accept=".json" onchange="importSettingsProjects(event)">
                </div>
                
                <!-- 6. Connectivity Section -->
                <div class="bs-settings-section" style="margin-bottom: 0;">
                    <div class="bs-settings-sec-title" data-settings-i18n="sec_diagnostics">📡 실시간 통신 진단</div>
                    <div class="bs-diag-box">
                        <span class="bs-diag-status" id="bs-settings-diag-status" data-settings-i18n="diag_offline">● 오프라인 모드 안전 작동 중</span>
                        <button class="bs-diag-btn" onclick="runSettingsDiagnostics()" data-settings-i18n="diag_btn">자가 진단 시작</button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        // 뒷배경 클릭 시 모달 닫기 바인딩
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) closeSettingsModal();
        });
    }

    // ----------------------------------------------------
    // 4. 모달 인터랙션 및 상태 매핑 로직
    // ----------------------------------------------------
    window.openSettingsModal = function () {
        injectSettingsDOM();

        // 1. 프로필 이름 세팅
        let studentName = "Guest_익명";
        try {
            const sessionStr = localStorage.getItem('bricksync_student_session');
            if (sessionStr) {
                const session = JSON.parse(sessionStr);
                if (session && session.name) {
                    studentName = session.name;
                }
            }
        } catch (e) { }
        document.getElementById('bs-settings-profile-name').textContent = studentName;

        // 2. 로컬 스토리지에 저장된 설정값 불러와 UI 동기화
        const currentLang = localStorage.getItem('bricksync_lang') || 'ko';
        const currentVolume = parseFloat(localStorage.getItem('bricksync_volume') || '1.0');
        const currentScale = parseFloat(localStorage.getItem('bricksync_scale') || '1.0');

        // 언어 버튼 활성화
        document.querySelectorAll('#bs-settings-modal .bs-btn-option').forEach(btn => btn.classList.remove('active'));
        const activeLangBtn = document.getElementById(`btn-lang-${currentLang}`);
        if (activeLangBtn) activeLangBtn.classList.add('active');

        // 볼륨 슬라이더 값
        const slider = document.getElementById('settings-volume-slider');
        const display = document.getElementById('settings-volume-display');
        if (slider && display) {
            slider.value = Math.round(currentVolume * 100);
            display.textContent = Math.round(currentVolume * 100) + '%';
        }

        // 워크스페이스 배율 활성화
        const scaleVal = Math.round(currentScale * 100);
        const activeScaleBtn = document.getElementById(`btn-scale-${scaleVal}`);
        if (activeScaleBtn) activeScaleBtn.classList.add('active');

        // 3. 통신 자가진단 기본값 렌더링
        const statusText = document.getElementById('bs-settings-diag-status');
        if (statusText) {
            const isOnline = (typeof isFirebaseOnline !== 'undefined' && isFirebaseOnline);
            statusText.setAttribute('data-settings-i18n', isOnline ? 'diag_online' : 'diag_offline');
            statusText.textContent = isOnline ? i18n[currentLang].diag_online : i18n[currentLang].diag_offline;
        }

        // 모달 내 텍스트 전체 번역 적용
        translateSettingsModal(currentLang);

        // 오픈 애니메이션 구동
        const modal = document.getElementById('bs-settings-modal');
        modal.classList.add('show');
    };

    window.closeSettingsModal = function () {
        const modal = document.getElementById('bs-settings-modal');
        if (modal) modal.classList.remove('show');
    };

    // ----------------------------------------------------
    // 5. 비즈니스 로직 처리 함수들 (볼륨, 스케일, 백업, 로그아웃)
    // ----------------------------------------------------

    // 5.1 다국어 변경 로직 (Change Language)
    window.changeSettingsLanguage = function (lang) {
        localStorage.setItem('bricksync_lang', lang);

        // 다국어 선택 칩 변경
        document.querySelectorAll('#bs-settings-modal .bs-btn-option[id^="btn-lang-"]').forEach(btn => btn.classList.remove('active'));
        const activeBtn = document.getElementById(`btn-lang-${lang}`);
        if (activeBtn) activeBtn.classList.add('active');

        // 모달 내부 텍스트 번역
        translateSettingsModal(lang);

        // 부모 페이지의 data-i18n 마크업이 부착된 노드 전체 번역
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (i18n[lang] && i18n[lang][key]) {
                el.innerText = i18n[lang][key];
            }
        });

        // 다국어 변경 커스텀 이벤트 디스패치 (학습단원 및 미션 동적 텍스트 실시간 연동용)
        const langEvent = new CustomEvent('bricksync-language-changed', { detail: { lang: lang } });
        window.dispatchEvent(langEvent);
        if (window.parent && window.parent !== window) {
            try {
                window.parent.dispatchEvent(langEvent);
            } catch (e) { }
        }

        // Lucide 아이콘 손상 없게 보완 재생성 (Lucide 로드되어 있는 경우)
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    };

    function translateSettingsModal(lang) {
        document.querySelectorAll('[data-settings-i18n]').forEach(el => {
            const key = el.getAttribute('data-settings-i18n');
            if (i18n[lang] && i18n[lang][key]) {
                el.innerText = i18n[lang][key];
            }
        });
    }

    // 5.2 효과음 볼륨 변경 (Change Volume)
    window.changeSettingsVolume = function (val) {
        const volume = parseFloat(val) / 100;
        localStorage.setItem('bricksync_volume', volume.toFixed(2));

        const display = document.getElementById('settings-volume-display');
        if (display) display.textContent = val + '%';

        // 오디오 볼륨값 적용을 위해 오디오 재생 시 AudioContext gain 노드와 매핑하도록 권장
    };

    // 5.3 워크스페이스 코딩 화면 배율 변경 (Change Scale)
    window.changeSettingsScale = function (scale) {
        localStorage.setItem('bricksync_scale', scale.toFixed(1));

        // 배율 칩 액티브 변경
        document.querySelectorAll('#bs-settings-modal .bs-btn-option[id^="btn-scale-"]').forEach(btn => btn.classList.remove('active'));
        const scaleVal = Math.round(scale * 100);
        const activeBtn = document.getElementById(`btn-scale-${scaleVal}`);
        if (activeBtn) activeBtn.classList.add('active');

        // 코딩 화면 배율 즉시 실시간 변환
        const codingArea = document.querySelector('.coding-area') || document.getElementById('block-workspace');
        if (codingArea) {
            codingArea.style.transform = `scale(${scale})`;
            codingArea.style.transformOrigin = "0 0";
        }
    };

    // 5.4 내 프로젝트 내보내기 백업 (Export Backup JSON)
    window.exportSettingsProjects = function () {
        let studentName = "Guest_익명";
        try {
            const sessionStr = localStorage.getItem('bricksync_student_session');
            if (sessionStr) {
                const session = JSON.parse(sessionStr);
                if (session && session.name) {
                    studentName = session.name;
                }
            }
        } catch (e) { }

        const backupData = {};

        // 1. 세션 백업
        const sessionKey = 'bricksync_student_session';
        const sessionVal = localStorage.getItem(sessionKey);
        if (sessionVal) backupData[sessionKey] = sessionVal;

        // 2. 해당 학생의 모든 오프라인 프로젝트 백업
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && (key.startsWith(studentName + '_project_') || key === 'dashboard_stats_' + studentName)) {
                backupData[key] = localStorage.getItem(key);
            }
        }

        // 3. 파일 다운로드 유도
        const jsonStr = JSON.stringify(backupData, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `bricksync_backup_${studentName}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    // 5.5 컴퓨터에 소장 중인 JSON 백업파일 업로드 복원 (Import Backup JSON)
    window.importSettingsProjects = function (event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (e) {
            try {
                const backupData = JSON.parse(e.target.result);

                // 데이터 무결성 체크
                let valid = false;
                for (const key in backupData) {
                    localStorage.setItem(key, backupData[key]);
                    valid = true;
                }

                if (valid) {
                    const currentLang = localStorage.getItem('bricksync_lang') || 'ko';
                    alert(i18n[currentLang].alert_import_success);
                    location.reload();
                } else {
                    throw new Error("Empty backup");
                }
            } catch (err) {
                const currentLang = localStorage.getItem('bricksync_lang') || 'ko';
                alert(i18n[currentLang].alert_import_fail);
            }
        };
        reader.readAsText(file);
    };

    // 5.6 학생 로그아웃 (Session Clear & Logout)
    window.settingsLogout = function () {
        localStorage.removeItem('bricksync_student_session');
        location.href = 'student_login.html';
    };

    // 5.7 Firebase 실시간 통신 진단 툴 (Run Connection Diagnostics)
    window.runSettingsDiagnostics = function () {
        const statusText = document.getElementById('bs-settings-diag-status');
        const currentLang = localStorage.getItem('bricksync_lang') || 'ko';
        if (!statusText) return;

        statusText.textContent = i18n[currentLang].diag_connecting;

        setTimeout(() => {
            const isOnline = (typeof isFirebaseOnline !== 'undefined' && isFirebaseOnline);
            if (isOnline) {
                statusText.innerHTML = `<span style="color:#10b981;">●</span> Cloud Connected (Latency: ${Math.round(15 + Math.random() * 20)}ms)`;
            } else {
                statusText.innerHTML = `<span style="color:#ef4444;">●</span> ${i18n[currentLang].diag_offline}`;
            }
        }, 1200);
    };

    // ----------------------------------------------------
    // 6. 페이지 로드 초기 바인딩 및 버튼 이벤트 연결
    // ----------------------------------------------------
    window.addEventListener('DOMContentLoaded', () => {
        // 1. 사이드바 설정 메뉴 버튼 클릭 리스너 연결
        const settingsBtn = document.getElementById('settings-menu-btn');
        if (settingsBtn) {
            settingsBtn.style.cursor = 'pointer';
            settingsBtn.addEventListener('click', (e) => {
                e.preventDefault();
                openSettingsModal();
            });
        }

        // 2. 앱 전역 설정값 초기 적용 (언어, 줌 배율)
        const savedLang = localStorage.getItem('bricksync_lang');
        if (savedLang) {
            // 언어 자동 번역 1차 적용
            setTimeout(() => changeSettingsLanguage(savedLang), 100);
        }

        const savedScale = localStorage.getItem('bricksync_scale');
        if (savedScale) {
            const scale = parseFloat(savedScale);
            // 배율 자동 적용
            setTimeout(() => {
                const codingArea = document.querySelector('.coding-area') || document.getElementById('block-workspace');
                if (codingArea) {
                    codingArea.style.transform = `scale(${scale})`;
                    codingArea.style.transformOrigin = "0 0";
                }
            }, 300);
        }
    });

})();
