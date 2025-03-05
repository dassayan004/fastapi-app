# FastAPI Boilerplate with PostgreSQL, JWT Authentication, Docker & Nginx

A fully structured **FastAPI** project with **PostgreSQL**, **JWT authentication**, and **Docker** for containerized deployment. Includes **Nginx** as a reverse proxy for production.

## 🚀 Features

✅ FastAPI with modular architecture  
✅ PostgreSQL database integration  
✅ Secure JWT authentication  
✅ Run with batch files
✅ Dockerized setup with `docker-compose`  
✅ Nginx as a reverse proxy  
✅ Environment-based configuration (`.env`)  
✅ Auto-generated Swagger & Redoc API docs

## 📦 Tech Stack

- **FastAPI** – High-performance web framework
- **PostgreSQL** – Relational database
- **SQLAlchemy** – ORM for database interactions
- **Pydantic** – Data validation and serialization
- **JWT** – Secure authentication
- **Docker & Docker Compose** – Containerized deployment
- **Nginx** – Reverse proxy for production

## 🔧 Setup & Usage

1. Clone the repository:
   ```sh
   git clone https://github.com/sayan-veridoc/fastapi-app.git
   cd fastapi-app
   ```
2. Create a `.env` file (see `.env.example`)
3. Create and Activate Virtual Environment:
   - **Linux/macOS**:
     ```sh
     python -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows**:
     ```sh
     python -m venv .venv
     .venv\Scripts\activate
     ```
4. Run the project locally without Docker:
   - Development mode:
     ```sh
     ./run_dev.bat
     ```
   - Production mode:
     ```sh
     ./run_prod.bat
     ```
5. Build and run with Docker Compose:
   ```sh
   docker-compose up --build
   ```
6. Access the API at:
   - `http://localhost:8000` (when running locally)
   - `http://localhost` (when using Docker with Nginx on port 80)
7. API docs available at:
   - Swagger UI: `/docs`
   - ReDoc: `/redoc`

## 📌 TODO

- Add Redis for caching
- Implement role-based access control (RBAC)
- Improve test coverage

📜 **License**: MIT License

🔥 Fork & customize for your projects! 🚀
