# modu_blog_project
모두의연구소 백엔드 5기 블로그 제작 팀 프로젝트

## 🗂️ WBS(Work Breakdown Structure)
```mermaid
gantt
    title 블로그 프로젝트 개발 일정
    dateFormat  YYYY-MM-DD
    section 1단계: JWT 인증 및 회원가입
    회원가입 API           :a1, 2025-10-02, 1d
    로그인 API            :a2, 2025-10-02, 1d
    JWT 토큰 검증          :a3, 2025-10-02, 1d
    1단계 테스트            :a4, 2025-10-02, 1d

    section 2단계: 메인페이지 & 블로그 CRUD
    게시글 모델 및 DB       :a5, 2025-10-02, 2d
    게시글 작성 API        :a6, 2025-10-03, 2d
    게시글 목록 및 검색 API :a7, 2025-10-03, 2d
    게시글 태그조회 API     :a8, 2025-10-03, 2d
    게시글 상세보기 API     :a9, 2025-10-03, 2d
    게시글 수정 API        :a10, 2025-10-03, 2d
    게시글 삭제 API        :a11, 2025-10-03, 2d
    2단계 테스트           :a12, 2025-10-03, 6d

    section 3단계: 추가 기능 및 배포
    회원 관련 추가 API      :a13, 2025-10-08, 2d
    댓글 API               :a14, 2025-10-08, 3d
    (선택) 파일 업로드       :a15, 2025-10-08, 2d
    (선택) 부가기능          :a16, 2025-10-08, 3d
    (선택) 클라우드 배포     :a17, 2025-10-08, 4d
    (선택) AI 기능 통합      :a18, 2025-10-08, 4d
    3단계 테스트             :a19, 2025-10-08, 5d
    최종 테스트 및 검증       :a20, 2025-10-13, 3d

```

## 📌와이어프레임(Wireframe)

첫번째, 두번째 페이지는 회원가입 & 로그인 페이지입니다

<img width="1919" height="1079" alt="Image" src="https://github.com/user-attachments/assets/ac730e7c-7f14-42f3-92fa-605ab75b9ce2" />
<img width="1919" height="1079" alt="Image" src="https://github.com/user-attachments/assets/5a4e992c-b10a-48bb-950f-1cbb7351a502" />

세번째 페이지는 블로그의 메인 화면입니다.

<img width="1919" height="1079" alt="Image" src="https://github.com/user-attachments/assets/fa17ec5d-4956-48a7-a306-ff983e750ccd" />

네번째 페이지는 사용자가 새 글 작성을 할수있는 페이지입니다.

<img width="1919" height="1079" alt="Image" src="https://github.com/user-attachments/assets/4898ad49-80e6-43c3-83d8-a7791059baab" />

다섯번째 페이지는 다른 사용자의 게시글 상세 정보 및 게시글내에 댓글 작성하는 화면입니다. (게시글 상세 페이지)

<img width="1919" height="1079" alt="Image" src="https://github.com/user-attachments/assets/a5436883-5669-48df-bdbe-f7b161d2fa6e" />

여섯번쨰 페이지는 본인이 작성한 게시글 수정 및 삭제할수있는 화면입니다. (게시글 수정/삭제 페이지)

<img width="1919" height="1079" alt="Image" src="https://github.com/user-attachments/assets/86ac6f22-bda2-485e-8c0c-3cba82435d0e" />

일곱번째 페이지는 게시글 검색 화면입니다. (검색 결과 페이지)

<img width="1919" height="1079" alt="Image" src="https://github.com/user-attachments/assets/21a4d3f6-01cb-4bd0-a897-d43b4f2965d2" />

여덟번째는 본인의 프로필 수정하거나 탈퇴할수 있는 페이지입니다. (사용자 프로필 페이지)

<img width="1919" height="1079" alt="Image" src="https://github.com/user-attachments/assets/a030b69c-33fb-4da3-b924-c91a36a81813" />

아홉번째도 정보 변경하는 페이지입니다. (프로필 수정 페이지)

<img width="1919" height="1079" alt="Image" src="https://github.com/user-attachments/assets/21903d9d-ebbe-4f00-8e92-a7c407d1f0e8" />

## 📌 URL 구조
| 구분                  | Method | Endpoint                                        | 기능 설명                  | JWT 인증 필요  |
| ------------------- | ------ | ----------------------------------------------- | ---------------------- | ------ |
| **Auth (회원 관련)**    | POST   | `/auth/register`                                | 회원가입                   | ❌      |
|                     | POST   | `/auth/login`                                   | 로그인, JWT 발급            | ❌      |
|                     | PUT    | `/auth/password`                                | 비밀번호 변경                | ✅      |
|                     | PUT    | `/auth/profile`                                 | 프로필 수정 (닉네임 등)         | ✅      |
|                     | GET    | `/auth/me`                                      | 내 정보 조회                | ✅      |
| **Blog (게시글)**      | POST   | `/blog`                                         | 게시글 작성                 | ✅      |
|                     | GET    | `/blog`                                         | 게시글 목록 조회 (검색, 정렬 지원)  | ❌      |
|                     | GET    | `/blog/{tag}`                                   | 특정 태그의 게시글 목록 조회       | ❌      |
|                     | GET    | `/blog/{post_id}`                               | 게시글 상세 조회              | ❌      |
|                     | PUT    | `/blog/{post_id}`                               | 게시글 수정 (작성자 본인만 가능)    | ✅      |
|                     | DELETE | `/blog/{post_id}`                               | 게시글 삭제 (작성자 본인만 가능)    | ✅      |
| **Comment (댓글)**    | POST   | `/blog/{post_id}/comments`                      | 댓글 작성                  | ✅      |
|                     | GET    | `/blog/{post_id}/comments`                      | 댓글 목록 조회               | ❌      |
|                     | PUT    | `/blog/{post_id}/comments/{comment_id}`         | 댓글 수정 (작성자 본인만 가능)     | ✅      |
|                     | DELETE | `/blog/{post_id}/comments/{comment_id}`         | 댓글 삭제 (작성자 본인만 가능)     | ✅      |
|                     | POST   | `/blog/{post_id}/comments/{comment_id}/replies` | 대댓글 작성                 | ✅      |
| **Upload (파일 업로드)** | POST   | `/upload/images`                                | 이미지 업로드 (로컬/S3)        | ✅      |
| **Extra (부가기능)**    | GET    | `/blog/{post_id}`                               | 조회수 자동 증가              | ❌      |
|                     | GET    | `/docs`, `/redoc`                               | API 문서(Swagger, ReDoc) | ❌      |
|                     | GET    | `/static/...`                                   | 정적 파일 서빙               | ❌      |
| **AI 기능**      | POST   | `/ai/autocomplete`                              | 글 자동완성                 | ❌      |
|                     | POST   | `/ai/summarize`                                 | 게시글 요약                 | ❌      |
|                     | POST   | `/ai/tags`                                      | 태그 자동 추천               | ❌      |
