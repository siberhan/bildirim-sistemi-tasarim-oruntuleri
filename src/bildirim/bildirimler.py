"""
Bildirim soyut sınıfı ve somut bildirim tipleri.

Bu modül, eski God Class'taki if-elif zincirinin yerine geçen polimorfik
yapıyı kurar. Her bildirim tipi kendi gonder davranışını bilir; çağıran
kod artık tip sormaz, sadece Bildirim arayüzüne göre konuşur.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from email.mime.text import MIMEText
from typing import Optional


class BildirimHatasi(Exception):
    """Bildirim gönderimi sırasında oluşan hataların ortak temeli."""


class GecersizAliciHatasi(BildirimHatasi):
    """Alıcı bilgisi geçersiz format veya boş."""


class GecersizMesajHatasi(BildirimHatasi):
    """Mesaj boş, çok uzun veya formatına uymuyor."""


class GonderimHatasi(BildirimHatasi):
    """Sağlayıcıyla iletişimde oluşan hata (ağ, kimlik doğrulama vb.)."""


@dataclass(frozen=True)
class BildirimSonucu:
    """Bir bildirim girişiminin sonucunu temsil eder."""
    basarili: bool
    detay: str
    bildirim_tipi: str
    alici: str


class Bildirim(ABC):
    """
    Tüm bildirim tiplerinin türediği soyut taban sınıf.

    Her somut alt sınıf kendi gonder davranışını uygular. Çağıran kod bu
    sınıfla konuşur; hangi somut tipin geldiğini bilmek zorunda değildir.
    """

    def __init__(self, alici: str, mesaj: str, oncelik: str = "normal") -> None:
        self.alici = alici
        self.mesaj = mesaj
        self.oncelik = oncelik
        self._dogrula_ortak()

    def _dogrula_ortak(self) -> None:
        """Tüm bildirim tipleri için geçerli olan temel doğrulamalar."""
        if not self.alici:
            raise GecersizAliciHatasi("Alıcı boş olamaz.")
        if not self.mesaj:
            raise GecersizMesajHatasi("Mesaj boş olamaz.")
        if len(self.mesaj) > 1000:
            raise GecersizMesajHatasi("Mesaj 1000 karakteri aşamaz.")

    @abstractmethod
    def gonder(self) -> BildirimSonucu:
        """Bildirimi gönderir; alt sınıflar uygular."""

    @property
    @abstractmethod
    def tip_adi(self) -> str:
        """İnsan tarafından okunabilir tip adı (örn. 'email', 'sms')."""


class EmailBildirimi(Bildirim):
    """E-posta bildirimi: SMTP üzerinden gönderim simülasyonu."""

    def __init__(
        self,
        alici: str,
        mesaj: str,
        oncelik: str = "normal",
        gonderen: str = "noreply@example.com",
    ) -> None:
        super().__init__(alici, mesaj, oncelik)
        self._dogrula_email()
        self.gonderen = gonderen

    def _dogrula_email(self) -> None:
        if "@" not in self.alici or "." not in self.alici:
            raise GecersizAliciHatasi(f"Geçersiz e-posta adresi: {self.alici}")

    @property
    def tip_adi(self) -> str:
        return "email"

    def _konu_belirle(self) -> str:
        return "[ÖNEMLİ] Bildirim" if self.oncelik == "yuksek" else "Bildirim"

    def gonder(self) -> BildirimSonucu:
        try:
            msg = MIMEText(self.mesaj)
            msg["Subject"] = self._konu_belirle()
            msg["From"] = self.gonderen
            msg["To"] = self.alici

            print(f"[EMAIL] {self.alici} adresine gönderiliyor...")
            print(f"  Konu: {msg['Subject']}")
            print(f"  Mesaj: {self.mesaj}")
            time.sleep(0.1)
            print(f"[EMAIL] Gönderildi.")

            return BildirimSonucu(
                basarili=True,
                detay="SMTP üzerinden başarıyla iletildi.",
                bildirim_tipi=self.tip_adi,
                alici=self.alici,
            )
        except Exception as exc:
            raise GonderimHatasi(f"E-posta gönderilemedi: {exc}") from exc


class SmsBildirimi(Bildirim):
    """SMS bildirimi: harici sağlayıcı simülasyonu."""

    MAX_KARAKTER = 160

    def __init__(self, alici: str, mesaj: str, oncelik: str = "normal") -> None:
        super().__init__(alici, mesaj, oncelik)
        self._dogrula_telefon()
        if len(self.mesaj) > self.MAX_KARAKTER:
            self.mesaj = self.mesaj[: self.MAX_KARAKTER - 3] + "..."

    def _dogrula_telefon(self) -> None:
        if not self.alici.startswith("+") or len(self.alici) < 10:
            raise GecersizAliciHatasi(f"Geçersiz telefon numarası: {self.alici}")

    @property
    def tip_adi(self) -> str:
        return "sms"

    def gonder(self) -> BildirimSonucu:
        try:
            print(f"[SMS] {self.alici} numarasına gönderiliyor...")
            print(f"  Mesaj: {self.mesaj}")
            time.sleep(0.1)
            print(f"[SMS] Gönderildi.")
            return BildirimSonucu(
                basarili=True,
                detay="SMS sağlayıcısı üzerinden iletildi.",
                bildirim_tipi=self.tip_adi,
                alici=self.alici,
            )
        except Exception as exc:
            raise GonderimHatasi(f"SMS gönderilemedi: {exc}") from exc


class PushBildirimi(Bildirim):
    """Mobil push bildirimi: uygulama içi anlık bildirim simülasyonu."""

    def __init__(
        self,
        alici: str,
        mesaj: str,
        oncelik: str = "normal",
        uygulama_id: Optional[str] = None,
    ) -> None:
        super().__init__(alici, mesaj, oncelik)
        self.uygulama_id = uygulama_id or "varsayilan_uygulama"

    @property
    def tip_adi(self) -> str:
        return "push"

    def gonder(self) -> BildirimSonucu:
        try:
            print(f"[PUSH] {self.alici} cihazına gönderiliyor...")
            print(f"  Uygulama: {self.uygulama_id}")
            print(f"  Mesaj: {self.mesaj}")
            if self.oncelik == "yuksek":
                print("  Yüksek öncelikli - anında bildirim")
            time.sleep(0.1)
            print(f"[PUSH] Gönderildi.")
            return BildirimSonucu(
                basarili=True,
                detay="Push servisi üzerinden iletildi.",
                bildirim_tipi=self.tip_adi,
                alici=self.alici,
            )
        except Exception as exc:
            raise GonderimHatasi(f"Push bildirimi gönderilemedi: {exc}") from exc
