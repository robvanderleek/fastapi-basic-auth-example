# FastAPI Basic Auth example

## Running

1. Install dependencies:

    ```shell
    poetry install
    ```

2. Run the server:

    ```shell
    poetry run python main.py
    ```

## Testing endpoint and static file

```shell
$ curl http://localhost:8080/
{"detail":"Not authenticated"}
```

```shell
$ curl http://myuser:mypassword@localhost:8080/
<html>
  <body>
    <h1>Hello world</h1>
  </body>
</html>
```

```shell
$ curl http://localhost:8080/api/hello
{"detail":"Not authenticated"}
```

```shell
$ curl http://myuser:mypassword@localhost:8080/api/hello
"world"
```
