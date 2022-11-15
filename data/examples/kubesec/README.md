# Test Kubesec.io integration analysis

- `echo1_no_resources.yaml` contains the deployment of the echo1 service, but without the
    specification of the serources limits and requests
- `echo1_no_securitycontext.yaml` contains the deployment of the echo1 service, but without the
    specification of the security context
- `echo1_privileged.yaml` contains the deployment of the echo1 service, but set to privileged mode

## Tool output

### Command to run

```
./data/examples/kubesec/run.sh
```

### No resources specification
```
KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_no_resources.yaml
	selector: containers[] .resources .limits .cpu
	reason: Enforcing CPU limits prevents DOS via resource exhaustion

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_no_resources.yaml
	selector: containers[] .resources .limits .memory
	reason: Enforcing memory limits prevents DOS via resource exhaustion

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_no_resources.yaml
	selector: containers[] .resources .requests .cpu
	reason: Enforcing CPU requests aids a fair balancing of resources across the cluster

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_no_resources.yaml
	selector: containers[] .resources .requests .memory
	reason: Enforcing memory requests aids a fair balancing of resources across the cluster
```

### Privileged pod
```
KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_privileged.yaml
	selector: containers[] .securityContext .runAsNonRoot == true
	reason: Force the running image to run as a non-root user to ensure least privilege

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_privileged.yaml
	selector: containers[] .securityContext .runAsUser -gt 10000
	reason: Run as a high-UID user to avoid conflicts with the host's user table
```

### No SecurityContext speficiation
```
KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_no_securitycontext.yaml
	selector: containers[] .securityContext .capabilities .drop
	reason: Reducing kernel capabilities available to a container limits its attack surface

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_no_securitycontext.yaml
	selector: containers[] .securityContext .capabilities .drop | index("ALL")
	reason: Drop all capabilities and add only those required to reduce syscall attack surface

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_no_securitycontext.yaml
	selector: containers[] .securityContext .readOnlyRootFilesystem == true
	reason: An immutable root filesystem can prevent malicious binaries being added to PATH and increase attack cost

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_no_securitycontext.yaml
	selector: containers[] .securityContext .runAsNonRoot == true
	reason: Force the running image to run as a non-root user to ensure least privilege

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_no_securitycontext.yaml
	selector: containers[] .securityContext .runAsUser -gt 10000
	reason: Run as a high-UID user to avoid conflicts with the host's user table
```


### Common results
All files will produce also these results.
These are checks done by Kubesec for usage/configuration of advanced and/or instable security fetaures of Kubernetes.

```
KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_no_resources.yaml
	selector: .metadata .annotations ."container.apparmor.security.beta.kubernetes.io/nginx"
	reason: Well defined AppArmor policies may provide greater protection from unknown threats. WARNING: NOT PRODUCTION READY

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in echo1_no_resources.yaml
	selector: .metadata .annotations ."container.seccomp.security.alpha.kubernetes.io/pod"
	reason: Seccomp profiles set minimum privilege and secure against unknown threats
```