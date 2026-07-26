# Deployment and Docker instructions (GazeHum)

## Build locally (Docker)

```bash
# build image
docker build -t gazehum:latest .

# run (mount models/data as volumes)
docker run -it --rm -p 8501:8501 \
  -v $(pwd)/models:/app/models:ro \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  gazehum:latest
```

## Docker Compose (local production-like)

```bash
docker-compose up --build -d
```

## Kubernetes

1. Create Secrets (replace values):

```bash
kubectl create secret generic gazehum-secrets --from-literal=SUPABASE_URL='...' --from-literal=SUPABASE_KEY='...'
```

2. Apply manifests:

```bash
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Storage recommendations

- Store large ML models in a dedicated object store (S3, GCS) or a separate PVC mounted at `/app/models`.
- Do NOT bake models into the image; mount them as a read-only volume.
- Use a separate PVC for application data and logs so they survive redeploys.

## Notes

- The Dockerfile creates a non-root user and sets Streamlit to headless mode for production.
- The `.dockerignore` excludes virtual envs, datasets, logs and local artifacts to keep image size minimal.
