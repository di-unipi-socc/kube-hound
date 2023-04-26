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
        File type: dockerfile
        File: /data/examples/secrets_in_docker_source/dockerfile1:4-5
        Error(s):
        -- 4 |RUN python -m pip install --extra-index-url https://username:pa******@my.pypi.com/pypi privatestuff


Hardcoded docker and source secrets analysis - detected smells {HS}
        Description: Base64 High Entropy String
        File type: sourcecode
        File: /data/examples/secrets_in_docker_source/temp.py:1-2
        Error(s):
        -- 1 |password = "secr*************"
```
