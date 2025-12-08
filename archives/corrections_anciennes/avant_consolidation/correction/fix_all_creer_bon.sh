#!/bin/bash

echo "🔧 Correction de tous les templates avec 'creer_bon'..."

# Trouver tous les templates avec 'creer_bon'
find ./templates -name "*.html" -type f | while read template; do
    if grep -q "creer_bon" "$template"; then
        echo "�� Correction de: $template"
        
        # Créer une sauvegarde
        cp "$template" "${template}.backup.$(date +%s)"
        
        # CORRECTION 1: 'creer_bon' avec argument 'membre.id' (vers 'creer_bon_pour_membre')
        sed -i '' "s|{% url 'creer_bon' membre.id %}|{% url 'assureur:creer_bon_pour_membre' membre.id %}|g" "$template"
        sed -i '' "s|{% url \"creer_bon\" membre.id %}|{% url \"assureur:creer_bon_pour_membre\" membre.id %}|g" "$template"
        
        # CORRECTION 2: 'creer_bon' sans argument (vers 'creer_bon')
        sed -i '' "s|{% url 'creer_bon' %}|{% url 'assureur:creer_bon' %}|g" "$template"
        sed -i '' "s|{% url \"creer_bon\" %}|{% url \"assureur:creer_bon\" %}|g" "$template"
        
        # CORRECTION 3: 'creer_bon' dans le texte ou autres contextes
        sed -i '' "s|href=\"{% url 'creer_bon'|href=\"{% url 'assureur:creer_bon'|g" "$template"
        sed -i '' "s|href=\"{% url \"creer_bon\"|href=\"{% url \"assureur:creer_bon\"|g" "$template"
        
        echo "✅ Fichier corrigé"
    fi
done

echo "🎉 Tous les templates corrigés !"
