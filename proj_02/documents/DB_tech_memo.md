## DB synchronization - (1)

  * Code
    ```python
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
    )

    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    ```

  * Create table process
    1. sqlalchemy make table definition to metadata
    2. sqlalchemy create engine with DATABASE_URL
    3. meatdata.create_all(engine)

  * The process that CRUD recorde on table
    1. Make 'database' object with DATABASE_URL
    2. Make query
    3. some_variable = database.SomethingCommand(query)


<br>
<br>

## ORM (one-to-many, many-to-many)

  * one-to-many:
    * Use ForeignKey
      * Table which has fk-column -> many
      * Table of which pk is going to be fk -> one

<br>

  * many-to-many:
    * Make a new table that has ForeignKeys which follows other's pk