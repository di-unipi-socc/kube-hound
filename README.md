# K8spurifier

K8spurifier is an automatic security smell detection tool targeting kubernetes deployed microservice applications.

## Running
The command line interface can be run via poetry
```
$ poetry run python -m k8spurifier
```

## Testing

To run unit tests
```sh
$ ./scripts/run_tests.sh
```

Preconfigured yaml config files for Online boutique and Sock shop can be found in the `test_files` folder.
To run the tool on those application do
```
$ ./scripts/run_online_boutique.sh

$ ./scripts/run_sock_shop.sh
```

## Type checking and linting
```
$ ./scripts/typecheck_and_lint.sh
```
