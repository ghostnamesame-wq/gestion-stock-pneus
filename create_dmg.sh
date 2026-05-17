#!/bin/bash

# =============================================
# CREATE DMG INSTALLER FOR MACOS
# Gestion Stock Pneus
# =============================================

APP_NAME="Gestion Stock Pneus"
VERSION="1.2.0"
DMG_NAME="${APP_NAME// /_}_v${VERSION}.dmg"

echo "🚀 Création de l'installateur macOS pour ${APP_NAME}..."

# 1. Nettoyage
rm -rf build dist *.dmg
echo "🧹 Nettoyage terminé..."

# 2. Création de l'application avec PyInstaller
echo "📦 Création de l'application .app..."
pyinstaller --onefile --windowed \
    --name "${APP_NAME}" \
    --icon=icon.icns \
    --add-data "stock_pneus.json:." \
    --add-data "mouvements_stock.json:." \
    --hidden-import=tkinter \
    --clean \
    gestion_pneus.py

# 3. Vérification que l'application a été créée
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo "❌ Erreur : L'application .app n'a pas été créée."
    exit 1
fi

echo "✅ Application créée avec succès !"

# 4. Création du dossier pour le DMG
mkdir -p "dist/installer"

cp -R "dist/${APP_NAME}.app" "dist/installer/"

# 5. Création du DMG (installateur visuel)
echo "💿 Création du fichier .dmg..."

# Installation de create-dmg si nécessaire
if ! command -v create-dmg &> /dev/null; then
    echo "Installation de create-dmg..."
    brew install create-dmg
fi

create-dmg \
  --volname "${APP_NAME} Installer" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 800 500 \
  --icon-size 100 \
  --icon "${APP_NAME}.app" 200 190 \
  --hide-extension "${APP_NAME}.app" \
  --app-drop-link 600 190 \
  --background "background.png" 2>/dev/null || true \
  "${DMG_NAME}" \
  "dist/installer/"

echo "🎉 Installation terminée !"
echo "📁 Fichier créé : ${DMG_NAME}"

# Ouverture du dossier
open .