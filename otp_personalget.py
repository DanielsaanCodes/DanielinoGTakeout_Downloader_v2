import base64
import hashlib
import hmac
import time
import struct
import os
from dotenv import load_dotenv

# Carica il file .env
load_dotenv()



def hotp(key, counter, digits=6):
    # Decodifica la chiave dalla codifica Base32
    key_bytes = base64.b32decode(key.upper())
    
    # Converte il contatore in formato binario (8 byte, big-endian)
    counter_bytes = struct.pack(">Q", counter)
    
    # Genera l'hash HMAC-SHA1
    hmac_hash = hmac.new(key_bytes, counter_bytes, hashlib.sha1).digest()
    
    # Estrai dinamicamente un codice a 4 byte dal valore HMAC
    offset = hmac_hash[-1] & 0x0F
    truncated_hash = hmac_hash[offset:offset + 4]
    
    # Converte il valore troncato in un numero intero
    code = struct.unpack(">I", truncated_hash)[0] & 0x7FFFFFFF
    
    # Riduci il numero a "digits" cifre
    return code % (10 ** digits)

def totp(key, time_step=30, digits=6):
    # Ottieni il timestamp corrente
    current_time = int(time.time() / time_step)
    
    # Genera l'HOTP per il contatore basato sul tempo
    return hotp(key, current_time, digits)

def verify_totp(key, otp, time_step=30, digits=6, window=1):
    # Ottieni il timestamp corrente
    current_time = int(time.time() / time_step)
    
    # Verifica l'OTP rispetto al valore corrente e ai vicini (finestra)
    for i in range(-window, window + 1):
        if hotp(key, current_time + i, digits) == otp:
            return True
    return False




def getCode(g2fa_key):
    # Chiave fornita, con spazi
    key_with_spaces = g2fa_key

    # Rimuovi gli spazi dalla chiave
    clean_key = key_with_spaces.replace(' ', '')

    # Genera l'OTP per il momento attuale
    current_otp = totp(clean_key)
    print(f'Current OTP: {current_otp}')

    # Verifica l'OTP generato
    is_valid = verify_totp(clean_key, current_otp)
    if is_valid:
        print(f'OTP verified: {is_valid}')
        return current_otp
    


#getCode = getCode(g2fa_key=os.getenv('g2fa_key'))
pass