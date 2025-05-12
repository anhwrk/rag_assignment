# Bra Fitting Recommendation System - Technical Assessment

# Introduction
This is a solution for the bra fitting recommendation system. The system provides personalized bra fitting recommendations through an interactive interface.

# Requirements
Python 3.7+
Node.js 14+
npm/yarn
Docker

# Run backend
```
cd backend
cp .env.example .env
docker compose up --build
```

# Run frontend
```
cd frontend
cp .env.example .env
docker compose up --build
```

The application will be running at:
```
Frontend: http://localhost:3007
Backend: http://localhost:8007
```

Below is the project's feature-based directory structure, highlighting the key components of both backend API (v1) and frontend application architecture:
```
.
├── backend/
│   ├── app/
│   │   ├── v1/
│   │   │   ├── recommendation/
│   │   │   ├── bra_fitting/
│   │   │   ├── monitoring/
│   │   │   ├── auth/
│   │   │   └── __init__.py
│   │   └── __init__.py
│   └── ...
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── brafitting/
    │   │   │   ├── components/
    │   │   │   ├── validations/
    │   │   │   ├── hooks/
    │   │   │   ├── styles/
    │   │   │   ├── services/
    │   │   │   └── index.js
    │   │   └── index.js
    │   ├── common/
    │   ├── App.js
    │   └── index.js
    └── ...
```
