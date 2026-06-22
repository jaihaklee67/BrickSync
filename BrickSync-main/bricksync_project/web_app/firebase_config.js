// BrickSync - Firebase 통합 설정 파일 (Auth + Firestore)
// ============================================================
// [v2.0] Firebase Authentication + Firestore 기반 역할별 인증 시스템
// 프로젝트: bricksync-1e814
// ============================================================

const firebaseConfig = {
    apiKey: "AIzaSyCSojrWgkQdtXGcbeUwdlJKmKJcLBupN7o",
    authDomain: "bricksync-1e814.firebaseapp.com",
    projectId: "bricksync-1e814",
    storageBucket: "bricksync-1e814.firebasestorage.app",
    messagingSenderId: "585550769605",
    appId: "1:585550769605:web:7b14af2edaadfa7f062fac"
};

// ── 전역 서비스 인스턴스 ──────────────────────────────────────
let database = null;        // Realtime DB (레거시 호환용)
let firestore = null;       // Firestore (신규 인증/데이터용)
let firebaseAuth = null;    // Firebase Authentication
let isFirebaseOnline = false;

try {
    if (typeof firebase !== 'undefined') {
        // 중복 초기화 방지
        if (!firebase.apps.length) {
            firebase.initializeApp(firebaseConfig);
        }

        // Auth 초기화
        if (typeof firebase.auth === 'function') {
            firebaseAuth = firebase.auth();
            console.log('[BrickSync] Firebase Auth 초기화 완료');
        }

        // Firestore 초기화
        if (typeof firebase.firestore === 'function') {
            firestore = firebase.firestore();
            console.log('[BrickSync] Firestore 초기화 완료');
        }

        // Realtime DB (기존 코드 호환성 유지)
        if (typeof firebase.database === 'function') {
            database = firebase.database();
            isFirebaseOnline = true;
            console.log('[BrickSync] Realtime DB 초기화 완료 (레거시 호환)');
        }

    } else {
        console.warn('[BrickSync] Firebase SDK 미로드 → 오프라인 모드');
    }
} catch (e) {
    console.error('[BrickSync] Firebase 초기화 오류 (오프라인 모드 전환):', e);
}
