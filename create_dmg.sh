#!/bin/bash

# =============================================
# CREATE DMG - VERSION SIMPLIFIÉE
# Pour distribution internet (hors App Store)
# =============================================

APP_NAME="Gestion Stock Pneus"
VERSION="1.2.0"
DMG_NAME="${APP_NAME// /_}_v${VERSION}.dmg"

echo "🚀 Création de l'installateur macOS simplifié..."

# Nettoyage
rm -rf build dist *.dmg 2>/dev/null

# Installation des outils si nécessaire
if ! command -v pyinstaller &> /dev/null; then
    echo "Installation de PyInstaller..."
    pip install pyinstaller
fi

if ! command -v create-dmg &> /dev/null; then
    echo "Installation de create-dmg..."
    brew install create-dmg
fi

# ====================== CRÉATION DE L'APPLICATION ======================
echo "📦 Création de l'application .app..."

pyinstaller --onefile --windowed \
    --name "${APP_NAME}" \
    --add-data "stock_pneus.json:." \
    --add-data "mouvements_stock.json:." \
    --hidden-import=tkinter \
    --clean \
    gestion_pneus.py

# Vérification
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo "❌ Erreur lors de la création de l'application"
    exit 1
fi

echo "✅ Application créée avec succès !"

# ====================== CRÉATION DU DMG ======================
echo "💿 Création du fichier .dmg pour distribution..."

mkdir -p "dist/installer"
cp -R "dist/${APP_NAME}.app" "dist/installer/"

create-dmg \
  --volname "${APP_NAME} v${VERSION}" \
  --window-pos 200 120 \
  --window-size 820 500 \
  --icon-size 90 \
  --icon "${APP_NAME}.app" 200 180 \
  --hide-extension "${APP_NAME}.app" \
  --app-drop-link 600 180 \
  --no-internet-enable \
  "${DMG_NAME}" \
  "dist/installer/"

if [ -f "${DMG_NAME}" ]; then
    echo ""
    echo "🎉 SUCCÈS ! Ton installateur est prêt :"
    echo "   📁 ${DMG_NAME}"
    echo ""
    echo "Tu peux maintenant le mettre en téléchargement sur ton site web."
    open .
else
    echo "⚠️ Erreur lors de la création du DMG"
fi
