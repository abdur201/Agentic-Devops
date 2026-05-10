#!/bin/bash

# --- RENKLER VE GÖRSEL ---
GREEN='\033[0;32m'
NC='\033[0m' # No Color
echo -e "${GREEN}"
echo "#############################################"
echo "#    AGENTIC DEVOPS - KURULUM SİHİRBAZI     #"
echo "#############################################"
echo -e "${NC}"

# 1. IP ADRESLERİNİ YÖNET
ESKI_IP="172.31.186.158"
OTOMATIK_IP=$(hostname -I | awk '{print $1}')

read -p "Sistemin çalışacağı yeni IP adresi [$OTOMATIK_IP]: " YENI_IP
YENI_IP=${YENI_IP:-$OTOMATIK_IP}

# 2. AWX BİLGİLERİNİ AL
read -p "AWX Kullanıcı Adı [admin]: " AWX_USER
AWX_USER=${AWX_USER:-admin}

read -sp "AWX Şifresi: " AWX_PASS
echo ""

# 3. .env DOSYASINI OLUŞTUR (Hassas Veriler Burada)
echo "--- .env dosyası oluşturuluyor..."
cat <<EOF > .env
AWX_BASE_URL=http://$YENI_IP:8080
AWX_USER=$AWX_USER
AWX_PASS=$AWX_PASS
AWX_DEPLOY_ID=7
AWX_STATUS_ID=9
AWX_STOP_ID=10
AWX_DELETE_ID=8
EOF

# 4. JSON DOSYASINDAKİ IP'LERİ GÜNCELLE (Sihirli Dokunuş)
echo "--- Altyapı dosyasındaki IP adresleri güncelleniyor ($ESKI_IP -> $YENI_IP)..."
sed -i "s/$ESKI_IP/$YENI_IP/g" awx_infrastructure.json

# 5. DOCKER SİSTEMİNİ BAŞLAT
echo "--- Docker konteynerleri ayağa kaldırılıyor..."
docker-compose up -d

echo -e "${GREEN}"
echo "------------------------------------------------------"
echo "Kurulum Tamamlandı! "
echo "AnythingLLM Arayüzü: http://$YENI_IP:3001"
echo "AWX Arayüzü: http://$YENI_IP:8080"
echo "------------------------------------------------------"
echo -e "${NC}"
# 6. AWX ALTYAPISINI İÇERİ AKTAR (IMPORT)
echo "--- AWX API'sinin hazır olması bekleniyor (30 saniye)..."
sleep 30 # AWX konteynerlerinin tam ayağa kalkması için süre tanıyoruz

echo "--- AWX Projeleri, Şablonları ve Envanterleri yükleniyor..."
TOWER_HOST="http://$YENI_IP:8080" TOWER_USERNAME="$AWX_USER" TOWER_PASSWORD="$AWX_PASS" awx import < awx_infrastructure.json
