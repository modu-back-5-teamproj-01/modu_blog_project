// ## 블로그 게시글 화면(post.html)에서 사용되는 자바스크립트 코드

// js/post.js
// 사용 전: post.html에 다음 ID 요소들이 있어야 합니다:
// backBtn, postTitle, postContent, postSummary, postTags, commentList, newComment, addCommentBtn

// ---------------------------
// helper: 안전한 JSON 파싱
// ---------------------------
async function safeJson(response) {
    try { return await response.json(); } catch (e) { return null; }
}

// ---------------------------
// helper: JWT 파싱 (payload.sub 사용 -> user id)
// ---------------------------
function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
            atob(base64)
                .split('')
                .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                .join('')
        );
        return JSON.parse(jsonPayload);
    } catch (e) {
        return null;
    }
}

// ---------------------------
// 설정 및 DOM
// ---------------------------
const token = localStorage.getItem("token"); // 로그인 시 저장한 키: "token"
const payload = token ? parseJwt(token) : null;
const currentUserId = payload?.sub ? String(payload.sub) : null;

const urlParams = new URLSearchParams(window.location.search);
const postId = urlParams.get("post_id");

const backBtn = document.getElementById("backBtn");
const postTitle = document.getElementById("postTitle");
const postContent = document.getElementById("postContent");
const postSummary = document.getElementById("postSummary");
const postTags = document.getElementById("postTags");
const commentList = document.getElementById("commentList");
const newComment = document.getElementById("newComment");
const addCommentBtn = document.getElementById("addCommentBtn");

// 안전: post_id 없으면 메인으로
if (!postId) {
    alert("잘못된 요청입니다.");
    window.location.href = "/static/main.html";
}

// ---------------------------
// 뒤로가기
// ---------------------------
backBtn?.addEventListener("click", () => window.location.href = "/static/main.html");

// ---------------------------
// 게시글 불러오기: GET /blog/{post_id}
// ---------------------------
async function loadPost() {
    try {
        const res = await fetch(`/blog/${encodeURIComponent(postId)}`, { method: "GET" });
        if (!res.ok) {
            const err = await safeJson(res);
            throw new Error(err?.detail || "게시글을 불러오지 못했습니다.");
        }
        const post = await res.json();

        postTitle.textContent = post.title ?? "";
        postContent.textContent = post.content ?? "";
        postSummary.textContent = post.summary ?? "";

        // tags 렌더링 (간단한 텍스트 형태)
        postTags.innerHTML = "";
        if (Array.isArray(post.tags)) {
            post.tags.forEach(t => {
                const span = document.createElement("span");
                span.className = "tag-badge";
                span.textContent = t.name;
                postTags.appendChild(span);
            });
        }

        // 작성자 본인일 경우 수정/삭제 버튼 표시
        const authorId = post.author?.id ? String(post.author.id) : null;
        if (currentUserId && authorId && currentUserId === authorId) {
            renderPostActionButtons();
        }
    } catch (err) {
        alert(err.message || "게시글 로드 중 오류가 발생했습니다.");
    }
}

// 게시글 수정/삭제 버튼 생성
function renderPostActionButtons() {
    if (document.getElementById("editPostBtn")) return; // 중복 방지

    const editBtn = document.createElement("button");
    editBtn.id = "editPostBtn";
    editBtn.textContent = "게시글 수정";
    editBtn.addEventListener("click", () => {
        window.location.href = `/static/post_edit.html?post_id=${encodeURIComponent(postId)}`;
    });

    const deleteBtn = document.createElement("button");
    deleteBtn.id = "deletePostBtn";
    deleteBtn.textContent = "게시글 삭제";
    deleteBtn.addEventListener("click", async () => {
        if (!confirm("게시글을 삭제하시겠습니까?")) return;
        try {
            const res = await fetch(`/blog/${encodeURIComponent(postId)}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (!res.ok) {
                const err = await safeJson(res);
                throw new Error(err?.detail || "게시글 삭제에 실패했습니다.");
            }
            alert("게시글 삭제 완료");
            window.location.href = "/static/main.html";
        } catch (err) {
            alert(err.message || "게시글 삭제 중 오류가 발생했습니다.");
        }
    });

    // postTags 뒤에 버튼들 추가
    postTags.parentNode.insertBefore(editBtn, postTags.nextSibling);
    postTags.parentNode.insertBefore(deleteBtn, postTags.nextSibling);
}

// ---------------------------
// 댓글 목록 불러오기: GET /blog/{post_id}/comments (토큰 불필요)
// ---------------------------
async function loadComments() {
    commentList.innerHTML = "";
    try {
        const res = await fetch(`/blog/${encodeURIComponent(postId)}/comments`, { method: "GET" });
        if (!res.ok) {
            const err = await safeJson(res);
            throw new Error(err?.detail || "댓글 불러오기 실패");
        }
        const comments = await res.json(); // 배열, 각 요소에 replies 배열 포함

        if (!Array.isArray(comments) || comments.length === 0) {
            commentList.innerHTML = "<li>댓글이 없습니다.</li>";
            return;
        }

        comments.forEach(c => {
            const el = createCommentElement(c);
            commentList.appendChild(el);
        });
    } catch (err) {
        alert(err.message || "댓글 로드 중 오류가 발생했습니다.");
    }
}

// ---------------------------
// 댓글 DOM 생성 (재귀 처리로 replies 렌더링)
// ---------------------------
function createCommentElement(comment) {
    const li = document.createElement("li");
    li.dataset.commentId = comment.id;

    // header: 작성자, 시간(optional)
    const header = document.createElement("div");
    header.className = "comment-header";
    const author = document.createElement("strong");
    author.textContent = comment.author?.username ?? "익명";
    const meta = document.createElement("span");
    meta.className = "comment-meta";
    const created = comment.created_at ? ` • ${new Date(comment.created_at).toLocaleString()}` : "";
    meta.textContent = created;
    header.appendChild(author);
    header.appendChild(meta);

    // content
    const content = document.createElement("div");
    content.className = "comment-content";
    content.textContent = comment.content;

    li.appendChild(header);
    li.appendChild(content);

    // actions
    const actions = document.createElement("div");
    actions.className = "comment-actions";

    // 수정/삭제: 작성자 본인만
    const authorId = comment.author?.id ? String(comment.author.id) : null;
    if (currentUserId && authorId && currentUserId === authorId) {
        const editBtn = document.createElement("button");
        editBtn.textContent = "수정";
        editBtn.className = "comment-edit-btn";
        editBtn.addEventListener("click", () => showEditArea(li, comment));
        actions.appendChild(editBtn);

        const delBtn = document.createElement("button");
        delBtn.textContent = "삭제";
        delBtn.className = "comment-delete-btn";
        delBtn.addEventListener("click", () => deleteComment(comment.id));
        actions.appendChild(delBtn);
    }

    // 대댓글 버튼 (로그인 사용자만)
    if (currentUserId) {
        const replyBtn = document.createElement("button");
        replyBtn.textContent = "대댓글";
        replyBtn.className = "comment-reply-btn";
        replyBtn.addEventListener("click", () => toggleReplyArea(li, comment.id));
        actions.appendChild(replyBtn);
    }

    li.appendChild(actions);

    // 대댓글 입력 영역 (초기 숨김)
    const replyArea = document.createElement("div");
    replyArea.className = "reply-area";
    replyArea.style.display = "none";

    const replyInput = document.createElement("input");
    replyInput.type = "text";
    replyInput.className = "reply-input";
    replyInput.placeholder = "대댓글을 입력하세요";

    const replySubmit = document.createElement("button");
    replySubmit.textContent = "대댓글 작성 완료";
    replySubmit.addEventListener("click", () => submitReply(comment.id, replyInput.value, replyArea, replyInput));

    const replyCancel = document.createElement("button");
    replyCancel.textContent = "취소";
    replyCancel.addEventListener("click", () => {
        replyInput.value = "";
        replyArea.style.display = "none";
    });

    replyArea.appendChild(replyInput);
    replyArea.appendChild(replySubmit);
    replyArea.appendChild(replyCancel);
    li.appendChild(replyArea);

    // replies (재귀)
    if (Array.isArray(comment.replies) && comment.replies.length > 0) {
        const ul = document.createElement("ul");
        ul.className = "replies";
        comment.replies.forEach(r => {
            ul.appendChild(createCommentElement(r));
        });
        li.appendChild(ul);
    }

    return li;
}

// ---------------------------
// 댓글 작성: POST /blog/{post_id}/comments (로그인 필요)
// ---------------------------
addCommentBtn?.addEventListener("click", async () => {
    if (!token) {
        alert("댓글 작성은 로그인 후 가능합니다.");
        window.location.href = "/static/index.html";
        return;
    }
    const content = (newComment.value || "").trim();
    if (!content) { alert("댓글을 입력하세요."); return; }

    try {
        const res = await fetch(`/blog/${encodeURIComponent(postId)}/comments`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ content })
        });
        if (!res.ok) {
            const err = await safeJson(res);
            throw new Error(err?.detail || "댓글 작성 실패");
        }
        alert("댓글 작성 완료");
        newComment.value = "";
        await loadComments();
    } catch (err) {
        alert(err.message || "댓글 작성 중 오류가 발생했습니다.");
    }
});

// ---------------------------
// 댓글 수정 표시/전송: PUT /blog/{post_id}/comments/{comment_id} (로그인 필요, 작성자만)
// ---------------------------
function showEditArea(containerLi, comment) {
    // comment 객체를 받아 인라인 편집 영역으로 교체
    containerLi.innerHTML = ""; // 기존 내용을 지우고
    const editDiv = document.createElement("div");
    editDiv.className = "edit-area";

    const input = document.createElement("input");
    input.type = "text";
    input.value = comment.content;

    const saveBtn = document.createElement("button");
    saveBtn.textContent = "댓글 수정 완료";
    saveBtn.addEventListener("click", async () => {
        const newContent = (input.value || "").trim();
        if (!newContent) { alert("댓글 내용을 입력하세요."); return; }

        try {
            const res = await fetch(`/blog/${encodeURIComponent(postId)}/comments/${encodeURIComponent(comment.id)}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ content: newContent })
            });
            if (!res.ok) {
                const err = await safeJson(res);
                throw new Error(err?.detail || "댓글 수정 실패");
            }
            alert("댓글 수정 완료");
            await loadComments();
        } catch (err) {
            alert(err.message || "댓글 수정 중 오류가 발생했습니다.");
        }
    });

    const cancelBtn = document.createElement("button");
    cancelBtn.textContent = "취소";
    cancelBtn.addEventListener("click", () => loadComments());

    editDiv.appendChild(input);
    editDiv.appendChild(saveBtn);
    editDiv.appendChild(cancelBtn);
    containerLi.appendChild(editDiv);
}

// ---------------------------
// 댓글 삭제: DELETE /blog/{post_id}/comments/{comment_id} (로그인 필요, 작성자만)
// ---------------------------
async function deleteComment(commentId) {
    if (!token) { alert("로그인이 필요합니다."); window.location.href = "/static/index.html"; return; }
    if (!confirm("댓글을 삭제하시겠습니까?")) return;

    try {
        const res = await fetch(`/blog/${encodeURIComponent(postId)}/comments/${encodeURIComponent(commentId)}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (!res.ok) {
            const err = await safeJson(res);
            throw new Error(err?.detail || "댓글 삭제 실패");
        }
        alert("댓글 삭제 완료");
        await loadComments();
    } catch (err) {
        alert(err.message || "댓글 삭제 중 오류가 발생했습니다.");
    }
}

// ---------------------------
// 대댓글 작성: POST /blog/{post_id}/comments/{comment_id}/replies (로그인 필요)
// ---------------------------
async function submitReply(parentCommentId, content, replyArea = null, replyInputEl = null) {
    if (!token) { alert("로그인이 필요합니다."); window.location.href = "/static/index.html"; return; }
    const trimmed = (content || "").trim();
    if (!trimmed) { alert("대댓글 내용을 입력하세요."); return; }

    try {
        const res = await fetch(`/blog/${encodeURIComponent(postId)}/comments/${encodeURIComponent(parentCommentId)}/replies`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ content: trimmed })
        });
        if (!res.ok) {
            const err = await safeJson(res);
            throw new Error(err?.detail || "대댓글 작성 실패");
        }
        alert("대댓글 작성 완료");
        if (replyInputEl) replyInputEl.value = "";
        if (replyArea) replyArea.style.display = "none";
        await loadComments();
    } catch (err) {
        alert(err.message || "대댓글 작성 중 오류가 발생했습니다.");
    }
}

// reply area 토글
function toggleReplyArea(containerLi, parentCommentId) {
    const replyArea = containerLi.querySelector(".reply-area");
    if (!replyArea) return;
    replyArea.style.display = (replyArea.style.display === "none" || replyArea.style.display === "") ? "block" : "none";
}

// ---------------------------
// 초기화
// ---------------------------
(async function init() {
    await loadPost();
    await loadComments();
})();
