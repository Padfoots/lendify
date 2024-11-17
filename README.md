### README.md

# Lendify Banking Loaning System Case Study

Welcome to the Lending System project! This guide will help you get started with the application.

---

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.

---

### How to Start

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Padfoots/lendify.git
   cd lendify/
   ```

2. **Find the assumptions**:

   - assumptions.md

3. **check the Architecture**:

   - Refer to the **UML diagrams** located in the `uml_diagrams` folder to get an overview of the system.

4. **Build and Start Services**:
   Use Docker Compose to build and start the project:

   ```bash
   cd /backend_dev
   docker-compose up --build
   ```

5. **Run Django Commands**:
   Access the Django container and execute necessary setup commands:

   ```bash
   docker-compose exec django sh
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Launch the Backend**:
   The backend will be accessible at:

   ```
   http://localhost:8000/
   ```

7. **Access the Swagger Documentation**:
   Visit the Swagger API documentation to explore and test endpoints:
   ```
   http://localhost:8000/api/schema/docs/
   ```
