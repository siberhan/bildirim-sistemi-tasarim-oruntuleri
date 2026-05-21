from __future__ import annotations
import time
from typing import Iterable, List
from ayar_yoneticisi import AyarYoneticisi
from bildirimler import BildirimHatasi, BildirimSonucu
from bildirim_fabrikasi import BildirimFabrikasi
from stratejiler import GonderimStratejisi, AnindaGonderim
from gozlemciler import Gozlemci

class BildirimYoneticisi:
    def __init__(self) -> None:
        self.ayarlar = AyarYoneticisi()
        self._gozlemciler: List[Gozlemci] = []
        self.varsayilan_strateji = AnindaGonderim()

    def gozlemci_ekle(self, gozlemci: Gozlemci) -> None:
        self._gozlemciler.append(gozlemci)

    def _gozlemcileri_haberdar_et(self, sonuc: BildirimSonucu) -> None:
        for g in self._gozlemciler:
            g.guncelle(sonuc)

    def gonder(self, tip: str, strateji: GonderimStratejisi = None, **parametreler) -> BildirimSonucu:
        aktif_strateji = strateji or self.varsayilan_strateji
        try:
            bildirim = BildirimFabrikasi.olustur(tip, **parametreler)
            sonuc = aktif_strateji.uygula(bildirim)
            self._gozlemcileri_haberdar_et(sonuc)
            return sonuc
        except BildirimHatasi as hata:
            sonuc = BildirimSonucu(False, str(hata), tip, parametreler.get("alici", "bilinmiyor"))
            self._gozlemcileri_haberdar_et(sonuc)
            return sonuc

    def toplu_gonder(self, tip: str, aliciler: Iterable[str], mesaj: str, **ekstra) -> List[BildirimSonucu]:
        return [self.gonder(tip, alici=al, mesaj=mesaj, **ekstra) for al in aliciler]

if __name__ == "__main__":
    from gozlemciler import LogGozlemcisi, AnalitikGozlemcisi
    from stratejiler import GecikmeliGonderim

    yonetici = BildirimYoneticisi()
    yonetici.gozlemci_ekle(LogGozlemcisi())
    yonetici.gozlemci_ekle(AnalitikGozlemcisi())

    print("\n--- Normal Gönderim ---")
    yonetici.gonder("email", alici="ahmet@example.com", mesaj="Merhaba!")

    print("\n--- Gecikmeli Strateji ile Gönderim ---")
    yonetici.gonder("sms", strateji=GecikmeliGonderim(1), alici="+905551234567", mesaj="Doğrulama: 123")
