#!/bin/bash

PRGNAM="SoundTagger"
VERSION=$(grep -Eo "([0-9]{2}.){2}[0-9]{2}" src/about.py)
DESTDIR=${DESTDIR:-''}
DOCDIR=${DOCDIR:-"/usr/share/doc"}

# shellcheck disable=SC2015
test -z "$DESTDIR" && {
  mkdir -p "/usr/share/$PRGNAM/{backgrounds,icons,lang,notification}" "$DOCDIR/$PRGNAM-$VERSION"
} || {
  mkdir -p "$DESTDIR/usr/share/$PRGNAM/{backgrounds,icons,lang,notification}" \
           "$DESTDIR/$DOCDIR/$PRGNAM-$VERSION" \
           "$DESTDIR/usr/{bin,share/{applications,pixmaps}}"
}

install -Dm 0644 common/"$PRGNAM".desktop "$DESTDIR/usr/share/applications"
install -Dm 0644 common/"$PRGNAM".png     "$DESTDIR/usr/share/pixmaps"

install -Dm 0644 backgrounds/*  "$DESTDIR/usr/share/$PRGNAM/backgrounds"
install -Dm 0644 icons/*        "$DESTDIR/usr/share/$PRGNAM/icons"
#install -Dm 0644 lang/*         "$DESTDIR/usr/share/$PRGNAM/lang"
install -Dm 0644 notification/* "$DESTDIR/usr/share/$PRGNAM/notification"

cp -a changelog LICENSE README.md "$DESTDIR/$DOCDIR/$PRGNAM-$VERSION"
cp -Tr src "$DESTDIR/usr/share/$PRGNAM"

echo -e "#!/bin/bash
cd /usr/share/$PRGNAM/src

python3 main.py \"\$@\" || exit 1
" > "$DESTDIR/usr/bin/$PRGNAM"

chmod 755 "$DESTDIR"/usr/bin/"$PRGNAM"