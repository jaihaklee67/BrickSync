// BrickSync - Firebase 실시간 DB 공통 설정 파일
// 구글 Firebase 콘솔(console.firebase.google.com)에서 발급받은 웹 앱 설정값을 아래에 복사해서 붙여넣으세요.
const firebaseConfig = {
    apiKey: "YOUR_API_KEY_HERE",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    databaseURL: "https://YOUR_PROJECT_ID-default-rtdb.firebaseio.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};

let database = null;
let isFirebaseOnline = false;

// 학교 방화벽 차단 등으로 SDK가 로드되지 않았을 경우를 대비한 안전 예외 처리
try {
    if (typeof firebase !== 'undefined' && firebaseConfig.apiKey && firebaseConfig.apiKey !== "YOUR_API_KEY_HERE") {
        firebase.initializeApp(firebaseConfig);
        database = firebase.database();
        isFirebaseOnline = true;
        console.log("Firebase Realtime Database가 연결되었습니다. (실시간 원격 동기화 작동)");
    } else {
        console.warn("Firebase SDK가 로드되지 않았거나 설정이 완료되지 않았습니다. 오프라인 모드로 안전하게 작동합니다.");
    }
} catch (e) {
    console.error("Firebase 초기화 에러 (오프라인 모드 자동 전환):", e);
}
