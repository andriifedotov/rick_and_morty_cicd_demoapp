Perfect! Let’s structure your README so it’s professional, clear, and complete. Here’s a full draft tailored for your Rick & Morty API project with Kubernetes + Helm + Redis/Postgres:

---

````markdown
# Rick & Morty CICD Demo App

A containerized **Rick & Morty API** application deployed using **Kubernetes**, **Helm**, and CI/CD pipelines. This demo includes Postgres, Redis, and Nginx Ingress, and is designed for easy local and CI/CD testing.

---

## Architecture

```mermaid
flowchart LR
    subgraph CI/CD Pipeline
        A[Build Docker Image] --> B[Push to DockerHub]
        B --> C[Helm Deploy]
    end

    subgraph Kubernetes Cluster
        subgraph Backend
            D[Postgres Database] --> E[Rick & Morty API]
            F[Redis Cache] --> E
        end
        subgraph Ingress
            G[Nginx Ingress Controller] --> E
        end
    end

    C --> Kubernetes Cluster
````

---

## Features

* Django REST API serving Rick & Morty characters.
* **Postgres** for persistent storage.
* **Redis** for caching.
* **Nginx Ingress** for routing.
* CI/CD pipeline for automated testing and deployment.

---

## Requirements

* [Docker](https://www.docker.com/)
* [Kubernetes cluster](https://kubernetes.io/docs/setup/)
* [Helm](https://helm.sh/docs/intro/install/)
* Python >= 3.12 (for local testing)
* kubectl CLI

---

## Setup & Deployment

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/rickmorty-cicd-demo.git
cd rickmorty-cicd-demo
```

### 2. Build & Push Docker Image

```bash
docker build -t andriifedotov/rickmorty-api:latest .
docker push andriifedotov/rickmorty-api:latest
```

### 3. Deploy with Helm

```bash
helm dependency build helm/rickmorty-api-chart
helm upgrade --install rickmorty helm/rickmorty-api-chart \
    --set image.tag=latest \
    --wait
```

> ⚠️ Ensure Postgres and Redis are deployed and ready before starting the API. In CI, you may need to wait for pods with `kubectl wait --for=condition=ready pod --all --timeout=180s`.

### 4. Port Forward for Local Access

```bash
kubectl port-forward svc/rickmorty-rickmorty-api 8000:8000
```

Now the API is accessible at: `http://localhost:8000/api/characters/`

---

## Testing

### Integration Test (Local)

```bash
export API_URL="http://localhost:8000/api/characters/"
python - <<EOF
import requests
r = requests.get("${API_URL}")
assert r.status_code == 200, f"Expected 200 but got {r.status_code}"
data = r.json()
assert "results" in data, "No results key in API response"
print("Integration test passed!")
EOF
```

### CI/CD

* The pipeline builds, pushes the image, deploys the chart, waits for Postgres/Redis pods, then runs integration tests.
* Logs and exit codes are used to determine success/failure.

---

## API Documentation

### Base URL

```
http://<your-host>/api/
```

### Endpoints

| Method | Endpoint          | Description            |
| ------ | ----------------- | ---------------------- |
| GET    | /characters/      | List all characters    |
| GET    | /characters/{id}/ | Get a single character |

### Example Response

```json
{
  "results": [
    {
      "id": 1,
      "name": "Rick Sanchez",
      "status": "Alive",
      "species": "Human",
      "origin": "Earth",
      "gender": "Male"
    }
  ]
}
```

> For a complete OpenAPI spec, see [openapi.yaml](./docs/openapi.yaml)

---

## Configuration

* **Helm Values** (`values.yaml`) allow customization:

```yaml
replicaCount: 2
image:
  repository: andriifedotov/rickmorty-api
  tag: latest
service:
  type: ClusterIP
  port: 8000
postgresql:
  auth:
    username: rnm
    password: rnm
    database: rnm
redis:
  enabled: true
  host: rickmorty-rickmorty-api-redis
  port: 6379
ingress:
  enabled: true
  host: localhost
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
```

* Secrets (like `databaseUrl` and `cacheUrl`) are provided via Helm values or Kubernetes Secrets.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

## License

MIT License © Andrii Fedotov

```

---

If you want, I can **also draw a nicer Mermaid diagram** with separate arrows for Postgres, Redis, and the API, so it’s fully professional and visually clear for your README.  

Do you want me to do that next?
```
