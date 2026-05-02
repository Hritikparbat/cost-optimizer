FROM python:3.9

WORKDIR /app

COPY k8s_optimizer.py .

RUN pip install kubernetes

CMD ["python", "k8s_optimizer.py"]