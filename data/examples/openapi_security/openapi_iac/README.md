# Test OpenAPI Insufficient Access Control detection

- `echo_no_schemes.yaml` contains an OpenAPI specification with missing SecuritySchemes component
- `echo_no_security.yaml` contains an OpenAPI specification where the POST /echo endpoint is missing
  the security field. This service is declared external.
- `echo_security_override.yaml` contains an OpenAPI specification where the POST /echo endpoint is
  overriding the global security policy with an empty policy

## Tool output

```
$ ./data/examples/openapi_security/openapi_iac/run.sh

Analysis results:
Insufficient Access Control in OpenAPI Analysis - detected smells {IAC, CA}
	SecurityScheme not specified in echo_no_schemes.yaml

Insufficient Access Control in OpenAPI Analysis - detected smells {IAC}
	No security field specified in echo_no_security.yaml, post /echo

Insufficient Access Control in OpenAPI Analysis - detected smells {IAC, CA}
	Empty field specified in echo_security_override.yaml, post /echo

```
