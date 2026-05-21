import time
from email.mime.text import MIMEText


class BildirimYoneticisi:
    def __init__(self):
        # SMTP ayarları - sabit kodlanmış
        self.smtp_sunucu = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_kullanici = "noreply@example.com"
        self.smtp_sifre = "gizli_sifre_123"

        # SMS sağlayıcı ayarları
        self.sms_api_url = "https://sms-saglayici.example.com/gonder"
        self.sms_api_anahtari = "abc123def456"

        # Push notification ayarları
        self.push_uygulama_id = "uygulama_123"
        self.push_anahtari = "push_key_xyz"

        # Log dosyası
        self.log_dosyasi = "bildirimler.log"

    def bildirim_gonder(self, tip, alici, mesaj, oncelik="normal"):
        # Doğrulama
        if not alici or not mesaj:
            print("HATA: Alici veya mesaj bos olamaz")
            self._log_yaz(f"HATA: Bos alici/mesaj - tip={tip}")
            return False

        if len(mesaj) > 1000:
            print("HATA: Mesaj cok uzun")
            return False

        # Tip kontrolü ve gönderim
        if tip == "email":
            if "@" not in alici or "." not in alici:
                print(f"HATA: Gecersiz email adresi: {alici}")
                return False

            if oncelik == "yuksek":
                konu = "[ÖNEMLİ] Bildirim"
            elif oncelik == "dusuk":
                konu = "Bildirim"
            else:
                konu = "Bildirim"

            try:
                msg = MIMEText(mesaj)
                msg["Subject"] = konu
                msg["From"] = self.smtp_kullanici
                msg["To"] = alici

                print(f"[EMAIL] {alici} adresine gönderiliyor...")
                print(f"  Konu: {konu}")
                print(f"  Mesaj: {mesaj}")
                time.sleep(0.1)
                print(f"[EMAIL] Gönderildi.")

                self._log_yaz(f"EMAIL gonderildi: {alici}")
                return True
            except Exception as e:
                print(f"HATA: Email gönderilemedi: {e}")
                self._log_yaz(f"EMAIL HATA: {alici} - {e}")
                return False

        elif tip == "sms":
            if not alici.startswith("+") or len(alici) < 10:
                print(f"HATA: Gecersiz telefon: {alici}")
                return False

            if len(mesaj) > 160:
                mesaj = mesaj[:157] + "..."
                print("UYARI: SMS mesajı kısaltıldı")

            try:
                print(f"[SMS] {alici} numarasına gönderiliyor...")
                print(f"  API: {self.sms_api_url}")
                print(f"  Mesaj: {mesaj}")
                time.sleep(0.1)
                print(f"[SMS] Gönderildi.")

                self._log_yaz(f"SMS gonderildi: {alici}")
                return True
            except Exception as e:
                print(f"HATA: SMS gönderilemedi: {e}")
                return False

        elif tip == "push":
            try:
                print(f"[PUSH] {alici} cihazına gönderiliyor...")
                print(f"  Uygulama: {self.push_uygulama_id}")
                print(f"  Mesaj: {mesaj}")

                if oncelik == "yuksek":
                    print("  Yüksek öncelikli - anında bildirim")

                time.sleep(0.1)
                print(f"[PUSH] Gönderildi.")

                self._log_yaz(f"PUSH gonderildi: {alici}")
                return True
            except Exception as e:
                print(f"HATA: Push gönderilemedi: {e}")
                return False

        else:
            print(f"HATA: Bilinmeyen bildirim tipi: {tip}")
            return False

    def toplu_bildirim_gonder(self, tip, aliciler, mesaj):
        basarili = 0
        basarisiz = 0
        for alici in aliciler:
            if self.bildirim_gonder(tip, alici, mesaj):
                basarili += 1
            else:
                basarisiz += 1

        print(f"Toplu gönderim tamamlandı: {basarili} basarili, {basarisiz} basarisiz")
        return basarili, basarisiz

    def _log_yaz(self, mesaj):
        zaman = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_dosyasi, "a", encoding="utf-8") as f:
            f.write(f"[{zaman}] {mesaj}\n")


if __name__ == "__main__":
    yonetici = BildirimYoneticisi()

    yonetici.bildirim_gonder("email", "ahmet@example.com", "Merhaba, hoş geldiniz!")
    yonetici.bildirim_gonder("sms", "+905551234567", "Doğrulama kodunuz: 123456")
    yonetici.bildirim_gonder("push", "cihaz_id_abc", "Yeni mesajınız var!", oncelik="yuksek")

    yonetici.toplu_bildirim_gonder(
        "email",
        ["user1@example.com", "user2@example.com", "user3@example.com"],
        "Sistem bakımı yarın 02:00'da yapılacaktır."
    )
