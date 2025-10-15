// 로그인 토큰 확인
const token = localStorage.getItem("token");
if (!token) {
  alert("로그인 후 사용 가능합니다.");
  window.location.href = "/static/index.html";
}

// DOM 요소
const titleInput = document.getElementById("titleInput");
const contentInput = document.getElementById("contentInput");
const summaryInput = document.getElementById("summaryInput");
const tagInput = document.getElementById("tagInput");
const addTagBtn = document.getElementById("addTagBtn");
const tagContainer = document.getElementById("tagContainer");
const submitBtn = document.getElementById("submitBtn");
const cancelBtn = document.getElementById("cancelBtn");

let tags = [];

// 태그 추가
addTagBtn.addEventListener("click", () => {
  const tagName = tagInput.value.trim();
  if (!tagName) return;
  if (tags.includes(tagName)) {
    alert("이미 추가된 태그입니다.");
    return;
  }

  tags.push(tagName);

  const span = document.createElement("span");
  span.className = "tag-badge";
  span.textContent = tagName;

  const removeBtn = document.createElement("span");
  removeBtn.className = "remove-tag";
  removeBtn.textContent = "X";
  removeBtn.addEventListener("click", () => {
    tags = tags.filter((t) => t !== tagName);
    tagContainer.removeChild(span);
  });

  span.appendChild(removeBtn);
  tagContainer.appendChild(span);
  tagInput.value = "";
});

// 게시글 작성
submitBtn.addEventListener("click", async () => {
  const title = titleInput.value.trim();
  const content = contentInput.value.trim();
  const summary = summaryInput.value.trim();

  if (!title || !content) {
    alert("제목과 내용을 입력하세요.");
    return;
  }

  try {
    const res = await fetch("/blog", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        title,
        content,
        summary: summary || null,
        tags
      })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "게시글 작성 실패");
    }

    alert("게시글 작성 완료");
    window.location.href = `/static/post.html?post_id=${data.id}`;
  } catch (err) {
    alert(err.message);
  }
});

// 작성 취소
cancelBtn.addEventListener("click", () => {
  window.location.href = "/static/main.html";
});
