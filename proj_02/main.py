from decouple import config

from fastapi import FastAPI, Request

# DB modules
import databases
import sqlalchemy

DATABASE_URL = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@localhost:{config('DB_PORT')}/FastAPI_proj_02"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Table
books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.String),
    sqlalchemy.Column("pages", sqlalchemy.Integer),
    sqlalchemy.Column("publishing_company_id", sqlalchemy.ForeignKey("publishing_company.id"), nullable=False)
)

readers = sqlalchemy.Table(
    "readers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
)

readers_books = sqlalchemy.Table(
    "readers_books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("readers_id", sqlalchemy.ForeignKey("readers.id"), nullable=False),
    sqlalchemy.Column("books_id", sqlalchemy.ForeignKey("books.id"), nullable=False),
)

publishing_company = sqlalchemy.Table(
    "publishing_company",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("company_name", sqlalchemy.String, nullable=False)
)

# FastAPI from here
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/books/")
async def get_all_books():
    query = books.select()
    return await database.fetch_all(query)


@app.post("/books/")
async def create_book(request: Request):
    data = await request.json()
    query = books.insert().values(**data)
    last_record_id = await database.execute(query)
    return {"id": last_record_id}


@app.post("/readers/")
async def create_reader(request: Request):
    data = await request.json()
    query = readers.insert().values(**data)
    last_record_id = await database.execute(query)
    return {"id": last_record_id}


@app.get("/readers/")
async def get_all_readers():
    query = readers.select()
    return await database.fetch_all(query)


@app.post("/read/")
async def read_book(request: Request):
    data = await request.json()
    query = readers_books.insert().values(**data)
    last_record_id = await database.execute(query)
    return {"id": last_record_id}


@app.get("/read/")
async def get_all_read_data():
    query = readers_books.select()
    result = await database.fetch_all(query)
    return result


@app.post("/publisher/")
async def create_publisher(request: Request):
    data = await request.json()
    query = publishing_company.insert().values(**data)
    last_record_id = await database.execute(query)
    return {"id": last_record_id}


@app.get("/publisher/")
async def get_all_publishers():
    query = publishing_company.select()
    return await database.fetch_all(query)