# Pizza Ordering API

This project is a simple FastAPI-based API for ordering pizzas. It allows users to create, retrieve, update, and delete pizza orders.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Docker (if running in a container)

You can install the required dependencies using:

```bash
pip install -r requirements.txt

#build docker image
docker build -t pizza-ordering-api .

#run docker container
docker run -d -p 8000:8000 pizza-ordering-api




