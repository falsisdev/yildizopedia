FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Bağımlılıkları yükle (Katman önbelleklemesi)
COPY bot/requirements.txt /app/bot/requirements.txt
RUN pip install --no-cache-dir -r /app/bot/requirements.txt

# Proje dosyalarını kopyala
COPY . /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python", "-m", "bot.main"]
