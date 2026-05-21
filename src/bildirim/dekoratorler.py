"""
Decorator (Dekoratör) tasarım örüntüsü uygulaması.

Mevcut Bildirim sınıflarına (Email, SMS, Push) dokunmadan,
onlara çalışma zamanında (runtime) yeni yetenekler (yeniden deneme,
maskeleme vb.) kazandırmamızı sağlar. Açık/Kapalı Prensibini (OCP)
davranış ekleme yönünden destekler.
"""
from __future__ import annotations
import time
from bildirimler import Bildirim, BildirimSonucu, BildirimHatasi

class BildirimDekoratoru(Bildirim):
    """
    Tüm dekoratörlerin türediği temel soyut sınıf.
    Kendiside bir 'Bildirim'dir, ancak içinde sarmaladığı (wrapped)
    başka bir 'Bildirim' nesnesi taşır. Çağrıları önce ona iletir.
    """
    def __init__(self, sarmalanan_bildirim: Bildirim) -> None:
        # Temel özellikleri asıl nesneden kopyalıyoruz
        super().__init__(
            alici=sarmalanan_bildirim.alici,
            mesaj=sarmalanan_bildirim.mesaj,
            oncelik=sarmalanan_bildirim.oncelik
        )
        self._sarmalanan = sarmalanan_bildirim

    @property
    def tip_adi(self) -> str:
        # Asıl nesnenin tip adını koru
        return self._sarmalanan.tip_adi

    def gonder(self) -> BildirimSonucu:
        # Varsayılan davranış: hiçbir şey yapmadan çağrıyı asıl nesneye ilet
        return self._sarmalanan.gonder()


class TekrarDenemeDekoratoru(BildirimDekoratoru):
    """Ağ hatası gibi durumlarda gönderimi belirli sayıda tekrar dener."""

    def __init__(self, sarmalanan_bildirim: Bildirim, max_deneme: int = 3, bekleme_sn: float = 1.0) -> None:
        super().__init__(sarmalanan_bildirim)
        self.max_deneme = max_deneme
        self.bekleme_sn = bekleme_sn

    def gonder(self) -> BildirimSonucu:
        son_hata = None
        for deneme in range(1, self.max_deneme + 1):
            try:
                if deneme > 1:
                    print(f"[{self.tip_adi.upper()} DEKORATÖRÜ] {deneme}. deneme yapılıyor...")

                # Asıl nesnenin gonder metodunu çağırıyoruz
                sonuc = self._sarmalanan.gonder()

                if deneme > 1:
                    # Eğer retry ile başarılı olduysa sonuca not düşelim
                    return BildirimSonucu(
                        basarili=sonuc.basarili,
                        detay=f"{sonuc.detay} ({deneme}. denemede başarılı oldu)",
                        bildirim_tipi=sonuc.bildirim_tipi,
                        alici=sonuc.alici
                    )
                return sonuc

            except BildirimHatasi as hata:
                son_hata = hata
                print(f"[{self.tip_adi.upper()} DEKORATÖRÜ] Gönderim hatası: {hata}. Kalan deneme: {self.max_deneme - deneme}")
                if deneme < self.max_deneme:
                    time.sleep(self.bekleme_sn)

        # Tüm denemeler bittiyse ve hala başarısızsa, asıl hatayı fırlat
        raise son_hata


class MaskelemeDekoratoru(BildirimDekoratoru):
    """
    Sistem güvenliği için mesaj içeriğindeki olası hassas verileri
    maskeler. Temel bir güvenlik katmanıdır.
    """

    def gonder(self) -> BildirimSonucu:
        orijinal_mesaj = self._sarmalanan.mesaj

        # Basit bir simülasyon: mesajda "şifre" veya "kod" geçiyorsa içeriği maskele
        if "şifre:" in orijinal_mesaj.lower() or "kod:" in orijinal_mesaj.lower():
            print(f"[{self.tip_adi.upper()} DEKORATÖRÜ] Güvenlik uyarısı: Hassas veri tespit edildi, maskeleniyor...")
            self._sarmalanan.mesaj = "******** (Güvenlik gereği maskelendi)"

        # Maskelenmiş (veya orijinal) mesajla gönderimi yap
        sonuc = self._sarmalanan.gonder()

        # Orijinal nesnenin mesajını eski haline getir ki sistemde kalıcı yan etki (side-effect) bırakmasın
        self._sarmalanan.mesaj = orijinal_mesaj

        return sonuc
