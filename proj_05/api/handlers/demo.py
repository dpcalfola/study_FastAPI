from fastapi import APIRouter, Query
from pydantic import BaseModel

from api.responses.detail import DetailResponse, DetailStateCounter

router = APIRouter(prefix="/api/v1/demo")


@router.get("/", response_model=DetailResponse)
def hello_fast_api():
    """
        This is the hello FastAPI endpoint
    :return:
        json type
        {"message: Hello FastAPI"}
    """

    return DetailResponse(
        message=f"Hello FastAPI",
    )


#
global_state: int = 0


@router.get("/state-counter", response_model=DetailStateCounter)
def state_counter():
    """
        Variable counter test
            global variable: counted
            functional local variable: not counted

        Global variable counted even if request other place

    :return:message, state, global_state
    """

    global global_state
    global_state += 1

    state: int = 0
    state += 1

    response = DetailStateCounter(
        message="State counter",
        state=f"{state}",
        global_state=f"{global_state}"
    )

    return response


class NameIn(BaseModel):
    name: str
    prefix: str = "Mr."


@router.post("/hello/name-in-body", response_model=DetailResponse)
def send_dat_body(name_in: NameIn):
    """
        Response with hello name, where name is user provided
    """
    return DetailResponse(message=f"hello {name_in.prefix} {name_in.name}")


@router.post("/hello/{name}", response_model=DetailResponse)
def send_data_path(name: str):
    return DetailResponse(
        message=f"hello {name}"
    )


@router.get("/hello-query", response_model=DetailResponse)
def send_data_query(name: str = Query(..., title="Name", description="The name")):
    return DetailResponse(
        message=f"Hello {name} - query"
    )
