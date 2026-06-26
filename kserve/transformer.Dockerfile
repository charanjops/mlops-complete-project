FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY kserve/transformer.py .
ENTRYPOINT ["python", "transformer.py"]
