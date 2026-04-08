# MLOps Deployment & CI/CD Checklist

This checklist acts as a guide to verify continuous delivery. When you update code or add a new machine learning model (e.g., adding the Gender Net and modifying the endpoints), pushing the changes to the `main` branch will automatically build and distribute the update across the local server based on the `.github/workflows/ci.yml`.

## Pre-Deployment Verification
- [ ] Code has been tested locally on the machine (`python main.py`).
- [ ] Features are verified functioning accurately (Age & Gender both returned).
- [ ] `git add`, `git commit` appropriately documenting changes.
- [ ] `git push origin main` executed successfully.

## CI/CD Pipeline Verification (GitHub Actions)
1. Navigate to the **Actions** tab on your GitHub repository.
2. Select the latest triggered continuous integration pipeline execution.
3. Validate these steps successfully passed (indicated with a green checkmark):
   - [ ] `Checkout code`
   - [ ] `Set up Docker Buildx`
   - [ ] `Build and push Docker image`
   - [ ] `Deploy` sequence (which interacts with your local server)

## Local Server Verification 
Since your environment operates GitHub Actions self-hosted runners, the final `Deploy` stage stops the existing containers and starts a fresh one with the new docker image built from your commit.
- [ ] Visit `http://127.0.0.1:8000/` and upload an image to confirm updates are active.
- [ ] Execute `docker ps` on the command line. Confirm `age-prediction-api` container states "Up Less than a minute".

## Troubleshooting Deployment Failures
If you encounter errors during or post-deployment, examine logs in the following areas:

### 1. GitHub Action Logs 
If the pipeline fails, click the exact step in the Actions tab that failed. If the `Build` step failed, likely a change in your `requirements.txt` or `Dockerfile` is syntactically invalid. If `Deploy` failed, the runner is likely disconnected or Docker is not running locally.

### 2. Local Container Logs 
If the deployment runner succeeds, but the application crashes continuously locally or doesn't start properly:
- Open your standard terminal.
- Run `docker logs age-prediction-api --tail 100` to retrieve application crashes (e.g., missing dependencies like `aiofiles` or typo in model variables).

### 3. Debugging within the Container
- If the app is up but misbehaving internally: `docker exec -it age-prediction-api /bin/bash`
- Check internal directory structural permissions or missing environment variables.
