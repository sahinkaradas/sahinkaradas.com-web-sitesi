# sahinkaradas.com: Proje Kuralları

Bu dosya projede çalışan her yapay zekâ aracı ve her geliştirici için tek kaynaktır. Burada yazan kural, sohbette söylenen tahmine üstündür.

İşe başlamadan kökteki `MEMORY.md`'yi oku. Anlamlı bir işi bitirince onu güncelle.

## Proje

- Şahin Karadaş'ın kişisel sitesi: kadın kuaförleri, güzellik merkezleri ve butiklere Meta reklam yönetimi ile yapay zekâ mesaj/randevu asistanı hizmeti.
- Hedef: Ziyaretçi (işletme sahibi) WhatsApp'tan yazsın; ikinci seçenek Calendly'den ücretsiz görüşme ayarlasın. Blog yazıları bu iki adıma yönlendirir.
- Canlı adres: https://sahinkaradas.com
- Kullanıcıların çoğu telefondan geliyor. Önce mobil düşün.

## Yığın

- Saf HTML + CSS + vanilla JavaScript. Framework yok.
- Yayın: Netlify, GitHub `main` dalından otomatik. Her yayın bir "production deploy" sayılır; ücretsiz planda ayda en fazla 20. Küçük değişiklikleri biriktir, tek commit'te yükle.
- Blog: `blog/blog_build.py` (yalnızca standart Python) her yayında yazıları sayfaya çevirir.
- Yazı paneli: `/yonetim/` GitHub girişiyle çalışır, yeni yazıları doğrudan repoya commit eder.

## Dosya haritası

| Dosya | Görevi |
|---|---|
| `site/index.html` | Ana sayfa (tek dosya, 295 KB, TR+EN) |
| `site/assets/site.css` | Ortak stil |
| `site/assets/cerez.js` | Çerez ayarları |
| `site/yonetim/` | Blog yazı paneli (`index.html`, `config.yml`) |
| `blog/posts/*.json` | Blog yazıları (panel yazar, dosya adı = adres) |
| `blog/shell.json` | Blog sayfalarının menüsü ve altbilgisi |
| `blog/yasal/*.md` | KVKK, çerez ve gizlilik metinleri (TR+EN) |
| `blog/blog_build.py` | Blog sayfalarını üretir |
| `netlify.toml` | Yayın ayarı |

**Tuzak:** Menü ve altbilgi hem `site/index.html`'de hem `blog/shell.json`'da durur. Birini değiştirirsen ikisini de aynı değişiklikle güncelle, yoksa blog sayfalarında eski menü kalır.

## Komutlar

```bash
python blog/blog_build.py --check   # yazıları kontrol eder, dosya yazmaz
```

- Kullanıcının Windows bilgisayarında `python` çalışır; `python3` Mağaza yer tutucusudur. Netlify ise `netlify.toml`'daki `python3`'ü kullanır.
- Yerel önizleme yöntemi doğrulanmadı. `blog_build.py --site site` komutu `site/` içine dosya yazar; bunu çalıştırırsan üretilen dosyaları commit'e ekleme.
- Canlıya yayın yalnızca kullanıcı onayıyla.

## Kod kuralları

- Mevcut CSS sınıflarını ve değişkenlerini yeniden kullan. Yeni sınıf eklemeden önce adın başka yerde kullanılmadığını doğrula.
- Yeni satır içi `style=""` ekleme; mevcutları toplu değiştirme.
- JavaScript'te global değişken yok; her özellik `if (öğe)` kontrolüyle başlar.
- Yeni bağımlılık, CDN kütüphanesi ya da framework ekleme. Gerekirse önce sor.
- Görsellerde `width`, `height`, `alt`; ekranın altında kalanlarda `loading="lazy"`.
- Ana sayfa, menü ve altbilgi metni iki dilli: `<span lang="tr">…</span><span lang="en">…</span>`. Birini eklersen ötekini de ekle.
- İstisna: blog yazı gövdeleri (`blog/posts/*.json`) yalnızca Türkçedir; panel ve `blog_build.py` İngilizce alan tanımaz. Bunlara İngilizce isteme.
- Değişiklik küçük ve geri alınabilir olsun. İstenmeyen dosyaya dokunma.

## Güvenlik ve kişisel veri

- Şifre, API anahtarı, token hiçbir dosyaya girmez. `.env` dosyalarını okuma.
- Sitede veri toplayan form ve veritabanı yok. Tek form (`dm-form`) bir demo sohbettir, hiçbir yere kayıt göndermez.
- Meta Pixel (`fbq`) `site/assets/cerez.js` içinde yüklenir ve WhatsApp ile Calendly tıklamalarını izler (`Contact`, `Schedule`). Çerez izni de aynı dosyada yönetilir; izleme kodunu başka yere ekleme ve yenisini izinsiz ekleme.
- Yasal metinlere (`blog/yasal/`) dokunmadan önce kullanıcıya sor; hukuki içeriktir.
- Silme ve canlıya yayın: kullanıcı açıkça onay vermeden yapılmaz.

## Form eklenirse (şu an yok)

1. Önce plan çıkar, onay al. Veriyi nereye yazacağını (Supabase, n8n, e-posta) kullanıcı seçer.
2. Gerçek müşteri verisi toplayan her formun yanında KVKK aydınlatma metni (`/kvkk/`) bağlantısı olsun; gereksiz alan ekleme.
3. Veritabanı kullanılacaksa: RLS açık, ziyaretçi yalnızca ekleyebilir, okuyamaz. Gizli anahtar kodda durmaz, Netlify ortam değişkeninde durur.
4. Bu bölüm o gün `AGENTS.md`'ye "Veri sözleşmesi" tablosu olarak taşınır (form alanı → sütun).
5. Test için `Test Kaydı` / `05000000000` kullan, gerçek kişi verisi kullanma.

## Bitti tanımı

1. Değişen sayfa açıldı, tarayıcı konsolunda hata yok.
2. 360 px (telefon) ve masaüstünde düzen bozulmuyor.
3. Menü/altbilgi değiştiyse `index.html` ile `blog/shell.json` aynı.
4. Blog değiştiyse `blog_build.py --check` çıktısındaki UYARI satırları okundu. Komut uyarı verse de çıkış kodu 0 döner; yasal sayfaları ve `index.html` ile `shell.json` eşitliğini denetlemez, onlara ayrıca bak.
5. Ne değişti, nasıl doğrulandı, ne açık kaldı: üç satırla raporlandı.

"Çalışıyor olmalı" bir doğrulama değildir. Denenemediyse "denenmedi" yaz.

## Dil ve ton

- Türkçe, tam imla ve Türkçe karakterlerle. İngilizce metinler sade ve doğal.
- Ziyaretçiye sıcak, kısa, net. "Hemen", "en iyi", "kaçırmayın" gibi abartı yok.
- Reklam metinlerinde sağlık iddiası ve "önce/sonra" vaadi yok.
