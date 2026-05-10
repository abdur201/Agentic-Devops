FROM python:3.11-slim

WORKDIR /app

# Gerekli kütüphaneleri kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm kodları konteynere kopyala
COPY . .

# Sunucuyu başlat
CMD ["python", "server.py"]