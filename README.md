# Flask + MySQL Registration with Jenkins CI/CD

## Prerequisites
- Git
- Docker Engine and Docker Compose plugin (`docker compose version`)
- Jenkins with Pipeline, Git, and credentials plugins
- Jenkins agent user permitted to run Docker commands

## Run locally with Docker Compose
1. Copy `.env.example` to `.env`.
2. Replace the example passwords and secret key.
3. Run:
   ```bash
   docker compose up -d --build
   ```
4. Open http://localhost:5000/register
5. Check health: http://localhost:5000/health

## Jenkins setup
1. Push this project to a Git repository.
2. Configure a Jenkins Pipeline job pointing to that repository.
3. Ensure the Jenkins agent has Python 3, Docker Engine, the Docker Compose plugin, and `curl`.
4. Ensure the Jenkins agent can access the Docker daemon.
5. Run the pipeline. The Jenkinsfile installs dependencies, runs tests, performs Bandit and pip-audit scans, builds the image, deploys with Compose, and checks `/health`.

## Useful commands
```bash
docker compose ps
docker compose logs -f web
docker compose logs -f db
docker compose down
docker compose down -v   # WARNING: deletes the MySQL data volume
```

## Notes for production
- Do not use the example credentials or SECRET_KEY in production.
- Store secrets in Jenkins Credentials or a secrets manager, not in Git.
- Add HTTPS/TLS, CSRF protection, rate limiting, secure cookie settings, database backups, and proper migration management before production use.
- The Jenkinsfile assumes the Jenkins agent runs on the Docker host where the Compose deployment should run.
- `docker compose` requires the Compose v2 plugin; the legacy `docker-compose` executable is a different command.
