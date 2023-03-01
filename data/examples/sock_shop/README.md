# Sock Shop testing

- `sock_shop_output.txt` contains the full output of the tool analyzing Sock shop

## Analysis highlights

### Unnecessary privileges to microservices

Kube-hound detected various Kubernetes configurations that did not specify resources limits or minimum provileges.

For example the `queue-master` do not have dropped capabilities, does not run as non privileged and does not have read-only root filesystem.

```
KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in 17-queue-master-dep.yaml
	selector: containers[] .securityContext .capabilities .drop
	reason: Reducing kernel capabilities available to a container limits its attack surface

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in 17-queue-master-dep.yaml
	selector: containers[] .securityContext .capabilities .drop | index("ALL")
	reason: Drop all capabilities and add only those required to reduce syscall attack surface

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in 17-queue-master-dep.yaml
	selector: containers[] .securityContext .readOnlyRootFilesystem == true
	reason: An immutable root filesystem can prevent malicious binaries being added to PATH and increase attack cost

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in 17-queue-master-dep.yaml
	selector: containers[] .securityContext .runAsNonRoot == true
	reason: Force the running image to run as a non-root user to ensure least privilege

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in 17-queue-master-dep.yaml
	selector: containers[] .securityContext .runAsUser -gt 10000
	reason: Run as a high-UID user to avoid conflicts with the host's user table
```

Similar results were found for the other services.

### OpenAPI Insufficient Access Control Analysis

Sock Shop internal services' API do not specify any kind of security scheme.

```
Insufficient Access Control in OpenAPI Analysis - detected smells {IAC, CA}
	SecurityScheme not specified in carts.json

Insufficient Access Control in OpenAPI Analysis - detected smells {IAC, CA}
	SecurityScheme not specified in catalogue.json

Insufficient Access Control in OpenAPI Analysis - detected smells {IAC, CA}
	SecurityScheme not specified in orders.json

Insufficient Access Control in OpenAPI Analysis - detected smells {IAC, CA}
	SecurityScheme not specified in payment.json

Insufficient Access Control in OpenAPI Analysis - detected smells {IAC, CA}
	SecurityScheme not specified in user.json
```

### Hardcoded secrets

The `catalogue-db` service has an environment variable called `MYSQL_ROOT_PASSWORD`, that contains the root password of the database.

```
Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod catalogue-db-6d49c7c65-l46bk, container catalogue-db
	variable: MYSQL_ROOT_PASSWORD=fake*********
	reason: Secret Keyword
```

### Traffic analysis

Unencrypted traffic was detected between the services.

```
Traffic analysis - detected smells {NSC}
	Unencrypted traffic detected in pod catalogue-5f495f9cf8-wvk5f
	here is a sample of the packets (HTTP):
	HTTP 10.2.2.204 -> 10.2.2.203 : GET /catalogue HTTP/1.1
	HTTP 10.2.2.203 -> 10.2.2.204 : HTTP/1.1 200 OK
	HTTP 10.2.2.204 -> 10.2.2.203 : GET /catalogue HTTP/1.1
	HTTP 10.2.2.203 -> 10.2.2.204 : HTTP/1.1 200 OK
	HTTP 10.2.2.204 -> 10.2.2.203 : GET /catalogue/03fef6ac-1896-4ce8-bd69-b798f85c6e0b HTTP/1.1
	HTTP 10.2.2.203 -> 10.2.2.204 : HTTP/1.1 200 OK
	HTTP 10.2.2.204 -> 10.2.2.203 : GET /catalogue/d3588630-ad8e-49df-bbd7-3167f7efb246 HTTP/1.1
	HTTP 10.2.2.203 -> 10.2.2.204 : HTTP/1.1 200 OK
	HTTP 10.2.2.204 -> 10.2.2.203 : GET /catalogue HTTP/1.1
	HTTP 10.2.2.203 -> 10.2.2.204 : HTTP/1.1 200 OK
	HTTP 10.2.2.204 -> 10.2.2.203 : GET /catalogue HTTP/1.1

Traffic analysis - detected smells {NSC}
	Unencrypted traffic detected in pod front-end-6585d48b5c-qkmqp
	here is a sample of the packets (HTTP):
	HTTP 10.2.0.1 -> 10.2.2.204 : GET /catalogue HTTP/1.1
	HTTP 10.2.2.204 -> 10.128.117.95 : GET /catalogue HTTP/1.1
	HTTP 10.128.117.95 -> 10.2.2.204 : HTTP/1.1 200 OK
	HTTP 10.2.2.204 -> 10.2.0.1 : 0
	HTTP 10.2.0.1 -> 10.2.2.204 : GET / HTTP/1.1
	HTTP 10.2.2.204 -> 10.2.0.1 : rue,
	HTTP 10.2.0.1 -> 10.2.2.204 : GET /login HTTP/1.1
	HTTP 10.2.2.204 -> 10.128.133.122 : GET /login HTTP/1.1
	HTTP 10.128.133.122 -> 10.2.2.204 : HTTP/1.1 200 OK
	HTTP 10.2.2.204 -> 10.128.113.103 : GET /carts/57a98d98e4b00679b4a830b2/merge?sessionId=Ys4Dh0tNeTyvFLdVJkgb6tM0GhwvLQ6C HTTP/1.1
	HTTP 10.128.113.103 -> 10.2.2.204 : 0
```
