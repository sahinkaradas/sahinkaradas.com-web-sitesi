/* sahinkaradas.com: çerez tercihi ve Meta Pikseli. Ziyaretçi izin vermeden piksel yüklenmez. */
(function () {
  'use strict';
  var PIXEL = '1121732379127113';
  var TXT = {"bar": ["Siteyi çalıştırmak için gerekenler dışında çerez kullanmıyorum. İzin verirseniz reklamlarımın sonucunu ölçmek için Meta Pikseli'ni çalıştırırım. Bu durumda ziyaret bilgileriniz yurt dışındaki Meta sunucularına gider.", "I don't use cookies beyond what's needed to run the site. If you allow it, I run the Meta Pixel to measure my ad results. In that case your visit information goes to Meta's servers abroad."], "intro": ["Hangi çerezlere izin verdiğinizi buradan seçebilirsiniz. Seçiminizi istediğiniz zaman sayfanın altındaki \"Çerez ayarları\" bağlantısından değiştirebilirsiniz.", "Choose which cookies you allow. You can change your choice any time with the \"Cookie settings\" link at the bottom of the page."], "nec": ["Dil, tema ve çerez tercihinizi cihazınızda hatırlar. Hiçbir yere gönderilmez.", "Remembers your language, theme and cookie choice on your device. Nothing is sent anywhere."], "mkt": ["Reklamlarımın sonucunu ölçmek ve siteyi ziyaret edenlere Instagram / Facebook'ta reklam göstermek için kullanılır. Açarsanız ziyaret bilgileriniz yurt dışındaki Meta sunucularına aktarılır.", "Used to measure my ad results and to show ads on Instagram / Facebook to site visitors. If you turn it on, your visit information is transferred to Meta's servers abroad."], "title": ["Çerez tercihiniz", "Your cookie choice"], "no": ["Reddet", "Reject"], "set": ["Ayarlar", "Settings"], "yes": ["Kabul et", "Accept"], "dtitle": ["Çerez ayarları", "Cookie settings"], "nect": ["Zorunlu", "Necessary"], "always": ["Her zaman açık", "Always on"], "mktt": ["Pazarlama: Meta Pikseli", "Marketing: Meta Pixel"], "noall": ["Tümünü reddet", "Reject all"], "save": ["Seçimimi kaydet", "Save my choice"], "yesall": ["Tümünü kabul et", "Accept all"]};
  var KEY = 'sk-consent', KEEP = 182 * 864e5;   // tercih 6 ay hatırlanır, sonra yeniden sorulur
  var me = document.currentScript;
  var ROOT = me && me.hasAttribute('data-root') ? me.getAttribute('data-root') : '/';
  var ART = !!me && me.getAttribute('data-kind') === 'art';
  var root = document.documentElement, body = document.body;
  var X = '<svg aria-hidden="true" focusable="false" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>';

  function page(p) { return ROOT + p + (ART ? 'index.html' : ''); }
  function T(k) { var v = TXT[k] || [k, k]; return '<span lang="tr">' + v[0] + '</span><span lang="en">' + v[1] + '</span>'; }
  function L(tr, trText, en, enText) { return '<a lang="tr" href="' + page(tr) + '">' + trText + '</a><a lang="en" href="' + page(en) + '">' + enText + '</a>'; }
  function isEn() { return body.getAttribute('data-lang') === 'en'; }

  function read() {
    try {
      var c = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (c && c.v === 1 && typeof c.m === 'boolean' && Date.now() - c.t < KEEP) return c;
    } catch (e) {}
    return null;
  }
  function save(m) { try { localStorage.setItem(KEY, JSON.stringify({ v: 1, m: m, t: Date.now() })); } catch (e) {} }

  // ---- Meta Pikseli: yalnızca izin verildiğinde ----
  var loaded = false;
  function pixel() {
    if (loaded || ART || !/^\d{6,20}$/.test(PIXEL)) return;   // claude.ai önizlemesinde piksel hiç çalışmaz
    loaded = true;
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', PIXEL);
    window.fbq('track', 'PageView');
  }
  // WhatsApp ve randevu butonlarına tıklama (yalnızca piksel çalışıyorsa)
  document.addEventListener('click', function (e) {
    if (!loaded || !window.fbq) return;
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    if (/^https:\/\/(wa\.me|api\.whatsapp\.com)\//.test(a.href)) window.fbq('track', 'Contact');
    else if (/^https:\/\/calendly\.com\//.test(a.href)) window.fbq('track', 'Schedule');
  }, true);
  function dropCookies() {
    var h = location.hostname, p = h.split('.'), doms = ['', h, '.' + h];
    if (p.length > 2) doms.push('.' + p.slice(-2).join('.'));
    ['_fbp', '_fbc'].forEach(function (n) {
      doms.forEach(function (d) { document.cookie = n + '=; Max-Age=0; path=/' + (d ? '; domain=' + d : ''); });
    });
  }
  function decide(m) {
    save(m);
    hideBar();
    if (m) { pixel(); return; }
    dropCookies();
    if (loaded) location.reload();   // çalışan piksel sayfadan ancak yenileyerek çıkar
  }

  // ---- bildirim kutusu ----
  var bar = null;
  function showBar() {
    if (bar) return;
    bar = document.createElement('section');
    bar.className = 'ck';
    bar.id = 'ck';
    bar.setAttribute('aria-labelledby', 'ck-h');
    bar.innerHTML =
      '<h2 id="ck-h">' + T('title') + '</h2>' +
      '<p>' + T('bar') + '</p>' +
      '<p class="ck-links">' + L('cerez-politikasi/', 'Çerez Politikası', 'en/cookies/', 'Cookie Policy') +
        L('acik-riza/', 'Açık Rıza Metni', 'en/consent/', 'Explicit Consent Text') + '</p>' +
      '<div class="ck-row">' +
        '<button type="button" class="ck-b" data-ck="no">' + T('no') + '</button>' +
        '<button type="button" class="ck-b ol" data-ck="set">' + T('set') + '</button>' +
        '<button type="button" class="ck-b" data-ck="yes">' + T('yes') + '</button>' +
      '</div>';
    body.insertBefore(bar, body.firstChild);
    root.classList.add('ck-on');
  }
  function hideBar() {
    if (bar && bar.parentNode) bar.parentNode.removeChild(bar);
    bar = null;
    root.classList.remove('ck-on');
  }

  // ---- ayarlar paneli ----
  var dlg = null, opener = null;
  function build() {
    dlg = document.createElement('dialog');
    dlg.className = 'ckd';
    dlg.id = 'ckd';
    dlg.setAttribute('aria-labelledby', 'ckd-h');
    dlg.innerHTML =
      '<div class="ckd-in">' +
        '<div class="ckd-hd"><h2 id="ckd-h">' + T('dtitle') + '</h2><button type="button" class="ckd-x" data-ck="close">' + X + '</button></div>' +
        '<p>' + T('intro') + '</p>' +
        '<div class="ck-opt"><h3>' + T('nect') + '</h3><span class="ck-always">' + T('always') + '</span><p>' + T('nec') + '</p></div>' +
        '<div class="ck-opt"><h3><label for="ck-m">' + T('mktt') + '</label></h3>' +
          '<input type="checkbox" role="switch" class="ck-sw" id="ck-m" aria-describedby="ck-m-d">' +
          '<p id="ck-m-d">' + T('mkt') + ' ' + L('acik-riza/', 'Açık Rıza Metni', 'en/consent/', 'Explicit Consent Text') + '</p></div>' +
        '<div class="ckd-row">' +
          '<button type="button" class="ck-b" data-ck="no">' + T('noall') + '</button>' +
          '<button type="button" class="ck-b ol" data-ck="save">' + T('save') + '</button>' +
          '<button type="button" class="ck-b" data-ck="yes">' + T('yesall') + '</button>' +
        '</div>' +
      '</div>';
    body.appendChild(dlg);
    dlg.addEventListener('close', function () {
      if (opener && opener.focus && document.body.contains(opener)) opener.focus();
      opener = null;
    });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) closeDlg(); });   // dışına tıklayınca kapanır
  }
  function openDlg(from) {
    if (!dlg) build();
    var c = read();
    dlg.querySelector('#ck-m').checked = !!(c && c.m);
    dlg.querySelector('.ckd-x').setAttribute('aria-label', isEn() ? 'Close' : 'Kapat');
    opener = from || document.activeElement;
    if (dlg.showModal) { if (!dlg.open) dlg.showModal(); } else dlg.setAttribute('open', '');
  }
  function closeDlg() {
    if (!dlg || !dlg.open) return;
    if (dlg.close) dlg.close(); else dlg.removeAttribute('open');
  }

  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('[data-ck],[data-act="cookies"]');
    if (!t) return;
    if (t.getAttribute('data-act') === 'cookies') { e.preventDefault(); openDlg(t); return; }
    var k = t.getAttribute('data-ck');
    if (k === 'yes') { closeDlg(); decide(true); }
    else if (k === 'no') { closeDlg(); decide(false); }
    else if (k === 'set') openDlg(t);
    else if (k === 'save') { var m = dlg.querySelector('#ck-m').checked; closeDlg(); decide(m); }
    else if (k === 'close') closeDlg();
  });

  var c = read();
  if (c) { if (c.m) pixel(); }
  else showBar();
})();
