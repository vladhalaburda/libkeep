# Microservices Project README

This repository contains multiple microservices built with FastAPI, Kafka, MongoDB, and Docker. The project simulates a user and book service architecture, demonstrating asynchronous interactions between services.
It`s solved task for internship in KeepSolid of Vladyslav Halaburda

## Getting Started

### Prerequisites
- Docker
- Docker Compose
- Python 3.10 (for local development if not using Docker)

### How to run

1. Building and up all containers
```bash
docker compose up --build
```
2. For each container you can use
```bash
docker compose up <SERVICE_NAME> up
```
3. And for logs checking
```bash
docker compose logs -f <SERVICE_NAME>
```
For <SERVICE_NAME> you can check compose file.

