# How to ensure PDF/A compliance

This is a collection of resources started as part of the PVLDB Vol 16 Publication Process. It outlines various resources and how-tos regarding achieving PDF/A compliance. This is a live document, so please come back for updated content and feel free to contribute as well.

+  In you latex source code use the package `pdfx`. The full documentation of the package is here: https://texdoc.org/serve/pdfx.pdf/0  
```
\usepackage[a-2b]{pdfx})
```` 
+ A recently published guide with more details: https://webpages.tuni.fi/latex/pdfa-guide.pdf 
+ A (slightly older) very detailed how-to guide: https://www.mathstat.dal.ca/~selinger/pdfa/. Note that this guide contains several steps that are not currently required, but they can help establish good practices.

### Adobe Acrobat for PDF/A

Adobe Acrobat can also save as PDF/A, however, note that this does not always mean that the file is compliant. Rather, it means that the file _claims to be compliant_. More checking is typically necessary. 
+ If you use `File > Save as Other > Archival PDF (PDF/A)` this will *not* ensure PDF/A compliance. In fact most of the time this will not be sufficient.
+ If you use Adobe Preflight to run a "Convert to PDF/A" profile and the process succeeds this will be sufficient. 


### Online tools to check for PDF/A compliance
+ https://www.pdfen.com/pdf-a-validator
+ https://pdf.online/validate-pdfa

### Online tools to convert to PDF/A 
+ https://pdf.online/pdf-to-pdfa
+ https://www.ilovepdf.com/convert-pdf-to-pdfa
