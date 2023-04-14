# Test Hardcoded Unencrypted Kubernetes Secrets
There is a violation of the following principle within the `secret.yaml` file. It is verified through the entropy check (field: password)

## How Test
by running the following command:

```
$ ./data/examples/secrets_kubernetes/run.sh

...
...

Analysis results:
Unencryped kubernetes secrets analysis - detected smells {HS}
        Description: Base64 High Entropy String
        File: /data/examples/secrets_kubernetes/secret.yaml:22-23
        Error(s):
        -- 22 |  password: cGF*********
```
