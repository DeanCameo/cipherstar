import ast
import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_protect

# -------------------------- HOME ----------------------------------

def home(request):
    return render(request, 'encrypt/home.html')

def choose_encryption(request):
    return render(request, 'encrypt/choose_encryption.html')

def choose_decryption(request):
    return render(request, 'encrypt/choose_decryption.html')

# -------------------------- CAESAR ----------------------------------

@csrf_protect
def encrypt_text(request):
    if request.method == 'POST':
        text = request.POST['text']
        shift = int(request.POST['shift'])

        encrypted_text = ""
        for char in text:
            if char.isalpha():
                shift_char = chr((ord(char.upper()) + shift - 65) % 26 + 65)
                if char.islower():
                    encrypted_text = encrypted_text + shift_char.lower()
                else:
                    encrypted_text = encrypted_text + shift_char
            else:
                encrypted_text = encrypted_text + char

        context = {'encrypted_text': encrypted_text, 'shift':shift}

        return render(request, 'encrypt/display.html', context)

    return render(request, 'encrypt/encrypt.html')


def caesar_decrypt(encrypted_text, shift):
    text = ""
    for char in encrypted_text:
        if char.isalpha():
            shift_char = chr((ord(char.lower()) - 97 - shift) % 26 + 97)
            if char.isupper():
                shift_char = shift_char.upper()
            text = text + shift_char
        else:
            text = text + char
    return text

@csrf_protect
def decrypt(request):
    if request.method == 'POST':
        encrypted_text = request.POST['encrypted_text']
        shift = int(request.POST['shift'])
        text = caesar_decrypt(encrypted_text, shift)
        context = {'text': text, 'shift': shift}
        return render(request, 'encrypt/dec_display.html', context)
    else:
        return render(request, 'encrypt/decrypt.html')


# -------------------------- SUBSTITUTION CIPHER ----------------------------------

def substitution_encrypt(text):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    shuffled_alphabet = list(alphabet)
    random.shuffle(shuffled_alphabet)
    
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            index = alphabet.index(char.upper())
            encrypted_char = shuffled_alphabet[index]
            if char.islower():
                encrypted_text += encrypted_char.lower()
            else:
                encrypted_text += encrypted_char
        else:
            encrypted_text += char

    return encrypted_text, shuffled_alphabet 


@csrf_protect
def substitution(request):
    if request.method == 'POST':
        text = request.POST['text']
        encrypted_text, shuffled_alphabet = substitution_encrypt(text)

        context = {'encrypted_text': encrypted_text, 'shuffled_alphabet': shuffled_alphabet}

        return render(request, 'encrypt/substitution_display.html', context)

    return render(request, 'encrypt/substitution.html')


def substitution_decrypt(encrypted_text, shuffled_alphabet):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    decryption_mapping = {shuffled_alphabet[i]: alphabet[i] for i in range(26)}
    
    decrypted_text = ""
    for char in encrypted_text:
        if char.isalpha():
            decrypted_char = decryption_mapping[char.upper()]
            if char.islower():
                decrypted_text += decrypted_char.lower()
            else:
                decrypted_text += decrypted_char
        else:
            decrypted_text += char

    return decrypted_text


@csrf_protect
def substitution_decrypt_view(request):
    if request.method == 'POST':
        encrypted_text = request.POST['encrypted_text']
        shuffled_alphabet_str = request.POST.get('shuffled_alphabet', '')
        
        # Parse the string representation of list into an actual list
        shuffled_alphabet = ast.literal_eval(shuffled_alphabet_str)

        decrypted_text = substitution_decrypt(encrypted_text, shuffled_alphabet)

        context = {'decrypted_text': decrypted_text}

        return render(request, 'encrypt/substitution_dec_display.html', context)

    return render(request, 'encrypt/substitution_decrypt.html')


# -------------------------- VIGENÈRE CIPHER ----------------------------------

def vigenere_encrypt(text, key):
    key = key.upper()
    encrypted_text = ""
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_index]) - 65
            if char.islower():
                encrypted_char = chr((ord(char) + shift - 97) % 26 + 97)
            else:
                encrypted_char = chr((ord(char) + shift - 65) % 26 + 65)

            encrypted_text += encrypted_char

            key_index = (key_index + 1) % len(key)
        else:
            encrypted_text += char

    return encrypted_text

def vigenere_decrypt(encrypted_text, key):
    key = key.upper()
    decrypted_text = ""
    key_index = 0

    for char in encrypted_text:
        if char.isalpha():
            shift = ord(key[key_index]) - 65
            if char.islower():
                decrypted_char = chr((ord(char) - shift - 97) % 26 + 97)
            else:
                decrypted_char = chr((ord(char) - shift - 65) % 26 + 65)

            decrypted_text += decrypted_char

            key_index = (key_index + 1) % len(key)
        else:
            decrypted_text += char

    return decrypted_text

@csrf_protect
def vigenere(request):
    if request.method == 'POST':
        text = request.POST['text']
        key = request.POST['key']
        encrypted_text = vigenere_encrypt(text, key)

        context = {'encrypted_text': encrypted_text, 'key': key}

        return render(request, 'encrypt/vigenere_display.html', context)

    return render(request, 'encrypt/vigenere.html')

@csrf_protect
def vigenere_decrypt_view(request):
    if request.method == 'POST':
        encrypted_text = request.POST['encrypted_text']
        key = request.POST['key']
        decrypted_text = vigenere_decrypt(encrypted_text, key)

        context = {'decrypted_text': decrypted_text}

        return render(request, 'encrypt/vigenere_dec_display.html', context)

    return render(request, 'encrypt/vigenere_decrypt.html')




    