# Heart Disease Prediction API

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/MojiburRahaman/heart-disease-prediction-api)
[![Live Demo](https://img.shields.io/badge/Live-Demo-success?logo=render)](https://heart-disease-prediction-api-eqbz.onrender.com/)
[![API Docs](https://img.shields.io/badge/API-Docs-orange?logo=fastapi)](https://heart-disease-prediction-api-eqbz.onrender.com/docs)

A FastAPI application that serves predictions from a machine learning classifier trained on the Heart Disease Dataset.

🌐 **Live API**: [https://heart-disease-prediction-api-eqbz.onrender.com](https://heart-disease-prediction-api-eqbz.onrender.com/)

## 🎯 Try It Now (Live API)

Test the live API without installing anything:

```bash
# Check API health
curl https://heart-disease-prediction-api-eqbz.onrender.com/health

# Get model information
curl https://heart-disease-prediction-api-eqbz.onrender.com/info

# Make a prediction
curl -X POST "https://heart-disease-prediction-api-eqbz.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233,
    "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0,
    "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
  }'
```

Or visit the **[Interactive API Docs](https://heart-disease-prediction-api-eqbz.onrender.com/docs)** 📚

## 🚀 Quick Start (Local Development)

```bash
# 1. Clone the repository
git clone https://github.com/MojiburRahaman/heart-disease-prediction-api.git
cd heart-disease-prediction-api

# 2. Start the application (Docker will train the model automatically)
make up

# 3. View logs to see training and startup
make logs

# 4. Test the API
make test
```

That's it! Access the API at:
- **Local**: `http://localhost:8000`
- **Live**: `https://heart-disease-prediction-api-eqbz.onrender.com` 🎉

## Features

- **Machine Learning Model**: Binary classifier for heart disease prediction
- **FastAPI Backend**: Modern, fast web framework
- **Automatic Training**: Model trains automatically on first Docker startup
- **Docker Support**: Fully containerized application with Docker Compose
- **Persistent Storage**: Model and data persist across container restarts
- **Health Monitoring**: Built-in health checks and auto-recovery
- **Cloud Ready**: Configured for deployment to Render or similar platforms

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── schemas.py           # Pydantic models
│   └── predictor.py         # Model prediction logic
├── model/
│   ├── __init__.py
│   ├── model_run.py         # Model training script
│   └── heart_model.joblib   # Trained model (generated)
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Docker Compose configuration
├── entrypoint.sh            # Container startup script
├── Makefile                 # Convenient commands
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Setup

### Prerequisites
- Docker and Docker Compose

### Quick Start with Docker

1. **Build and start the application** (this will automatically train the model on first run):
```bash
make up
```

2. **View logs** to see training progress and server startup:
```bash
make logs
```

3. **Access the API**:
   - Local: `http://localhost:8000`
   - Live: `https://heart-disease-prediction-api-eqbz.onrender.com`

4. **Test the endpoints**:
```bash
make test
```

That's it! The model will be trained automatically when you first run `make up`. On subsequent runs, it will detect the existing model and skip training.

### Available Make Commands

- `make help` - Show all available commands
- `make build` - Build Docker images
- `make up` - Build and start the application
- `make down` - Stop the application
- `make logs` - View application logs (follow mode)
- `make restart` - Restart the application
- `make clean` - Remove all containers, volumes, and images

### How It Works

The `entrypoint.sh` script automatically:
1. Checks if a trained model exists
2. If not found, downloads the dataset and trains the model
3. Starts the FastAPI application

The trained model and dataset are persisted in Docker volumes, so training only happens once.

### Learn More About Docker

For detailed Docker and Docker Compose concepts, see [Docker_and_DockerCompose_Guide.md](Docker_and_DockerCompose_Guide.md)

## API Endpoints

### Health Check
```bash
GET /health
```
Returns the health status of the API and model.

### Model Information
```bash
GET /info
```
Returns model type, features, and metadata.

### Make Prediction
```bash
POST /predict
Content-Type: application/json

{
  "age": 63,
  "sex": 1,
  "cp": 3,
  "trestbps": 145,
  "chol": 233,
  "fbs": 1,
  "restecg": 0,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 2.3,
  "slope": 0,
  "ca": 0,
  "thal": 1
}
```
Returns prediction with confidence score.

## Features Description

- **age**: Age in years
- **sex**: Sex (1 = male; 0 = female)
- **cp**: Chest pain type (0-3)
- **trestbps**: Resting blood pressure (mm Hg)
- **chol**: Serum cholesterol (mg/dl)
- **fbs**: Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)
- **restecg**: Resting electrocardiographic results (0-2)
- **thalach**: Maximum heart rate achieved
- **exang**: Exercise induced angina (1 = yes; 0 = no)
- **oldpeak**: ST depression induced by exercise
- **slope**: Slope of peak exercise ST segment (0-2)
- **ca**: Number of major vessels colored by fluoroscopy (0-3)
- **thal**: Thalassemia (0 = normal; 1 = fixed defect; 2 = reversible defect)

## Deployment to Cloud

🎯 **Already Deployed**: This API is live at [https://heart-disease-prediction-api-eqbz.onrender.com](https://heart-disease-prediction-api-eqbz.onrender.com/)

### Deployment to Render

1. **Push your code to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit: Heart Disease Prediction API"
git remote add origin https://github.com/MojiburRahaman/heart-disease-prediction-api.git
git push -u origin main
```

2. **Create a Render account** at [render.com](https://render.com)

3. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: heart-disease-api (or your choice)
     - **Environment**: Docker
     - **Region**: Choose your preferred region
     - **Branch**: main
     - **Docker Build Context Path**: ./
     - **Dockerfile Path**: ./Dockerfile
   - Click "Create Web Service"

4. **Wait for deployment**: Render will automatically:
   - Build your Docker image
   - Train the model on first startup
   - Deploy the API

5. **Access your API**: 
   - Your API will be available at: `https://your-service-name.onrender.com`
   - View docs at: `https://your-service-name.onrender.com/docs`

**Example (This Repository)**:
- API: `https://heart-disease-prediction-api-eqbz.onrender.com`
- Docs: `https://heart-disease-prediction-api-eqbz.onrender.com/docs`

### Alternative: Deploy to Other Platforms

**Railway.app**:
- Connect GitHub repo
- Railway auto-detects Dockerfile
- Set PORT environment variable to 8000

**Fly.io**:
```bash
fly launch
fly deploy
```

**Google Cloud Run / AWS ECS / Azure Container Instances**:
- Push Docker image to container registry
- Deploy from registry
- Expose port 8000

## API Documentation

### Local Development
- **Root**: `http://localhost:8000/` - API information
- **Swagger UI**: `http://localhost:8000/docs` - Interactive API docs
- **ReDoc**: `http://localhost:8000/redoc` - Alternative API docs

### Live Deployment
- **Root**: `https://heart-disease-prediction-api-eqbz.onrender.com/` - API information
- **Swagger UI**: `https://heart-disease-prediction-api-eqbz.onrender.com/docs` - Interactive API docs
- **ReDoc**: `https://heart-disease-prediction-api-eqbz.onrender.com/redoc` - Alternative API docs

