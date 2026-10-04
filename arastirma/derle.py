# Araştırma dosyalarından sitenin verisini yeniden üretir.
#   index.html içindeki DATA dizisi        ← arastirma/rakilar.json
#   data/ureticiler.json (tesis + konum)   ← arastirma/ureticiler.json
#   data/lisans.json                       ← arastirma/lisans-raki.json
#   data/mezeler.json, balik.json, kultur.json, topluluk.json
#   data/satis.json                        ← arastirma/satis.json (zincir + duty-free)
#   data/fiyatlar.json: yalnızca henüz kaydı olmayan KAYNAKLI fiyatlar eklenir (aylık görevin kayıtları korunur)
#   data/baglantilar.json, data/gorseller.json yoksa boş iskelet yazılır
# Kullanım: python3 arastirma/derle.py
import json, os, re, sys

KOK = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(KOK)
HTML = os.path.join(SITE, 'index.html')
DATA_DIR = os.path.join(SITE, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
TARIH = '2026-10-04'


def oku(ad, var=None):
    p = os.path.join(KOK, ad)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else var


def yaz(ad, veri):
    with open(os.path.join(DATA_DIR, ad), 'w', encoding='utf-8') as f:
        json.dump(veri, f, ensure_ascii=False, indent=1)
        f.write('\n')


KATEGORILER = ['suma', 'yas-uzum', 'kuru-uzum', 'gobek', 'mese', 'ozel-seri', 'yabanci-anason']
BULLAR = {'kolay', 'tekel', 'zor', 'uretim-durdu'}
YABANCI = ['Yunanistan', 'Fransa', 'Lübnan', 'Avusturya']


def uretici_adi(u):
    """'Mey|Diageo' → 'Mey (Diageo)'; boşsa açıkça belirtilir."""
    u = (u or '').strip()
    if not u:
        return 'Üreticisi doğrulanamadı'
    if '|' in u:
        a, b = u.split('|', 1)
        return f'{a.strip()} ({b.strip()})'
    return u


def ulke(tesis):
    for u in YABANCI:
        if (tesis or '').startswith(u):
            return u
    return 'Türkiye'


# ---------- 1. Rakılar → DATA ----------
rakilar = oku('rakilar.json', [])
hatalar = []
ids = set()
DATA = []
for r in rakilar:
    if r['id'] in ids:
        hatalar.append('çift id: ' + r['id'])
    ids.add(r['id'])
    if r['kategori'] not in KATEGORILER:
        hatalar.append(f"{r['id']}: bilinmeyen kategori {r['kategori']}")
    if r['bul'] not in BULLAR:
        hatalar.append(f"{r['id']}: bilinmeyen bulunabilirlik {r['bul']}")
    d = {
        'id': r['id'], 'ad': r['ad'], 'marka': r['marka'] or r['ad'],
        'ure': uretici_adi(r['uretici']), 'il': r.get('tesis_il') or '', 'ulke': ulke(r.get('tesis_il')),
        'kat': r['kategori'], 'abv': r['abv'] if r['abv'] else 0,
        'hacim': r.get('hacim_cl') or [], 'dist': r.get('distilasyon') or '', 'dinl': r.get('dinlendirme') or '',
        'anason': r.get('anason') or '', 'tat': r.get('tat') or '', 'not': r.get('not') or '',
        'puan': r.get('puan') or 0, 'tl': r.get('tl') or 0, 'tlK': r.get('tl_kaynak') or '',
        'yil': r.get('yil') or '', 'bul': r['bul'], 'kaynak': r.get('kaynak') or [],
    }
    if d['tl'] and not d['tlK']:
        hatalar.append(f"{r['id']}: kaynaksız fiyat (tl={d['tl']})")
    DATA.append(d)

if hatalar:
    print('\n'.join('⚠️ ' + h for h in hatalar))

SIRA = {k: i for i, k in enumerate(KATEGORILER)}
DATA.sort(key=lambda d: (d['ulke'] != 'Türkiye', d['ure'], d['marka'], SIRA.get(d['kat'], 9), -(d['puan'] or 0)))

satirlar = []
onceki = None
for d in DATA:
    if d['ure'] != onceki:
        satirlar.append('// ===== ' + d['ure'] + ' =====')
        onceki = d['ure']
    satirlar.append(json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ',')
blok = 'const DATA = [\n' + '\n'.join(satirlar) + '\n];'

s = open(HTML, encoding='utf-8').read()
i = s.index('const DATA = [')
j = s.index('\n];', i) + 3
s = s[:i] + blok + s[j:]
open(HTML, 'w', encoding='utf-8').write(s)

# ---------- 2. Fiyatlar (kaynaklı olanlar) ----------
fp = os.path.join(DATA_DIR, 'fiyatlar.json')
fiy = json.load(open(fp, encoding='utf-8')) if os.path.exists(fp) else {'guncelleme': None, 'kur': None, 'fiyatlar': {}, 'denendi': {}, 'inceleme': []}
eklenen = 0
for d in DATA:
    if d['tl'] > 0 and d['tlK'] and d['id'] not in fiy['fiyatlar']:
        fiy['fiyatlar'][d['id']] = {'tl': d['tl'], 'tarih': TARIH, 'tur': 'tr_liste', 'guven': 'orta',
                                    'kaynak': d['tlK'], 'not': 'Ekim 2026 Türkiye perakende, 70 cl',
                                    'gecmis': [[TARIH, d['tl']]]}
        eklenen += 1
fiy['fiyatlar'] = dict(sorted(fiy['fiyatlar'].items()))
fiy['guncelleme'] = fiy.get('guncelleme') or TARIH
yaz('fiyatlar.json', fiy)

# ---------- 3. Üreticiler + harita konumu ----------
# Yaklaşık konumlar: ilçe biliniyorsa ilçe merkezi, yoksa il merkezi (şehir düzeyi yeterli)
KONUM = {
    'Manisa|Alaşehir': [38.350, 28.517], 'Manisa|Salihli': [38.483, 28.139], 'Manisa|Akhisar': [38.918, 27.840],
    'Manisa|Turgutlu': [38.500, 27.700], 'Nevşehir|Merkez': [38.625, 34.714], 'İzmir|Menderes': [38.253, 27.134],
    'Antalya|Döşemealtı': [37.023, 30.600], 'Antalya|Serik': [36.917, 31.100], 'Kırklareli|Merkez': [41.735, 27.225],
    'Kırklareli|Lüleburgaz': [41.404, 27.356], 'Tekirdağ|Süleymanpaşa': [40.978, 27.511], 'İstanbul|Beykoz': [41.134, 29.092],
    'Manisa': [38.614, 27.430], 'Nevşehir': [38.625, 34.714], 'İzmir': [38.423, 27.143], 'Antalya': [36.897, 30.713],
    'Kırklareli': [41.735, 27.225], 'Tekirdağ': [40.978, 27.511], 'İstanbul': [41.008, 28.978], 'Gaziantep': [37.066, 37.383],
    'Diyarbakır': [37.914, 40.231], 'Kilis / Karaman': [36.716, 37.115],
}
ureticiler = oku('ureticiler.json', [])
kullanilan = {}
for u in ureticiler:
    k = u['il'] + '|' + (u.get('ilce') or '')
    c = KONUM.get(k) or KONUM.get(u['il'])
    if not c:
        print('⚠️ konum yok: ' + u['firma'] + ' ' + k)
        continue
    n = kullanilan.get(tuple(c), 0)
    kullanilan[tuple(c)] = n + 1
    # Aynı noktaya düşen tesisler üst üste binmesin
    u['konum'] = [round(c[0] + 0.045 * n, 4), round(c[1] + 0.06 * n, 4)]
    u['tarihi'] = bool(u.get('tarihi'))
yaz('ureticiler.json', {'_aciklama': 'Lisanslı rakı tesisleri ve tarihî (Tekel dönemi) tesisler. konum: ilçe/il merkezine göre yaklaşık.',
                        'ureticiler': ureticiler})

# ---------- 4. Resmî lisans listesi ----------
lis = oku('lisans-raki.json', [])
yaz('lisans.json', {
    '_aciklama': 'T.C. Tarım ve Orman Bakanlığı Tütün ve Alkol Dairesi Başkanlığı — Alkollü İçki Üretim İzin Belgesi Sahibi Firmalar listesinden rakı satırları.',
    'kaynak': 'https://pdtadb.tarimorman.gov.tr/webUibList.aspx', 'tarih': TARIH, 'tesisler': lis})

# ---------- 5. Meze, balık, kültür, topluluk ----------
yaz('mezeler.json', {'mezeler': oku('mezeler.json', [])})
yaz('balik.json', oku('balik.json', {}))
yaz('kultur.json', oku('kultur.json', {}))
yaz('topluluk.json', {'topluluklar': oku('meyhaneler.json', [])})

# ---------- 6. Satış yerleri (zincir + duty-free) ----------
sat = oku('satis.json', {'yasal_not': '', 'yerler': []})
sat['yerler'] = [y for y in sat['yerler'] if y.get('tur') in ('zincir', 'duty-free')]
yaz('satis.json', sat)

# ---------- 7. Boş iskeletler (görevler doldurur) ----------
for ad, anahtar in (('baglantilar.json', 'baglantilar'), ('gorseller.json', 'gorseller')):
    if not os.path.exists(os.path.join(DATA_DIR, ad)):
        yaz(ad, {anahtar: {}, 'yok': {}})

print(f'{len(DATA)} rakı · {len({d["ure"] for d in DATA})} üretici · {len({d["marka"] for d in DATA})} marka · '
      f'{sum(1 for d in DATA if d["tlK"])} kaynaklı fiyat ({eklenen} yeni kayıt) · {len(ureticiler)} tesis')
