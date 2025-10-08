# test_post.py

import requests
import json

# 1. 💡 여기에 POST /api/auth/login 에서 받은 유효한 토큰을 붙여넣으세요.
VALID_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJka2RsZGI5MzA1QG5hdmVyLmNvbSIsImV4cCI6MTc1OTk0MDYzNX0.70IJUh3lH3aSg2k8r093NnzF0wcPl2AgwktWKw-Um78"

# 2. 요청 URL
URL = "http://127.0.0.1:8000/api/posts"

# 3. 요청 헤더 (Authorization 헤더 수동 주입)
HEADERS = {
    "Authorization": f"Bearer {VALID_JWT_TOKEN}",
    "Content-Type": "application/json"
}

# 4. 요청 바디 (게시물 데이터)
PAYLOAD = {
    "title": "requests 라이브러리 최종 테스트",
    "content": "Swagger UI 버그 우회를 위한 마지막 테스트입니다.",
    "category": "Final Test"
}

try:
    # POST 요청 보내기
    response = requests.post(URL, headers=HEADERS, data=json.dumps(PAYLOAD))

    print(f"Status Code: {response.status_code}")
    print("--- 응답 본문 ---")
    # 5. Status 201이 나오면 성공
    if response.status_code == 201 or response.status_code == 200:
        print("✅ 게시물 작성 성공! 백엔드 기능 100% 완료.")
    else:
        print("❌ 실패. 서버의 검증 로직을 확인하세요.")
        print(response.json())

except Exception as e:
    print(f"요청 중 에러 발생: {e}")