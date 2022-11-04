# Test Secrets in environment variables analysis

For this test we deploy the Pod specified in secrets-holder.yaml, which is a Pod containing secrets
in the environment variables.
When we run the tool we will see the secrets detected

## Set up
```
$ kubectl apply -f data/examples/secrets_in_env/secrets-holder.yaml
```

## Tool output
```
Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod secrets-holder, container ubuntu
	variable: base64_secr=KTgr4Wyk/e5vfOK1GoEeLlIfkWIfaxzJEVBGEWehL5A/cIAgCjiDX5f7T7fARiIKoVL6Wj137yZADszCnN8Gew
	reason: Base64 High Entropy String

Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod secrets-holder, container ubuntu
	variable: hex_secret=4e1cda9a9c9d9699cb270a3a2021769d4aacd1bec6ab6b7419d538dc6d82511716e3083c35bc6a637f8522bec85f7bb944e1dc537d7acc55b67803788ce4dd05
	reason: Hex High Entropy String

Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod secrets-holder, container ubuntu
	variable: hex_secret=4e1cda9a9c9d9699cb270a3a2021769d4aacd1bec6ab6b7419d538dc6d82511716e3083c35bc6a637f8522bec85f7bb944e1dc537d7acc55b67803788ce4dd05
	reason: Secret Keyword

Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod secrets-holder, container ubuntu
	variable: basic_auth=http://username:whywouldyouusehttpforpasswords@example.com
	reason: Basic Auth Credentials

Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod secrets-holder, container ubuntu
	variable: aws_access_key=AKIAIOSFODNN7EXAMPLE
	reason: AWS Access Key

```

## Clean up

```
$ kubectl delete -f data/examples/secrets_in_env/secrets-holder.yaml
```