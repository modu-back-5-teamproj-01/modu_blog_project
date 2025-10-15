// ## 메인 화면(main.html)에서 사용되는 자바스크립트 코드
document.addEventListener("DOMContentLoaded", () => {
    const postList = document.getElementById("postList");
    const pagination = document.getElementById("pagination");
    const searchInput = document.getElementById("searchInput");
    const sortSelect = document.getElementById("sortSelect");
    const searchBtn = document.getElementById("searchBtn");
    const tagInput = document.getElementById("tagInput");
    const tagSearchBtn = document.getElementById("tagSearchBtn");
    const profileBtn = document.getElementById("profileBtn");
    const logoutBtn = document.getElementById("logoutBtn");
    const createPostBtn = document.getElementById("createPostBtn");

    let currentPage = 0;
    const limit = 10;
    let currentQuery = "";
    let currentSort = "desc";

    // 게시글 불러오기
    async function fetchPosts(page = 0, query = "", sort = "desc") {
        try {
            const params = new URLSearchParams({
                skip: page * limit,
                limit,
                search: query,
                sort
            });
            const response = await fetch(`/blog?${params.toString()}`, {
                method: "GET"
            });
            if (!response.ok) throw new Error("게시글 불러오기 실패");
            const data = await response.json();
            renderPosts(data);  // total 없으므로 data 그대로 전달
            renderPagination(data.length);  // data 길이 기준으로 이전/다음 버튼
        } catch (err) {
            alert(err.message);
        }
    }

    // 게시글 렌더링
    function renderPosts(posts) {
        postList.innerHTML = "";
        posts.forEach(post => {
            const li = document.createElement("li");
            li.textContent = `${post.title} - ${post.author.username}`;
            li.addEventListener("click", () => {
                window.location.href = `/static/post.html?post_id=${post.id}`;
            });
            postList.appendChild(li);
        });
    }

    // 이전/다음 버튼 렌더링
    function renderPagination(postsLength) {
        pagination.innerHTML = "";
        if (currentPage > 0) {
            const prevBtn = document.createElement("button");
            prevBtn.textContent = "이전";
            prevBtn.addEventListener("click", () => {
                currentPage--;
                fetchPosts(currentPage, currentQuery, currentSort);
            });
            pagination.appendChild(prevBtn);
        }
        if (postsLength === limit) {
            const nextBtn = document.createElement("button");
            nextBtn.textContent = "다음";
            nextBtn.addEventListener("click", () => {
                currentPage++;
                fetchPosts(currentPage, currentQuery, currentSort);
            });
            pagination.appendChild(nextBtn);
        }
    }

    // 검색 버튼 클릭
    searchBtn.addEventListener("click", () => {
        currentQuery = searchInput.value;
        currentSort = sortSelect.value;
        currentPage = 0;
        fetchPosts(currentPage, currentQuery, currentSort);
    });

    // 태그 검색 버튼 클릭
    tagSearchBtn.addEventListener("click", () => {
        const tagName = tagInput.value.trim();
        if (!tagName) return;
        window.location.href = `/static/tag_search.html?tag_name=${encodeURIComponent(tagName)}`;
    });

    // 프로필 버튼
    profileBtn.addEventListener("click", () => {
        window.location.href = "/static/profile.html";
    });

    // 로그아웃 버튼
    logoutBtn.addEventListener("click", async () => {
        const token = localStorage.getItem("token");
        if (!token) return;
        try {
            const response = await fetch("/auth/logout", {
                method: "POST",
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (!response.ok) throw new Error("로그아웃 실패");
            localStorage.removeItem("token");
            alert("로그아웃 완료");
            window.location.href = "/static/index.html";
        } catch (err) {
            alert(err.message);
        }
    });

    // 게시글 작성 버튼
    createPostBtn.addEventListener("click", () => {
        window.location.href = "/static/post_create.html";
    });

    // 페이지 로드 시 초기 게시글 불러오기
    fetchPosts(currentPage, currentQuery, currentSort);

});
