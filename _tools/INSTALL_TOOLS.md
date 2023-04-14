# Install tools to check PDF/A compliance and fonts

This process has been tested with macOS 13.3.

## Configuring Tools 
+ install python
+ Install PyPDF2 (needed for pdf-import.py)

```
pip3 install PyPDF2
```

## VeraPDF
+ Install veraPDF (for PDF/A compliance check)
    + Create veraPDF directory `mkdir veraPDF; cd veraPDF`
    + Download & install latest stable version of veraPDF using

```
mkdir veraPDF-download; cd veraPDF-download
wget https://software.verapdf.org/rel/verapdf-installer.zip
unzip verapdf-installer.zip
cd verapdf-greenfield-1.22.3
./verapdf-install
```
    
   + When executing `./verapdf-install` provide as installation folder `<root>/_tools/veraPDF`, which will be a newly created folder.
   + Note that the `/veraPDF` and `/veraPDF-download` folders are in .gitignore.
   + After installation is completed you can delete the `/veraPDF-download` folder and all its contents.

## Setup Poppler 
+ Install poppler-utils (e.g., `brew install poppler`) (for checking embedded fonts)

