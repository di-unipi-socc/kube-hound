# Test External-IP analysis

- `echo1_load_balancer.yaml` contains a Kubernetes service of kind LoadBalancer, so externally exposed

## Set up

```
$ kubectl delete -f data/examples/external_ip/echo1_load_balancer.yaml
```

## Tool output

```
Exernal-IP analysis - detected smells {PAM}
	External service detected: echo1-load-balancer
	exposed on external ip [REAL_IP_HERE], on host unknown
```

## Clean up

```
$ kubectl delete -f data/examples/external_ip/echo1_load_balancer.yaml
```
