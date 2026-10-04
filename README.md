# 🥛 Rakı Atlası

Türkiye'nin rakıları üretici ve marka marka; meze & sofra rehberi, balık takvimi, rakı kültürü ve kişisel tadım defteri.
Viski Atlası ve Bira Atlası'nın kardeşi: https://viski-atlas.pages.dev · https://bira-atlas.pages.dev

## Özellikler

- **Katalog:** 94 rakı ve anasonlu içki, *Üretici → Marka → Rakı* ağacı ya da *türe göre* düzen.
  Filtreler: bulunabilirlik (markette, tekelde, zor bulunur, üretimi durdu), tür, fiyat aralığı, alkol derecesi.
- **Rakı künyesi:** tür, derece, hacimler, damıtım, dinlendirme, anason, tat, not, puan, fiyat
  (Ekim 2026 Türkiye perakende, 70 cl; kaynaklı fiyatlarda “doğrulanmış” rozeti), kaynak bağlantıları,
  “Yanında ne iyi gider” (3 meze önerisi), benzer rakılar. Paylaşılabilir bağlantı: `#s=<id>`.
- **Rakı Türleri:** suma rakısı, yaş üzüm, kuru üzüm, göbek, meşede dinlenmiş, özel seri, dünyanın anasonluları;
  üstte coğrafi işaret tanımına dayanan “Rakı nasıl yapılır?” adımları.
- **Üreticiler:** resmî üretim izni listesindeki rakı tesisleri il il, markalarıyla; resmî kayıt kutusu;
  ayrı “Tarihî tesisler (Tekel)” bölümü; Leaflet haritası.
- **Meze & Sofra:** 50 meze türüne göre gruplu ve filtreli; “Bu ay hangi balık?” (12 ay, av yasakları ve asgari boylar);
  “Bu akşam sofra kur” (kişi sayısı ve mevsime göre 5-7 meze + uygun rakı).
- **Kültür:** sofra adabı, tarihçe zaman çizelgesi, edebiyat ve müzikte rakı, Dünya Rakı Günü.
- **Magazin:** rakı sofrasıyla anılan ünlüler (her kartta kaynak).
- **Meyhaneler & Topluluk**, **Nereden Alınır** (zincir marketler, duty-free; yasal not).
- **Koleksiyon:** Denedim / Deneyeceğim listeleri, tadım notu ve kişisel puan, Gurme puanı
  (Meraklı → Sofraya Yeni Oturan → Meze Ustası → Demlenmiş → Çilingir Sofrası Üstadı → Aslan Sütü Hocası),
  marka ve tür damgalı Rakı Pasaportu, istatistik ve paylaşım kartı, akıllı öneriler, yedek al/yükle.
- **Sosyal:** bulut kaydı (kod ya da telefon + PIN), tadım geceleri (kör tadım dahil), davetle kapalı kulüpler.
- PWA: çevrimdışı çalışır (`sw.js`), ana ekrana eklenebilir. 18 yaş onayı vardır.

## Veri politikası

- **Uydurma yok.** Her rakı kaydında kaynak bağlantıları (`kaynak`) bulunur; doğrulanamayan alan boş bırakılır
  (ör. puan yoksa “—”, üretici doğrulanamadıysa “Üreticisi doğrulanamadı”).
- **Fiyatlar kaynaklıdır ya da yoktur.** Katalogdaki fiyatlar Ekim 2026 Türkiye perakende fiyatlarıdır (70 cl) ve
  `data/fiyatlar.json`'da kaynak adresiyle tutulur. Otomatik görev bir fiyatı kaynaksız bulursa `tahmin` olarak işaretler;
  tahmin, son 6 ayda doğrulanmış bir fiyatın üzerine yazılmaz.
- Puanlar, tadım yazılarındaki değerlendirmelerden derlenen editoryal puanlardır (0-100), tek bir sitenin canlı puanı değildir.
- Üretici listesi Tarım ve Orman Bakanlığı'nın alkollü içki üretim izni listesine dayanır; harita konumları ilçe/il düzeyinde yaklaşıktır.
- Gerçek kişiler yalnızca kamuya açık, kaynaklı bilgilerle yer alır.

## Dosyalar

| Yol | İçerik |
|---|---|
| `index.html` | Tek sayfalık uygulama; `DATA` dizisi `arastirma/derle.py` ile üretilir |
| `arastirma/` | Ham araştırma verisi (`rakilar.json`, `ureticiler.json`, `lisans-raki.json`, `mezeler.json`, `balik.json`, `kultur.json`, `meyhaneler.json`, `satis.json`) ve `derle.py` |
| `data/` | Sitenin okuduğu JSON'lar: `fiyatlar`, `ureticiler`, `lisans`, `mezeler`, `balik`, `kultur`, `topluluk`, `satis`, `baglantilar`, `gorseller` |
| `api/` | Platformdan bağımsız sunucu çekirdeği: `sync.ts` (bulut kaydı), `gece.ts` (tadım geceleri), `kulup.ts`, `ortak.ts`, `kv.ts` |
| `functions/api/` | Cloudflare Pages katmanı (KV bağlaması: `VERI`, `wrangler.toml`) |
| `scripts/fiyat-guncelle.mjs` | Aylık fiyat doğrulama yardımcısı (`sec` / `uygula`) |
| `scripts/baglanti.mjs` | Üreticilerin resmî site/sosyal medya bağlantıları |

Veriyi yeniden üretmek için: `python3 arastirma/derle.py`

Alkolü ölçülü tüketin; içtiyseniz araç kullanmayın. Bu site 18 yaşından büyükler içindir.
