#!/usr/bin/env bash
# Kilit: kalite-denetcisi yalnizca BU projenin kendi hafiza klasorune yazabilir.
# Ana oturum ve diger ajanlar etkilenmez. Denetcinin istegindeki HER yol
# izinli klasorde olmali; aksi halde, ".." iceren yolda ya da yol bulunamazsa engellenir (exit 2).
girdi=$(cat | tr -d '\n')

# Istekte herhangi bir yerde denetci geciyorsa kilit devrede (kasitli olarak temkinli).
# Kacis karakterine dayanikli: "kalite" ile "denetcisi" arasinda ne olursa olsun yakalar (kalite\u002ddenetcisi gibi).
printf '%s' "$girdi" | grep -q '"agent_type"[[:space:]]*:[[:space:]]*"kalite[^"]*denetcisi"' || exit 0

# Windows'ta (Git Bash) yollar harf duyarsizdir ve C:\ ile /c/ ayni yerdir; baska sistemlerde dokunma.
case "$(uname -s 2>/dev/null)" in MINGW*|MSYS*|CYGWIN*) win=1 ;; *) win=0 ;; esac
duz() {
  local p; p=$(printf '%s' "$1" | sed 's#\\\\#/#g; s#\\#/#g')
  if [ "$win" = 1 ]; then p=$(printf '%s' "$p" | tr 'A-Z' 'a-z' | sed -E 's#^([a-z]):/#/\1/#'); fi
  printf '%s' "$p"
}
kok=$(duz "${CLAUDE_PROJECT_DIR:-}")
izinli="${kok%/}/.claude/agent-memory/kalite-denetcisi/"
red() { echo "Denetci proje dosyalarini degistiremez. Bulguyu raporla; duzeltmeyi ana oturum yapsin." >&2; exit 2; }
[ -n "$kok" ] || red

sayi=0
yollar=$(printf '%s' "$girdi" | grep -oE '"(file_path|notebook_path)"[[:space:]]*:[[:space:]]*"[^"]*"')
# Kacisli yol ("\u" ya da "\"") temkinli olarak reddedilir.
case "$yollar" in *'\u'*|*'\"'*) red ;; esac
eski_ifs=$IFS; IFS='
'
for ham in $yollar; do
  yol=$(duz "$(printf '%s' "$ham" | sed 's/.*:[[:space:]]*"\(.*\)"$/\1/')")
  case "$yol" in *..*) red ;; "$izinli"*) sayi=$((sayi+1)) ;; *) red ;; esac
done
IFS=$eski_ifs
[ "$sayi" -gt 0 ] || red
exit 0
