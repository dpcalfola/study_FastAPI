### pip upgrade

* pip upgrade
    ```shell
    pip install --upgrade pip
    ``` 

### install requirements

* install requirements - only for app

    ```shell
    pip install -r requirements.txt
    ```

* install requirements - app, tests, dev
    ```shell
    pip install -r requirements.txt -r requirements.dev.txt -r requirements.test.txt
    ```




### Linting
  ```shell
    black .
  ```


### pytest
```shell
  pytest .
```