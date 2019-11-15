## Rserve with Sidecar Example

* Main funtionality from a [Rserve](https://www.rforge.net/Rserve/)-based web service
* Sidecar service, created by [FastAPI](https://fastapi.tiangolo.com/), handles authentication and relays requests/responses from authenticated users
* See [this post](https://jaehyeon.me/blog/2019-11-01-Linux-Dev-Environment-on-Windows) for more details.

### Docker Compose

```bash
git clone https://github.com/jaehyeon-kim/k8s-rserve.git
cd k8s-rserve
docker-compose up -d
```

### Kubernetes

```bash
kubectl apply -f manifest.yml
```