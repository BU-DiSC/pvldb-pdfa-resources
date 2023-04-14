"""
Authors: Lijun Chang, Manos Athanassoulis
Code adapted from PVLDB16 proceedings scripts
"""
#Requires pdffonts, grep, awk, veraPDF

import argparse
import subprocess

parser = argparse.ArgumentParser(description='Check whether all fonts are embedded and file is PDF/A compliant')

parser.add_argument('--dir', action='store',
                    help='Folder containing PDFs', required=True)

parser.add_argument('--veraPDFpath', action='store',
                    help='Folder containing veraPDF', required=False, default="_tools/veraPDF")

parser.add_argument('--corr_filename', action='store',
                    help='File containing the automated corrections veraPDF (def: corrections.txt)', required=False, default="corrections.txt")

parser.add_argument('--corr_path', action='store',
                    help='Path containing the automated corrections veraPDF (def: CRC-Corrections)', required=False, default=".")


args = parser.parse_args()

import os
import subprocess

folder = args.dir

print("Iterate over all files for PDF/A and Fonts")
message_pdfa="File is not PDF/A compliant. More details on making a file PDF/A compliant are here: https://github.com/BU-DiSC/pvldb-pdfa-resources."
message_embed_fonts="Not all fonts are embedded. Please embed all fonts. "
message_type3_fonts="Please remove any Type 3 fonts you have in the PDF. "
corr_text=""
start="a"
print

for f in sorted(os.listdir(folder)):
    path = os.path.join(folder, f)
    if not path.lower().endswith(".pdf"):
        # print("Skipping file because it is not PDF")
        continue
    print("\tCheck file %s" % path)
    # paper_id=f.split('-')[0].split('p')[1]
    paper_id=f.split('.')[0]
    # print(paper_id)
    count = 0 # count of errors for file f
    fonts = 0 # count of font errors for file f
    res = subprocess.check_output([args.veraPDFpath+"/verapdf --flavour 0 --format text \""+path+"\" | grep \"\""],shell=True)
    res = str(res)

    cur_paper_corrections = ""    
    
    if 'FAIL' in res:
        print("... not a valid PDF/A")
        cur_paper_corrections=cur_paper_corrections+"#("+chr(ord(start) + count)+") "+message_pdfa
        count = count + 1

    res = subprocess.check_output(['pdffonts', path])
    res = str(res)
    if 'Type 3' in res:
        print("... contains Type 3 fonts")
        cur_paper_corrections=cur_paper_corrections+"#("+chr(ord(start) + count)+") "+message_type3_fonts
        count = count + 1
        fonts = fonts + 1
    
    missing_fonts=int(subprocess.check_output(["pdffonts \""+path+"\" | grep \"no\s*no\" | grep -v \"yes\s*no\s*no\" | awk 'BEGIN{mf=0}{mf++}END{print mf}'"],shell=True))
    if missing_fonts>0:
        print("... has %d missing fonts" % missing_fonts)
        cur_paper_corrections=cur_paper_corrections+"#("+chr(ord(start) + count)+") "+message_embed_fonts
        count = count + 1
        fonts = fonts + 1

    corr_text=corr_text+paper_id+cur_paper_corrections
    corr_text=corr_text+"\n"
    # if count > 0:
    #     corr_text=corr_text+paper_id+cur_paper_corrections
    #     corr_text=corr_text+"\n"
    # else:
    if count == 0:
        print("... OK: PDF/A compliant, all fonts are embedded and there are no Type 3 fonts.")
    if fonts == 0 and count>0:
        print("... Fonts are OK: all fonts are embedded and there are no Type 3 fonts.")
    print()



print("\n***** Corrections *****")
print(corr_text)
print("***********************\n\n")

corrections_filename = os.path.join(args.corr_path, args.corr_filename)
corr_file = open(corrections_filename, 'w')
corr_file.write(corr_text)
corr_file.close()

print("Corrections also saved in %s" % corrections_filename)

quit()




#Legacy code
print("Checking fonts using pdffonts")


for f in sorted(os.listdir(folder)):
    path = os.path.join(folder, f)
    if not path.lower().endswith(".pdf"):
        # print("Skipping file because it is not PDF")
        continue
    print("\tCheck file %s" % path)
    res = subprocess.check_output(['pdffonts', path])
    res = str(res)
    if 'Type 3' in res:
        print("%s:\tType 3 font" % path)
        continue
    # print(["pdffonts " + path + " | grep \"no\s*no\" | grep -v \"yes\s*no\s*no\" | awk 'BEGIN{mf=0}{mf++}END{print mf}'"])
    # missing_fonts=subprocess.call(["pdffonts "+path+" | grep \"no\s*no\" | grep -v \"yes\s*no\s*no\" | awk 'BEGIN{mf=0}{mf++}END{print mf}'"],shell=True)
    missing_fonts=int(subprocess.check_output(["pdffonts \""+path+"\" | grep \"no\s*no\" | grep -v \"yes\s*no\s*no\" | awk 'BEGIN{mf=0}{mf++}END{print mf}'"],shell=True))
    # print(missing_fonts)
    # print(path)
    if missing_fonts>0:
        print("%s:\t%d missing fonts" % (path,missing_fonts))
        continue
    print ("... OK")
    # subprocess.run(['pdffonts', path,' | grep "mp\s*no"'])
    # pdffonts pdfs/1/p298-wang.pdf | grep "no\s*no" | grep -v "yes\s*no\s*no" | awk 'BEGIN{mf=0}{mf++}END{print mf}'
    # if 'no  no  no' in res:
    #     print("%s:\tNot all fonts are embedded" % path)
    #     continue
    # if 'no  no' in res:
    #     print("%s:\tPotentially not all fonts are embedded" % path)

ret = subprocess.call([args.veraPDFpath+"/verapdf","--version"], stdout=subprocess.DEVNULL)
if ret != 0:
    print("You may have to correctly install veraPDF and/or provide the write path to it.")

print("")
print("Verify PDF/A using veraPDF")

for f in sorted(os.listdir(folder)):
    path = os.path.join(folder, f)
    if not path.lower().endswith(".pdf"):
        # print("Skipping file because it is not PDF")
        continue
    subprocess.call([args.veraPDFpath+"/verapdf","--flavour","0","--format","text",path])
