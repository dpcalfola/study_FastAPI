### Frequently used commands list

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

#### alembic DB migration
* Initialize alembic migration
  * This command makes migrations directory

```shell
alembic init migrations
```