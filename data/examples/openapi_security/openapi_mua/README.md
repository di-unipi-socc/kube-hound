# Test OpenAPI Multiple User Authentication Analysis

- `gateway_multiple_auth.yaml` contains an OpenAPI specification where the /login and /authenticate
  endpoints are secured through Basic HTTP authorization

## Tool output

```
$ ./data/examples/openapi_security/openapi_iac/run.sh

Analysis results:
Multiple User Authentication in OpenAPI Analysis - detected smells {MUA}
	Multiple user authentication endpoints:
	- Basic http authorization in gateway_multiple_auth.yaml, post /login
	- Basic http authorization in gateway_multiple_auth.yaml, post /authenticate

```
