# Online Boutique testing

- `full_no_istio_output.txt` shows the tool's output when running on Online Boutique, without enabling the Istio service mesh.
- `full_istio_output.txt` shows the tool's output when running on Online Boutique,with the Istio service mesh enabled.


## Set up

Deployment of Istio service mesh (optional)
```
kubectl apply -f ./release/istio-manifests.yaml
```

Deployment of the application
```
kubectl apply -f ./release/kubernetes-manifests.yaml
```

## Run test

```
./scripts/run_online_boutique.sh
```


## Highlights of analysis

It was detected that all services run as root and do not have set up AppArmor and SecComp profiles:
```
KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in cartservice.yaml
	selector: .metadata .annotations ."container.apparmor.security.beta.kubernetes.io/nginx"
	reason: Well defined AppArmor policies may provide greater protection from unknown threats. WARNING: NOT PRODUCTION READY

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in cartservice.yaml
	selector: .metadata .annotations ."container.seccomp.security.alpha.kubernetes.io/pod"
	reason: Seccomp profiles set minimum privilege and secure against unknown threats

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in cartservice.yaml
	selector: containers[] .securityContext .runAsNonRoot == true
	reason: Force the running image to run as a non-root user to ensure least privilege

KubeSec analysis - detected smells {UPM}
	Kubesec.io found potential problems in cartservice.yaml
	selector: containers[] .securityContext .runAsUser -gt 10000
	reason: Run as a high-UID user to avoid conflicts with the host's user table


(similar for the other services)
```

With **Istio enabled**, no "Non-secured Service-to-Service communications" was detected.

With **Istio disabled**, it was detected unencrypted HTTP traffic from the load generator to the gateway, and unencrypted HTTP2 traffic between the services:

```
Traffic analysis - detected smells {NSC}
	Unencrypted traffic detected in pod frontend-547c944df9-p25b5
	here is a sample of the packets (HTTP):
	HTTP 10.2.1.37 -> 10.2.1.35 : GET /product/0PUK6V6EV0 HTTP/1.1
	HTTP 10.2.1.35 -> 10.2.1.37 : t-quantity-dropdown">
	HTTP 10.2.1.37 -> 10.2.1.35 : product_id=0PUK6V6EV0&quantity=2
	HTTP 10.2.1.35 -> 10.2.1.37 : HTTP/1.1 302 Found
	HTTP 10.2.1.37 -> 10.2.1.35 : GET /cart HTTP/1.1
	HTTP 10.2.1.35 -> 10.2.1.37 : container">
	HTTP 10.2.1.37 -> 10.2.1.35 : email=someone%40example.com&street_address=1600+Amphitheatre+Parkway&zip_code=94043&city=Mountain+View&state=CA&country=United+States&credit_card_number=4432-8015-6152-0454&credit_card_expiration_month=1&credit_card_expiration_year=2039&credit_card_cvv=672
	HTTP 10.2.1.35 -> 10.2.1.37 : -pepper-shakers.jpg">
	HTTP 10.2.1.37 -> 10.2.1.35 : GET /product/L9ECAV7KIM HTTP/1.1
	HTTP 10.2.1.35 -> 10.2.1.37 :       <select name="quantity" id="quantity">
	HTTP 10.2.1.37 -> 10.2.1.35 : currency_code=JPY

...

Traffic analysis - detected smells {NSC}
	Unencrypted traffic detected in pod paymentservice-5b8fb945f-9bsm2
	here is a sample of the packets (HTTP2, maybe gRPC?):
	HTTP2 10.2.1.34 -> 10.2.2.36
	HTTP2 10.2.1.34 -> 10.2.2.36
	HTTP2 10.2.2.36 -> 10.2.1.34
	HTTP2 10.2.2.36 -> 10.2.1.34
	HTTP2 10.2.1.34 -> 10.2.2.36
	HTTP2 10.2.2.36 -> 10.2.1.34
	HTTP2 10.2.2.36 -> 10.2.1.34
	HTTP2 10.2.1.34 -> 10.2.2.36
	HTTP2 10.2.2.36 -> 10.2.1.34
```

## Linode API token

One interesting thing is that running these tests on a Linode Kubernetes cluster, the "Secrets in environment variables" analysis will output that the linode Pods in the container (probably used for management) have a Linode API Token in their environment:

```
Secrets in environment variables analysis - detected smells {HS}
	Detected secret in pod csi-linode-node-v4tts, container csi-linode-plugin
	variable: LINODE_TOKEN=f882************************************************************
	reason: Hex High Entropy String
```
