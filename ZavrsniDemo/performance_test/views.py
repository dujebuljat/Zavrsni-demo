import base64
import concurrent.futures
import io
import os
import time
import urllib

import matplotlib.pyplot as plt
import psutil
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from django.shortcuts import render


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

    # Početna mjerenja CPU-a
    initial_cpu_percent = psutil.cpu_percent(interval=None, percpu=True)

    total_time = 0
    min_time = float('inf')
    max_time = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(perform_encryption_decryption) for _ in range(500)]  # 500 paralelnih poziva

    results = [f.result() for f in futures]

    for success, exec_time in results:
        total_time += exec_time
        if exec_time < min_time:
            min_time = exec_time
        if exec_time > max_time:
            max_time = exec_time

    avg_time = total_time / len(futures)
    execution_time_total = round(time.time() - start_time, 2)  # Ukupno vrijeme za sve zahtjeve

    # Završna mjerenja CPU-a
    final_cpu_percent = psutil.cpu_percent(interval=None, percpu=True)

    # Numeracija jezgri (od 1 do n)
    cores = range(1, len(initial_cpu_percent) + 1)

    # Grafički prikaz CPU opterećenja
    plt.figure(figsize=(6, 3))
    plt.plot(cores, initial_cpu_percent, label='Initial CPU Percent', color='blue', marker='o')
    plt.plot(cores, final_cpu_percent, label='Final CPU Percent', color='red', marker='o')
    plt.xlabel('CPU Core')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage Before and After Execution')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Pretvorba grafika u sliku za HTML prikaz
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    return render(request, 'performance_test/cpu_graph.html', {
        'cpu_usage_graph': uri,
        'total_execution_time': execution_time_total,
        'average_time_per_request': round(avg_time, 6),
        'min_time': round(min_time, 6),
        'max_time': round(max_time, 6)
    })
