from fastapi import APIRouter

from api.responses.detail import DetailResponse

router = APIRouter(prefix="/api/v1/demo")


@router.get("/", response_model=DetailResponse)
def hello_fast_api():
    """
        This is the hello FastAPI endpoint
    :return:
        json type
        {"message: Hello FastAPI"}
    """
    return DetailResponse(message="Hello FastAPI")
