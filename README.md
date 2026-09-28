# How to ensure PDF/A compliance

This is a collection of resources started as part of the PVLDB Vol 16 Publication Process. It outlines various resources and how-tos regarding achieving PDF/A compliance. This is a live document, so please come back for updated content and feel free to contribute as well.

# Getting started

## Set up the tools
The checking scripts need Python 3 with PyPDF2, poppler (for `pdffonts`) and veraPDF (which needs Java). More details are in [_tools/INSTALL_TOOLS.md](_tools/INSTALL_TOOLS.md).

```
pip3 install "PyPDF2>=3"
brew install poppler            # or: apt install poppler-utils

cd _tools && mkdir -p veraPDF-download && cd veraPDF-download
curl -LO https://software.verapdf.org/rel/verapdf-installer.zip
unzip verapdf-installer.zip && cd verapdf-greenfield-*
./verapdf-install               # choose <repo>/_tools/veraPDF as the installation folder
```

Check that everything is in place:
```
python3 -c "import PyPDF2; print(PyPDF2.__version__)"
pdffonts -v
_tools/veraPDF/verapdf --version
```

## Minimal example
Copy your paper into `_testdir` (the default input folder, ignored by git) and run both checks:
```
mkdir -p _testdir
cp /path/to/p1234-smith.pdf _testdir/
./check_fonts_pdfa.py     # PDF/A compliance, embedded fonts, no Type 3 fonts
./check_format.py         # common PVLDB formatting issues
```
A paper that passes the font and PDF/A check prints:
```
	Check file _testdir/p1234-smith.pdf
... OK: PDF/A compliant, all fonts are embedded and there are no Type 3 fonts.
```
Use `--dir <folder>` to check a different folder, and `-h` to see all options and their defaults. `check_fonts_pdfa.py` also writes the list of needed corrections to `corrections.txt`.

If a check fails, the sections below explain how to fix it. If your paper declares PDF/A-1b and fails, try declaring PDF/A-2b with `\hypersetup{pdfapart=2,pdfaconformance=b}`. PVLDB accepts PDF/A-2, which allows things PDF/A-1 forbids, such as transparency in figures. Then re-run the check.

AI coding agents can use the getting-started skill in [.claude/skills/pvldb-pdfa-getting-started/SKILL.md](.claude/skills/pvldb-pdfa-getting-started/SKILL.md), which also covers interpreting and fixing failures.

## LaTeX configuration to embed all fonts
+ Ensure that the options `pdftexDownloadBase14` and `dvipsDownloadBase35` are set to true in your `updmap.cfg` file. In order to ensure that that you are editing the correct file run first `updmap -sys` to see which files are used. 

## LaTeX packages to ensure PDF/A 
+  Modify the documentclass to include pdfa, for example:
```
\documentclass[sigconf, nonacm, pdfa]{acmart}
```
+  In you latex source code use the package `pdfx`. The full documentation of the package is here: https://texdoc.org/serve/pdfx.pdf/0  
```
\usepackage[a-2b]{pdfx})
```` 
+ A recently published guide with more details: https://webpages.tuni.fi/latex/pdfa-guide.pdf 
+ A (slightly older) very detailed how-to guide: https://www.mathstat.dal.ca/~selinger/pdfa/. Note that this guide contains several steps that are not currently required, but they can help establish good practices.

## Adobe Acrobat for PDF/A

Adobe Acrobat can also save as PDF/A, however, note that this does not always mean that the file is compliant. Rather, it means that the file _claims to be compliant_. More checking is typically necessary. 
+ If you use `File > Save as Other > Archival PDF (PDF/A)` this will *not* ensure PDF/A compliance. In fact most of the time this will *not* be sufficient.

### Adobe Acrobat Preflight for PDF/A
+ If you use Adobe Preflight to run a "Convert to PDF/A" profile and the process succeeds this will be sufficient. 
  + In the Creative Cloud Suite, this can be found in Adobe Acrobat under `Edit > Preflight` where you can select the profile "Convert to PDF/A-2b" and click on "Analyze and fix". This will open a new dialogue box that will ask you to give the desired output filename.


# How to test for PDF/A and font compliance.

OK, so you have followed all the above guidelines to make your file compliant. Can you verify with the same tools as the PVLDB Publication Process? To do that, we add below a simple version of the testing suite used during publication.

## PVLDB Vol 16 Testing Scripts
+ Before you start, follow the guidelines in [_tools/INSTALL_TOOLS.md](_tools/INSTALL_TOOLS.md) to install the necessary tools.
+ Once the tools are installed, you can run the two scripts `check_fonts_pdfa.py` to check fonts and PDF/A compliance and `check_format.py` to check other common formatting errors. 
+ Note that these are not exhaustive!
+ Give `python check_fonts_pdfa.py --dir <directory with pdf files to check>` and all files in that folder will be checked for PDF/A and font compliance.
+ Give `python check_format.py --dir <directory with pdf files to check>` and all files in that folder will be checked for common formatting errors.

## Online tools

### Online tools to check for PDF/A compliance
+ https://www.pdfen.com/pdf-a-validator
+ https://pdf.online/validate-pdfa
+ https://avepdf.com/pdfa-validation

### Online tools to convert to PDF/A 
+ https://pdf.online/pdf-to-pdfa
+ https://www.ilovepdf.com/convert-pdf-to-pdfa

### Removing Type 3 fonts (this is a best-effort collection of online links)
Note that typically, if you ensure PDF/A compliance there should be no Type 3 fonts. Just in case, below we have a collection of links solely about removing Type 3 fonts in a more ad hoc manner.
+ https://me.net.nz/post/type3fonts/
+ https://blog.mattoverby.net/2021/07/you-can-remove-type-3-fonts-with.html
+ https://tex.stackexchange.com/questions/18687/how-to-generate-pdf-without-any-type3-fonts
