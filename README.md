# CrediSure Full Stack Software Engineer Assessment

## Project Overview

CrediSure is a credit intelligence platform that enables users to:
- Register and authenticate securely
- Complete KYC verification
- Upload bank statements for analysis
- Receive automated credit assessment scores
- Apply for funding based on creditworthiness

This repository contains the complete implementation of the backend API system along with frontend components, database design, and cloud architecture documentation as required by the assessment.

---

## Live Demo

- **Backend API**: [https://credisure-assessment-repository-backend.onrender.com/docs](https://credisure-assessment-repository-backend.onrender.com/docs#/)

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
   - [Frontend](#frontend)
   - [Backend](#backend)
   - [Database](#database)
   - [Development Tools](#development-tools)
3. [System Architecture Overview](#system-architecture-overview)
4. [Authentication Flow](#authentication-flow)
5. [API Endpoint](#api-endpoint)
   - [Authentication](#authentication)
   - [Credit Assessment](#credit-assessment)
   - [File Upload](#file-upload)
6. [Database Design Summary](#database-design-summary)
7. [Data Relationship](#data-relationship)
8. [File Storage Strategy](#file-storage-strategy)
9. [Security Design](#security-design)
10. [Deployment Design](#deployment-design)

---

## Technology Stack

### Frontend
| Technology | Purpose | Version |
|------------|---------|---------|
| Next.js | React Framework with SSR/SSG | 14.x |
| TypeScript | Static type checking | 5.x |
| Tailwind CSS | Utility-first CSS framework | 3.x |
| React Hook Form | Form management | 7.x |
| Zod | Schema validation | 3.x |
| Axios | HTTP client | 1.x |


### Backend
| Technology | Purpose | Version |
|------------|---------|---------|
| FastAPI | Modern web framework | 0.104.x |
| Python | Programming language | 3.11 |
| SQLAlchemy | ORM | 2.x |
| Pydantic | Data validation | 2.x |
| PyJWT | JWT token handling | 2.x |
| Passlib | Password hashing (bcrypt) | 1.7.x |
| Alembic | Database migrations | 1.x |
| Python-Multipart | File upload handling | 0.0.x |
| Uvicorn | ASGI server | 0.23.x |

### Database
| Technology | Purpose | Version |
|------------|---------|---------|
| MySQL | Relational database | 8.0 |
| SQLAlchemy | ORM | 2.x |
| PyMySQL | MySQL driver | 1.x |

### Development Tools
| Tool | Purpose |
|------|---------|
| Git | Version control |
| GitHub | Repository hosting |
| Pre-commit | Code quality checks |
| Black | Python code formatting |
| ESLint | JavaScript linting |
| Prettier | Code formatting |
| Docker | Containerization |
| Docker Compose | Local development |

---

### System Architecture Overview

```
Users
  ↓ HTTPS
Next.js Frontend (TypeScript + Tailwind)
  ↓ REST API
FastAPI Backend
  ├── Authentication Service (JWT)
  ├── Credit Assessment Service
  ├── KYC Management Service
  ├── File Upload Service
  └── AI Processing Service (future enhancement)
  ↓
MySQL Database + File Storage (S3-ready)
```

---

### Authentication FLOW

1. User registers with email & password.
2. Password is hashed using bcrypt.
3. User logs in with credentials.
4. JWT token is generated and returned.
5. Token is used to access protected endpoints.

--- 

## API Endpoints

### Authentication

- `POST /auth/register` → Create User Account.
- `POST /auth/login` → Authenticate user & return JWT.

### KYC

- `POST /kyc/` → Submit KYC information.

Stores user identity details including:
- Name, Address, ID verification Data, Date of Birth.

### Credit Assessment

- `POST /assessment/`

Generates Credit Score based on:
- monthly income.
- monthly expense.
- existing loan.

### File Upload

- `POST /upload/` → Uploads bank statement (PDF) and stores metadata

---

## Database Design Summary

The system uses a relational MySQL Database with the following entities:

- `users`
- `kyc_records`
- `uploaded_documents`
- `credit_assessments`
- `loan_applications`
- `businesses`


### Users Table

```sql
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  INDEX idx_email (email)
);
```

```sql
CREATE TABLE kyc_records (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  
  title VARCHAR(20),
  first_name VARCHAR(100) NOT NULL,
  middle_name VARCHAR(100),
  last_name VARCHAR(100) NOT NULL,
  
  gender VARCHAR(20),
  date_of_birth DATE,
  
  mobile_number VARCHAR(20),
  address VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(100),
  country VARCHAR(100),
  postal_code VARCHAR(20),
  
  id_type VARCHAR(50),
  id_number VARCHAR(100),
  id_document_path VARCHAR(500),
  
  kyc_status VARCHAR(20) DEFAULT 'pending',
  
  submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  verified_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(id),
  INDEX idx_user_id (user_id),
  INDEX idx_kyc_status (kyc_status)
);
```

```sql
Table credit_assessments {
  id INT [pk, increment]
  user_id INT [ref: > users.id, not null]
  monthly_income DECIMAL(15,2) [not null]
  monthly_expense DECIMAL(15,2) [not null]
  existing_loans DECIMAL(15,2) [not null]
  credit_score INT [not null]
  rating VARCHAR(50) [not null]
  risk_level VARCHAR(50) [not null]
  created_at TIMESTAMP [default: `CURRENT_TIMESTAMP`]
  
  indexes {
    user_id
  }
}
```


```sql
Table uploaded_documents {
  id INT [pk, increment]
  user_id INT [ref: > users.id, not null]
  document_type VARCHAR(50) [not null]
  file_name VARCHAR(255) [not null]
  file_path VARCHAR(500) [not null]
  file_size INT [not null]
  upload_status ENUM('pending', 'completed', 'failed') [default: 'completed']
  uploaded_at TIMESTAMP [default: `CURRENT_TIMESTAMP`]
  
  indexes {
    user_id
    document_type
  }
}
```


```sql
Table loan_applications {
  id INT [pk, increment]
  user_id INT [ref: > users.id, not null]
  assessment_id INT [ref: > credit_assessments.id, null]
  amount DECIMAL(15,2) [not null]
  purpose VARCHAR(255)
  term_months INT [not null]
  application_status ENUM('pending', 'approved', 'rejected') [default: 'pending']
  created_at TIMESTAMP [default: `CURRENT_TIMESTAMP`]
  
  indexes {
    user_id
    application_status
  }
}
```

```sql
Table businesses {
  id INT [pk, increment]
  user_id INT [ref: > users.id, not null]
  business_name VARCHAR(255) [not null]
  business_type VARCHAR(100)
  registration_number VARCHAR(100) [unique]
  annual_revenue DECIMAL(15,2)
  created_at TIMESTAMP [default: `CURRENT_TIMESTAMP`]
  updated_at TIMESTAMP [default: `CURRENT_TIMESTAMP`]
  
  indexes {
    user_id
    registration_number [unique]
  }
}
```


### Data Relationship

```sql
Users (1) → (M) KYC Records
Users (1) → (M) Credit Assessments
Users (1) → (M) Uploaded Documents
Users (1) → (M) Loan Applications
Users (1) → (M) Businesses
Credit Assessments (1) → (M) Loan Applications
```
--- 

### File Storage Strategy

Bank statements and KYC documents are stored in:
- Local storage (development)
- S3-compatible storage (production)

--- 

### Security Design

- Passwords hashed using bcrypt.
- JWT authentication for protected routes.
- Dependency-based route protection (FastAPI Depends).
- Input validation via Pydantic schemas

.................................................

### Deployment Design

#### Backend Deployment

- Platform: Render
- Service: FastAPI (Uvicorn ASGI server)
- Live API URL: https://credisure-assessment-repository-backend.onrender.com
- API Documentation (Swagger): https://credisure-assessment-repository-backend.onrender.com/docs


#### Frontend Deployment
- Platform: Vercel (or planned if not yet deployed)
- Framework: Next.js (TypeScript)


#### Database Deployment
- Platform: Railway MySQL (Managed Database)
- Engine: MySQL 9.x
- Connection: Provided via Railway proxy URL
Note: Tables are auto-created via SQLAlchemy in development mode.


#### File Storage
- Current: Local server storage (/storage or /uploads inside backend project)
- Production-ready option: AWS S3 (not yet implemented)


#### Monitoring & Logging
- Current: Render logs + Uvicorn logs
- Future improvement: Sentry / CloudWatch integration (not yet configured)