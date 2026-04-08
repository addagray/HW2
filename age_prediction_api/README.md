# Age Prediction API

This is a lightweight FastAPI-based web service that predicts a person's age from an uploaded image using OpenCV DNN and pre-trained Caffe models.

## Usage Locally

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
3. Test using `/docs` via your browser at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) or send a POST request with an image file to `/predict`.

## Docker

Build and run the project using Docker:

```bash
# Build the Docker image
docker build -t age-prediction-api .

# Run the Docker container
docker run -p 8000:8000 age-prediction-api
```

## CI/CD Pipeline

The `.github/workflows/ci.yml` file is configured to automatically build and push the Docker image to your Docker Hub every time you push to the `main` branch. 

Setup requirements for github:
1. Go to Github Repository Settings -> Secrets and variables -> Actions
2. Click `New repository secret`
3. Add `DOCKER_USERNAME` (your Docker hub ID)
4. Add `DOCKER_PASSWORD` (your Docker hub token/password)
