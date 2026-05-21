"""
Adapter (Adaptör) tasarım örüntüsü uygulaması.
Dış dünyadan gelen, kendi arayüzümüze uymayan sınıfları (Adaptee),
sistemimizin beklediği arayüze (Bildirim) çevirir.
"""
from __future__ import annotations
import time
from bildirimler import Bildirim, BildirimSonucu, BildirimHatasi

class EskiSistemSmsSaglayici:
    """Dış dünyanın karmaşık/eski arayüzü. Bizim sistemimizle uyumsuz."""
    def send_message_to_target(self, target_phone: str, msg_body: str, api_key: str) -> bool:
        print(f"[HARİCİ SMS API] Bağlantı kuruluyor...")
        time.sleep(0.2)
        if not target_phone or not msg_body:
            return False
        print(f"[HARİCİ SMS API] Mesaj iletildi: {target_phone} -> {msg_body}")
        return True

class HariciSmsAdaptoru(Bildirim):
    """Dış sistemi bizim Bildirim arayüzümüze uyduran adaptör."""
    def __init__(self, alici: str, mesaj: str, oncelik: str = "normal") -> None:
        super().__init__(alici, mesaj, oncelik)
        self._harici_servis = EskiSistemSmsSaglayici()
        self._api_key = "gizli_api_anahtari_123"

    @property
    def tip_adi(self) -> str:
        return "harici_sms"

    def gonder(self) -> BildirimSonucu:
        try:
            basarili = self._harici_servis.send_message_to_target(
                target_phone=self.alici,
                msg_body=self.mesaj,
                api_key=self._api_key
            )
            if basarili:
                return BildirimSonucu(True, "Harici API üzerinden gönderildi", self.tip_adi, self.alici)
            else:
                raise BildirimHatasi("Harici API reddetti.")
        except Exception as e:
            raise BildirimHatasi(f"Harici adaptör hatası: {e}")
