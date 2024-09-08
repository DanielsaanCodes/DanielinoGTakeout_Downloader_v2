import re
from playwright.sync_api import Playwright, sync_playwright, expect

import os
def run(playwright: Playwright, nPacchetti, url_mail) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url_mail)
   # Trova l'elemento link
    contatore = 1
    lista_url = []


    while contatore <= int(nPacchetti):
        link_element = page.get_by_role("link", name=f"Download {contatore} di")
        link_url = link_element.get_attribute('href')

        preElement = {
            "numDownload": contatore,
            "url": link_url,
            "scaricato": "False"
        }
        lista_url.append(preElement)
        contatore += 1
    # Ottieni l'URL dall'attributo href
    pass

    # ---------------------
    context.close()
    browser.close()
    return lista_url



def getUrl_fromMail(nPacchetti, url_mail):
    

    with sync_playwright() as playwright:
        listaurl = run(playwright, nPacchetti, url_mail)
        return listaurl









