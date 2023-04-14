"""
Authors: Lijun Chang, Manos Athanassoulis
Code adapted from PVLDB16 proceedings scripts
"""

import argparse
import re
import PyPDF2 as pypdf # this one still seems to be maintained
import os


parser = argparse.ArgumentParser(description='Check some common formatting issues')

parser.add_argument('--dir', action='store',
                    help='Folder containing PDFs', required=True)

args = parser.parse_args()
folder = args.dir



for f in sorted(os.listdir(folder)):
    path = os.path.join(folder, f)
    if not path.lower().endswith(".pdf"):
        # print("Skipping file because it is not PDF")
        continue
    print("\tCheck file %s" % path)

    exception=0
    pdf_document = pypdf.PdfFileReader(path, strict=False)
    pdf_pages = pdf_document.getNumPages()
    
    first_page = pdf_document.getPage(0)
    plaintext = first_page.extractText()
    plaintext = re.sub('˙', 'ff', plaintext)
    plaintext = re.sub('˛', 'tt', plaintext)
    plaintext = re.sub('˚', 'Qu', plaintext)
    #use the first line as title
    end_title=plaintext.find('\n')
    possible_title=plaintext[0:end_title]
    #
    plaintext = re.sub('\\s', '', plaintext)

    # if paper_id == 361:
    #     print(plaintext)
    #     break

    #Note that the ISSN is the same across volumes
    if 'ISSN2150-8097' not in plaintext:
        print("\t%s: ISSN 2150-8097 not found" % f)
        exception=1

    if 'PVLDBReferenceFormat' not in plaintext:
        print("\t%s: PVLDB Reference block not found" % f)
        exception=1

# There is no way to know if the artifact block is required. This is only a warning.
    if 'PVLDBArtifactAvailability' not in plaintext:
        print("\t%s: PVLDB Artifact block not found (this is an error only if the artifact block is required)" % f)
        exception=0

    if 'ABSTRACT' not in plaintext:
        print("\t%s: Capitalized \"ABSTRACT\" not found" % f)
        exception=1


    if 'URL_TO_YOUR_ARTIFACTS' in plaintext:
        print("\t%s: Default availability URL found" % f)
        exception=1

    full_paper=plaintext
    for p in range (1,pdf_pages-1):
        full_paper=full_paper+pdf_document.getPage(p).extractText()
    # if 'ACKNOWLEDGMENTS' in full_paper:
        # print("\t%d: acck found" % paper_id)
    if 'Acknowledgments' in full_paper:
        print("\t%s: Acknowledgments not complying to format" % f)
        exception=1

    
    if exception==0:
        print("... OK")
    print()


