#!/usr/bin/env python
"""
CORRECTIF SPÉCIFIQUE POUR FIREFOX
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def fix_login_template():
    """Corrige le template de login pour Firefox"""
    print("🔧 Correction du template login pour Firefox...")
    
    login_path = BASE_DIR / 'templates' / 'registration' / 'login.html'
    
    if not login_path.exists():
        print("❌ login.html non trouvé")
        return
    
    # Template corrigé
    corrected_template = """{% extends 'base.html' %}

{% block title %}Connexion - Mutuelle{% endblock %}

{% block extra_css %}
<style>
/* Reset cross-browser */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    width: 100%;
    height: 100%;
    overflow-x: hidden;
}

/* Correctifs spécifiques Firefox */
@-moz-document url-prefix() {
    body {
        display: block;
        width: 100vw;
    }
    
    .login-container {
        display: flex !important;
        min-height: 100vh;
        width: 100%;
        margin: 0;
        padding: 20px;
    }
    
    .login-card {
        margin: auto;
        width: 100%;
        max-width: 400px;
    }
    
    input, button {
        -moz-appearance: none;
        border-radius: 0;
    }
    
    input:focus, button:focus {
        outline: 2px solid #007bff;
    }
}

/* Styles communs */
.login-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
}

.login-card {
    background: white;
    border-radius: 15px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    padding: 2.5rem;
    width: 100%;
    max-width: 400px;
}

.login-header {
    text-align: center;
    margin-bottom: 2rem;
}

.login-header h2 {
    color: #333;
    margin-bottom: 0.5rem;
    font-size: 1.8rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-control {
    width: 100%;
    padding: 1rem;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
    line-height: 1.5;
}

.form-control:focus {
    border-color: #007bff;
    box-shadow: 0 0 0 0.2rem rgba(0,123,255,0.25);
    outline: none;
}

.btn-login {
    width: 100%;
    padding: 1rem;
    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    line-height: 1.2;
}

.btn-login:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,123,255,0.3);
}

/* Responsive */
@media (max-width: 480px) {
    .login-card {
        margin: 10px;
        padding: 1.5rem;
    }
    
    .login-header h2 {
        font-size: 1.5rem;
    }
}
</style>
{% endblock %}

{% block content %}
<div class="login-container">
    <div class="login-card">
        <div class="login-header">
            <h2><i class="fas fa-lock"></i> Connexion</h2>
            <p>Accédez à votre espace mutuelle</p>
        </div>
        
        {% if form.errors %}
        <div class="alert alert-danger" style="background: #f8d7da; color: #721c24; padding: 0.75rem; border-radius: 5px; margin-bottom: 1rem;">
            <i class="fas fa-exclamation-triangle"></i> Identifiant ou mot de passe incorrect.
        </div>
        {% endif %}
        
        <form method="post" action="{% url 'login' %}">
            {% csrf_token %}
            
            <div class="form-group">
                <label for="id_username" class="form-label" style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Nom d'utilisateur</label>
                <input type="text" name="username" id="id_username" class="form-control" 
                       required autofocus placeholder="Votre nom d'utilisateur">
            </div>
            
            <div class="form-group">
                <label for="id_password" class="form-label" style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Mot de passe</label>
                <input type="password" name="password" id="id_password" class="form-control" 
                       required placeholder="Votre mot de passe">
            </div>
            
            <div class="form-group" style="margin-bottom: 1.5rem;">
                <input type="checkbox" name="remember_me" id="remember_me" style="margin-right: 0.5rem;">
                <label for="remember_me">Se souvenir de moi</label>
            </div>
            
            <button type="submit" class="btn-login">
                <i class="fas fa-sign-in-alt"></i> Se connecter
            </button>
        </form>
    </div>
</div>

<script>
// Correctif JavaScript pour Firefox
if (navigator.userAgent.toLowerCase().includes('firefox')) {
    document.addEventListener('DOMContentLoaded', function() {
        // Force le reflow pour corriger l'affichage
        setTimeout(function() {
            document.body.style.display = 'block';
            const container = document.querySelector('.login-container');
            if (container) {
                container.style.minHeight = '100vh';
                container.style.width = '100%';
            }
        }, 100);
    });
}
</script>
{% endblock %}"""

    with open(login_path, 'w', encoding='utf-8') as f:
        f.write(corrected_template)
    
    print("✅ Template login corrigé pour Firefox")

if __name__ == "__main__":
    fix_login_template()
    print("🎉 Correctifs appliqués ! Testez sur Firefox.")