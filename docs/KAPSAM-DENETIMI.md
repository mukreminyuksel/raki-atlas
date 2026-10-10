# Kapsam denetimi — Ekim 2026

Amaç: lisanslı her rakı üreticisinin resmî portföyündeki ürünlerin katalogda (`arastirma/rakilar.json`) olup olmadığını kontrol etmek. (Şarap Atlası'nda Kayra'nın 15 markasından yalnızca 4'ünün bulunduğu hata burada tekrarlanmasın diye yapıldı.)

**Yöntem:** `arastirma/lisans-raki.json` (Tarım ve Orman Bakanlığı rakı lisans listesi, 11 tesis / 10 firma) esas alındı. Her firma için resmî site ve marka sayfaları `curl` ile okundu; resmî sayfa portföy vermiyorsa Louche Effect'in "Türkiye'de Rakılar" tablosu (47 ürün), degustasyon.net rakı arşivi (50 tadım) ve Karekod Ekim 2026 fiyat listesi ile çapraz kontrol yapıldı. Yaş/captcha kapısı aşılmadı; tanıtım yasağı nedeniyle yalnızca ad veren sayfalarda yalnızca ad alındı.

## Üretici bazında sonuç

| Lisanslı firma | Resmî portföy kaynağı | Katalogda | Eklenen | Not |
|---|---|---|---|---|
| Mey Alkollü İçkiler (Diageo) — Alaşehir + Nevşehir | diageoturkiye.com rakı sayfası (8 marka), yeniraki.com ürün listesi (13 ürün) | 40 | 1: **Yeni Rakı Farbenfreude** (2019, Almanya'ya özel, 70 cl, %45) | 8 markanın hepsi var. Diageo sayfası çeşit listelemiyor; Altınbaş/Kulüp/Vefa/Tayfa/İzmir çeşitleri Louche Effect + degustasyon + Karekod ile tam. prototipraki.com yaş kapılı, okunmadı. |
| Distile İçki (Efe) — İzmir | Resmî site bulunamadı (efe.com.tr başka firma) | 13 | 0 | Louche Effect ve Karekod'daki tüm Efe/Sarı Zeybek çeşitleri katalogda. |
| Sarper Damıtımcılık (Beylerbeyi) — Akhisar | sarper.com açılmıyor | 9 | 0 | Karekod Ekim 2026 Beylerbeyi listesi ve Louche Effect ile tam. |
| Alcosan (Saki) — Salihli | sakiraki.com pasif | 9 | 0 | Louche Effect + Karekod ile tam ("Ustağ Seri" Karekod'da yazım hatası, Uludağ Seri). |
| İzmir Alkollü İçecek — Turgutlu | izmiralkollu.com/markalar (6 ürün) | 6 | 0 | Resmî liste ile birebir. |
| Ankol — Antalya Döşemealtı | ankol.com.tr marka listesi | 4 → 5 | 1: **Topkapı Rakı** | Resmî listede rakı olarak yalnızca Topkapı var; Burgaz/Ata adları listede yok (katalogda kaynaklarıyla duruyor). Topkapı'nın çeşit/derecesi yayımlanmamış. |
| Deva İçecek (Lokal) — Salihli | devaicecek.com içerik vermiyor | 3 | 0 | degustasyon.net'teki 3 Lokal ürünü katalogda. |
| Tariş Üzüm — Alaşehir | tarisuzum.com.tr (yalnızca "rakı üretimi yapılır") | 1 (+1 tarihî) | 0 | Mercan Göbek var; marka listesi yayımlanmıyor. |
| Brysis İçecek — Kırklareli | brysis.com Rakı Grubu sayfası | 0 → 2 | 2: **Bahriyeli Premium Rakı**, **Ergene Rakı** | Derece/hacim/tür yayımlanmamış; tür alanı yaklaşık ve notta belirtildi. |
| Kırbıyık İçecek — Antalya Serik | kirbiyikholding.com.tr açılmıyor | 0 | 0 | Kamuya açık bir rakı markası bulunamadı (bilinen alkollü markası 14.4 SHOT). |

**Toplam:** 4 ürün eklendi (Mey 1, Ankol 1, Brysis 2); katalog 94 → 98.

**Düzeltilen:** `yeniceri-altin-seri` kaydının boş `uretici` alanı → "Üreticisi doğrulanamadı (Afyonkarahisar)". Üretici hiçbir resmî kaynakta bulunamadı; Afyon'da bugün lisanslı rakı tesisi yok.

## Bulunamayanlar / açık kalanlar
- Prototip Rakı LOT 6 ya da sonrası: kamuya açık kaynakta yok (prototipraki.com yaş kapılı).
- Topkapı, Bahriyeli, Ergene: derece, hacim, tadım notu, fiyat yok.
- Kırbıyık'ın rakı markası: bulunamadı.
- Efe, Sarper, Alcosan, Deva'nın güncel resmî ürün sayfaları: yok ya da açılmıyor; portföy ikincil kaynaklardan doğrulandı.
- Yeniçeri Altın Seri üreticisi: doğrulanamadı.
