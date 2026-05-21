from abc import ABC, abstractmethod
import time
from bildirimler import Bildirim, BildirimSonucu

class GonderimStratejisi(ABC):
    @abstractmethod
    def uygula(self, bildirim: Bildirim) -> BildirimSonucu:
        pass

class AnindaGonderim(GonderimStratejisi):
    def uygula(self, bildirim: Bildirim) -> BildirimSonucu:
        return bildirim.gonder()

class GecikmeliGonderim(GonderimStratejisi):
    def __init__(self, gecikme_sn: int = 1):
        self.gecikme_sn = gecikme_sn

    def uygula(self, bildirim: Bildirim) -> BildirimSonucu:
        print(f"[STRATEJİ] {self.gecikme_sn} saniye gecikme uygulanıyor...")
        time.sleep(self.gecikme_sn)
        return bildirim.gonder()
