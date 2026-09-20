docker run -d \
  --name devops-lab-api-test \
  -p 18080:8080 \
  -e APP_NAME=devops-lab-api \
  -e APP_ENV=local \
  -e APP_VERSION=0.0.0-local \
  harunsert/devops-lab-api:local
