import env
import uvicorn

from api.api import create_app


def main():
    app = create_app()
    uvicorn.run(app, host=env.HOST, port=env.PORT)


if __name__ == "__main__":
    main()
