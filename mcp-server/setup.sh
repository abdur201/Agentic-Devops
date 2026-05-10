#!/bin/bash

echo "🚀 Otonom DevOps Sistemine Hoş Geldiniz!"
echo "Lütfen kurulum için gerekli bilgileri girin:"

# Kullanıcıdan bilgileri alma
read -p "AWX Sunucu IP ve Portu [http://172.31.186.158:8080]: " awx_url
awx_url=${awx_url:-http://172.31.186.158:8080}

read -p "AWX Kullanıcı Adı [admin]: " awx_user
awx_user=${awx_user:-admin}

read -sp "AWX Şifresi: " awx_pass
echo "" # Şifre girişinden sonra alt satıra geçmek için

# .env dosyasını oluşturma
echo "AWX_BASE_URL=$awx_url" > .env
echo "AWX_USER=$awx_user" >> .env
echo "AWX_PASS=$awx_pass" >> .env

# Gelecekte AWX API üzerinden Job oluşturma komutları buraya eklenecek
# Şimdilik sadece ID'leri .env dosyasına yazalım
echo "AWX_DEPLOY_ID=7" >> .env
echo "AWX_STATUS_ID=9" >> .env
echo "AWX_STOP_ID=10" >> .env
echo "AWX_DELETE_ID=8" >> .env

echo "✅ .env dosyası güvenle oluşturuldu!"
echo "Sistemi başlatmak için: docker-compose up -d"
