# Faz 1 — AI Etkileşim Günlüğü

## Faz 0 Hazırlık Etkileşimi

**Sorduğum prompt:**
"Bu kodda hangi tasarım sorunlarını görüyorsun? Hangi tasarım örüntüleri
bu sorunları çözebilir? Her sorun için kısa bir açıklama yaz."

**AI'ın yanıtı (özet):**
AI, kodda 8-9 farklı sorun tespit etti: if-elif zinciri (OCP ihlali),
God Class yapısı (SRP ihlali), sabit kodlanmış sırlar, yetersiz hata
yönetimi (sadece boolean ve print), bildirim "nesnesi" kavramının
yokluğu, sıkı bağımlılıklar (test edilemezlik), toplu gönderimin
bağımsız bir strateji olarak görülmemesi, loglamanın sınıfa gömülü
olması ve doğrulama ile gönderim mantığının iç içe geçmiş olması.

**Kendi değerlendirmem:**
AI'ın listesi benim PROBLEMS.md'deki 6 sorunla büyük ölçüde örtüştü.
Atladığım bir nokta logger'ın metod içinde dosyayı her seferinde açıp
kapatması ve toplu gönderimin aslında ayrı bir strateji olduğuydu.
Bunları PROBLEMS.md'ye karşılaştırma bölümünde not ettim. AI'ın
"yapılandırma davranışla iç içe" eleştirisi ise Faz 0 için bence biraz
fazla detaydı; bu zaten Faz 1'de Singleton ile çözülecek bir konu.

---

## Faz 1 — Örüntü Seçimi Tartışması

**Sorduğum prompt:**
"Bildirim sistemi için Creational kategoriden hangi örüntüleri seçmem
mantıklı? Factory Method ve Abstract Factory'nin farkını bu projede
nasıl ayırt ederim?"

**AI'ın yanıtı (özet):**
AI, Factory Method'un tek bir nesne ailesi için yeterli olacağını;
Abstract Factory'nin ise birden fazla ilişkili ürün ailesi (örneğin
"kurumsal email + kurumsal SMS + kurumsal push" vs "kişisel" varyant)
gerektiğinde anlamlı olacağını söyledi. Mevcut proje yalnızca tek bir
bildirim ailesiyle çalıştığı için Abstract Factory'nin erken bir
optimizasyon olacağını belirtti. Singleton için yapılandırma yönetiminin
meşru bir kullanım alanı olduğunu, ancak test izolasyonu zorluğu
nedeniyle "kaçış kapısı" (reset metodu) eklenmesini önerdi.

**Kendi değerlendirmem:**
AI'ın Factory Method önerisini kabul ettim, ancak fabrikanın kendi
içinde de bir if-elif olmasının yine OCP'yi kırdığını fark ettim ve
AI'a "fabrika içindeki if-elif nasıl önlenir" diye tekrar sordum.

---

## Faz 1 — Fabrika Tasarım Sorusu

**Sorduğum prompt:**
"Factory Method uygulasam bile fabrika sınıfının kendi içinde 'tip
email ise EmailBildirimi döndür' gibi bir zincir oluyor. Bu da OCP
ihlali değil mi? Nasıl çözebilirim?"

**AI'ın yanıtı (özet):**
AI, "registry pattern" (kayıt mekanizması) yaklaşımını önerdi: fabrika
somut sınıfları doğrudan bilmek yerine bir sözlük tutar; yeni sınıflar
çalışma zamanında kaydedilir. Bu yaklaşımın hem fabrikayı OCP-uyumlu
yaptığını hem de eklenti benzeri bir mimari (plugin architecture)
kurmaya zemin hazırladığını söyledi.

**Kendi değerlendirmem:**
Bu öneriyi uyguladım çünkü mantıklı geldi: yeni bir tip eklerken
fabrika koduna hiç dokunmamak hocanın "OCP'yi gerçekten göster" beklentisini
karşılıyor. Klasik bir Factory Method örneği yerine bu yaklaşımı seçmem
PATTERNS.md'de gerekçelendirildi.

---

## Faz 1 — Singleton'ın Riskleri Konusu

**Sorduğum prompt:**
"Singleton kullanmam gerekiyor ama global state ve test edilebilirlik
konusunda tartışmalı olduğunu biliyorum. Hangi savunmaları kullanmalıyım,
nelere dikkat etmeliyim?"

**AI'ın yanıtı (özet):**
AI, Singleton'ın eleştirilerini özetledi: global durum yaratması, test
izolasyonunu zorlaştırması, gizli bağımlılık oluşturması. Çözüm olarak:
(1) `sifirla` gibi bir test kaçış kapısı eklemek, (2) thread-safe
başlatma kullanmak, (3) hassas verileri ortam değişkenlerinden okumak.

**Kendi değerlendirmem:**
Üç öneriyi de uyguladım. Ayrıca PATTERNS.md'de Singleton bölümüne
"Bilinçli risk" başlığı ekledim — hocanın gözünde bu örüntüyü körü
körüne değil, sakıncalarını bilerek kullandığımı göstermek için.

---

## Kendi Yorumum

> **NOT (sen yazacaksın):** Aşağıdaki 3-4 cümleyi kendi sesinle yaz.
> Şu sorulara cevap ver — formal olma, doğal yaz:
> - Bu fazda AI sana en çok hangi konuda yardımcı oldu?
> - AI'ın önerdiği ama uygulamadığın bir şey var mı? Neden?
> - AI yanılttı ya da eksik bilgi verdi mi?
> - AI olmadan bu fazı ne kadar sürerdi?
>
> Örnek bir cümle: "AI Factory Method ve Singleton ayrımında çok yardımcı
> oldu ama registry yaklaşımını ben sordum, kendi başına önermedi.
> Singleton'ın test sorunu için bana sifirla metodu önerisi gelmeseydi
> muhtemelen testte takılırdım. AI olmadan bu fazı yaklaşık 4-5 saat
> sürerdi sanırım, ama AI'ın hazır kod örnekleri vermesi süreyi 1.5
> saate indirdi."

[Bu kısmı yukarıdaki "Örnek cümle"yi silip kendi cümlelerinle doldur.]
