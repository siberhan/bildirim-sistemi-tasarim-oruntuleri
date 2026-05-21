## Faz 1 — AI Etkileşim Günlüğü

## Faz 0 Hazırlık Etkileşimi

**Sorduğum prompt:**
"Bu kodda hangi tasarım sorunlarını görüyorsun? Hangi tasarım
örüntüleri bu sorunları çözebilir? Her sorun için kısa bir
açıklama yaz."

**AI'ın yanıtı (özet):**
AI, mevcut sınıfın her işi üstlenen bir "Tanrı Sınıf" (God Class) olduğunu belirterek SRP ve OCP gibi temel SOLID prensiplerini çiğnediğimizi söyledi. `if-elif` zincirinin esnekliği öldürdüğünü, şifrelerin koda gömülü olmasının güvenlik açığı yarattığını ve sıkı bağlılık yüzünden test yazılamayacağını belirtti. Çözüm olarak da Strategy Pattern, Dependency Injection ve ortam değişkenleri (.env) kullanmamı önerdi.

**Kendi değerlendirmem:**
SOLID ihlalleri, hard-coded şifreler ve test edilebilirlik gibi pratik sorunları tamamen haklı bulup doğrudan PROBLEMS.md'ye geçirdim. Ancak AI'ın henüz yolun başında (Faz 0'da) `__init__` içindeki basit kurulumları bile devasa bir suçmuş gibi eleştirmesini "aşırı mühendislik" olarak görüp şimdilik eledim; onun yerine kendi fark ettiğim "Bildirim Nesnesi" eksikliğini rapora ekledim. Loglamadaki I/O maliyeti ve toplu gönderimin ayrı bir strateji olması gerektiği yönündeki mantıklı uyarılarını ise sonraki fazlarda kullanmak üzere notlarıma aldım.
