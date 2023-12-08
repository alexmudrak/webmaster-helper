# Stage 1: Build backend service
FROM python:3.11 AS backend

WORKDIR /backend

COPY requirements.txt /backend/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
RUN playwright install chromium
RUN playwright install-deps chromium

# Stage 2: Build frontend service
FROM node:18 AS frontend

WORKDIR /frontend

COPY ui/package*.json ./
RUN npm install

COPY ui/ .

# Stage 3: Build nginx
FROM nginx:latest AS production

WORKDIR /www
