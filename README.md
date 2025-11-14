# Pokemon API Backend

API REST desarrollada con FastAPI que consume la PokeAPI y expone endpoints procesados con autenticación JWT.

## Características

- API REST con FastAPI
- Autenticación JWT
- Consumo de PokeAPI
- Base de datos PostgreSQL (Railway)
- Dockerizado
- CI/CD con GitHub Actions
- Análisis de código con SonarQube
- Despliegue automático en AWS ECS Fargate
- Infraestructura como código con Ansible
- HTTPS con Cloudflare

## Arquitectura
```
Usuario → Cloudflare (SSL/TLS) → AWS ECS Fargate → Railway PostgreSQL
                                                   → PokeAPI
                                                   → AWS ECR
```

### Componentes

- **Frontend**: Cloudflare (DNS, SSL, CDN)
- **Backend**: AWS ECS Fargate (contenedor FastAPI)
- **Base de datos**: Railway PostgreSQL
- **Registro de imágenes**: AWS ECR
- **CI/CD**: GitHub Actions
- **IaC**: Ansible

## Requisitos Previos

- Python 3.11+
- Docker & Docker Compose
- AWS CLI configurado
- Cuenta de AWS
- Cuenta de Railway (PostgreSQL)
- Cuenta de SonarCloud
- Ansible (para despliegue)

## Instalación Local

### Clonar repositorio
```bash
git clone https://github.com/HenryBonillaDev/pokemon-api-backend.git
cd pokemon-api-backend
```

### Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Configurar variables de entorno
```bash
cp .env.example .env
```

Editar `.env`:
```env
SECRET_KEY=tu-secret-key
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
POKEAPI_BASE_URL=https://pokeapi.co/api/v2
ENVIRONMENT=development
```

### Ejecutar migraciones
```bash
alembic upgrade head
```

### Ejecutar aplicación
```bash
uvicorn app.main:app --reload
```

API disponible en: `http://localhost:8000`
Documentación: `http://localhost:8000/docs`

## Docker

### Desarrollo local
```bash
docker-compose up --build
```

Esto inicia PostgreSQL (puerto 5432) y la API (puerto 8000).

## Testing
```bash
pytest
pytest --cov=app --cov-report=html
```

## Endpoints

### Autenticación

**POST /auth/register**
```json
{
  "username": "usuario",
  "email": "email@example.com",
  "password": "password123"
}
```

**POST /auth/login**
```
Form data:
  username: usuario
  password: password123

Response:
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Pokemon (requiere token JWT)

**GET /pokemon?limit=20&offset=0**

Lista pokemon con paginación.

**GET /pokemon/{id_o_nombre}**

Obtiene detalles de un pokemon específico.

**GET /pokemon/search?name=pika**

Busca pokemon por nombre.

**GET /pokemon/compare?pokemon1=pikachu&pokemon2=charizard**

Compara estadísticas de dos pokemon.

Todos los endpoints de pokemon requieren header:
```
Authorization: Bearer <token>
```

## Despliegue en AWS

### Con Ansible
```bash
cd ansible
cp vars.yml.example vars.yml
# Editar vars.yml con valores reales
ansible-playbook -i inventory.ini deploy-infrastructure.yml
```

### Manual
```bash
# Login a ECR
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com

# Build y push
docker build -t pokemon-api .
docker tag pokemon-api:latest ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com/pokemon-api:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com/pokemon-api:latest

# Actualizar servicio
aws ecs update-service --cluster pokemon-cluster --service pokemon-api-service --force-new-deployment --region us-east-2
```

## CI/CD Pipeline

Pipeline automático en GitHub Actions para `develop` y `main`:

1. **Test**: Ejecuta tests unitarios con cobertura
2. **SonarQube**: Análisis estático de código
3. **Build & Push**: Construye y sube imagen a ECR
4. **Deploy**: Despliega a ECS Fargate

### Configurar Secrets en GitHub
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
SONAR_TOKEN
SONAR_HOST_URL
```

## Dominio y SSL

Configurado con Cloudflare para SSL/TLS y DNS.

URL de producción: https://pokemon-api.duvanbonilladev.com

## Estructura del Proyecto
```
pokemon-api-backend/
├── .github/workflows/ci-cd.yml
├── alembic/
├── ansible/
│   ├── deploy-infrastructure.yml
│   ├── inventory.ini
│   ├── requirements.yml
│   └── vars.yml.example
├── app/
│   ├── api/
│   │   ├── routes/
│   │   └── dependencies.py
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── utils/
│   └── main.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Flujo de Trabajo Git
```
main (producción)
  ↑
develop (staging)
  ↑
feature/* (desarrollo)
```

Commits con Conventional Commits:
- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `docs:` documentación
- `chore:` tareas de mantenimiento
- `test:` tests

## Troubleshooting

### Ver logs del contenedor
```bash
aws logs tail /ecs/pokemon-api-task --follow --region us-east-2
```

### Verificar estado de tarea
```bash
aws ecs describe-tasks --cluster pokemon-cluster --tasks TASK_ARN --region us-east-2
```

### Verificar servicio
```bash
aws ecs describe-services --cluster pokemon-cluster --services pokemon-api-service --region us-east-2
```