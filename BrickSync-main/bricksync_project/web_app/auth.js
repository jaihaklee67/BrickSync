// BrickSync - 역할 기반 인증 공통 모듈 (auth.js)
// ============================================================
// 로그인/회원가입/로그아웃 + 역할별(student/teacher/parent) 접근 제어
// firebase_config.js 이후에 로드되어야 합니다.
// ============================================================

const BrickSyncAuth = (() => {

    // ── 역할별 접근 허용 페이지 맵 ────────────────────────────────
    const ROLE_HOME = {
        student: 'index.html',
        teacher: 'teacher_dashboard.html',
        parent: 'parent_dashboard.html'
    };

    const ROLE_LABELS = {
        student: '학생',
        teacher: '교사',
        parent: '학부모'
    };

    // ── 내부 유틸 ─────────────────────────────────────────────────

    /**
     * Firestore에서 사용자 프로필(역할 포함) 조회
     * @param {string} uid
     * @returns {Promise<Object|null>}
     */
    async function getUserProfile(uid) {
        if (!firestore) return null;
        try {
            const doc = await firestore.collection('users').doc(uid).get();
            return doc.exists ? doc.data() : null;
        } catch (e) {
            console.error('[Auth] 프로필 조회 실패:', e);
            return null;
        }
    }

    /**
     * Firestore에 사용자 프로필 생성/업데이트
     */
    async function setUserProfile(uid, data) {
        if (!firestore) return;
        await firestore.collection('users').doc(uid).set(data, { merge: true });
    }

    /**
     * 클래스 코드 유효성 검증 (교사 발급 코드인지 확인)
     * @param {string} classCode
     * @returns {Promise<Object|null>} 클래스 정보 또는 null
     */
    async function validateClassCode(classCode) {
        if (!firestore) return null;
        try {
            const doc = await firestore.collection('classes').doc(classCode).get();
            return doc.exists ? { id: classCode, ...doc.data() } : null;
        } catch (e) {
            console.error('[Auth] 클래스 코드 검증 실패:', e);
            return null;
        }
    }

    /**
     * 학부모 연결 코드 유효성 검증
     * @param {string} parentCode
     * @returns {Promise<Object|null>} 연결 정보 또는 null
     */
    async function validateParentCode(parentCode) {
        if (!firestore) return null;
        try {
            const doc = await firestore.collection('parentCodes').doc(parentCode).get();
            if (!doc.exists) return null;
            const data = doc.data();
            // 코드 만료 여부 확인 (7일)
            if (data.expiresAt && data.expiresAt.toMillis() < Date.now()) {
                return null;
            }
            return { id: parentCode, ...data };
        } catch (e) {
            console.error('[Auth] 학부모 코드 검증 실패:', e);
            return null;
        }
    }

    // ── 공개 API ──────────────────────────────────────────────────

    /**
     * 현재 로그인 상태 감지 + 프로필 반환
     * @returns {Promise<{user, profile}|null>}
     */
    async function getCurrentUser() {
        if (!firebaseAuth) {
            // Firebase 미연결 시 localStorage 레거시 세션 확인
            const legacy = getLegacySession();
            if (legacy) return { user: null, profile: { role: 'student', displayName: legacy.name }, legacy: true };
            return null;
        }

        return new Promise((resolve) => {
            firebaseAuth.onAuthStateChanged(async (user) => {
                if (!user) { resolve(null); return; }
                const profile = await getUserProfile(user.uid);
                resolve({ user, profile });
            });
        });
    }

    /**
     * 이메일/비밀번호 로그인
     * @param {string} email
     * @param {string} password
     * @returns {Promise<{user, profile}>}
     */
    async function signIn(email, password) {
        if (!firebaseAuth) throw new Error('Firebase Auth 미초기화');
        const cred = await firebaseAuth.signInWithEmailAndPassword(email, password);
        const profile = await getUserProfile(cred.user.uid);
        if (!profile) throw new Error('사용자 프로필을 찾을 수 없습니다.');
        return { user: cred.user, profile };
    }

    /**
     * 학생 회원가입 (클래스 코드 필수)
     */
    async function signUpStudent({ email, password, displayName, classCode }) {
        if (!firebaseAuth || !firestore) throw new Error('Firebase 미초기화');

        // 1. 먼저 계정 생성 (로그인 상태가 되어야 Firestore 읽기 가능)
        const cred = await firebaseAuth.createUserWithEmailAndPassword(email, password);
        await cred.user.updateProfile({ displayName });

        // 2. 로그인 상태에서 클래스 코드 검증
        const classInfo = await validateClassCode(classCode);
        if (!classInfo) {
            // 코드 무효 시 생성된 계정 삭제 후 오류
            await cred.user.delete();
            throw new Error('유효하지 않은 클래스 코드입니다. 선생님께 확인하세요.');
        }

        // 3. Firestore 프로필 저장
        const profile = {
            uid: cred.user.uid,
            email,
            displayName,
            role: 'student',
            classCode,
            teacherUid: classInfo.teacherUid,
            className: classInfo.className,
            createdAt: firebase.firestore.FieldValue.serverTimestamp()
        };
        await setUserProfile(cred.user.uid, profile);

        // 4. 클래스에 학생 추가
        await firestore.collection('classes').doc(classCode).update({
            studentUids: firebase.firestore.FieldValue.arrayUnion(cred.user.uid)
        });

        return { user: cred.user, profile };
    }

    /**
     * 교사 회원가입
     */
    async function signUpTeacher({ email, password, displayName, schoolName }) {
        if (!firebaseAuth || !firestore) throw new Error('Firebase 미초기화');

        const cred = await firebaseAuth.createUserWithEmailAndPassword(email, password);
        await cred.user.updateProfile({ displayName });

        const profile = {
            uid: cred.user.uid,
            email,
            displayName,
            role: 'teacher',
            schoolName: schoolName || '',
            createdAt: firebase.firestore.FieldValue.serverTimestamp()
        };
        await setUserProfile(cred.user.uid, profile);

        return { user: cred.user, profile };
    }

    /**
     * 학부모 회원가입 (교사 발급 연결 코드 필수)
     */
    async function signUpParent({ email, password, displayName, parentCode }) {
        if (!firebaseAuth || !firestore) throw new Error('Firebase 미초기화');

        // 1. 먼저 계정 생성 (로그인 상태에서 코드 검증 가능)
        const cred = await firebaseAuth.createUserWithEmailAndPassword(email, password);
        await cred.user.updateProfile({ displayName });

        // 2. 로그인 상태에서 학부모 연결 코드 검증
        const codeInfo = await validateParentCode(parentCode);
        if (!codeInfo) {
            await cred.user.delete();
            throw new Error('유효하지 않거나 만료된 연결 코드입니다. 담임 선생님께 문의하세요.');
        }

        // 3. Firestore 프로필 저장
        const profile = {
            uid: cred.user.uid,
            email,
            displayName,
            role: 'parent',
            linkedStudentUid: codeInfo.studentUid,
            linkedStudentName: codeInfo.studentName,
            teacherUid: codeInfo.teacherUid,
            createdAt: firebase.firestore.FieldValue.serverTimestamp()
        };
        await setUserProfile(cred.user.uid, profile);

        // 4. 사용된 코드 만료 처리
        await firestore.collection('parentCodes').doc(parentCode).update({
            usedByUid: cred.user.uid,
            usedAt: firebase.firestore.FieldValue.serverTimestamp()
        });

        return { user: cred.user, profile };
    }

    /**
     * 로그아웃
     */
    async function signOut() {
        // 레거시 세션도 함께 정리
        localStorage.removeItem('bricksync_student_session');
        if (firebaseAuth) {
            await firebaseAuth.signOut();
        }
        window.location.href = 'login.html';
    }

    /**
     * 역할에 따라 홈 화면으로 리다이렉트
     */
    function redirectToHome(role) {
        const target = ROLE_HOME[role] || 'index.html';
        window.location.href = target;
    }

    /**
     * 현재 페이지 접근 권한 확인 (허가되지 않은 역할이면 리다이렉트)
     * @param {string[]} allowedRoles - 허용할 역할 배열 (예: ['teacher'])
     */
    async function requireRole(allowedRoles) {
        const session = await getCurrentUser();
        if (!session) {
            window.location.href = 'login.html';
            return null;
        }
        const role = session.profile?.role;
        if (allowedRoles && allowedRoles.length > 0 && !allowedRoles.includes(role)) {
            alert(`이 페이지는 ${allowedRoles.map(r => ROLE_LABELS[r] || r).join('/')} 전용입니다.`);
            redirectToHome(role);
            return null;
        }
        return session;
    }

    /**
     * 레거시 localStorage 세션 읽기 (이전 버전 호환)
     */
    function getLegacySession() {
        try {
            const raw = localStorage.getItem('bricksync_student_session');
            if (!raw) return null;
            const data = JSON.parse(raw);
            if (Date.now() > data.expires) {
                localStorage.removeItem('bricksync_student_session');
                return null;
            }
            return data;
        } catch {
            return null;
        }
    }

    // ── 교사 전용: 클래스 코드 발급 ──────────────────────────────
    async function createClassCode(teacherUid, className) {
        if (!firestore) throw new Error('Firestore 미초기화');
        // 6자리 영문+숫자 코드 생성
        const code = 'BS-' + Math.random().toString(36).substring(2, 8).toUpperCase();
        await firestore.collection('classes').doc(code).set({
            teacherUid,
            className,
            studentUids: [],
            createdAt: firebase.firestore.FieldValue.serverTimestamp()
        });
        return code;
    }

    // ── 교사 전용: 학부모 연결 코드 발급 ─────────────────────────
    async function createParentCode(teacherUid, studentUid, studentName) {
        if (!firestore) throw new Error('Firestore 미초기화');
        const code = 'PRT-' + Math.random().toString(36).substring(2, 9).toUpperCase();
        const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000); // 7일 유효
        await firestore.collection('parentCodes').doc(code).set({
            teacherUid,
            studentUid,
            studentName,
            expiresAt: firebase.firestore.Timestamp.fromDate(expiresAt),
            usedByUid: null,
            createdAt: firebase.firestore.FieldValue.serverTimestamp()
        });
        return code;
    }

    return {
        getCurrentUser,
        signIn,
        signUpStudent,
        signUpTeacher,
        signUpParent,
        signOut,
        redirectToHome,
        requireRole,
        getLegacySession,
        createClassCode,
        createParentCode,
        getUserProfile,
        ROLE_HOME,
        ROLE_LABELS
    };
})();
