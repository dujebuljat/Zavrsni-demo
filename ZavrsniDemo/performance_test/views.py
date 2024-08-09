from django.http import JsonResponse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import time
import concurrent.futures

# Funkcija za generiranje slučajnog stringa
def generate_random_string(length):
    return os.urandom(length).hex()

# Funkcija za kriptiranje stringa koristeći AES
def encrypt_string_aes(random_string):
    key = get_random_bytes(16)  # 16 bajtova za AES-128
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(random_string.encode())
    return key, cipher.nonce, ciphertext, tag

# Funkcija za dekriptiranje stringa koristeći AES
def decrypt_string_aes(key, nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try:
        decrypted_string = cipher.decrypt_and_verify(ciphertext, tag).decode()
        return decrypted_string
    except ValueError:
        return None

# Funkcija koja vrši cijeli proces i mjeri vrijeme
def perform_encryption_decryption():
    random_string = generate_random_string(5000)  # Generiraj slučajni string od 5000 znakova
    start_time = time.time()
    key, nonce, ciphertext, tag = encrypt_string_aes(random_string)  # Kriptiraj string
    decrypted_string = decrypt_string_aes(key, nonce, ciphertext, tag)  # Dekriptiraj string
    end_time = time.time()
    return decrypted_string == random_string, end_time - start_time

# Glavni view za testiranje performansi
def test_performance(request):
    start_time = time.time()  # Započni mjerenje ukupnog vremena

    total_time = 0
    min_time = float('inf')
    max_time = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(perform_encryption_decryption) for _ in range(1000)]  # 1000 paralelnih poziva

    results = [f.result() for f in futures]

    for success, exec_time in results:
        total_time += exec_time
        if exec_time < min_time:
            min_time = exec_time
        if exec_time > max_time:
            max_time = exec_time

    avg_time = total_time / len(futures)
    execution_time_total = round(time.time() - start_time, 2)  # Ukupno vrijeme za sve zahtjeve

    return JsonResponse({
        'total_execution_time': execution_time_total,
        'average_time_per_request': round(avg_time, 6),
        'min_time': round(min_time, 6),
        'max_time': round(max_time, 6)
    })
