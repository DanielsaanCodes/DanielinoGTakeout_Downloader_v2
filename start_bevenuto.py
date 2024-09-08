import os


from emlScarper import getUrl_fromMail
from emlReader import EmailServer
from dotenv import load_dotenv

# Carica il file .env
load_dotenv()


from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from danioGoogleFucker import downloadSingleUrl
Base = declarative_base()
import os
import shutil

from danio_telegramExtension import SendToTelegram
import time
downloads_folder = "downloads"


def crea_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Il percorso '{path}' è stato creato.")
    else:
        pass
    #print(f"Il percorso '{path}' esiste già.")


crea_path(downloads_folder)
crea_path("Saves")


class Download(Base):
    __tablename__ = 'downloads'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Identificatore univoco
    url = Column(String, nullable=False)  # URL da memorizzare
    scaricato = Column(Boolean, default=False)  # Stato del download

# Creazione della connessione al database e della tabella
def create_database(file_path):
    engine = create_engine(f'sqlite:///{file_path}')
    Base.metadata.create_all(engine)
    return engine

def load_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

# Funzione per inserire dati nel database
def save_data_to_db(session, data):
    for item in data:
        download = Download(url=item['url'], scaricato=False)
        session.add(download)
    session.commit()

# Funzione per caricare dati dal database
def load_data_from_db(session):
    return session.query(Download).all()



def cicloneDownloader(session):
    print("Tranquillo riprendo dall'ultimo scaricato!")
    SendToTelegram("Nuovo ciclo avviato.. in bocca al lupo")
    record = session.query(Download).filter_by(scaricato=False).order_by(Download.id.asc()).first()
    
    while (record != None):
        summary = get_download_status_summary(session)
        print(f"Sto per scaricare dal pulsante numero: {record.id}")
        SendToTelegram(f"Sto per scaricare dal pulsante numero: {record.id}")
        isdownload = downloadSingleUrl(record.url) 
        
        if isdownload == True:
            record.scaricato = True
            session.commit()
            SendToTelegram("Un altro pacchetto è stato completato.")

        if isdownload != True:
            print("Un download è fallito.. ci riprovo..")
            SendToTelegram("Un download è fallito.. ci riprovo ma farà un tentativo tra mezz'ora..")
            time.sleep(1800)

        
        record = session.query(Download).filter_by(scaricato=False).order_by(Download.id.asc()).first()
    
    print("Tutti i download sono stati completato")
    SendToTelegram("Tutti i download sono stati completato")
    

 


def get_download_status_summary(session):
    """Restituisce un riassunto del conteggio dei record in base allo stato di scaricato."""
    try:
        # Conteggia i record con scaricato = 'False'
        count_not_downloaded = session.query(Download).filter_by(scaricato=False).count()
        
        # Conteggia i record con scaricato = 'True'
        count_downloaded = session.query(Download).filter_by(scaricato=True).count()
        total = session.query(Download).filter_by().count()
        # Crea il riassunto come stringa
        summary = (
            f"Totale Downloads: {total}n"
            f"Totale record scaricati: {count_downloaded}\n"
            f"Totale record non scaricati: {count_not_downloaded}\n"
        )
        print(summary)
        SendToTelegram(summary)
        
        return summary
    except Exception as e:
        print(f"Errore durante il conteggio dei record: {e}")
        return "Errore durante il conteggio dei record."

def cancella_file_se_esiste(percorso_relativo):
    # Controlla se il file esiste
    if os.path.exists(percorso_relativo):
        # Cancella il file
        os.remove(percorso_relativo)
        print(f"File '{percorso_relativo}' cancellato con successo.")
    else:
        print(f"Il file '{percorso_relativo}' non esiste.")




# Esempio di utilizzo
if __name__ == "__main__":
    # Creazione e connessione al database
    #mode = "getURL"

    print("Benvenuto!  \n Leggi la reference per capire il funzionamento dello strumento")
    SendToTelegram("Benvenuto nel bot di google takeout, prosegui sul pc per continuare")
    print(" Please, read first the instruction on the repo on github.\n\n")
    mode = input("1: Resetta DB \n2. Riprendi da dov'eri\n\nScelta: ")
    if mode == "1":
        mode = "getURL"
        cancella_file_se_esiste("Saves/example.db")
        #shutil.rmtree(downloads_folder)
        print("ASSICURATI DI SVUOTARE LA CARTELLA DEI DOWNLOAD PRIMA.. e prmemi invio per continuare: ")
        s= input()
        os.makedirs(downloads_folder, exist_ok=True)

        pass
    elif mode == "2":
        mode = "downloader"


    db_path = "Saves/example.db"
    engine = create_database(db_path)
    session = load_session(engine)


    if mode == "getURL":
        nPacchetti = input("Inserire il numero di pacchetti da scaricare: ")
            
        server = EmailServer()
        server.run()
        web_path = server.get_web_path()
        if web_path:

            example_data = getUrl_fromMail(nPacchetti=nPacchetti, url_mail=web_path)
            # Inserimento dei dati
            print(f"###TOTALE ELEMENTI DA SCARICARE: {len(example_data)}")
            SendToTelegram(f"###TOTALE ELEMENTI DA SCARICARE: {len(example_data)}")
            save_data_to_db(session, example_data)
            server.shutdown_server()
            print("LINK ACQUISITI E MESSI IN DB. OTTIMO! RIAVVIA PER PROCEDERE!")
            pass






    elif mode == "downloader":

        print("Lista pronta scarico")
        print("Assicurati che il file .env custodista la passw di google, e anche la chiave di TOTP")
        cicloneDownloader(session)









