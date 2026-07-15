
from django.contrib import admin
from django.urls import path

from  link  import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name="home"),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('tableau-de-bord/', views.tableau_de_bord, name='tableau_de_bord'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('a-propos/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profil/', views.profil, name='profil'),
    path('lien/', views.lien, name='lien'),
    path('design/', views.design, name='design'),
    path('partager/', views.partager, name='partager'),
    path('apercu/', views.apercu, name='apercu'),
    path('profil/sauvegarder/', views.sauvegarder_profil, name='sauvegarder_profil'),
    path('api/liens/', views.api_liens, name='api_liens'),
    path('api/liens/<int:lien_id>/', views.api_lien_detail, name='api_lien_detail'),
    path('partager/', views.page_partage, name='page_partage'),
    path('creer-partage/', views.creer_partage, name='creer_partage'),
    path('telecharger-qr-code/', views.telecharger_qr_code, name='telecharger_qr_code'),
    path('admin_dash/', views.admin_dash, name='lien'),
                     
     
]                                                                                                                     
   





                        