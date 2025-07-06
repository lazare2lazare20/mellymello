#!/usr/bin/env python3
"""
Serveur HTTP simple pour servir le site web du restaurant Melly Mello
Auteur: Assistant IA
Usage: python main.py
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Configuration du serveur
PORT = 8000
HOST = 'localhost'
HTML_FILE = 'jeu1.html'

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personnalisé pour servir les fichiers HTML"""
    
    def end_headers(self):
        # Ajouter des headers pour éviter les problèmes de cache
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_GET(self):
        # Si la racine est demandée, servir le fichier HTML principal
        if self.path == '/':
            self.path = f'/{HTML_FILE}'
        return super().do_GET()

def create_html_file():
    """Créer le fichier HTML s'il n'existe pas"""
    if not os.path.exists(HTML_FILE):
        print(f"⚠️  Le fichier {HTML_FILE} n'existe pas.")
        print("📝 Veuillez copier le code HTML du site Melly Mello dans un fichier nommé 'index.html'")
        print("   dans le même dossier que ce script Python.")
        return False
    return True

def check_port_available(port):
    """Vérifier si le port est disponible"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, port))
            return True
        except socket.error:
            return False

def find_available_port(start_port=8000, max_attempts=10):
    """Trouver un port disponible"""
    for port in range(start_port, start_port + max_attempts):
        if check_port_available(port):
            return port
    return None

def start_server():
    """Démarrer le serveur HTTP"""
    
    print("🍽️  Serveur web pour le restaurant Melly Mello")
    print("=" * 50)
    
    # Vérifier que le fichier HTML existe
    if not create_html_file():
        sys.exit(1)
    
    # Trouver un port disponible
    available_port = find_available_port(PORT)
    if not available_port:
        print(f"❌ Impossible de trouver un port disponible à partir de {PORT}")
        sys.exit(1)
    
    if available_port != PORT:
        print(f"⚠️  Le port {PORT} n'est pas disponible, utilisation du port {available_port}")
    
    try:
        # Créer et configurer le serveur
        with socketserver.TCPServer((HOST, available_port), CustomHTTPRequestHandler) as httpd:
            server_url = f"http://{HOST}:{available_port}"
            
            print(f"🚀 Serveur démarré avec succès !")
            print(f"📍 URL: {server_url}")
            print(f"📁 Dossier servi: {os.getcwd()}")
            print(f"📄 Fichier principal: {HTML_FILE}")
            print("\n🌐 Ouverture automatique du navigateur...")
            print("\n⏹️  Pour arrêter le serveur, appuyez sur Ctrl+C")
            print("=" * 50)
            
            # Ouvrir le navigateur automatiquement
            try:
                webbrowser.open(server_url)
                print("✅ Navigateur ouvert avec succès")
            except Exception as e:
                print(f"⚠️  Impossible d'ouvrir le navigateur automatiquement: {e}")
                print(f"🔗 Ouvrez manuellement: {server_url}")
            
            # Démarrer le serveur
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt du serveur demandé par l'utilisateur")
        print("👋 Au revoir !")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")
        sys.exit(1)

def main():
    """Fonction principale"""
    try:
        start_server()
    except Exception as e:
        print(f"💥 Erreur critique: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()