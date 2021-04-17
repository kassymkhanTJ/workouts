FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY ./ /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 main:app