import time
import os
from playwright.sync_api import sync_playwright
from otp_personalget import getCode
from danio_telegramExtension import SendToTelegram
import shutil
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def run(playwright, url_file, google_passw, g2fa_key):
    mode = "login"

    browser = playwright.chromium.launch(
        headless=False,
        args=[
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--disable-setuid-sandbox',
            '--no-first-run',
            '--no-sandbox',
            '--no-zygote',
            '--ignore-certificate-errors',
            '--disable-extensions',
            '--disable-infobars',
            '--disable-notifications',
            '--disable-popup-blocking',
            '--remote-debugging-port=9222',
            '--disable-blink-features=AutomationControlled'
        ]
    )
    context = browser.new_context()
    page = context.new_page()

    isDownloaded = False

    if mode == "login":
        try:
            # Naviga all'URL fornito
            page.goto(url_file)
            time.sleep(2)
            page.get_by_role("button", name="Avanti").click()
            time.sleep(1)
            page.get_by_label("Inserisci la password").fill(google_passw)
            time.sleep(1)
            page.get_by_role("button", name="Avanti").click()
            time.sleep(2)
            try:
                page.get_by_role("button", name="Prova un altro metodo").click(timeout=3000)
                print("skippo pagina prova un altro metodo - fix settembre 2024")
            except PlaywrightTimeoutError:
                print("La schermata 'prova un altro metodo non è uscita, ottimo")
            time.sleep(2)
            page.get_by_role("link", name="Ricevi un codice di verifica dall'app").click()
            time.sleep(2)
            otp = getCode(g2fa_key)
            page.get_by_label("Inserisci codice").fill(str(otp))
            
            page.get_by_label("Inserisci codice").press("Enter")
            time.sleep(10)
        except Exception as e:
            SendToTelegram("Ci sono prolblemi con il login.. sta fallendo")
            print("Ci sono prolblemi con il login.. sta fallendo")


        # Attendere l'inizio del download
        with page.expect_download() as download_info:
            print("In attesa del completamento del download...")
            time.sleep(5)  # Aumenta se necessario per garantire l'avvio del download

        download = download_info.value
        try:

            download_path = download.path()
            original_filename = os.path.basename(download_path)




            if os.path.exists(download_path):
                print(f"Download Completato: {download_path}")
                new_path = os.path.join("downloads", original_filename)

                if os.path.exists(new_path):
                    os.remove(new_path)  # Elimina il file esistente

                shutil.move(download_path._str, new_path)
                if os.path.exists(new_path):
                    print(f"File scaricato con successo: {download_path}")
                    isDownloaded = True

        except Exception as e:
            print(e)

    # Chiudi il contesto e il browser
    context.close()
    browser.close()

    return isDownloaded





def downloadSingleUrl(google_tOut_downloadUrl):
    try:

        google_passw = os.getenv('google_passw')
        g2fa_key = os.getenv('g2fa_key')

        url = google_tOut_downloadUrl
        with sync_playwright() as playwright:
            isDownloader = run(playwright, url_file= url, google_passw= google_passw, g2fa_key= g2fa_key)
        
        return isDownloader
    except Exception as e:
        print(e)
        return False




   