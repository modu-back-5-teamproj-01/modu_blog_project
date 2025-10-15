// ✅ 모든 JS는 DOM이 완전히 로드된 뒤에 실행되도록 함
document.addEventListener("DOMContentLoaded", () => {
    // === 로그인 화면(index.html) ===
    const loginBtn = document.getElementById("loginBtn");
    if (loginBtn) {
        loginBtn.addEventListener("click", async () => {
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            if (!username || !password) {
                alert("모든 입력칸을 채워주세요.");
                return;
            }

            try {
                const response = await fetch("/auth/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password })
                });

                if (!response.ok) throw new Error("로그인 실패");

                const data = await response.json();
                localStorage.setItem("token", data.access_token);
                window.location.href = "/static/main.html";
            } catch (err) {
                alert(err.message);
            }
        });
    }

    const gotoSignupBtn = document.getElementById("gotosignupBtn");
    if (gotoSignupBtn) {
        gotoSignupBtn.addEventListener("click", () => {
            window.location.href = "/static/signup.html";
        });
    }

    // === 회원가입 화면(signup.html) ===
    const signupBtn = document.getElementById("signupBtn");
    if (signupBtn) {
        signupBtn.addEventListener("click", async () => {
            const username = document.getElementById("username").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            const confirmPassword = document.getElementById("confirmPassword").value;

            if (!username || !email || !password || !confirmPassword) {
                alert("모든 입력칸을 채워주세요.");
                return;
            }

            if (password !== confirmPassword) {
                alert("비밀번호가 일치하지 않습니다.");
                return;
            }

            try {
                const response = await fetch("/auth/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, email, password })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || "회원가입 실패");
                }

                alert("회원가입 성공!");
                window.location.href = "/static/index.html";
            } catch (err) {
                alert(err.message);
            }
        });
    }

    const backBtn = document.getElementById("backBtn");
    if (backBtn) {
        backBtn.addEventListener("click", () => {
            window.location.href = "/static/index.html";
        });
    }
});
