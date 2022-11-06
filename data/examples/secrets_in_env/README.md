# Test Secrets in environment variables analysis

- `secrets-holder.yaml`contains a Pod specification that holds secrets in its environment

## Set up
```
$ kubectl apply -f data/examples/secrets_in_env/secrets-holder.yaml
```

## Tool output
```
Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod secrets-holder, container ubuntu
	variable: DB_PASSWORD=pass****
	reason: Secret Keyword

Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod secrets-holder, container ubuntu
	variable: base64_secr=KTgr**********************************************************************************
	reason: Base64 High Entropy String

Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod secrets-holder, container ubuntu
	variable: hex_secret=4e1c****************************************************************************************************************************
	reason: Hex High Entropy String

Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod secrets-holder, container ubuntu
	variable: hex_secret=4e1c****************************************************************************************************************************
	reason: Secret Keyword

Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod secrets-holder, container ubuntu
	variable: basic_auth=http******************************************************
	reason: Basic Auth Credentials

Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod secrets-holder, container ubuntu
	variable: aws_access_key=AKIA****************
	reason: AWS Access Key


```

## Clean up

```
$ kubectl delete -f data/examples/secrets_in_env/secrets-holder.yaml
```