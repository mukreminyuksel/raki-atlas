# Rakı Atlası — geliştirici notları

Türkçe rakı kataloğu, meze & sofra rehberi ve rakı kültürü. Yayın: https://raki-atlas.pages.dev · Depo: `mukreminyuksel/raki-atlas` (`main`).

## Çalıştırma
- Yerel: `python3 -m http.server 8000`; 18 yaş onayı için `localStorage.setItem('raki_yas','1')`.
- Veri araştırma dosyalarından üretilir: `python3 arastirma/derle.py` → `index.html` içindeki `DATA` ve `data/*.json`. Ham veriyi `arastirma/` altında düzenle, sonra derle. `data/fiyatlar.json`'a yalnızca henüz kaydı olmayan **kaynaklı** fiyatlar eklenir (aylık görevin kayıtları korunur).

## Yapı
- `arastirma/` — `rakilar.json` (98 ürün), `ureticiler.json`, `lisans-raki.json` (resmî lisans listesi), `mezeler.json` (50), `balik.json` (aylık balık + av yasakları, 6/1 sayılı tebliğ, 2024-2028), `kultur.json` (adap, tarihçe, üretim, edebiyat, ünlüler), `meyhaneler.json`, `satis.json`.
- Sekmeler: Katalog (Üretici → Marka → Rakı), Rakı Türleri (+ üretim), Üreticiler (lisans + tarihî Tekel tesisleri + harita), **Meze & Sofra** (balık takvimi, "bu akşam sofra kur"), Kültür, Magazin (yalnızca vefat etmiş edebiyatçılar), Topluluk, Nereden Alınır.
- Bu sitede Atatürk, yaşayan Türk ünlü ya da iş insanı **yer almaz** (bilinçli karar); magazin listesini genişletirken bu kuralı koru.
- Dünya Rakı Günü Aralık'ın **ikinci** cumartesisi (ilki 2011, Adana); tarih kodda her yıl hesaplanır.
- **Kapsam denetimi (yeni veri turlarında zorunlu):** Katalog genişletilirken esas, resmî lisans listesi (`arastirma/lisans-raki.json`) ve her üreticinin **resmî portföyüdür** (resmî site/marka sayfası; yoksa güvenilir ikincil liste). Her lisanslı üretici için portföydeki ürün sayısı ile katalogdaki ürün sayısı karşılaştırılır (`python3 -c "import json,collections;print(collections.Counter(x['uretici'] for x in json.load(open('arastirma/rakilar.json'))))"`), eksikler kaynaklı eklenir, bulunamayanlar not edilir. Son denetim: `docs/KAPSAM-DENETIMI.md`.
- **Rakı profili (detay kartı):** görünüm/louche, gözyaşı, koku, damak çubukları (anason, tatlılık, yağlılık, sertlik 1-5), servis (su, buz, kadeh). `rakilar.json` içinde isteğe bağlı `profil` nesnesi (kaynaklı) varsa onu gösterir; yoksa kategori/derece/damıtım/meşe bilgisinden **"≈ türetilmiş"** etiketiyle üretir. Tadım metninde beyazlaşma/koku cümlesi varsa "📖 tadım notundan" diye gösterilir. Kaynaksız `profil` değeri yazma.

## Veri dosyaları ve betikler
- `scripts/denetim.mjs` — işlev denetimi (Playwright): her sekme, arama kutusu, seçim menüsü ve zararsız düğme masaüstü + 390 px mobilde denenir; sayfa hatası, etkisiz arama ve yatay taşma raporlanır (`node scripts/denetim.mjs`, hata varsa çıkış kodu 1). Arayüz değişikliğinden sonra çalıştır; aylık görev de çalıştırır.
- `scripts/gorsel.mjs` — şişe görseli ekleme: `sec | ekle <id> <gorselURL> <sayfaURL> <sahip> | yok <id> | sil <id>`. Yalnızca **resmî üretici sitelerinden** (yaş kapılı siteler atlanır); görsel 160 px yüksekliğinde WebP'ye çevrilir (`img/sise/`, kayıt `data/gorseller.json`). Aylık görev ayın 8'inde çalışır.
- `data/fiyatlar.json` — fiyat kayıtları (kaynak, güven, tarih). Elle düzenleme; aylık görev `scripts/fiyat-guncelle.mjs` ile yazar (`sec` → araştırılacaklar, `uygula dosya.json` → güvenlik kontrolleriyle yazar; şüpheli değişimleri reddeder).
- `data/baglantilar.json` — üreticilerin resmî site ve sosyal medya bağlantıları. `scripts/baglanti.mjs` (`sec` / `ekle` / `yok` / `kontrol` / `sil`). Yalnızca **resmî** hesaplar.
- `data/satis.json` — "Nereden Alınır" (yasal not, zincir, duty-free, butik); `data/topluluk.json` — kulüp, grup, festival, kanallar.

## Genel kurallar (bütün atlas siteleri için)
- **Dil:** Site metinleri, commit mesajları ve kullanıcıyla yazışma **Türkçe**. Kod ve değişken adları mevcut dosyadaki dile uysun.
- **Tek dosyalık uygulama:** Arayüz ve mantık `index.html` içinde (satır içi `<script>`); ortak yardımcılar `raf.js`. Derleme adımı yok. Sözdizimi kontrolü: `node -e "const s=require('fs').readFileSync('index.html','utf8');[...s.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)].forEach(x=>new Function(x[1]));console.log('ok')"` (**non-greedy** regex; sayfada birden fazla `<script>` var).
- **Önbellek:** Sayfa ya da veri değiştirince `sw.js` içindeki `CACHE` adındaki sürüm numarasını artır (ör. `…-v38` → `…-v39`). Artırmazsan kullanıcılar eski sürümü görür.
- **Yayın:** `main`'e push = Cloudflare Pages otomatik yayın (build komutu yok, çıktı dizini `/`). PR gerekmez. Veri deposu KV bağlaması `wrangler.toml` içinde, adı `VERI`.
- **Sunucu tarafı:** `api/*.ts` platformdan bağımsız çekirdek, `functions/api/*.ts` Cloudflare katmanı (KV: `api/kv.ts`). Uç noktalar: `/api/sync` (bulut kodu + telefon/PIN), `/api/gece` (tadım geceleri), `/api/kulup` (kulüpler), `/api/barkod` (Raf Asistanı barkod sözlüğü). Yerelde denemek için `npx wrangler pages dev .`; saf mantık testi için `node --experimental-strip-types` ile `api/*.ts` içindeki `isle(req, depo)` bellek içi sahte depoyla çağrılabilir.
- **Gizlilik ilkeleri (bozma):** Telefon ve PIN düz metin saklanmaz (SHA-256 özeti); bulut kodu ve PIN ekranda varsayılan **gizli** (👁 düğmesi); tadım gecesinde başkalarının puanı oylama bitmeden gizli; GoatCounter çerezsiz sayaçtır, kişisel veri yok.
- **Veri dürüstlüğü (en önemli kural):**
  - Uydurma bilgi, fiyat, puan ya da ödül **yok**. Emin olunmayan alan boş bırakılır; fiyatı kaynaksız olan "tahmin" diye işaretlenir.
  - Gerçek kişiler hakkında yalnızca kamuya açık ve kaynağı gösterilebilen bilgi. Özel hayat, sağlık, bağımlılık, paparazzi/özel fotoğraftan çıkarım **yok**. Türkiye'den yaşayan gerçek kişi (iş insanı, ünlü) magazin listelerine eklenmez.
  - Untappd, BeerAdvocate, RateBeer, Whiskybase, Vivino, CellarTracker gibi sitelerden veri **kazınmaz**.
  - Giriş, captcha, bot koruması ya da yaş doğrulama kapısı olan sayfalar **aşılmaz**; açılmıyorsa atlanır.
  - Türk sitelerini okurken `WebFetch` çalışmaz: `curl -sL -m 25 -A 'Mozilla/5.0' URL` kullan.
  - Türkiye'de alkolün internetten tüketiciye satışı yasaktır: "internetten satın al" bağlantısı verilmez; yalnızca fiziksel mağaza, duty-free ve markanın kendi sitesi.
- **Commit mesajı:** Türkçe, ne ve neden. Sonuna şu iki satır eklenir (yapay zekâ ile yapılan işlerde):
  ```
  Co-Authored-By: Claude <noreply@anthropic.com>
  Claude-Session: <oturum bağlantısı>
  ```
- **Otomatik görevler (Claude Routines) bu depolara kendiliğinden push eder:** fiyat (ayın 1-6'sı, siteye göre), görseller (3-4'ü, viski ve bira), üretici bağlantıları (ayın 5'i, hepsi). **Çalışmaya başlamadan önce `git pull`.** Bu görevler yalnızca kendi veri dosyasına dokunur (`data/fiyatlar.json`, `data/gorseller.json` + `img/`, `data/baglantilar.json`).
- **Kardeş siteler:** viski-atlas, bira-atlas, raki-atlas, sarap-atlas (hepsi `*.pages.dev`). Ortak parçalar (api, raf.js, kardeş bağlantı kutusu, göz düğmesi, filtre yapıları) siteler arasında kopyadır; birinde yapılan ortak bir düzeltme genelde diğerlerine de gerekir. Yol haritası: `docs/ONERILER.md`.
- **localStorage anahtarları site önekli** (`viski_`, `bira_`, `raki_`, `sarap_`); ayrı alan adlarında çakışmaz ama önekleri değiştirme, kayıtlı kullanıcı verisi kaybolur.
