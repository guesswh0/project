FROM python:3.10
EXPOSE 8000
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src .
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
