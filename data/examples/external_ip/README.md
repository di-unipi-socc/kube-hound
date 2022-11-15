# Test External-IP analysis

- `echo1_load_balancer.yaml` contains a Kubernetes service of kind LoadBalancer, so externally exposed

## Set up

```
$ # deploy the modified version of echo1 service
$ kubectl delete -f data/examples/external_ip/echo1_load_balancer.yaml
$ # expose the echo2 service
$ kubectl expose pod echo2 --type=LoadBalancer --name='echo2-exposed'
```

## Tool output

```
$ ./data/examples/external_ip/run.sh

Analysis results:
Exernal-IP analysis - detected smells {PAM}
	External service detected: echo1-load-balancer
	exposed on external ip [REAL_IP_HERE], on host unknown

Exernal-IP analysis - detected smells {PAM}
	External service detected: echo2-exposed
	exposed on external ip [REAL_IP_HERE], on host unknown
```

## Clean up

```
$ kubectl delete -f data/examples/external_ip/echo1_load_balancer.yaml
$ kubectl delete service echo2-exposed
```
