#!/bin/bash
echo "🔍 VÉRIFICATION MANUELLE DES URLs DANS LES TEMPLATES"
for template in templates/pharmacien/*.html; do
    echo "=== $template ==="
    grep -n "{% url" "$template" | while read -r line; do
        echo "  $line"
    done
done
