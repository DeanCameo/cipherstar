from django.urls import path
from .views import home, encrypt_text, caesar_decrypt, decrypt, substitution, substitution_decrypt_view, vigenere, vigenere_decrypt_view, choose_encryption, choose_decryption

urlpatterns = [
    path('', home, name='home'),
    path('decrypt/', decrypt, name='decrypt'),
    path('choose-encryption/', choose_encryption, name='choose_encryption'),
    path('choose_decryption/', choose_decryption, name='choose_decryption'),
    path('encrypt/caesar/', encrypt_text, name='caesar_encryption'),
    path('decrypt/caesar/', decrypt, name='caesar_decryption'),
    path('encrypt/substitution/', substitution, name='substitution_encryption'),
    path('decrypt/substitution/', substitution_decrypt_view, name='substitution_decryption'),
    path('encrypt/vigenere/', vigenere, name='vigenere_encryption'),
    path('decrypt/vigenere/', vigenere_decrypt_view, name='vigenere_decryption'),
    # path('encrypt/file/', file_encryption, name='file_encryption'),
]