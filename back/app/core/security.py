# back/app/core/security.py 파일 전체 내용

from passlib.context import CryptContext

# CryptContext 설정: 사용할 해시 알고리즘 정의
# 일반적으로 bcrypt를 강력하게 권장합니다.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호를 해시하는 함수
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 해시된 비밀번호와 입력된 비밀번호를 비교하는 함수
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)