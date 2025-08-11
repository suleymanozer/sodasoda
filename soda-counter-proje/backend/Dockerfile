# Python'ın resmi imajını temel al
FROM python:3.9-slim

# Çalışma dizinini ayarla
WORKDIR /app

# requirements.txt dosyasını kopyala
COPY requirements.txt .

# Bağımlılıkları kur
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Konteynerin 8080 portunu dinlediğini belirt
EXPOSE 8080

# Uygulamayı başlat
# Gunicorn, Flask'ın kendi sunucusundan daha performanslıdır.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
