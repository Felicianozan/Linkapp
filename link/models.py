from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings



class UtilisateurManager(BaseUserManager):
    def create_user(self, email, nom, prenom, password=None):
        if not email:
            raise ValueError('Les utilisateurs doivent avoir une adresse email')
        
        user = self.model(
            email=self.normalize_email(email),
            nom=nom,       
            prenom=prenom,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user   
    
    def create_superuser(self, email, nom, prenom, password=None):
        user = self.create_user(
            email=email,
            password=password,
            nom=nom,
            prenom=prenom,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Utilisateur(AbstractBaseUser):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=255)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)  # ← AJOUTÉ
    
    objects = UtilisateurManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

class Profil(models.Model):
    nom_profil = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    statut = models.CharField(max_length=100)
    image_profil = models.ImageField(upload_to='profils/', blank=True, null=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='profils')  
    date_creation = models.DateTimeField(auto_now_add=True) 
    design = models.ForeignKey('Design', on_delete=models.SET_NULL, null=True, blank=True)  
    partage = models.ForeignKey('Partage', on_delete=models.SET_NULL, null=True, blank=True)  
    
    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils" 
    
    def __str__(self):
        return self.nom_profil

class Partage(models.Model):
    mode_partage = models.TextField()
    profils = models.ManyToManyField(Profil, related_name='partages', blank=True)  # ← AJOUTÉ
    
    class Meta:
        verbose_name = "Partage"
        verbose_name_plural = "Partages"
    
    def __str__(self):
        return f"Partage {self.id}"

class Design(models.Model):
    type_fond = models.CharField(max_length=100)
    couleur_fond = models.CharField(max_length=7)
    
    class Meta:
        verbose_name = "Design"
        verbose_name_plural = "Designs"
    
    def __str__(self): 
        return f"Design {self.id}"

class Administrateur(Utilisateur):
    
    
    class Meta:
        proxy = True
        verbose_name = "Administrateur"
        verbose_name_plural = "Administrateurs"  

class Groupe(models.Model):
    ordre_affichage = models.IntegerField()
    nom_groupe = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Groupe"
        verbose_name_plural = "Groupes"
        ordering = ['ordre_affichage']
    
    def __str__(self):
        return self.nom_groupe

class Lien(models.Model):
    titre = models.CharField(max_length=100)
    url = models.URLField()
    type_lien = models.CharField(max_length=100)
    ordre_affichage = models.IntegerField()
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='liens') 
    est_actif = models.BooleanField(default=True)  
    class Meta:
        verbose_name = "Lien"
        verbose_name_plural = "Liens"
        ordering = ['ordre_affichage']
    
    def __str__(self):
        return f"Lien {self.id} - {self.titre}"
    

class Apercu(models.Model):
    profil = models.OneToOneField(
        'Profil',
        on_delete=models.CASCADE,
        related_name='apercu',
        verbose_name="Profil associé"
    )
    photo_profil = models.ImageField(
        upload_to='apercu_photos/',
        verbose_name="Photo de profil",
        blank=True,
        null=True
    )
    nom_affichage = models.CharField(
        max_length=100,
        verbose_name="Nom à afficher"
    )
    liens = models.ManyToManyField(
        'Lien',
        through='LienApercu',
        related_name='apercus',
        verbose_name="Liens de l'aperçu",
        blank=True
    )
    
    class Meta:
        verbose_name = "Aperçu"
        verbose_name_plural = "Aperçus"
    
    def __str__(self):
        return f"Aperçu - {self.nom_affichage}"
    
    def get_photo(self):
        return self.photo_profil or self.profil.image_profil
    
    def get_liens_ordonnes(self):
        return self.liens.filter(
            lienapercu__est_actif=True
        ).order_by('lienapercu__ordre_affichage')[:6]

class LienApercu(models.Model):
    apercu = models.ForeignKey(Apercu, on_delete=models.CASCADE)
    lien = models.ForeignKey('Lien', on_delete=models.CASCADE)
    ordre_affichage = models.IntegerField(default=0)
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['ordre_affichage']
        constraints = [
            models.CheckConstraint(
                check=models.Q(ordre_affichage__gte=0) & models.Q(ordre_affichage__lte=5),
                name='ordre_affichage_0_a_5'
            )
        ]

































