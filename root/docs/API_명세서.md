1. 인증(회원가입 & 로그인) API 명세
회원가입과 로그인은 사용자의 신원을 관리하는 중요한 기능입니다. 보안과 데이터 형식을 명확히 정의하는 것이 중요해요.

POST /api/auth/signup

설명: 새로운 사용자를 생성하고 회원가입을 처리합니다.

요청 (Request Body):

username (string): 사용자가 사용할 이름. (필수)

email (string): 사용자의 이메일 주소. 고유해야 합니다. (필수)

password (string): 사용자의 비밀번호. (필수)

응답 (Response Body - 201 Created):

id (integer): 생성된 사용자의 고유 ID.

username (string): 생성된 사용자 이름.

email (string): 생성된 사용자 이메일.

created_at (string): 계정 생성일.

오류 응답 (400 Bad Request):

detail (string): "Email already registered" 또는 "Username already taken"

POST /api/auth/login

설명: 사용자의 로그인을 처리하고 JWT(JSON Web Token)를 발급합니다.

요청 (Request Body):

email (string): 사용자의 이메일. (필수)

password (string): 사용자의 비밀번호. (필수)

응답 (Response Body - 200 OK):

access_token (string): API 요청에 사용할 JWT.

token_type (string): 토큰 유형. "bearer"로 고정.

오류 응답 (401 Unauthorized):

detail (string): "Incorrect email or password"

2. 게시글(Posts) API 명세
게시글 생성, 조회, 수정, 삭제 기능을 정의합니다. 모든 게시글 관련 엔드포인트는 로그인(인증)을 필요로 합니다.

GET /api/posts

설명: 최신 게시글 목록을 조회합니다.

쿼리 파라미터 (Query Parameters):

skip (integer, optional): 건너뛸 게시글 수. (기본값: 0)

limit (integer, optional): 가져올 게시글 수. (기본값: 100)

응답 (Response Body - 200 OK):

[ ] (array): 게시글 객체의 배열입니다. 각 객체는 id, title, summary, author, created_at 필드를 가집니다.

POST /api/posts

설명: 새로운 게시글을 생성합니다. 인증 필요.

요청 (Request Body):

title (string): 게시글 제목. (필수)

content (string): 게시글 내용. (필수)

응답 (Response Body - 201 Created):

id (integer): 생성된 게시글의 ID.

title (string): 게시글 제목.

content (string): 게시글 내용.

summary (string): AI가 생성한 요약.

tags (array of strings): AI가 추천한 태그.

author_id (integer): 작성자 ID.

오류 응답 (401 Unauthorized): detail: "Not authenticated"

GET /api/posts/{post_id}

설명: 특정 게시글의 상세 내용을 조회합니다.

경로 파라미터 (Path Parameter):

post_id (integer): 조회할 게시글의 고유 ID.

응답 (Response Body - 200 OK):

id (integer): 게시글 ID.

title (string): 게시글 제목.

content (string): 게시글 본문.

summary (string): AI가 생성한 요약.

tags (array of strings): AI가 추천한 태그.

author_id (integer): 작성자 ID.

created_at (string): 생성일.

comments (array): 댓글 목록. 각 객체는 author와 content를 포함합니다.

오류 응답 (404 Not Found): detail: "Post not found"

PUT /api/posts/{post_id}

설명: 특정 게시글을 수정합니다. 인증 필요. 작성자만 가능.

요청 (Request Body):

title (string): 수정할 제목. (선택적)

content (string): 수정할 내용. (선택적)

응답 (Response Body - 200 OK): 수정된 게시글 객체.

오류 응답:

401 Unauthorized: detail: "Not authenticated"

403 Forbidden: detail: "You are not the author"

404 Not Found: detail: "Post not found"

DELETE /api/posts/{post_id}

설명: 특정 게시글을 삭제합니다. 인증 필요. 작성자만 가능.

응답 (Response Body - 204 No Content): 본문 없음.

오류 응답:

401 Unauthorized: detail: "Not authenticated"

403 Forbidden: detail: "You are not the author"

404 Not Found: detail: "Post not found"

3. 검색 API 명세
GET /api/posts/search

설명: 제목 또는 내용에 검색어가 포함된 게시글을 조회합니다.

쿼리 파라미터 (Query Parameters):

q (string): 검색할 키워드. (필수)

응답 (Response Body - 200 OK):

[ ] (array): 검색 결과 게시글 객체 배열. 필드는 /api/posts와 동일.