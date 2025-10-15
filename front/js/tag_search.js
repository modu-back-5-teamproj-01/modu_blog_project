// js/tag_search.js

// URL에서 tag_name 가져오기 (예: tag_search.html?tag_name=Python)
const urlParams = new URLSearchParams(window.location.search);
const tagName = urlParams.get("tag_name");

document.getElementById("tagInput").value = tagName;

// 게시글 리스트 가져오기
async function fetchPostsByTag(tag) {
    try {
        const response = await fetch(`/blog/tag/${encodeURIComponent(tag)}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("게시글을 불러오는 데 실패했습니다.");
        }

        const data = await response.json();

        const postList = document.getElementById("postList");
        postList.innerHTML = ""; // 기존 리스트 초기화

        if (data.length === 0) {
            postList.innerHTML = "<li>해당 태그와 관련된 게시글이 없습니다.</li>";
            return;
        }

        data.forEach(post => {
            const li = document.createElement("li");

            // 게시글 제목 클릭 시 해당 게시글 화면으로 이동
            const titleLink = document.createElement("a");
            titleLink.href = `/static/post.html?post_id=${post.id}`;
            titleLink.textContent = post.title;
            li.appendChild(titleLink);

            // 작성자 표시
            const authorSpan = document.createElement("span");
            authorSpan.textContent = ` (작성자: ${post.author.username})`;
            li.appendChild(authorSpan);

            postList.appendChild(li);
        });
    } catch (err) {
        alert(err.message);
    }
}

// 페이지 로드 시 실행
if (tagName) {
    fetchPostsByTag(tagName);
}

// 메인 화면으로 돌아가기 버튼
document.getElementById("backBtn").addEventListener("click", () => {
    window.location.href = "/static/main.html";
});
