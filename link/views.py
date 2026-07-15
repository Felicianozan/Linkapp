from django.shortcuts import render, redirect 
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, logout
from .forms import InscriptionForm, ConnexionForm, PartageForm

from django.views.decorators.http import require_POST,require_http_methods
from .models import Profil,Lien, Groupe, Partage

import json
import qrcode
from io import BytesIO
import base64
import uuid








def index(request):
    return render(request, 'link/index.html')

def admin_dash(request):
    return render(request, 'link/admin_dashboard.html')




def about(request):
    return render(request, 'link/about.html')


def contact(request):
    return render(request, 'link/contact.html')

def profil(request):
    return render(request, 'link/profil.html')

def lien(request):
    return render(request, 'link/lien.html')

def design(request):
    return render(request, 'link/design.html')

def partager(request):
    return render(request, 'link/partager.html')
    


def apercu(request):
    return render(request, 'link/apercu.html')





def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie !')
            return redirect('tableau_de_bord')  
    else:
        form = InscriptionForm()
        
    return render(request, 'link/inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.prenom} !')
                return redirect('tableau_de_bord')  
            else:
                messages.error(request, 'Email ou mot de passe incorrect.')
    else:
        form = ConnexionForm()
    return render(request, 'link/connexion.html', {'form': form})

def deconnexion(request):
    logout(request)
    messages.success(request, 'Déconnexion réussie.')
    return redirect('connexion') 

@login_required

def tableau_de_bord(request):
    # Récupérer le profil de l'utilisateur s'il existe
    profil = None
    if request.user.is_authenticated:
        try:
            profil = Profil.objects.get(utilisateur=request.user)
        except Profil.DoesNotExist:
            # Créer un profil par défaut s'il n'existe pas
            profil = Profil.objects.create(
                utilisateur=request.user,
                nom_profil=request.user.prenom or "Votre Prénom",
                description="Aucune description",
                statut="activé"
            )
    
    # Récupérer tous les groupes ordonnés par ordre d'affichage
    groupes = Groupe.objects.all().order_by('ordre_affichage')
    
    context = {
        'user': request.user,
        'profil': profil,
        'groupes': groupes  # Ajout des groupes ici
    }
    return render(request, 'link/dashboard.html', context)
@require_POST
@csrf_exempt

def sauvegarder_profil(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Utilisateur non authentifié'})
    
    try:
        profil, created = Profil.objects.get_or_create(
            utilisateur=request.user,
            defaults={
                'nom_profil': request.user.prenom or "Votre Prénom",
                'description': "Aucune description",
                'statut': "activé"
            }
        )
        
        # Mettre à jour les champs
        profil.nom_profil = request.POST.get('nom_profil', profil.nom_profil)
        profil.description = request.POST.get('description', profil.description)
        
        # Gérer l'upload de l'image
        if 'image_profil' in request.FILES:
            profil.image_profil = request.FILES['image_profil']
        
        profil.save()
        
        return JsonResponse({'success': True, 'message': 'Profil mis à jour avec succès'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def is_admin(user):
    return user.is_authenticated and user.is_admin

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'link/admin_dashboard.html')


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_liens(request):
    if request.method == 'GET':
        # Récupérer tous les liens
        liens = Lien.objects.all().order_by('ordre_affichage')
        data = []
        for lien in liens:
            data.append({
                'id': lien.id,
                'titre': lien.titre,
                'url': lien.url,
                'type_lien': lien.type_lien,
                'ordre_affichage': lien.ordre_affichage,
                'groupe': lien.groupe.id,
                'est_actif': lien.est_actif
            })
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        try:
            # Debug: Afficher les données reçues
            data = json.loads(request.body)
            print("Données reçues:", data)  # Debug
            
            # Validation des champs obligatoires
            required_fields = ['titre', 'url', 'type_lien', 'ordre_affichage', 'groupe']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({'error': f'Champ manquant: {field}'}, status=400)
            
            lien_id = data.get('id')
            
            if lien_id:
                # Modification
                lien = Lien.objects.get(id=lien_id)
                lien.titre = data['titre']
                lien.url = data['url']
                lien.type_lien = data['type_lien']
                lien.ordre_affichage = data['ordre_affichage']
                lien.groupe_id = data['groupe']
                lien.est_actif = data.get('est_actif', True)
                lien.save()
            else:
                # Création
                lien = Lien.objects.create(
                    titre=data['titre'],
                    url=data['url'],
                    type_lien=data['type_lien'],
                    ordre_affichage=data['ordre_affichage'],
                    groupe_id=data['groupe'],
                    est_actif=data.get('est_actif', True)
                )
            
            return JsonResponse({
                'id': lien.id,
                'titre': lien.titre,
                'url': lien.url,
                'type_lien': lien.type_lien,
                'ordre_affichage': lien.ordre_affichage,
                'groupe': lien.groupe.id,
                'est_actif': lien.est_actif
            })
            
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'JSON invalide'}, status=400)
        except Groupe.DoesNotExist:
            return JsonResponse({'error': 'Groupe non trouvé'}, status=400)
        except Exception as e:
            print("Erreur détaillée:", str(e))  # Debug
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET", "DELETE", "PATCH"])
def api_lien_detail(request, lien_id):
    try:
        lien = Lien.objects.get(id=lien_id)
        
        if request.method == 'GET':
            return JsonResponse({
                'id': lien.id,
                'titre': lien.titre,
                'url': lien.url,
                'type_lien': lien.type_lien,
                'ordre_affichage': lien.ordre_affichage,
                'groupe': lien.groupe.id,
                'est_actif': lien.est_actif
            })
            
        elif request.method == 'DELETE':
            lien.delete()
            return JsonResponse({'success': True})
            
        elif request.method == 'PATCH':
            data = json.loads(request.body)
            if 'ordre_affichage' in data:
                lien.ordre_affichage = data['ordre_affichage']
                lien.save()
            return JsonResponse({'success': True}) 
            
    except Lien.DoesNotExist:
        return JsonResponse({'error': 'Lien non trouvé'}, status=404)

def page_partage(request):
    """Page principale de partage"""
    form = PartageForm()
    return render(request, 'link/partager.html', {'form': form})

def creer_partage(request):
    """Créer un nouveau partage avec génération de QR code"""
    if request.method == 'POST':
        form = PartageForm(request.POST)
        if form.is_valid():
            # Récupérer le contenu du formulaire
            contenu = form.cleaned_data['contenu']
            
            # Créer le partage dans la base de données (sans aucun champ)
            partage = Partage.objects.create()
            
            # Générer le QR code
            qr_code_base64 = generer_qr_code_base64(contenu)
            
            # Générer un identifiant unique pour ce partage
            identifiant_unique = str(uuid.uuid4())
            
            return JsonResponse({
                'success': True,
                'partage_id': partage.id,
                'identifiant_unique': identifiant_unique,
                'contenu': contenu,
                'qr_code_base64': qr_code_base64
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

def generer_qr_code_base64(contenu):
    """Génère un QR code et retourne en base64"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(contenu)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir en base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode()

def telecharger_qr_code(request):
    """Télécharger le QR code"""
    if request.method == 'POST':
        qr_code_base64 = request.POST.get('qr_code_base64')
        identifiant_unique = request.POST.get('identifiant_unique')
        
        if qr_code_base64:
            # Convertir base64 en image
            image_data = base64.b64decode(qr_code_base64)
            response = HttpResponse(image_data, content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="qr_code_{identifiant_unique}.png"'
            return response
    
    return JsonResponse({'success': False, 'error': 'Données manquantes'})   