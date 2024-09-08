import os
import http.server
import socketserver
import threading
import tkinter as tk
from tkinter import filedialog
from email import policy
from email.parser import BytesParser

class EmailServer:
    def __init__(self):
        self.filepath = None
        self.html_file = None
        self.server_thread = None
        self.httpd = None
        self.port = 8000  # Porta su cui viene eseguito il server HTTP

    def select_eml_file(self):
        """Apre una finestra di dialogo per selezionare un file .eml."""
        root = tk.Tk()
        root.withdraw()  # Nasconde la finestra principale
        self.filepath = filedialog.askopenfilename(
            title="Seleziona un file .eml",
            filetypes=(("Email files", "*.eml"), ("All files", "*.*"))
        )
        print(f"Hai selezionato il file: {self.filepath}")

    def convert_eml_to_html(self):
        """Converte il file .eml in un file HTML."""
        if self.filepath:
            with open(self.filepath, 'rb') as f:
                msg = BytesParser(policy=policy.default).parse(f)
            
            for part in msg.iter_parts():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_payload(decode=True).decode(part.get_content_charset())
                    break
            
            self.html_file = self.filepath.replace('.eml', '.html')
            with open(self.html_file, 'w') as html_f:
                html_f.write(html_content)
            print(f"File HTML generato: {self.html_file}")
        else:
            print("Nessun file .eml selezionato.")

    def serve_html(self):
        """Serve il file HTML su un server HTTP."""
        if self.html_file:
            handler = http.server.SimpleHTTPRequestHandler
            self.httpd = socketserver.TCPServer(("", self.port), handler)
            os.chdir(os.path.dirname(self.html_file))  # Cambia la directory per servire l'HTML

            # Esegue il server in un thread separato per non bloccare l'esecuzione
            self.server_thread = threading.Thread(target=self.httpd.serve_forever)
            self.server_thread.daemon = True  # Permette di chiudere il server con il programma principale
            self.server_thread.start()
            print(f"Servendo {self.html_file} su http://localhost:{self.port}")
        else:
            print("Nessun file HTML da servire.")

    def get_web_path(self):
        """Ritorna il percorso web del file HTML servito."""
        if self.html_file:
            filename = os.path.basename(self.html_file)
            web_path = f"http://localhost:{self.port}/{filename}"
            print(f"Percorso web del file HTML: {web_path}")
            return web_path
        else:
            print("Nessun file HTML disponibile.")
            return None

    def shutdown_server(self):
        """Ferma il server HTTP e cancella i file temporanei."""
        if self.httpd:
            print("Chiudendo il server HTTP...")
            self.httpd.shutdown()
            self.server_thread.join()  # Attende che il thread del server si chiuda
            print("Server HTTP chiuso.")

        # Cancella i file temporanei
        if self.filepath and os.path.exists(self.filepath):
            os.remove(self.filepath)
            print(f"File .eml eliminato: {self.filepath}")

        if self.html_file and os.path.exists(self.html_file):
            os.remove(self.html_file)
            print(f"File HTML eliminato: {self.html_file}")

    def run(self):
        """Esegue tutti i passaggi per selezionare, convertire, servire e chiudere il server."""
        self.select_eml_file()
        self.convert_eml_to_html()
        self.serve_html()