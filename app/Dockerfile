FROM python:3.11

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements-app.txt /app/

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements-app.txt

EXPOSE 8080

COPY ./ /app

CMD ["python", "api.py"]