// BrickSync - Firestore 클라우드 저장/불러오기 공통 모듈 (cloud_storage.js)
// ============================================================
// 의존성: firebase_config.js (firestore, firebaseAuth 전역 변수)
// 사용법: lesson.html, ai_fusion.html, index.html에서 include 후 사용
// ============================================================

const BrickSyncCloud = (() => {

    // ── 저장 상태 배지 UI ─────────────────────────────────────
    let _saveStatusEl = null;
    let _saveStatusTimer = null;

    function _getOrCreateStatusEl() {
        if (_saveStatusEl) return _saveStatusEl;
        _saveStatusEl = document.createElement('div');
        _saveStatusEl.id = 'bs-cloud-status';
        _saveStatusEl.style.cssText = `
            position: fixed;
            top: 14px;
            right: 20px;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
            font-family: 'Outfit', sans-serif;
            z-index: 99999;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        `;
        document.body.appendChild(_saveStatusEl);
        return _saveStatusEl;
    }

    /**
     * 저장 상태 배지 표시
     * @param {'saving'|'saved'|'error'|'loading'} status
     * @param {string} [msg] 커스텀 메시지
     */
    function showStatus(status, msg) {
        const el = _getOrCreateStatusEl();
        clearTimeout(_saveStatusTimer);

        const configs = {
            saving:  { bg: 'rgba(99,102,241,0.92)',  text: '#fff', icon: '⏳', label: '클라우드 저장 중...' },
            saved:   { bg: 'rgba(16,185,129,0.92)',  text: '#fff', icon: '☁️', label: '저장됨' },
            error:   { bg: 'rgba(239,68,68,0.92)',   text: '#fff', icon: '⚠️', label: '저장 실패 (로컬 보존)' },
            loading: { bg: 'rgba(245,158,11,0.92)',  text: '#fff', icon: '🔄', label: '불러오는 중...' }
        };
        const c = configs[status] || configs.saved;
        el.style.background = c.bg;
        el.style.color = c.text;
        el.innerHTML = `<span>${c.icon}</span><span>${msg || c.label}</span>`;
        el.style.opacity = '1';

        if (status === 'saved' || status === 'error') {
            _saveStatusTimer = setTimeout(() => { el.style.opacity = '0'; }, 2500);
        }
    }

    // ── Firestore 가용성 확인 ─────────────────────────────────
    function _isAvailable() {
        return typeof firestore !== 'undefined' && firestore &&
               typeof firebaseAuth !== 'undefined' && firebaseAuth &&
               firebaseAuth.currentUser;
    }

    function _getUid() {
        return firebaseAuth?.currentUser?.uid || null;
    }

    // ── 핵심 CRUD ─────────────────────────────────────────────

    // Date.now() 기반 타임스탬프 (FieldValue 충돌 방지)
    function _nowTS() { return Date.now(); }

    /**
     * Firestore에 프로젝트 저장 (비동기, 백그라운드)
     * @param {string} docId  Firestore 문서 ID (예: 'unit_1', 'ai_3')
     * @param {Object} data   프로젝트 데이터 객체
     * @param {boolean} [silent] true이면 상태 배지 숨김
     */
    async function saveProject(docId, data, silent = false) {
        if (!_isAvailable()) return false;
        const uid = _getUid();
        if (!silent) showStatus('saving');
        try {
            const now = _nowTS();
            await firestore
                .collection('projects')
                .doc(uid)
                .collection('items')
                .doc(docId)
                .set({
                    ...data,
                    uid,
                    updatedAt: now,
                    createdAt: data.createdAt || now
                }, { merge: true });
            if (!silent) showStatus('saved');
            return true;
        } catch (e) {
            console.error('[Cloud] 저장 실패:', e);
            if (!silent) showStatus('error');
            return false;
        }
    }

    /**
     * Firestore에서 프로젝트 불러오기
     * @param {string} docId
     * @returns {Object|null}
     */
    async function loadProject(docId) {
        if (!_isAvailable()) return null;
        const uid = _getUid();
        try {
            const snap = await firestore
                .collection('projects')
                .doc(uid)
                .collection('items')
                .doc(docId)
                .get();
            return snap.exists ? snap.data() : null;
        } catch (e) {
            console.error('[Cloud] 불러오기 실패:', e);
            return null;
        }
    }

    /**
     * 학생의 모든 프로젝트 목록 조회
     * @returns {Array}
     */
    async function listProjects() {
        if (!_isAvailable()) return [];
        const uid = _getUid();
        try {
            const snap = await firestore
                .collection('projects')
                .doc(uid)
                .collection('items')
                .orderBy('updatedAt', 'desc')
                .get();
            return snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        } catch (e) {
            console.error('[Cloud] 목록 조회 실패:', e);
            return [];
        }
    }

    /**
     * Firestore에서 프로젝트 삭제
     * @param {string} docId
     */
    async function deleteProject(docId) {
        if (!_isAvailable()) return false;
        const uid = _getUid();
        try {
            await firestore
                .collection('projects')
                .doc(uid)
                .collection('items')
                .doc(docId)
                .delete();
            return true;
        } catch (e) {
            console.error('[Cloud] 삭제 실패:', e);
            return false;
        }
    }

    // ── localStorage → Firestore 마이그레이션 ─────────────────

    /**
     * 기존 localStorage 데이터를 Firestore로 1회 이전
     * @param {string} studentName  localStorage 키 prefix로 사용된 학생 이름
     */
    async function migrateFromLocalStorage(studentName) {
        if (!_isAvailable()) return;
        if (!studentName) return;

        // 이미 마이그레이션했는지 확인
        const uid = _getUid();
        const migKey = `bs_migrated_${uid}`;
        if (localStorage.getItem(migKey)) return;

        const prefix = studentName + '_project_';
        const toMigrate = [];

        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (!key || !key.startsWith(prefix)) continue;
            try {
                const raw = localStorage.getItem(key);
                if (!raw) continue;
                const data = JSON.parse(raw);
                if (!data || !data.blocks || data.blocks.length === 0) continue;

                // Firestore docId 생성: {학생명}_project_unit_1 → unit_1
                const docId = key.replace(prefix, '').replace('unit_', 'unit_').replace('ai_', 'ai_');
                toMigrate.push({ docId, data });
            } catch (e) {}
        }

        if (toMigrate.length === 0) {
            localStorage.setItem(migKey, '1');
            return;
        }

        console.log(`[Cloud] 마이그레이션 시작: ${toMigrate.length}개 프로젝트`);
        showStatus('saving', `☁️ 기존 프로젝트 ${toMigrate.length}개 클라우드 이전 중...`);

        let ok = 0;
        for (const { docId, data } of toMigrate) {
            const success = await saveProject(docId, data, true);
            if (success) ok++;
        }

        localStorage.setItem(migKey, '1');
        showStatus('saved', `☁️ ${ok}개 프로젝트 클라우드 저장 완료!`);
        console.log(`[Cloud] 마이그레이션 완료: ${ok}/${toMigrate.length}`);
    }

    // ── 공개 API ──────────────────────────────────────────────
    return {
        saveProject,
        loadProject,
        listProjects,
        deleteProject,
        migrateFromLocalStorage,
        showStatus,
        isAvailable: _isAvailable
    };

})();
