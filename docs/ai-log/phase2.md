  # Faz 2 AI Etkileşim Günlüğü
  
  ## Örüntü Seçimi ve Adapter vs Facade Tartışması
  **Sorduğum prompt:**
  "Harici bir SMS sağlayıcısını sisteme entegre etmek istiyorum. Adapter pattern burada uygun mu, yoksa Facade mı? Farkını açıkla."
  
  **AI'ın yanıtı (özet):**
  Yapay zeka, Adapter örüntüsünün burada kesin tercih olduğunu belirtti. Adapter'ın, *uyumsuz* bir arayüzü sistemin beklediği *belirli* bir arayüze uydurmak için kullanıldığını; Facade'ın ise arkadaki çok karmaşık bir alt sistemin önüne basit ve tek bir arayüz koymak için kullanıldığını açıkladı.
  
  **Kendi değerlendirmem:**
  AI'ın açıklaması ayrımı çok netleştirdi. Facade'ın amacı karmaşıklığı gizlemekken, Adapter'ın amacı uyumsuzluğu gidermek. Benim problemim tamamen uyumsuzluk olduğu için doğrudan Adapter'ı uyguladım.
  
  ## Kendi Yorumum
Bu örnek bana tasarım örüntülerinde isimden çok amacın önemli olduğunu gösterdi. İlk başta ikisi de “aradaki katman” gibi görünüyordu ama kullanım nedenleri tamamen farklıymış. Problemi doğru tanımlayınca hangi pattern’in uygun olduğu da netleşti.
