#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "🌟 Yıldızopedia Tekli Binary (Executable) Derleyici"
echo "=========================================================="

# 1. Sanal ortam veya yerel Python tespiti
PYTHON_BIN="python3"
if [ -d "venv" ] && [ -f "venv/bin/python3" ]; then
    PYTHON_BIN="venv/bin/python3"
fi

echo "1. Python Bağımlılıkları Kontrol Ediliyor ($PYTHON_BIN)..."
$PYTHON_BIN -m pip install --upgrade pip
$PYTHON_BIN -m pip install aiogram pyinstaller

echo "2. Tekil Bağımsız Binary Paketleniyor (PyInstaller)..."
if [ -d "venv" ] && [ -f "venv/bin/pyinstaller" ]; then
    PYINSTALLER_BIN="venv/bin/pyinstaller"
else
    PYINSTALLER_BIN="pyinstaller"
fi

$PYINSTALLER_BIN --clean --noconfirm --onefile --name yildizopedia-bot bot/main.py

echo ""
echo "=========================================================="
echo "✅ DERLEME BAŞARIYLA TAMAMLANDI!"
echo "Oluşan Tekil Dosya: dist/yildizopedia-bot (Boyut: ~16 MB)"
echo ""
echo "Kullanım:"
echo "  1. Bu dosyayı (.env dosyasıyla aynı klasörde) çalıştırın:"
echo "     ./dist/yildizopedia-bot"
echo "  2. Sunucuya taşırken YALNIZCA bu tek dosyayı ve .env'yi atmanız yeterlidir."
echo "     Dökümanlar otomatik olarak github.com/falsisdev/yildizopedia üzerinden çekilecektir."
echo "=========================================================="
