"""
Bildirim sisteminin dışarıya açık yüzü.

Eski sürümde bu sınıf bir "God Class"tı: SMTP ayarları, doğrulama, tip
seçimi, gönderim ve loglama hepsi bu dosyadaydı. Faz 1 sonunda bu sınıf,
ince bir koordinatöre dönüştürülmüştür. Artık:

- Nesne yaratma sorumluluğu `BildirimFabrikasi`'na devredilmiştir.
- Konfigürasyon `AyarYoneticisi` (Singleton) üzerinden okunur.
- Gönderim mantığı her `Bildirim` alt sınıfının kendi içindedir.
- Bu sınıfın tek görevi: fabrikayı kullanarak nesneyi üretmek, gönderim
  sonucunu toplamak ve loglamak.

if-elif zinciri tamamen kaldırılmıştır; yeni bir bildirim tipi eklemek
bu dosyaya tek bir satır bile dokunmayı gerektirmez (OCP).
"""

from __future__ import annotations

import time
from typing import Iterable, List

from .ayar_yoneticisi import AyarYoneticisi
from .bildirimler import BildirimHatasi, BildirimSonucu
from .bildirim_fabrikasi import BildirimFabrikasi


class BildirimYoneticisi:
    """Bildirim oluşturma ve gönderim akışını koordine eden ince sınıf."""

    def __init__(self) -> None:
        self.ayarlar = AyarYoneticisi()

    def gonder(self, tip: str, **parametreler) -> BildirimSonucu:
        """
        Tek bir bildirim gönderir.

        :param tip: Fabrikada kayıtlı tip adı (örn. 'email', 'sms', 'push').
        :param parametreler: İlgili bildirim sınıfının ihtiyaç duyduğu
                             alıcı, mesaj, öncelik vb. anahtar-değer çiftleri.
        """
        try:
            bildirim = BildirimFabrikasi.olustur(tip, **parametreler)
            sonuc = bildirim.gonder()
            self._log_yaz(
                f"BAŞARILI - {sonuc.bildirim_tipi} - {sonuc.alici} - {sonuc.detay}"
            )
            return sonuc
        except BildirimHatasi as hata:
            self._log_yaz(f"HATA - {tip} - {hata}")
            return BildirimSonucu(
                basarili=False,
                detay=str(hata),
                bildirim_tipi=tip,
                alici=parametreler.get("alici", "bilinmiyor"),
            )

    def toplu_gonder(
        self, tip: str, aliciler: Iterable[str], mesaj: str, **ekstra
    ) -> List[BildirimSonucu]:
        """Aynı tipte birden fazla alıcıya bildirim gönderir."""
        sonuclar: List[BildirimSonucu] = []
        for alici in aliciler:
            sonuc = self.gonder(tip, alici=alici, mesaj=mesaj, **ekstra)
            sonuclar.append(sonuc)
        basarili = sum(1 for s in sonuclar if s.basarili)
        print(
            f"Toplu gönderim tamamlandı: {basarili} başarılı, "
            f"{len(sonuclar) - basarili} başarısız"
        )
        return sonuclar

    def _log_yaz(self, mesaj: str) -> None:
        zaman = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.ayarlar.log.dosya_yolu, "a", encoding="utf-8") as f:
            f.write(f"[{zaman}] {mesaj}\n")


if __name__ == "__main__":
    yonetici = BildirimYoneticisi()

    yonetici.gonder("email", alici="ahmet@example.com", mesaj="Merhaba, hoş geldiniz!")
    yonetici.gonder(
        "sms", alici="+905551234567", mesaj="Doğrulama kodunuz: 123456"
    )
    yonetici.gonder(
        "push",
        alici="cihaz_id_abc",
        mesaj="Yeni mesajınız var!",
        oncelik="yuksek",
    )

    yonetici.toplu_gonder(
        "email",
        ["user1@example.com", "user2@example.com", "user3@example.com"],
        "Sistem bakımı yarın 02:00'da yapılacaktır.",
    )
