## Frequently Used Commands

<br>
<br>

* Clear all docker-compose containers then rebuild, restart
    ```shell
    docker-compose down && \
    docker-compose build --no-cache && \
    docker-compose up
    ```
* Execute inside container
    ```shell
    docker-compose run --rm api_app sh -c "python main.py"
    ```