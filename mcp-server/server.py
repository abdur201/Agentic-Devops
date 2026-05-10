import sys
import json
import requests
import base64
import time
from mcp.server.fastmcp import FastMCP

# Logları anlık görmek için
sys.stderr = open("mcp_debug.log", "w", encoding="utf-8")

mcp = FastMCP("masaustu-mcp")

# --- AYARLAR ---
# Artık değerleri .env dosyasından okuyoruz. Bulamazsa varsayılanları kullanır.
AWX_BASE_URL = os.getenv("AWX_BASE_URL", "http://172.31.186.158:8080")
AWX_USER = os.getenv("AWX_USER", "admin")
AWX_PASS = os.getenv("AWX_PASS", "12332145") 

TEMPLATE_IDS = {
    "deploy": "7",
    "status": "9",   # tabloyu getirecek olan ID
    "stop": "10",    # Sadece durdurma yapacak ID
    "delete": "8"    # Sadece silme yapacak ID
}

def get_auth():
    auth_str = f"{AWX_USER}:{AWX_PASS}"
    encoded = base64.b64encode(auth_str.encode()).decode()
    return {
        "Authorization": f"Basic {encoded}", 
        "Content-Type": "application/json"
    }

def wait_for_result(job_id: int):
    """İşlem bitene kadar bekler, logu çeker ve LLM için temizler."""
    status_url = f"{AWX_BASE_URL}/api/v2/jobs/{job_id}/"
    log_url = f"{AWX_BASE_URL}/api/v2/jobs/{job_id}/stdout/?format=txt"
    
    for _ in range(20): # Max 40 saniye bekle
        try:
            r = requests.get(status_url, headers=get_auth(), verify=False, timeout=10)
            job_status = r.json().get("status")
            
            if job_status in ["successful", "failed", "error"]:
                # Logların API'ye tam yansıması için 2 saniye nefes payı
                time.sleep(2) 
                
                log_r = requests.get(log_url, headers=get_auth(), verify=False, timeout=10)
                raw_log = log_r.text
                
                # LLM'in kafasını karıştıran gereksiz Ansible yazılarını temizle
                clean_log = ""
                capture = False
                for line in raw_log.split('\n'):
                    # Sadece hata veya debug mesajlarını (bizim json formatlı sonucumuzu) al
                    if "Sonucu AWX Loglarına" in line or "fatal:" in line or "msg\":" in line or "ok: [" in line and "=>" in line:
                        capture = True
                    if capture:
                        clean_log += line + "\n"
                
                # Temizleyici işe yaramazsa ham logu dön
                final_output = clean_log if clean_log.strip() else raw_log
                return f"Durum: {job_status.upper()}\nLog Çıktısı:\n{final_output.strip()}"
                
        except Exception as e:
            return f"Log kontrolü sırasında hata: {str(e)}"
            
        time.sleep(2)
        
    return "İşlem zaman aşımına uğradı (40sn), AWX üzerinden kontrol edin."

# --- TOOL 1: DEPLOY ---
@mcp.tool()
def deploy_project() -> str:
    """Yeni bir Docker konteyneri deploy eder."""
    url = f"{AWX_BASE_URL}/api/v2/job_templates/{TEMPLATE_IDS['deploy']}/launch/"
    try:
        r = requests.post(url, headers=get_auth(), json={}, verify=False, timeout=10)
        if r.status_code in (200, 201, 202):
            job_id = r.json().get('id')
            sonuc = wait_for_result(job_id)
            return f"--- DEPLOY İŞLEMİ SONUCU (Job ID: {job_id}) ---\n{sonuc}"
        return f"Hata: {r.status_code} - {r.text}"
    except Exception as e:
        return f"İstisna Hatası: {str(e)}"

# --- TOOL 2: STATUS (PS) ---
@mcp.tool()
def get_container_status() -> str:
    """Çalışan veya duran test konteynerlarının tablosunu getirir."""
    url = f"{AWX_BASE_URL}/api/v2/job_templates/{TEMPLATE_IDS['status']}/launch/"
    try:
        r = requests.post(url, headers=get_auth(), json={}, verify=False, timeout=10)
        if r.status_code in (200, 201, 202):
            job_id = r.json().get("id")
            sonuc = wait_for_result(job_id)
            return f"--- STATUS İŞLEMİ SONUCU (Job ID: {job_id}) ---\n{sonuc}"
        return f"Hata: {r.status_code} - {r.text}"
    except Exception as e:
        return f"İstisna Hatası: {str(e)}"

# --- TOOL 3: STOP ---
@mcp.tool()
def stop_container(container_id: str = "all") -> str:
    """
    Belirli bir konteyneri (ID ile) veya 'all' diyerek hepsini durdurur.
    Örnek: container_id='e4b3a2c1' veya container_id='all'
    """
    url = f"{AWX_BASE_URL}/api/v2/job_templates/{TEMPLATE_IDS['stop']}/launch/"
    payload = {"extra_vars": {"target_container": container_id}}
    
    try:
        r = requests.post(url, headers=get_auth(), json=payload, verify=False, timeout=10)
        if r.status_code in (200, 201, 202):
            job_id = r.json().get("id")
            sonuc = wait_for_result(job_id)
            return f"--- STOP İŞLEMİ SONUCU (Job ID: {job_id}) ---\n{sonuc}"
        return f"Hata: {r.status_code} - {r.text}"
    except Exception as e:
        return f"İstisna Hatası: {str(e)}"

# --- TOOL 4: DELETE ---
@mcp.tool()
def delete_container(container_id: str = "all") -> str:
    """
    Belirli bir konteyneri (ID ile) veya 'all' diyerek hepsini sistemden zorla siler.
    """
    url = f"{AWX_BASE_URL}/api/v2/job_templates/{TEMPLATE_IDS['delete']}/launch/"
    payload = {"extra_vars": {"target_container": container_id}}
    
    try:
        r = requests.post(url, headers=get_auth(), json=payload, verify=False, timeout=10)
        if r.status_code in (200, 201, 202):
            job_id = r.json().get("id")
            sonuc = wait_for_result(job_id)
            return f"--- DELETE İŞLEMİ SONUCU (Job ID: {job_id}) ---\n{sonuc}"
        return f"Hata: {r.status_code} - {r.text}"
    except Exception as e:
        return f"İstisna Hatası: {str(e)}"

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    mcp.run(transport="stdio")
