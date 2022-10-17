# Frequently used commands list

<br>
<br>

* pip upgrade
```shell
python -m pip install --upgrade pip
```

* pip package install at once
```shell
pip install -r requirements.txt
```

* run FastAPI server
```shell
python -m uvicorn main:app --reload
```

<br>
<br>

## alembic DB migration

<br>

* Initialize alembic migration
  * ```shell
    alembic init migrations
    ```
  * This command makes migrations directory

<br>

* Create a new version of migrations
  * ```shell
    alembic revision --autogenerate -m "<Revision message>"
    ```

<br>

* Apply to DB with lastest migration version
  * ```shell
    alembic upgrade head
    ```