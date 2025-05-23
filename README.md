# 📝 DocGEN Legal Document Generator

A Python-based automated legal document generator that leverages templating to produce dynamic documents. This project supports containerized deployments with **Docker**, CI/CD integration with **Jenkins**, and a modular file architecture for scalability and maintainability.

---

## 📁 Project Structure

```
├── app/                # Core application logic
├── components/         # Reusable components used in documents
├── charts/             # Visual or chart assets
├── forms/              # Form definitions and handlers
├── instance/           # Instance-specific files/configs
├── static/             # Static files (CSS, JS, images)
├── tables/             # Table generation logic or static data
├── .env                # Environment variables
├── Dockerfile          # Docker image instructions
├── docker-compose      # Multi-container configuration
├── Jenkinsfile         # Jenkins pipeline definition
├── LICENSE             # Open-source license
├── README.md           # You're here!
├── requirements.txt    # Python dependencies
├── run.py              # Application runner
├── create_templates.py # Script to generate document templates
```

---

## 🚀 Features

- 📄 **Templated Legal Document Generation** using Python.
- 🐳 **Dockerized** for easy deployment.
- 🔁 **CI/CD Ready** with Jenkins pipeline support.
- 📦 Clean project structure for easy extension and collaboration.
- 🌐 Modular components and forms.
- ⚙️ Custom static and dynamic table integration.

---

## 🧰 Tech Stack

- **Python 3.10+**
- **Jinja2 / Template Engine**
- **Docker**
- **Jenkins**
- **Flask** (if used inside `app/`)
- **Bootstrap / Custom JS** (via static folder)

---

## 🏗️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/abhijjeeet/DocGEN-Python.git
cd legal-doc-generator
```

### 2. Configure Environment

Create and edit your `.env` file:

```bash
cp .env.example .env
```

Update credentials, template paths, and other variables.

### 3. Run with Docker

Build and run using Docker:

```bash
docker build -t legal-doc-generator .
docker run -p 5000:5000 legal-doc-generator
```

Or use Docker Compose:

```bash
docker-compose up --build
```

---

## 🔄 CI/CD with Jenkins

Make sure Jenkins is installed and configured.

1. Add Jenkinsfile to a pipeline project.
2. Set up environment variables in Jenkins UI.
3. Hook it to GitHub for automatic triggers.

---

## 🛠️ Development

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

---

## 📑 How It Works

1. Navigate to form interface.
2. Fill out details for the legal document.
3. Submit to render and download the final document.
4. Custom templates are stored and managed via `create_templates.py`.
