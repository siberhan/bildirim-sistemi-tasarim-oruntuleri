from abc import ABC, abstractmethod

from bildirimler import BildirimSonucu


class Gozlemci(ABC):
    @abstractmethod
    def guncelle(self, sonuc: BildirimSonucu) -> None:
        pass


class LogGozlemcisi(Gozlemci):
    def guncelle(self, sonuc: BildirimSonucu) -> None:
        durum = "BAŞARILI" if sonuc.basarili else "BAŞARISIZ"
        print(
            f"[GÖZLEMCİ - LOG] {durum} | Tip: {sonuc.bildirim_tipi} | Alıcı: {sonuc.alici}"
        )


class AnalitikGozlemcisi(Gozlemci):
    def guncelle(self, sonuc: BildirimSonucu) -> None:
        if sonuc.basarili:
            print(f"[GÖZLEMCİ - ANALİTİK] Metrik arttırıldı: {sonuc.bildirim_tipi}")
