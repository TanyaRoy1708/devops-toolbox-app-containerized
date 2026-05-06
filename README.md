# DevOps Toolbox

A simple FastAPI-based toolbox for DevOps practitioners, featuring tools like Cron Explainer, JWT Decoder, CIDR Calculator, and more.

## How to Run Locally

### 1. Prerequisites
- Python 3.8+ installed on your system.

### 2. Setup Virtual Environment
Open your terminal in the project root and run:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Copy `.env.example` to `.env` and update the database and Redis connection strings if necessary:
```powershell
copy .env.example .env
```

### 5. Initialize MySQL Database
Before running the app, ensure you have a MySQL database named `devops_toolbox` created:
```sql
CREATE DATABASE devops_toolbox;
```

### 6. Verify the Setup (Tests)
Run the unit tests to ensure database and cache integrations are working correctly:
```powershell
pytest
```

### 7. Run the Application
```powershell
uvicorn main:app --reload
```

### 8. Access the Web UI
Open your browser and go to:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

## Features
- **Cron Explainer**: Convert cron expressions into human-readable text (Cached in Redis).
- **JWT Decoder**: Decode and inspect JSON Web Tokens (Cached in Redis).
- **CIDR Calculator**: Calculate IP ranges and netmasks (Cached in Redis).
- **K8s Manifest Explainer**: Get a high-level summary of Kubernetes YAML files.
- **Dockerfile Linter**: Basic security and best-practice checks for Dockerfiles.
- **Usage Logging**: All tool usage is logged to a MySQL database and displayed on the homepage.

---
*Note: This version requires MySQL and Redis. Ensure they are running and accessible via the URLs in your `.env` file.*
