from fastapi import FastAPI
from todo import todo_router
from fastapi.middleware.cors import CORSMiddleware

# fastapi 객체 생성
app = FastAPI()

# CORS 설정
origins = ["http://recommendfromt.s3-website.ap-northeast-2.amazonaws.com"]  # 프론트엔드의 주소로 변경
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 기본 요청(/ 주소에 get 요청)이 오면 수행
# 요청에 따라 아래의 함수를 수행하고 결과를 리턴함
@app.get("/")
async def welcomefunc() -> dict:
    return {
        "message" : "Welcome message & CI/CD error fix Success!"
    }

# fastapi 객체가 라우터를 포함하도록 만듦
app.include_router(todo_router)
