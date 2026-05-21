# Bildirim Sistemi Tasarım Örüntüleri Ödevi

**Seçilen Konu:** A - Bildirim Sistemi

## Proje Hakkında
Bu proje, başlangıçta if-else zincirlerine sahip ("God Class") bir bildirim sisteminin tasarım örüntüleri kullanılarak nasıl temiz, genişletilebilir ve esnek bir yapıya dönüştürüldüğünü gösterir.

## Kullanılan Tasarım Örüntüleri
1. **Factory Method (Creational):** Bildirim nesnelerinin yaratılışını soyutlar ve OCP'ye uygun bir kayıt (registry) mekanizması sunar.
2. **Singleton (Creational):** Uygulama yapılandırmasını (config) tek bir merkezden yönetir.
3. **Decorator (Structural):** Bildirimlere sonradan "Tekrar Deneme" ve "Maskeleme" özellikleri ekler.
4. **Adapter (Structural):** Uyumsuz bir harici SMS API'sini sistemin arayüzüne bağlar.
5. **Strategy (Behavioral):** Bildirimlerin gönderim taktiklerini (Anında, Gecikmeli) runtime'da değiştirilebilir hale getirir.
6. **Observer (Behavioral):** Bildirim sonuçlarını dinleyen loglama ve analitik gibi yapıları ana akıştan ayırır.

## Mimari Diyagram
*UML diyagramları ve örüntü detayları `PATTERNS.md` dosyasında yer almaktadır.*

## Nasıl Çalıştırılır
```bash
python -m src.bildirim.bildirim_yoneticisi
