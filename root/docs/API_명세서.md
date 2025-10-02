<img width="683" height="555" alt="Image" src="https://github.com/user-attachments/assets/e3a1bf6b-d17a-4d09-871c-5678f98dc340" />

위에 사진은 표로 정리해드린건데 AI도움을 받았습니다.




HTTP 메서드	URL	설명
POST	/api/auth/signup	새로운 사용자를 생성하고 회원가입을 처리합니다.

POST	/api/auth/login	사용자의 이메일과 비밀번호로 로그인하고, JWT 토큰을 발급합니다.

GET	/api/posts	최신 게시글 목록을 조회합니다. 페이지네이션과 검색 기능을 포함합니다.

POST	/api/posts	새로운 게시글을 작성하고 저장합니다. 로그인 인증이 필요합니다.

GET	/api/posts/{post_id}	특정 게시글의 상세 내용을 조회합니다.

PUT	/api/posts/{post_id}	특정 게시글을 수정합니다. 작성자 본인만 가능합니다.

DELETE	/api/posts/{post_id}	특정 게시글을 삭제합니다. 작성자 본인만 가능합니다.

GET	/api/posts/search	제목 또는 내용에 검색어가 포함된 게시글을 조회합니다.

POST	/api/posts/{post_id}/comments	특정 게시글에 댓글을 작성합니다.

DELETE	/api/comments/{comment_id}	특정 댓글을 삭제합니다. 작성자 본인만 가능합니다.