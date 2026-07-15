from django.contrib import admin
from django.contrib.auth.hashers import make_password
from link.models import Utilisateur, Profil, Partage, Design, Administrateur, Groupe, Lien

# Inline pour afficher les liens directement dans les groupes
class LienInline(admin.TabularInline):
    model = Lien
    extra = 1
    fields = ('titre', 'url', 'type_lien', 'ordre_affichage', 'est_actif')
    ordering = ('ordre_affichage',)

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('email', 'nom', 'prenom', 'is_active', 'is_admin', 'date_joined')
    list_filter = ('is_active', 'is_admin', 'date_joined')
    search_fields = ('email', 'nom', 'prenom')
    list_editable = ('is_active',)
    ordering = ('-date_joined',)
    list_per_page = 50
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'prenom')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('nom_profil', 'statut', 'utilisateur', 'date_creation', 'afficher_image')
    search_fields = ('nom_profil', 'utilisateur__email', 'description')
    list_filter = ('statut', 'date_creation')
    autocomplete_fields = ('utilisateur', 'design', 'partage')
    list_per_page = 50
    readonly_fields = ('afficher_image', 'date_creation')
    fieldsets = (
        (None, {'fields': ('nom_profil', 'utilisateur')}),
        ('Contenu', {'fields': ('description', 'statut', 'image_profil', 'afficher_image')}),
        ('Personnalisation', {'fields': ('design', 'partage')}),
        ('Dates', {'fields': ('date_creation',)}),
    )
    
    def afficher_image(self, obj):
        if obj.image_profil:
            return f'<img src="{obj.image_profil.url}" style="width: 50px; height: 50px; object-fit: cover;" />'
        return "Aucune image"
    afficher_image.short_description = 'Aperçu image'
    afficher_image.allow_tags = True

@admin.register(Partage)
class PartageAdmin(admin.ModelAdmin):
    list_display = ('id', 'mode_partage', 'get_nombre_profils')
    search_fields = ('mode_partage',)
    list_per_page = 50
    filter_horizontal = ('profils',)
    
    def get_nombre_profils(self, obj):
        return obj.profils.count()
    get_nombre_profils.short_description = 'Nombre de profils'

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_fond', 'couleur_fond', 'get_nombre_profils')
    list_editable = ('type_fond', 'couleur_fond')
    list_per_page = 50
    search_fields = ('type_fond', 'couleur_fond')
    
    def get_nombre_profils(self, obj):
        return obj.profil_set.count()
    get_nombre_profils.short_description = 'Profils utilisant ce design'

@admin.register(Administrateur)
class AdministrateurAdmin(admin.ModelAdmin):
    list_display = ('email', 'nom', 'prenom', 'get_date_creation', 'is_active')
    search_fields = ('email', 'nom', 'prenom')
    list_filter = ('is_active', 'date_joined')
    ordering = ('nom', 'prenom')
    list_per_page = 50
    
    def get_date_creation(self, obj):
        return obj.date_joined
    get_date_creation.short_description = 'Date de création'
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_admin=True)

@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display = ('nom_groupe', 'ordre_affichage', 'get_nombre_liens')
    ordering = ('ordre_affichage',)
    search_fields = ('nom_groupe',)
    list_per_page = 50
    list_editable = ('ordre_affichage',)
    inlines = [LienInline]
    
    def get_nombre_liens(self, obj):
        return obj.liens.count()
    get_nombre_liens.short_description = 'Nombre de liens'

@admin.register(Lien)
class LienAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_lien', 'ordre_affichage', 'groupe', 'est_actif', 'url_truncated')
    list_filter = ('type_lien', 'groupe', 'est_actif')
    ordering = ('ordre_affichage',)
    search_fields = ('titre', 'url', 'groupe__nom_groupe')
    list_editable = ('ordre_affichage', 'est_actif', 'type_lien')
    autocomplete_fields = ('groupe',)
    list_per_page = 50
    fieldsets = (
        (None, {'fields': ('titre', 'url', 'type_lien')}),
        ('Organisation', {'fields': ('groupe', 'ordre_affichage', 'est_actif')}),
    )
    
    def url_truncated(self, obj):
        return obj.url[:50] + '...' if len(obj.url) > 50 else obj.url
    url_truncated.short_description = 'URL'
    
    actions = ['activer_liens', 'desactiver_liens']
    
    def activer_liens(self, request, queryset):
        updated = queryset.update(est_actif=True)
        self.message_user(request, f"{updated} lien(s) activé(s) avec succès.")
    
    def desactiver_liens(self, request, queryset):
        updated = queryset.update(est_actif=False)
        self.message_user(request, f"{updated} lien(s) désactivé(s) avec succès.")
    
    activer_liens.short_description = "Activer les liens sélectionnés"
    desactiver_liens.short_description = "Désactiver les liens sélectionnés"

# Personnalisation de l'interface d'administration
admin.site.site_header = "Administration de l'application Link"
admin.site.site_title = "Plateforme Link"
admin.site.index_title = "Tableau de bord"

