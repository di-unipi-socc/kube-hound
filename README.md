# Kube-hound

Kube-hound is an automatic security smell detection tool targeting kubernetes deployed microservice applications.

Currently there are five analyses implemented:
- OpenAPI securityScheme
- Kubesec.io integration
- Secrets in environment variables
- External-IP detection
- Pod-to-Pod traffic inspection

The folder `data/examples` contains various examples of analyses, to get a feel of what this tool does.

## Running

Install the python dependencies
```
poetry install
```


Run the command line interface
```
poetry run python -m kube_hound
```

## Testing



Preconfigured yaml config files for Online boutique and Sock shop can be found in the `test_files` folder.
To run Kube-hound on those application run:

```
$ ./scripts/run_online_boutique.sh
$ ./scripts/run_sock_shop.sh
```

To run unit tests
```sh
./scripts/run_tests.sh
```