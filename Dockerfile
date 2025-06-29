FROM python:3.10.17-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1

COPY . .

CMD ["python", "bot.py"]
