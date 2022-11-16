# Kube-hound

Kube-hound is an automatic security smell detection tool targeting kubernetes deployed microservice applications.

Currently there are five analyses implemented:
- OpenAPI securityScheme
- Kubesec.io integration
- Secrets in environment variables
- External-IP detection
- Pod-to-Pod traffic inspection

The folder `data/examples` contains various examples of analyses, to get a feel of what this tool does.



## Usage

### Command line interface

```
poetry run python -m kube_hound
```

```
usage: kube-hound [-h] [-c CONTEXT] [-d] [-s] [-l ANALYSIS_LIST] [-v] [-vv] config_file

kube-hound: detect securitysmells in kubernetes based applications

positional arguments:
  config_file           path to the config file

optional arguments:
  -h, --help            show this help message and exit
  -c CONTEXT, --context CONTEXT
                        path to the application context
  -d                    run only dynamic analyses
  -s                    run only static analyses
  -l ANALYSIS_LIST      comma separated list of analysis to run (default all available)
  -v                    verbose output
  -vv                   more verbose output
```

### Other Python scripts

```py
from pathlib import Path
from typing import List, Mapping

from kube_hound.hound import Hound
from kube_hound.analysis import AnalysisResult, StaticAnalysis
from kube_hound.applicationobject import ApplicationObject


class HelloWorldAnalysis(StaticAnalysis):
    analysis_id = 'hello_world'
    analysis_name = 'Hello World Analysis'
    analysis_description = 'This analysis prints Hello, World!'
    input_types = ['kubernetes_config', 'dockerfile']

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]])\
            -> List[AnalysisResult]:
        print('Hello, World!')
        return []


# instantiate the Hound object and load the Kubernetes config from the environment
hound = Hound(Path("test_files/mock-application/application"))
hound.set_config_path(Path("test_files/mock-application/mock-config.yaml"))

# acquire and parse the application
hound.aquire_application()
hound.parse_application()

# register HelloWorldAnalysis to the scheduler
hound.register_analysis(HelloWorldAnalysis)

# only run static analyses
hound.run_dynamic = False

# run the analyses and show the results
hound.run_analyses()
hound.show_results()
```


## Dependencies

Install the python dependencies
```
poetry install
```

Kube-hound needs the Docker engine, kubectl and [ksniff](https://github.com/eldadru/ksniff) installed.

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