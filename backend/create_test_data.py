#!/usr/bin/env python
"""
Script pour créer des données de test complètes
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockpro_backend.settings')
django.setup()

from accounts.models import User
from stores.models import Magasin
from products.models import Produit
from suppliers.models import Fournisseur
from stock.models import Stock

def create_test_data():
    """Créer des données de test complètes"""
    
    print("🏪 Création des magasins...")
    
    # Créer des magasins
    magasin1, created = Magasin.objects.get_or_create(
        nom='Magasin Centre-Ville',
        defaults={
            'adresse': '123 Rue de la République, 75001 Paris',
            'latitude': 48.8566,
            'longitude': 2.3522
        }
    )
    
    magasin2, created = Magasin.objects.get_or_create(
        nom='Magasin Banlieue',
        defaults={
            'adresse': '456 Avenue des Champs, 92000 Nanterre',
            'latitude': 48.8924,
            'longitude': 2.2069
        }
    )
    
    print("🚚 Création des fournisseurs...")
    
    # Créer des fournisseurs
    fournisseur1, created = Fournisseur.objects.get_or_create(
        nom='Fournisseur Tech',
        defaults={
            'adresse': '789 Rue de l\'Innovation, 69000 Lyon',
            'contact': '04 78 90 12 34'
        }
    )
    
    fournisseur2, created = Fournisseur.objects.get_or_create(
        nom='Fournisseur Mode',
        defaults={
            'adresse': '321 Boulevard du Style, 13000 Marseille',
            'contact': '04 91 55 66 77'
        }
    )
    
    print("📦 Création des produits...")
    
    # Créer des produits
    produit1, created = Produit.objects.get_or_create(
        reference='TECH001',
        defaults={
            'nom': 'Smartphone Galaxy',
            'categorie': 'Électronique',
            'prix_unitaire': 599.99,
            'seuil_alerte': 5,
            'fournisseur': fournisseur1
        }
    )
    
    produit2, created = Produit.objects.get_or_create(
        reference='TECH002',
        defaults={
            'nom': 'Laptop Dell',
            'categorie': 'Informatique',
            'prix_unitaire': 899.99,
            'seuil_alerte': 3,
            'fournisseur': fournisseur1
        }
    )
    
    produit3, created = Produit.objects.get_or_create(
        reference='MODE001',
        defaults={
            'nom': 'T-shirt Premium',
            'categorie': 'Vêtements',
            'prix_unitaire': 29.99,
            'seuil_alerte': 10,
            'fournisseur': fournisseur2
        }
    )
    
    produit4, created = Produit.objects.get_or_create(
        reference='MODE002',
        defaults={
            'nom': 'Jean Slim',
            'categorie': 'Vêtements',
            'prix_unitaire': 79.99,
            'seuil_alerte': 8,
            'fournisseur': fournisseur2
        }
    )
    
    print("📊 Création des stocks...")
    
    # Créer des stocks
    stocks_data = [
        (produit1, magasin1, 15),
        (produit1, magasin2, 8),
        (produit2, magasin1, 5),
        (produit2, magasin2, 12),
        (produit3, magasin1, 25),
        (produit3, magasin2, 18),
        (produit4, magasin1, 10),
        (produit4, magasin2, 6),
    ]
    
    for produit, magasin, quantite in stocks_data:
        stock, created = Stock.objects.get_or_create(
            produit=produit,
            magasin=magasin,
            defaults={'quantite': quantite}
        )
        if created:
            print(f"  ✅ Stock créé: {produit.nom} dans {magasin.nom} - {quantite} unités")
    
    print("👥 Création des utilisateurs...")
    
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
        print("  ✅ Administrateur créé: admin@stockpro.com / admin123")
    
    # Créer un employé pour chaque magasin
    employe1, created = User.objects.get_or_create(
        email='employe1@stockpro.com',
        defaults={
            'nom': 'Dupont',
            'prenom': 'Jean',
            'role': 'employe',
            'magasin': magasin1,
            'is_active': True
        }
    )
    
    if created:
        employe1.set_password('employe123')
        employe1.save()
        print(f"  ✅ Employé créé: employe1@stockpro.com / employe123 - {magasin1.nom}")
    
    employe2, created = User.objects.get_or_create(
        email='employe2@stockpro.com',
        defaults={
            'nom': 'Martin',
            'prenom': 'Marie',
            'role': 'employe',
            'magasin': magasin2,
            'is_active': True
        }
    )
    
    if created:
        employe2.set_password('employe123')
        employe2.save()
        print(f"  ✅ Employé créé: employe2@stockpro.com / employe123 - {magasin2.nom}")

if __name__ == "__main__":
    print("🚀 Création des données de test complètes...")
    print("=" * 60)
    
    create_test_data()
    
    print("\n" + "=" * 60)
    print("✅ Données de test créées avec succès!")
    print("\n📋 Comptes disponibles:")
    print("• Admin: admin@stockpro.com / admin123")
    print("• Employé 1: employe1@stockpro.com / employe123")
    print("• Employé 2: employe2@stockpro.com / employe123")
    print("\n📦 Données créées:")
    print("• 2 magasins")
    print("• 2 fournisseurs")
    print("• 4 produits")
    print("• 8 stocks")
    print("• 3 utilisateurs")