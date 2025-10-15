// 로그인 토큰 확인
const token = localStorage.getItem("token");
if (!token) {
    alert("로그인 후 사용 가능합니다.");
    window.location.href = "/static/index.html";
}

// DOM 요소
const currentPasswordInput = document.getElementById("currentPasswordInput");
const newPasswordInput = document.getElementById("newPasswordInput");
const confirmPasswordInput = document.getElementById("confirmPasswordInput");
const submitBtn = document.getElementById("submitBtn");
const cancelBtn = document.getElementById("cancelBtn");

// 비밀번호 변경
submitBtn.addEventListener("click", async () => {
    const oldPassword = currentPasswordInput.value.trim();
    const newPassword = newPasswordInput.value.trim();
    const confirmPassword = confirmPasswordInput.value.trim();

    if (!oldPassword || !newPassword || !confirmPassword) {
        alert("모든 입력칸을 채워주세요.");
        return;
    }

    if (newPassword !== confirmPassword) {
        alert("새 비밀번호와 확인용 비밀번호가 일치하지 않습니다.");
        return;
    }

    try {
        const res = await fetch("/auth/password", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                old_password: oldPassword,
                new_password: newPassword
            })
        });

        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.detail || "비밀번호 변경 실패");
        }

        alert("비밀번호 변경 성공");
        window.location.href = "/static/profile.html";

    } catch (err) {
        alert(err.message);
    }
});

// 취소
cancelBtn.addEventListener("click", () => {
    window.location.href = "/static/profile.html";
});
