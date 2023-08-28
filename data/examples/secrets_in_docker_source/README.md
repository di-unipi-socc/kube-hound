# Test Hardcoded Unencrypted Secrets in Docker and Source code
for the test two files were created (one for docker and one with the source code) which contain a hard-coded secret.

the supported formats for the source code are as follows:
- .py 
- .js
- .properties
- .pem
- .php
- .xml
- .ts
- .env
- .java
- .rb
-  go
-  cs
- .txt

## How Test
by running the following command:

```
$ ./data/examples/secrets_in_docker_source/run.sh

...
...

Analysis results:
Hardcoded docker and source secrets analysis - detected smells {HS}
        Description: Basic Auth Credentials
        File: /data/examples/secrets_in_docker_source/Dockerfile.command-secret:4-5 
        Error(s): 
        -- 4 |RUN python -m pip install --extra-index-url https://username:pa******@my.pypi.com/pypi privatestuff


Hardcoded docker and source secrets analysis - detected smells {HS}
        Description: Base64 High Entropy String
        File: /source_secret.java:6-7 
        Error(s): 
        -- 6 |        String password = "pa*********";


Hardcoded docker and source secrets analysis - detected smells {HS}
        Description: Base64 High Entropy String
        File: /source_secret.js:1-2 
        Error(s): 
        -- 1 |const SECRET_KEY = "743677**************************";


Hardcoded docker and source secrets analysis - detected smells {HS}
        Description: Base64 High Entropy String
        File: /source_secret.py:3-4 
        Error(s): 
        -- 3 |api_key = "d91f05**************************"
```
