# Proje Hafızası

Bu dosya projenin defteridir: alınan kararlar, kullanıcının tercihleri, açık işler. Her oturumun başında okunur, anlamlı her işin sonunda güncellenir. Kuralları AGENTS.md ve CLAUDE.md belirler; bu dosya "ne oldu, neden" sorusunu cevaplar.

Yazma kuralları:
- En yeni not en üstte. Her not tek satır: `AAAA-AA-GG: ne oldu / neden`.
- Şifre, anahtar, müşteri adı, telefon, kişisel veri yazılmaz.
- 100 satırı geçerse eski ve artık geçerli olmayan notlar silinir, benzerleri birleştirilir.
- Bir not kalıcı kurala dönüştüyse (aynı şey iki kez söylendiyse) kullanıcı onayıyla AGENTS.md'ye taşınır, buradan silinir.
- Bu dosyayı yalnızca ana oturum yazar; ajanlar raporlarında not bırakır.

## Kararlar

- 2026-11-27: `.gitattributes` eklendi (`*.sh text eol=lf`) / Windows'ta CRLF'e çevrilen `sadece-hafiza.sh` bozulur, hook çökerse engelleme garantisi yok, denetçi kilidi sessizce kapanır. Doğrulandı: dizinde ve çalışma klasöründe LF.
- 2026-11-27: Ekip dosyaları commit `a4cf371` ile GitHub'a yüklendi; commit'ler `[skip ci]` ile atılır (Netlify yayın hakkı harcanmasın) ve bu repoda git kimliği GitHub gizli adresiyle ayarlı / yazar e-postası herkese açık görünür, gerçek adres açılmasın.
- 2026-11-27: Denetçi bulguları uygulandı: blog gövdeleri tek dilli istisnası, `--check` çıktısını okuma notu, Meta Pixel ve demo formun açık yazılması, `npx -y/--yes serve` onaya alındı, `.gitignore` düzeltildi, CLAUDE.md onay listesi tamamlandı / denetçi raporu, kullanıcı 1-7 maddelerini onayladı.
- 2026-11-27: "Form eklenirse" için AGENTS.md'ye 5 maddelik not eklendi / sitede şu an veri toplayan form yok, ileride kural sıfırdan yazılmasın.
- 2026-11-27: `backend-uzmani` görevi blog üretimi, yazı paneli ve yayın akışına çevrildi; araçları Read, Write, Edit, Glob, Grep, Bash ile kısıtlandı / Supabase, Meta, Resend vb. bağlayıcılara erişmesin.
- 2026-11-27: AGENTS.md bu siteye göre baştan yazıldı (Netlify, blog, iki dilli metin); Vercel/Supabase şablon kuralları çıkarıldı / site Netlify'da ve form verisi toplamıyor.
- 2026-11-27: Sitenin hedefi: ziyaretçi (işletme sahibi) önce WhatsApp'tan yazsın, ikinci seçenek Calendly'den ücretsiz görüşme ayarlasın; blog yazıları bu iki adıma yönlendirir / kullanıcı bu cümleyi verdi.
- 2026-11-27: Ajan kuralına istisna eklendi: metin düzeltmesi, tek dosyalık küçük iş ve "hızlı düzelt" ajansız yapılır; veritabanı/form işleri hep ajana gider / global ve proje CLAUDE.md çelişiyordu, kullanıcı onayladı.

## Kullanıcı tercihleri

- Küçük işte ajan kurulmaz ("hızlı düzelt" = doğrudan yap); 3'ten fazla dosya, sistem değişikliği ya da müşteri verisi varsa önce plan.
- Commit'i Claude hazırlar, mesajı ve dosya listesini önce gösterir, onay sonrası commit'ler; `git push`'u kullanıcı kendisi çalıştırır (`! git push origin main`). Claude'un terminalinde GitHub oturumu yoktur, push orada çalışmaz.
- "yayına hazırla" denince yalnızca değişen dosyaların listesi verilir.

## Açık işler

- [x] Hook gerçek ortamda denendi (2026-11-27): `kalite-denetcisi` proje köküne yazamadı, `.hook-test.tmp` oluşmadı; kendi hafıza klasörüne yazabildi.
- [x] AGENTS.md'ye "blog yazı gövdeleri yalnızca Türkçe" istisnası: "her metin iki dilli" kuralı blog yazılarıyla çelişiyor, denetçi her yazıyı işaretler.
- [x] `blog_build.py --check` uyarı verse de çıkış kodu 0 (`blog_build.py:559`); AGENTS.md'ye "çıktıdaki UYARI satırlarını oku" notu. `--check` yasal sayfaları ve index.html/shell.json eşitliğini denetlemez.
- [x] AGENTS.md ve frontend ajanında "form yok" yerine "veri toplayan form yok (demo sohbet formu `dm-form` hariç)"; Meta Pixel (`fbq`) `cerez.js`'te, çerez bölümünde açıkça yazılsın.
- [x] `settings.json`: `npx -y serve*` ve `npx --yes serve*` onaysız indirme yapar; `ask` grubuna alınsın mı?
- [x] `.gitignore`: `.netlify/` eklensin, eski `.vercel` satırı silinsin (blog çıktı satırlarıyla aynı işte, onay bekliyor).
- [x] CLAUDE.md "Sormadan yapma" listesine global kuraldaki "ödeme, şifre, giriş ayarı değişikliği" satırı eklensin.
- [x] `backend-uzmani.md:36` kuralına "`adres` alanı dosya adını belirler (JSON'da `slug` alanı yok)" cümlesi.
- [ ] `/yonetim/` panelinin GitHub girişi tarayıcıda denenmedi (Decap CMS için ayrıca OAuth kurulumu gerekir); açılıyor mu, giriş çalışıyor mu bakılacak.
- [ ] Decap CMS unpkg CDN'den yükleniyor (`site/yonetim/index.html:11`, sürüm 3.17.3 sabit); "CDN ekleme" kuralının bilinçli istisnası, önceden var.
- [ ] `settings.json`'daki `"onFailure": "block"` anahtarının geçerli olup olmadığı doğrulanmadı (betik `exit 2` ile zaten engelliyor; beklenmedik çökmede engelleme garantisi belirsiz).
- [x] `.gitignore`'a `site/blog/`, `site/sitemap.xml`, `site/robots.txt` eklensin mi? Kullanıcı onayı bekliyor; yoksa `blog_build.py --site site` çıktısı commit'e girebilir.
- [ ] `kalite-denetcisi` dört grup kullanıyor (ÖNCEDEN VAR ekli), kullanıcının kuralı üç grup; "Düzeltildi / Ertelendi / Yanlış alarm" tek satır kuralı projede yok. Hizalansın mı?
- [ ] Hook mesajları ve yorumları ASCII (Türkçe karakter yok); kullanıcının imla kuralıyla uyuşmuyor, bilerek mi bırakıldı karar verilecek.
- [ ] Yerel önizleme yöntemi belirsiz (AGENTS.md'de "doğrulanmadı"); `npx serve` ile denenecek, Node kurulu.
- [ ] `backend-uzmani` Bash'i serbest; komut sınırı yalnızca `settings.json` izinlerinde.
- [x] Yeni ekip dosyaları `kalite-denetcisi` ile denetlendi (2026-11-27): engelleyici yok, aşağıdaki "Sonra" maddeleri çıktı.
- [x] Ekip dosyaları GitHub'a yüklendi (`a4cf371`, 2026-11-27).
- [ ] `.gitattributes` commit'i (`988b11f`) yerelde hazır; push'u kullanıcı çalıştıracak. Yüklendiği doğrulanınca bu satırı `[x]` yap.
- [ ] `[skip ci]` Netlify'da gerçekten çalıştı mı? Belgede var, denenmedi: Netlify Deploys sayfasında `a4cf371` ve `988b11f` için yeni yayın görünmemeli. Görünürse yayın hakkı harcanmış demektir.
- [ ] `site/index.html` içinde mevcut satır içi `style=""` var; toplu temizlik istenmedi, yalnızca yenisi eklenmez.

## Tuzaklar

- Menü ve altbilgi iki yerde durur: `site/index.html` ve `blog/shell.json`. Biri değişirse ikisi de aynı değişsin (önce frontend, sonra backend).
- Netlify ücretsiz planda ayda en fazla 20 production deploy. Panelden her yazı bir commit, her commit bir yayın; değişiklikleri biriktir.
- Kullanıcının Windows bilgisayarında `python3` Mağaza yer tutucusudur; `python` kullan. Netlify `python3` kullanır.
- `python blog/blog_build.py --site site` komutu `site/` içine dosya yazar; üretilen dosyaları commit'e ekleme. `--check` dosya yazmaz.
- Panel alanları (`site/yonetim/config.yml`) ile `blog_build.py`'nin beklediği alanlar eşleşmeli; birini değiştiren ikisini günceller.
- Yazının adresi (dosya adı) yayınlandıktan sonra değişmez, bağlantılar bozulur.
- Ana sayfa, menü ve altbilgi iki dilli: her yeni metin hem `lang="tr"` hem `lang="en"` yazılır. Blog yazı gövdeleri yalnızca Türkçedir (istisna).
- `[skip ci]` commit mesajının ilk satırında olmalı. Etiketsiz bir sonraki commit yayın tetikler ve atlanan değişiklikleri de içerir. `/yonetim/` panelinin commit'lerinde etiket yoktur, onlar yayın hakkı harcar.
- `.sh` dosyaları LF kalmalı (`.gitattributes`); bir editör ya da Git ayarı CRLF yaparsa hook bozulur.
