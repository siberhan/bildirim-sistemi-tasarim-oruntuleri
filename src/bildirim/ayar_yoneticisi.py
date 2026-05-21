"""
Singleton tasarım örüntüsünün uygulandığı yapılandırma yöneticisi.

Eski God Class'ta SMTP, SMS ve push ayarları constructor içinde sabit
kodlanmıştı. Bu yapılandırma artık tek bir noktada toplanır ve sistemin
her yerinden aynı örneğe erişilir. Singleton burada bilinçli bir
tercihtir: yapılandırma global bir kaynaktır ve birden fazla örneğin
birbirinden farklı değerler tutması istenmeyen bir durumdur.

Singleton'ın bilinen sakıncaları (test izolasyonunu zorlaştırması,
global durum yaratması) farkındadır; bu yüzden sınıf bir `sifirla`
yöntemi sunar, böylece testler arasında temiz başlangıç sağlanabilir.
"""

from __future__ import annotations

import os
import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SmtpAyarlari:
    sunucu: str = "smtp.gmail.com"
    port: int = 587
    kullanici: str = "noreply@example.com"
    sifre: str = ""


@dataclass
class SmsAyarlari:
    api_url: str = "https://sms-saglayici.example.com/gonder"
    api_anahtari: str = ""


@dataclass
class PushAyarlari:
    uygulama_id: str = "varsayilan_uygulama"
    anahtar: str = ""


@dataclass
class LogAyarlari:
    dosya_yolu: str = "bildirimler.log"
    seviye: str = "INFO"


class AyarYoneticisi:
    """
    Tüm uygulama yapılandırmasını tek noktada toplayan Singleton sınıf.

    Aynı örneğin döndürülmesini sağlamak için __new__ üzerinden kontrol
    edilir. Thread-safe başlatma için bir kilit kullanılır.
    """

    _ornek: Optional["AyarYoneticisi"] = None
    _kilit = threading.Lock()
    _baslatildi: bool = False

    def __new__(cls) -> "AyarYoneticisi":
        if cls._ornek is None:
            with cls._kilit:
                if cls._ornek is None:
                    cls._ornek = super().__new__(cls)
        return cls._ornek

    def __init__(self) -> None:
        # Singleton olduğu için __init__ her erişimde tetiklenir;
        # değerler yalnızca ilk seferde yüklenir.
        if AyarYoneticisi._baslatildi:
            return
        self.smtp = SmtpAyarlari(
            sifre=os.environ.get("SMTP_SIFRE", "gelistirme_sifresi"),
        )
        self.sms = SmsAyarlari(
            api_anahtari=os.environ.get("SMS_API_ANAHTARI", "gelistirme_anahtari"),
        )
        self.push = PushAyarlari(
            anahtar=os.environ.get("PUSH_ANAHTARI", "gelistirme_anahtari"),
        )
        self.log = LogAyarlari()
        AyarYoneticisi._baslatildi = True

    @classmethod
    def sifirla(cls) -> None:
        """
        Testler için Singleton durumunu sıfırlar.

        Üretim kodunda kullanılmaz; yalnızca test izolasyonu için vardır.
        """
        with cls._kilit:
            cls._ornek = None
            cls._baslatildi = False

    def ozet(self) -> str:
        """Yapılandırmanın hassas olmayan özetini döndürür."""
        return (
            f"SMTP: {self.smtp.sunucu}:{self.smtp.port} "
            f"({self.smtp.kullanici}) | "
            f"SMS: {self.sms.api_url} | "
            f"Push: {self.push.uygulama_id} | "
            f"Log: {self.log.dosya_yolu} ({self.log.seviye})"
        )
