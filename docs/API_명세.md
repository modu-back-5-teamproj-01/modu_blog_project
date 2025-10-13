📝 블로그 API 명세서 (Blog API Specification)
본 명세서는 프로젝트 노션의 단계별 요구사항(JWT 인증, 게시글 CRUD, 댓글, 추가 회원 API)을 모두 반영하여 작성되었습니다.

I. 게시글 (Blog Post) API 명세 (Prefix: /blog)
ID

기능

Endpoint

Method

인증

Request Body / Query Params

응답 (성공)

에러 (실패)

요구사항

2

게시글 작성

/blog

POST

필수 (JWT)

{"title": "str", "content": "str", "category": "str"}

생성된 게시글 정보 (JSON, 201 Created)

401 Unauthorized, 422 Unprocessable Entity

title, content 필수. 작성자 정보는 토큰에서 추출.

3-1

게시글 목록 조회

/blog

GET

필요 없음

Query: skip, limit, sort=desc

게시글 목록 및 페이지네이션 정보 (JSON)

-

{"total": int, "items": [...]} 구조 권장.

3-2

게시글 검색

/blog

GET

필요 없음

Query: search=검색어

검색 결과 목록 (JSON)

404 Not Found (결과 없음)

GET /blog?search={query} 사용.

3-3

게시글 태그 조회

/blog

GET

필요 없음

Query: tag=태그명

태그 결과 목록 (JSON)

404 Not Found (결과 없음)

GET /blog?tag={tag} 사용.

4

게시글 상세 보기

/blog/{post_id}

GET

필요 없음

-

특정 게시글 상세 정보 (JSON)

404 Not Found (ID 없음)

작성자 정보 및 댓글 목록 포함.

5

게시글 수정

/blog/{post_id}

PUT

필수 (JWT)

{"title": "수정된 제목", "content": "수정된 내용"}

수정된 게시글 정보 (JSON)

401 Unauthorized, 403 Forbidden (작성자 불일치), 404 Not Found

작성자 본인 확인 필수.

6

게시글 삭제

/blog/{post_id}

DELETE

필수 (JWT)

-

(응답 본문 없음, 204 No Content)

401 Unauthorized, 403 Forbidden (작성자 불일치), 404 Not Found

작성자 본인 확인 필수.

II. 사용자 인증 및 프로필 (Auth/Profile) API 명세 (Prefix: /auth)
ID

기능

Endpoint

Method

인증

Request Body

응답 (성공)

에러 (실패)

요구사항

1-1

회원가입

/auth/register

POST

필요 없음

{"username": "아이디", "password": "비밀번호"}

생성된 사용자 정보 (JSON, 201 Created)

409 Conflict (중복), 422 Unprocessable Entity

비밀번호 해싱 처리 권장.

1-2

로그인

/auth/login

POST

필요 없음

{"username": "아이디", "password": "비밀번호"}

{"access_token": "JWT...", "token_type": "bearer"}

401 Unauthorized (인증 실패)

JWT 토큰 발급.

3-1

내 정보 조회

/auth/me

GET

필수 (JWT)

-

사용자 상세 정보 (JSON, 200 OK)

401 Unauthorized

닉네임 필드 포함 가능.

3-2

비밀번호 변경

/auth/password

PUT

필수 (JWT)

{"old_password": "str", "new_password": "str"}

성공 메시지 (JSON, 200 OK)

401 Unauthorized, 403 Forbidden

현재 비밀번호 확인 필수.

3-3

프로필 수정

/auth/profile

PUT

필수 (JWT)

{"nickname": "str", "email": "str"} (예시)

수정된 사용자 정보 (JSON, 200 OK)

401 Unauthorized, 409 Conflict

프로필 필드(닉네임, 이메일 등) 수정.

III. 댓글 (Comment) API 명세 (Prefix: /blog/{post_id}/comments 또는 /comments)
ID

기능

Endpoint

Method

인증

Request Body / Query Params

응답 (성공)

에러 (실패)

요구사항

4-1

댓글 작성

/blog/{post_id}/comments

POST

필수 (JWT)

{"content": "댓글 내용"}

생성된 댓글 정보 (JSON, 201 Created)

401 Unauthorized, 404 Not Found (게시글 ID 없음)

-

4-2

댓글 목록 조회

/blog/{post_id}/comments

GET

필요 없음

Query: skip, limit

해당 게시글의 댓글 목록 (JSON)

404 Not Found

계층형 댓글 구조 구현.

4-3

대댓글 작성

/comments/{comment_id}/replies

POST

필수 (JWT)

{"content": "대댓글 내용"}

생성된 대댓글 정보 (JSON, 201 Created)

401 Unauthorized, 404 Not Found

부모 댓글 ID 기반으로 대댓글 생성.

4-4

댓글 수정

/comments/{comment_id}

PUT

필수 (JWT)

{"content": "수정된 내용"}

수정된 댓글 정보 (JSON)

401 Unauthorized, 403 Forbidden, 404 Not Found

댓글 작성자 본인만 수정 가능.

4-5

댓글 삭제

/comments/{comment_id}

DELETE

필수 (JWT)

-

(응답 본문 없음, 204 No Content)

401 Unauthorized, 403 Forbidden, 404 Not Found

댓글 작성자 본인만 삭제 가능.