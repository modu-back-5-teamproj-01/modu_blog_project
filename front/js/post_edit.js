// 로그인 토큰 확인
const token = localStorage.getItem("token");
if (!token) {
    alert("로그인 후 사용 가능합니다.");
    window.location.href = "/static/index.html";
}

// URL에서 post_id 가져오기
const urlParams = new URLSearchParams(window.location.search);
const postId = urlParams.get("post_id");
if (!postId) {
    alert("잘못된 요청입니다.");
    window.location.href = "/static/main.html";
}

// DOM
const titleInput = document.getElementById("titleInput");
const contentInput = document.getElementById("contentInput");
const summaryInput = document.getElementById("summaryInput");
const tagInput = document.getElementById("tagInput");
const addTagBtn = document.getElementById("addTagBtn");
const tagContainer = document.getElementById("tagContainer");
const saveBtn = document.getElementById("saveBtn");
const cancelBtn = document.getElementById("cancelBtn");

let tags = []; // 기존 태그 + 새로 추가한 태그

// ----------------------------
// 기존 게시글 불러오기
// ----------------------------
async function loadPost() {
    try {
        const res = await fetch(`/blog/${encodeURIComponent(postId)}`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("게시글을 불러오지 못했습니다.");

        const post = await res.json();

        titleInput.value = post.title || "";
        contentInput.value = post.content || "";
        summaryInput.value = post.summary || "";

        // 기존 태그 표시
        if (Array.isArray(post.tags)) {
            tags = post.tags.map(t => t.name); // 기존 태그 초기화
            renderTags();
        }

    } catch (err) {
        alert(err.message || "게시글 로드 중 오류 발생");
        window.location.href = "/static/main.html";
    }
}

// ----------------------------
// 태그 렌더링
// ----------------------------
function renderTags() {
    tagContainer.innerHTML = "";
    tags.forEach(tagName => {
        const span = document.createElement("span");
        span.className = "tag-badge";
        span.textContent = tagName;

        const removeBtn = document.createElement("span");
        removeBtn.className = "remove-tag";
        removeBtn.textContent = "X";
        removeBtn.addEventListener("click", () => {
            tags = tags.filter(t => t !== tagName);
            renderTags();
        });

        span.appendChild(removeBtn);
        tagContainer.appendChild(span);
    });
}

// ----------------------------
// 태그 추가
// ----------------------------
addTagBtn.addEventListener("click", () => {
    const tagName = tagInput.value.trim();
    if (!tagName) return;
    if (tags.includes(tagName)) { alert("이미 추가된 태그입니다."); return; }

    tags.push(tagName);
    renderTags();
    tagInput.value = "";
});

// ----------------------------
// 게시글 수정 완료
// ----------------------------
saveBtn.addEventListener("click", async () => {
    const title = titleInput.value.trim();
    const content = contentInput.value.trim();
    const summary = summaryInput.value.trim();

    if (!title && !content && !summary && tags.length === 0) {
        alert("적어도 하나의 필드를 수정해야 합니다.");
        return;
    }

    const body = {};
    if (title) body.title = title;
    if (content) body.content = content;
    if (summary) body.summary = summary || null;
    if (tags.length > 0) body.tags = tags;

    try {
        const res = await fetch(`/blog/${encodeURIComponent(postId)}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(body)
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "게시글 수정 실패");

        alert("게시글 수정 완료");
        window.location.href = `/static/post.html?post_id=${data.id}`;
    } catch (err) {
        alert(err.message);
    }
});

// ----------------------------
// 수정 취소
// ----------------------------
cancelBtn.addEventListener("click", () => {
    window.location.href = `/static/post.html?post_id=${postId}`;
});

// 초기화
loadPost();
