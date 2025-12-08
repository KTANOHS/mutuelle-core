#!/bin/bash

echo "🎬 Correction des problèmes vidéo..."
echo ""

# Créer la structure
mkdir -p static/mutuelle_core/images
mkdir -p static/mutuelle_core/videos

echo "✅ Dossiers créés:"
echo "   - static/mutuelle_core/images/"
echo "   - static/mutuelle_core/videos/"

# Vérifier les fichiers
if [ ! -f "static/mutuelle_core/videos/presentation.mp4" ]; then
    echo "❌ Fichier vidéo manquant: presentation.mp4"
    echo ""
    echo "🎯 SOLUTIONS:"
    echo "1. Utilisez une vidéo externe (recommandé):"
    echo "   <source src=\"https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4\">"
    echo ""
    echo "2. Ou ajoutez votre propre fichier:"
    echo "   mv votre_video.mp4 static/mutuelle_core/videos/presentation.mp4"
else
    echo "✅ Fichier vidéo trouvé"
fi

if [ ! -f "static/mutuelle_core/images/video-poster.jpg" ]; then
    echo "❌ Poster manquant: video-poster.jpg"
    echo ""
    echo "🖼️  Créez une image 800x450px ou utilisez CSS:"
    echo "   <div style=\"background: linear-gradient(135deg, #2c5aa0, #3a7bd5);\">"
else
    echo "✅ Poster trouvé"
fi

echo ""
echo "🚀 CODE HTML FONCTIONNEL:"
echo "Copiez-collez ceci dans votre template:"
echo ""
cat << 'EOF'

<!-- Section Vidéo Fonctionnelle -->
<section class="video-section">
    <div class="container">
        <h2 class="section-title">Découvrez Notre Engagement</h2>
        <div class="video-container">
            <div class="video-with-overlay" id="videoTrigger">
                <div style="background: linear-gradient(135deg, #2c5aa0, #3a7bd5); width: 100%; height: 400px; display: flex; align-items: center; justify-content: center; color: white; border-radius: 10px; cursor: pointer;">
                    <div style="text-align: center;">
                        <i class="fas fa-play-circle" style="font-size: 4rem; margin-bottom: 1rem;"></i>
                        <h3>MaSante Direct</h3>
                        <p>Notre engagement en vidéo</p>
                    </div>
                </div>
                <div class="play-button-overlay">
                    <i class="fas fa-play"></i>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Modal -->
<div class="video-modal" id="videoModal">
    <div class="modal-content">
        <span class="close-modal">&times;</span>
        <video controls id="mainVideo" class="modal-video">
            <source src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" type="video/mp4">
            Votre navigateur ne supporte pas la lecture de vidéos.
        </video>
    </div>
</div>
EOF

echo ""
echo "✅ Correction terminée!"