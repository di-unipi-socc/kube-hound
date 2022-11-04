# Test OpenAPI security schemes analysis

- `echo_no_schemes.yaml` contains an OpenAPI specification with missing SecuritySchemes component
- `echo_no_security.yaml` contains an OpenAPI specification where the POST /echo endpoint is missing
    the security field
- `echo_security_override.yaml` contains an OpenAPI specification where the POST /echo endpoint is
    overriding the global security policy with an empty policy
- `echo_basic_auth.yaml` contains an OpenAPI specification where the POST /echo endpoint is
    secured through Basic HTTP authorization, but the service is not declared external nor it
    preforms authorization

## Tool output

```
SecurityScheme analysis - detected smells {IAC}
	SecurityScheme not specified in echo_no_schemes.yaml
SecurityScheme analysis - detected smells {IAC}
	No security field specified in echo_no_security.yaml, post /echo
SecurityScheme analysis - detected smells {IAC}
	Empty field specified in echo_security_override.yaml, post /echo
SecurityScheme analysis - detected smells {CA, MUA}
	Detected basic http authorization in echo_basic_auth.yaml, post /echo
```