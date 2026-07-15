from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

class InscriptionForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Entrez votre {field}'
            }) 

class ConnexionForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Votre email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Votre mot de passe'
    }))
      
class PartageForm(forms.Form):
    contenu = forms.CharField(
        label="Votre lien ou texte à partager",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com ou un lien',
            'rows': 3,
            'required': True
        })
    )
   