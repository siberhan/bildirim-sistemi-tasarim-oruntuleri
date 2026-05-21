"""
Factory Method örüntüsünün uygulandığı bildirim fabrikası.

Bu modül, bildirim oluşturma sorumluluğunu çağrı kodundan ayırır. Çağıran
kod yalnızca bir tip adı (örn. "email") ve gerekli parametreleri verir;
hangi somut sınıfın örneklendiği bilgisini bilmez.

Klasik Factory Method'un bir adım ötesine geçilmiştir: fabrika, sabit bir
if-elif zinciri içermez. Bunun yerine bir kayıt mekanizması (registry)
tutar ve yeni bildirim tipleri çalışma zamanında kaydedilebilir. Bu
sayede yeni bir tip eklemek için fabrika kodunu değiştirmek gerekmez —
yalnızca yeni sınıf yazılır ve fabrikaya kaydedilir. Açık/Kapalı
Prensibi (OCP) tam olarak bu noktada uygulanmış olur.
"""

from __future__ import annotations

from typing import Dict, Type

from .bildirimler import (
    Bildirim,
    EmailBildirimi,
    PushBildirimi,
    SmsBildirimi,
)


class BilinmeyenBildirimTipiHatasi(Exception):
    """Fabrikada kayıtlı olmayan bir tip istendiğinde fırlatılır."""


class BildirimFabrikasi:
    """
    Bildirim nesnelerini üreten merkezi fabrika.

    Tipler `kaydet` yöntemiyle sınıfa bağlanır. `olustur` çağrıldığında
    fabrika, istenen tipi kayıt defterinden bulup uygun sınıfı örnekler.
    """

    _kayit: Dict[str, Type[Bildirim]] = {}

    @classmethod
    def kaydet(cls, tip_adi: str, sinif: Type[Bildirim]) -> None:
        """Yeni bir bildirim tipini fabrikaya kaydeder."""
        if not issubclass(sinif, Bildirim):
            raise TypeError(
                f"{sinif.__name__} Bildirim sınıfından türetilmelidir."
            )
        cls._kayit[tip_adi.lower()] = sinif

    @classmethod
    def kayitli_tipler(cls) -> list[str]:
        """Şu anda kayıtlı olan tüm tip adlarını döndürür."""
        return sorted(cls._kayit.keys())

    @classmethod
    def olustur(cls, tip_adi: str, **parametreler) -> Bildirim:
        """
        Verilen tip adına karşılık gelen bildirim nesnesini üretir.

        :param tip_adi: Kayıtlı tip anahtarı (örn. 'email', 'sms', 'push').
        :param parametreler: İlgili sınıfın constructor'ına aktarılacak
                             anahtar-değer çiftleri.
        :raises BilinmeyenBildirimTipiHatasi: Tip kayıtlı değilse.
        """
        anahtar = tip_adi.lower()
        if anahtar not in cls._kayit:
            raise BilinmeyenBildirimTipiHatasi(
                f"'{tip_adi}' tipi tanımlı değil. "
                f"Kayıtlı tipler: {cls.kayitli_tipler()}"
            )
        sinif = cls._kayit[anahtar]
        return sinif(**parametreler)


# Sistemin başlangıcında varsayılan tipleri kaydet.
BildirimFabrikasi.kaydet("email", EmailBildirimi)
BildirimFabrikasi.kaydet("sms", SmsBildirimi)
BildirimFabrikasi.kaydet("push", PushBildirimi)
