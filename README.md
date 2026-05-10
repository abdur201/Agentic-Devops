🚀 Agentic DevOps: Tam Kapsamlı Kurulum Rehberi
Bu belge, Agentic DevOps ekosisteminin (AnythingLLM, Model Context Protocol, AWX ve Docker mimarisi) yepyeni bir sunucuya veya yerel makineye (Linux/WSL) sıfırdan nasıl kurulacağını adım adım açıklamaktadır.

📌 Ön Koşullar (Prerequisites)
Kuruluma başlamadan önce hedef sistemde aşağıdaki araçların kurulu ve çalışır durumda olduğundan emin olun:

Git (Projeyi indirmek için)

Docker & Docker Compose (Konteyner mimarisini ayağa kaldırmak için)

Python 3 & pip (AWX CLI aracını çalıştırmak için)

🛠️ Adım 1: Projeyi Klonlama
Öncelikle GitHub üzerindeki repository'yi hedef makineye indiriyoruz:

Bash
git clone https://github.com/abdur201/Agentic-Devops.git
cd Agentic-Devops
📦 Adım 2: AWX CLI (awxkit) Kurulumu
Kurulum sihirbazı (setup.sh), altyapı şablonlarını sisteme otomatik basabilmek için AWX'in resmi komut satırı aracına ihtiyaç duyar. Bunu Python üzerinden kuruyoruz:

Bash
sudo apt update
sudo apt install python3-pip -y
pip install awxkit
⚙️ Adım 3: Otomatik Kurulum Sihirbazı (setup.sh)
Proje, ortam değişkenlerini (.env) ve IP konfigürasyonlarını otomatik ayarlayan bir bash scripti ile gelmektedir. Sistemi başlatmak için şu komutları çalıştırın:

Bash
chmod +x setup.sh
./setup.sh
Sihirbaz Çalıştığında Ne Olacak?

Sistem sizden o anki makinenin IP adresini onaylamanızı isteyecek (Otomatik tespit edilir, Enter ile geçebilirsiniz).

AWX için belirlemek istediğiniz Kullanıcı Adı ve Şifreyi soracak.

Arka planda gizli .env dosyasını oluşturacak.

awx_infrastructure.json içindeki eski IP adreslerini bulup, girdiğiniz yeni IP ile değiştirecek.

docker-compose up -d komutunu tetikleyerek konteynerleri ayağa kaldıracak.

Konteynerler hazır olduktan sonra (yaklaşık 30 sn), projeleri, envanterleri ve job template'leri AWX API'si üzerinden içeri aktaracak (Import).

🔐 Adım 4: Manuel Güvenlik Yapılandırması (Kritik!)
Kurulum bittikten sonra projelerin, şablonların (Deploy, Stop, Delete vb.) ve envanterlerin AWX'e eksiksiz geldiğini göreceksiniz. Ancak güvenlik standartları gereği, sunuculara ait SSH şifreleri Git üzerinde taşınmaz.

Sistemin tam otonom çalışabilmesi için bir defaya mahsus şu işlemi yapmalısınız:

AWX arayüzüne giriş yapın.

Sol menüden Credentials sekmesine tıklayın.

Listeden Machine (veya sunucu SSH anahtarınızı tutan) kimlik bilgisine tıklayın ve Edit (Düzenle) deyin.

Hedef sunucularınıza bağlanmak için gereken parolayı (veya SSH Private Key'i) ilgili alana girip kaydedin.

(Varsa) Docker Hub veya Registry token'ınız için oluşturduğunuz Credential'ı da aynı şekilde güncelleyin.

🌐 Adım 5: Arayüzlere Erişim
Sistem başarıyla ayağa kalktığında servislerinize aşağıdaki adreslerden ulaşabilirsiniz:

AnythingLLM (Yapay Zeka ve Ajan Kontrol Paneli): 👉 http://<SUNUCU_IP>:3001

AWX (DevOps Altyapı ve Otomasyon Paneli): 👉 http://<SUNUCU_IP>:8080

🆘 Sorun Giderme (Troubleshooting)
Konteynerlerin Durumunu Kontrol Etmek İçin:

Bash
docker ps
Sistem Loglarını (Hataları) İncelemek İçin:

Bash
docker-compose logs -f
Sistemi Tamamen Kapatmak İçin:

Bash
docker-compose down
Ajanların (MCP Sunucusu) AWX ile Bağlantısını Test Etmek İçin:
AnythingLLM arayüzünde ilgili workspace'e giderek yapay zekaya şu komutu verin:
"Sistemdeki mevcut AWX şablonlarını listele." (Bağlantı başarılıysa Deploy, Delete, Status gibi şablonlar listelenecektir).
