#!/bin/sh
rm -rf build
mkdir -p build/usr/bin/multisekai
cp -a deb/. build/
cp -a source/. build/usr/bin/multisekai
dpkg-deb --build -Zgzip -z9 build/