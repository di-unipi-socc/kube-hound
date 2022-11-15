# Test Pod-to-Pod traffic analysis

This test works on an Istio-enabled cluster.

- `mTLS-disable.yaml`contains a PeerAuthentication object that disables mTLS in Pod-to-Pod communications
- `mTLS-strict.yaml`contains a PeerAuthentication object that enables mTLS in Pod-to-Pod communications and sets it to strict mode


## Set up
To enable/disable mTLS simply deploy the corresponding Kubernetes object

```
$ kubectl apply -f data/examples/pod_to_pod_traffic/mTLS-disable.yaml
$ kubectl apply -f data/examples/pod_to_pod_traffic/mTLS-strict.yaml
```

## Tool output

If we run the analysis with mTLS in strict mode, then no smells will be detected.

However if we run it with mTLS disabled, it will output unsecured service-to-service communications.
This output is generated while testing on the mock microservices application with disabled mTLS.
```
$ ./data/examples/pod_to_pod_traffic/run.sh

Analysis results:
Traffic analysis - detected smells {NSC}
	Unencrypted traffic detected in pod authserver-5f44f4f8b6-vfs9v
	here is a sample of the packets:
	HTTP 10.2.2.3 -> 10.2.1.4 : POST /login HTTP/1.1
	HTTP 10.2.1.4 -> 10.2.2.3 : HTTP/1.1 200 OK
	HTTP 10.2.2.3 -> 10.2.1.4 : POST /validate HTTP/1.1
	HTTP 10.2.1.4 -> 10.2.2.3 : HTTP/1.1 200 OK
	HTTP 10.2.2.3 -> 10.2.1.4 : POST /validate HTTP/1.1
	HTTP 10.2.1.4 -> 10.2.2.3 : HTTP/1.1 200 OK
	HTTP 10.2.2.3 -> 10.2.1.4 : POST /login HTTP/1.1
	HTTP 10.2.1.4 -> 10.2.2.3 : HTTP/1.1 200 OK
	HTTP 10.2.2.3 -> 10.2.1.4 : POST /validate HTTP/1.1
	HTTP 10.2.1.4 -> 10.2.2.3 : HTTP/1.1 200 OK
	HTTP 10.2.2.3 -> 10.2.1.4 : POST /validate HTTP/1.1

Traffic analysis - detected smells {NSC}
	Unencrypted traffic detected in pod echo1-d8fc66857-78m5n
	here is a sample of the packets:
	HTTP 10.2.2.4 -> 10.2.2.5 : POST /echo HTTP/1.1
	HTTP 10.2.2.5 -> 10.2.2.4 : {"echo3": [{"echo5": []}]}
	HTTP 10.2.2.4 -> 10.2.2.3 : HTTP/1.1 200 OK
	HTTP 10.2.2.3 -> 10.2.2.4 : POST /echo HTTP/1.1
	HTTP 10.2.2.4 -> 10.2.1.6 : POST /echo HTTP/1.1
	HTTP 10.2.1.6 -> 10.2.2.4 : HTTP/1.1 200 OK
	HTTP 10.2.2.4 -> 10.2.2.5 : POST /echo HTTP/1.1
	HTTP 10.2.2.5 -> 10.2.2.4 : HTTP/1.1 200 OK
	HTTP 10.2.2.4 -> 10.2.2.3 : HTTP/1.1 200 OK
	HTTP 10.2.2.3 -> 10.2.2.4 : POST /echo HTTP/1.1
	HTTP 10.2.2.4 -> 10.2.1.6 : POST /echo HTTP/1.1

Traffic analysis - detected smells {NSC}
	Unencrypted traffic detected in pod echo2-5bb6588768-8pnqv
	here is a sample of the packets:
	HTTP 10.2.2.3 -> 10.2.1.5 : POST /echo HTTP/1.1
	HTTP 10.2.1.5 -> 10.2.2.6 : POST /echo HTTP/1.1
	HTTP 10.2.2.6 -> 10.2.1.5 : HTTP/1.1 200 OK
	HTTP 10.2.1.5 -> 10.2.2.3 : HTTP/1.1 200 OK
	HTTP 10.2.2.3 -> 10.2.1.5 : POST /echo HTTP/1.1
	HTTP 10.2.1.5 -> 10.2.2.6 : POST /echo HTTP/1.1
	HTTP 10.2.2.6 -> 10.2.1.5 : HTTP/1.1 200 OK
	HTTP 10.2.1.5 -> 10.2.2.3 : HTTP/1.1 200 OK
	HTTP 10.2.2.3 -> 10.2.1.5 : POST /echo HTTP/1.1
	HTTP 10.2.1.5 -> 10.2.2.6 : POST /echo HTTP/1.1
	HTTP 10.2.2.6 -> 10.2.1.5 : HTTP/1.1 200 OK

Traffic analysis - detected smells {NSC}
	Unencrypted traffic detected in pod echo3-64d44c5cff-wv5ms
	here is a sample of the packets:
	HTTP 10.2.2.4 -> 10.2.2.5 : POST /echo HTTP/1.1
	HTTP 10.2.2.5 -> 10.2.2.6 : POST /echo HTTP/1.1
	HTTP 10.2.2.6 -> 10.2.2.5 : HTTP/1.1 200 OK
	HTTP 10.2.2.5 -> 10.2.2.4 : HTTP/1.1 200 OK
	HTTP 10.2.2.4 -> 10.2.2.5 : POST /echo HTTP/1.1
	HTTP 10.2.2.5 -> 10.2.2.6 : POST /echo HTTP/1.1
	HTTP 10.2.2.6 -> 10.2.2.5 : HTTP/1.1 200 OK
	HTTP 10.2.2.5 -> 10.2.2.4 : HTTP/1.1 200 OK
	HTTP 10.2.2.4 -> 10.2.2.5 : POST /echo HTTP/1.1
	HTTP 10.2.2.5 -> 10.2.2.6 : POST /echo HTTP/1.1
	HTTP 10.2.2.6 -> 10.2.2.5 : HTTP/1.1 200 OK

Traffic analysis - detected smells {NSC}
	Unencrypted traffic detected in pod echo4-5c79f5c86b-gkw2v
	here is a sample of the packets:
	HTTP 10.2.2.4 -> 10.2.1.6 : POST /echo HTTP/1.1
	HTTP 10.2.1.6 -> 10.2.2.4 : HTTP/1.1 200 OK
	HTTP 10.2.2.4 -> 10.2.1.6 : POST /echo HTTP/1.1
	HTTP 10.2.1.6 -> 10.2.2.4 : HTTP/1.1 200 OK
	HTTP 10.2.2.4 -> 10.2.1.6 : POST /echo HTTP/1.1
	HTTP 10.2.1.6 -> 10.2.2.4 : HTTP/1.1 200 OK
	HTTP 10.2.2.4 -> 10.2.1.6 : POST /echo HTTP/1.1
	HTTP 10.2.1.6 -> 10.2.2.4 : HTTP/1.1 200 OK
	HTTP 10.2.2.4 -> 10.2.1.6 : POST /echo HTTP/1.1
	HTTP 10.2.1.6 -> 10.2.2.4 : HTTP/1.1 200 OK
	HTTP 10.2.2.4 -> 10.2.1.6 : POST /echo HTTP/1.1

Traffic analysis - detected smells {NSC}
	Unencrypted traffic detected in pod echo5-7b7f8886b5-75r8c
	here is a sample of the packets:
	HTTP 10.2.2.5 -> 10.2.2.6 : POST /echo HTTP/1.1
	HTTP 10.2.2.6 -> 10.2.2.5 : HTTP/1.1 200 OK
	HTTP 10.2.1.5 -> 10.2.2.6 : POST /echo HTTP/1.1
	HTTP 10.2.2.6 -> 10.2.1.5 : HTTP/1.1 200 OK
	HTTP 10.2.2.5 -> 10.2.2.6 : POST /echo HTTP/1.1
	HTTP 10.2.2.6 -> 10.2.2.5 : HTTP/1.1 200 OK
	HTTP 10.2.1.5 -> 10.2.2.6 : POST /echo HTTP/1.1
	HTTP 10.2.2.6 -> 10.2.1.5 : HTTP/1.1 200 OK
	HTTP 10.2.2.5 -> 10.2.2.6 : POST /echo HTTP/1.1
	HTTP 10.2.2.6 -> 10.2.2.5 : HTTP/1.1 200 OK
	HTTP 10.2.1.5 -> 10.2.2.6 : POST /echo HTTP/1.1

Traffic analysis - detected smells {NSC}
	Unencrypted traffic detected in pod gateway-775d87ff7b-l5bqz
	here is a sample of the packets:
	HTTP 10.2.2.4 -> 10.2.2.3 : HTTP/1.1 200 OK
	HTTP 10.2.2.3 -> 10.2.1.3 : HTTP/1.1 200 OK
	HTTP 10.2.1.3 -> 10.2.2.3 : POST /echo2 HTTP/1.1
	HTTP 10.2.2.3 -> 10.2.1.3 : HTTP/1.1 401 Unauthorized
	HTTP 10.2.1.3 -> 10.2.2.3 : POST /echo2 HTTP/1.1
	HTTP 10.2.2.3 -> 10.2.1.4 : POST /validate HTTP/1.1
	HTTP 10.2.1.4 -> 10.2.2.3 : HTTP/1.1 200 OK
	HTTP 10.2.2.3 -> 10.2.1.5 : POST /echo HTTP/1.1
	HTTP 10.2.1.5 -> 10.2.2.3 : HTTP/1.1 200 OK
	HTTP 10.2.2.3 -> 10.2.1.3 : HTTP/1.1 200 OK
	HTTP 10.2.1.3 -> 10.2.2.3 : POST /login HTTP/1.1
```