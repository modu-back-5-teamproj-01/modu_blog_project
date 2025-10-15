// 로그인 토큰 확인
const token = localStorage.getItem("token");
if (!token) {
    alert("로그인 후 사용 가능합니다.");
    window.location.href = "/static/index.html";
}

// DOM
const usernameSpan = document.getElementById("username");
const emailSpan = document.getElementById("email");
const bioSpan = document.getElementById("bio");

const backBtn = document.getElementById("backBtn");
const editProfileBtn = document.getElementById("editProfileBtn");
const changePasswordBtn = document.getElementById("changePasswordBtn");

// ---------------------------
// 사용자 정보 불러오기: GET /auth/me
// ---------------------------
async function loadProfile() {
    try {
        const res = await fetch("/auth/me", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!res.ok) {
            throw new Error("프로필 정보를 불러오지 못했습니다.");
        }

        const data = await res.json();
        usernameSpan.textContent = data.username || "-";
        emailSpan.textContent = data.email || "-";
        bioSpan.textContent = data.bio || "-";
    } catch (err) {
        alert(err.message || "프로필 로드 중 오류가 발생했습니다.");
    }
}

// ---------------------------
// 버튼 이벤트
// ---------------------------
backBtn.addEventListener("click", () => {
    window.location.href = "/static/main.html";
});

editProfileBtn.addEventListener("click", () => {
    window.location.href = "/static/profile_edit.html";
});

changePasswordBtn.addEventListener("click", () => {
    window.location.href = "/static/password_change.html";
});

// ---------------------------
// 초기화
// ---------------------------
(async function init() {
    await loadProfile();
})();
