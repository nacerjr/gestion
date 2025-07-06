#!/usr/bin/env python
"""
Script pour créer des utilisateurs de test
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockpro_backend.settings')
django.setup()

from accounts.models import User
from stores.models import Magasin

def create_test_users():
    """Créer des utilisateurs de test"""
    
    # Créer un magasin de test si nécessaire
    magasin, created = Magasin.objects.get_or_create(
        nom='Magasin Test',
        defaults={
            'adresse': '123 Rue de Test, 75001 Paris',
            'latitude': 48.8566,
            'longitude': 2.3522
        }
    )
    
    # Créer un administrateur
    admin_user, created = User.objects.get_or_create(
        email='admin@stockpro.com',
        defaults={
            'nom': 'Admin',
            'prenom': 'StockPro',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✅ Administrateur créé:")
        print("   Email: admin@stockpro.com")
        print("   Mot de passe: admin123")
    else:
        print("ℹ️  Administrateur existe déjà")
    
    # Créer un employé
    employe_user, created = User.objects.get_or_create(
        email='employe@stockpro.com',
        defaults={
            'nom': 'Dupont',
            'prenom': 'Jean',
            'role': 'employe',
            'magasin': magasin,
            'is_active': True
        }
    )
    
    if created:
        employe_user.set_password('employe123')
        employe_user.save()
        print("✅ Employé créé:")
        print("   Email: employe@stockpro.com")
        print("   Mot de passe: employe123")
        print(f"   Magasin: {magasin.nom}")
    else:
        print("ℹ️  Employé existe déjà")

if __name__ == "__main__":
    print("🚀 Création des utilisateurs de test...")
    print("=" * 50)
    
    create_test_users()
    
    print("\n" + "=" * 50)
    print("✅ Utilisateurs de test créés!")
    print("\n📋 Vous pouvez maintenant vous connecter avec:")
    print("• Admin: admin@stockpro.com / admin123")
    print("• Employé: employe@stockpro.com / employe123")