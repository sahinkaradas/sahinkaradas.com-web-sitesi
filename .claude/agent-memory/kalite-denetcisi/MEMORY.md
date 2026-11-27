# kalite-denetcisi hafızası

Bu ajanın kendi notları: kararlar, tuzaklar, tekrar eden hatalar. Kodun kopyası, anahtar ve kişisel veri yazılmaz.

## Öğrenilenler

- 2026-11-27 (ilk denetim, ekip/kural dosyaları): Hook canlıda doğrulandı: proje köküne Write engellendi. Hafıza klasörüne yazma yolu bu kayıtla denendi.
- Önce bak: AGENTS.md iddiaları (form yok, dosya haritası) gerçek dosyalarla. `site/index.html:534` demo sohbet formu (`dm-form`) var, ağ isteği yok; "form yok" ifadesi bu yüzden dikkatli okunmalı. Meta Pixel `site/assets/cerez.js` içinde (`fbq`), izne bağlı.
- `blog_build.py --check` uyarı olsa da çıkış kodu 0 verir (satır 558); "uyarısız" kontrolü çıktıyı okumayı gerektirir. Yasal sayfaları ve shell.json-index.html eşitliğini denetlemez.
- Blog yazıları yalnızca Türkçe; "her metin iki dilli" kuralı yalnızca ana sayfa/menü/altbilgi için geçerli. Yazı gövdesinde EN yok diye bulgu yazma.
- `config.yml` `adres` alanı JSON'a yazılır ama slug dosya adından gelir (`blog_build.py:236`); REQ'deki `slug` her zaman dolu. Eşleşme tamam.
- Sır taraması `.md` hariç: temiz çıktı (2026-11-27).
- Büyük dosya okuma: `site/index.html` satır 22-23 base64 font, satır 489/781 çok uzun; Read yerine Grep `-o` ile kısa desen kullan. Ham metin Read'i 60K token yer.
- JSON-LD ve "sitede zaten açık" iddiaları: kullanıcının "açık" dediği bilgiyi (e-posta, Instagram) Grep ile görünür metinde doğrula; Instagram adresi yalnızca JSON-LD'de çıktı (2026-11-27).
- `a.logo` aria-label: görünen yazı `.wm-sub` içinde TR+EN span; blog shell'de iki span de var ama blog tek dilli.
- Panel (`site/yonetim/index.html:11`) Decap CMS'i unpkg CDN'den yüklüyor; AGENTS "CDN ekleme" kuralının önceden var olan istisnası.
- CSS ayrışması: `index.html` kendi satır içi CSS'ini taşır, `site.css` yalnızca blog/yasal. Blog `.pcard/.cards3/.steps/.step/.need/.hero-by` sınıflarını kullanmıyor (Grep sayısı 0, 2026-11-27); bu sınıflar index'te değişince site.css'e taşıma gerekmez, ölü kod kalır. Ortak olanlar: `.eye`, `--r-s/--r-m` değişkenleri, `.prose .ex`.
- CRLF kontrolü: Grep `[^\r]\n` multiline ile çıplak LF aranır; 2026-11-27'de üç dosyada 0 çıktı.
- Grep'te `-P` parametresi yok; çok satırlı arama `multiline:true` ile.
- Boş bırakılmış `@media (max-width:1020px){}` index.html:282 (kalıntı, zararsız).
