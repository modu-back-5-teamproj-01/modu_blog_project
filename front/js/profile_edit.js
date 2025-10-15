// js/profile_edit.js

// 로그인 토큰 확인
const token = localStorage.getItem("token");
if (!token) {
    alert("로그인 후 사용 가능합니다.");
    window.location.href = "/static/index.html";
}

// DOM 요소
const usernameInput = document.getElementById("usernameInput");
const emailInput = document.getElementById("emailInput");
const bioInput = document.getElementById("bioInput");

const saveBtn = document.getElementById("saveBtn");
const cancelBtn = document.getElementById("cancelBtn");

// ---------------------------
// 기존 사용자 정보 불러오기: GET /auth/me
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
        usernameInput.value = data.username || "";
        emailInput.value = data.email || "";
        bioInput.value = data.bio || "";
    } catch (err) {
        alert(err.message);
    }
}

// ---------------------------
// 프로필 수정: PUT /auth/profile
// ---------------------------
saveBtn.addEventListener("click", async () => {
    const username = usernameInput.value.trim();
    const email = emailInput.value.trim();
    const bio = bioInput.value.trim();

    // 필수 입력 검증
    if (!username || !email) {
        alert("Username과 Email은 반드시 입력해야 합니다.");
        return;
    }

    try {
        const res = await fetch("/auth/profile", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ username, email, bio })
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "프로필 수정 실패");
        }

        alert("프로필 변경 완료");
        window.location.href = "/static/profile.html";
    } catch (err) {
        alert(err.message);
    }
});

// ---------------------------
// 취소 버튼
// ---------------------------
cancelBtn.addEventListener("click", () => {
    window.location.href = "/static/profile.html";
});

// 초기화
loadProfile();
