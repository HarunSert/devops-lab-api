# DevOps Lab API

A lightweight FastAPI application designed for hands-on DevOps, CI/CD, Kubernetes, autoscaling and monitoring scenarios.

## Features

- FastAPI REST API
- Dockerized application
- Non-root container
- Liveness endpoint
- Readiness endpoint
- Application version endpoint
- Environment configuration
- CPU load generation endpoint
- Prometheus metrics endpoint
- Automated API tests

## Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Application information |
| `/health/live` | Kubernetes liveness probe |
| `/health/ready` | Kubernetes readiness probe |
| `/version` | Running application version |
| `/config` | Application environment information |
| `/load` | Generates CPU load for HPA testing |
| `/metrics` | Prometheus metrics |

## Build

```bash
docker build -t harunsert/devops-lab-api:local .
```

## Run

```bash
docker run -d \
  --name devops-lab-api \
  -p 18080:8080 \
  -e APP_NAME=devops-lab-api \
  -e APP_ENV=local \
  -e APP_VERSION=0.0.0-local \
  harunsert/devops-lab-api:local
```

## Test

```bash
curl http://127.0.0.1:18080/
curl http://127.0.0.1:18080/version
curl http://127.0.0.1:18080/health/live
curl http://127.0.0.1:18080/health/ready
```

## Planned CI/CD Flow

```text
Git Tag
   |
   v
Jenkins
   |
   +--> Automated Tests
   |
   +--> Docker Build
   |
   +--> Docker Hub
   |
   +--> Helm Upgrade
   |
   v
Kubernetes
```

A Git release tag will be used directly as the Docker image version.

Example:

```text
Git tag:      1.10.5
Docker image: harunsert/devops-lab-api:1.10.5
```

## Author

Harun Sert
