---
name: pvldb-pdfa-getting-started
description: Get started with the pvldb-pdfa-resources repo - install the checking tools (veraPDF, poppler, PyPDF2), run check_fonts_pdfa.py and check_format.py on a paper, interpret the results, and fix common PDF/A and font problems in PVLDB camera-ready papers. Use when someone asks how to set up or use this repo, wants to check a paper for PDF/A or font compliance, or needs help fixing a failing check.
---

# Getting started with pvldb-pdfa-resources

This repo helps authors make PVLDB camera-ready papers PDF/A compliant, with all fonts embedded and no Type 3 fonts. It contains a small version of the checks that the PVLDB publication process runs.

## Repo map

| Path | What it is |
|---|---|
| `README.md` | Setup and a minimal example |
| `PDFA-how-to.md` | How-tos: LaTeX settings, Acrobat, testing scripts, online validators, removing Type 3 fonts |
| `VLDB-formatting.md` | Camera-ready formatting rules (page limits, author blocks, and so on) |
| `_tools/INSTALL_TOOLS.md` | Detailed install notes for the tools |
| `check_fonts_pdfa.py` | veraPDF PDF/A check, Type 3 font check, unembedded font check. Writes `corrections.txt` |
| `check_format.py` | Checks the first page and body text for ISSN, PVLDB reference and artifact blocks, `ABSTRACT`, the template's placeholder artifact URL, and the acknowledgments heading |
| `_testdir/` | Default input folder for both scripts (gitignored) |
| `_tools/veraPDF/` | Where veraPDF is installed (gitignored) |

## 1. Set up the tools

On macOS (Homebrew), Debian/Ubuntu or Fedora, run `./setup.sh` from the repo root. It installs everything below, puts veraPDF in `_tools/veraPDF`, and skips anything already installed. If the system Python refuses pip installs, it puts PyPDF2 in `.venv` instead, and you then need to run `source .venv/bin/activate` before using the scripts. Use `--skip-system` to skip the package manager. The manual steps below are for other systems or for debugging.

Check what is already installed:

```sh
python3 -c "import PyPDF2; print(PyPDF2.__version__)"   # need 3.x (the code uses the PdfReader API)
pdffonts -v                                             # poppler
_tools/veraPDF/verapdf --version                        # veraPDF
java -version                                           # veraPDF needs Java
```

Install anything that is missing:

- **PyPDF2:** `pip3 install "PyPDF2>=3"`
- **poppler (provides `pdffonts`):** `brew install poppler` on macOS, `apt install poppler-utils` on Debian/Ubuntu
- **veraPDF:** download and unzip the installer, then run it and choose `<repo>/_tools/veraPDF` as the install folder. The unzipped folder name contains the version number, hence the glob.
  ```sh
  cd _tools && mkdir -p veraPDF-download && cd veraPDF-download
  curl -LO https://software.verapdf.org/rel/verapdf-installer.zip
  unzip verapdf-installer.zip && cd verapdf-greenfield-*
  ./verapdf-install     # install folder: <repo>/_tools/veraPDF
  ```
  You can delete `_tools/veraPDF-download` afterwards. If veraPDF is installed somewhere else, pass `--veraPDFpath <folder>` to `check_fonts_pdfa.py`.

## 2. Minimal example

```sh
mkdir -p _testdir
cp /path/to/p1234-smith.pdf _testdir/
./check_fonts_pdfa.py      # PDF/A and font checks on _testdir
./check_format.py          # formatting checks on _testdir
```

Script behavior to know about:
- Both scripts default to `--dir _testdir`, and `-h` shows every option with its default.
- If `_testdir` does not exist, the scripts create it and exit. A missing custom `--dir` is an error. A folder with no PDFs exits cleanly.
- Only `*.pdf` files at the top level of the folder are checked, in alphabetical order. Subfolders are not searched.
- `check_fonts_pdfa.py` writes `corrections.txt` to `--corr_path` (default `.`). A file that passes appears there with its paper ID and no corrections.

A passing paper looks like this:
```
Check file _testdir/p1234-smith.pdf
... OK: PDF/A compliant, all fonts are embedded and there are no Type 3 fonts.
```

## 3. Interpreting and fixing failures

### "not a valid PDF/A"
The script runs veraPDF with `--flavour 0`, which checks the file against the PDF/A level the file declares in its metadata (`pdfaid:part`). To see the specific failed rules:
```sh
_tools/veraPDF/verapdf --flavour 2b --format mrr paper.pdf | grep -E 'status="failed"|<description>'
```
- **The paper declares PDF/A-1b** (common with older templates). PDF/A-1 forbids transparency, xref streams, and font subsets without CharSet/CIDSet, so matplotlib figures often fail it. PVLDB accepts PDF/A-2 or later. Check against 2b first. If the only failure is clause 6.6.4 (`pdfaid:part` does not match), the fix is correct and not a workaround:
  ```latex
  \hypersetup{pdfapart=2,pdfaconformance=b}
  ```
  Declaring a level the file does not actually pass only changes its claim. Always re-run veraPDF against the declared level.
- **Template setup:** `\documentclass[sigconf, nonacm, pdfa]{acmart}` or `\usepackage[a-2b]{pdfx}`. See `PDFA-how-to.md` for details.
- **Acrobat's "Save as PDF/A"** only makes the file claim compliance. Use Preflight's "Convert to PDF/A-2b" instead.

### "contains Type 3 fonts" or "has N missing fonts"
Find the offending fonts with `pdffonts paper.pdf`: look for `Type 3` in the type column or `no` in the `emb` column. Then check each figure PDF separately (`pdffonts fig.pdf`) to find where they come from. Usual causes and fixes:
- **matplotlib:** set `plt.rcParams['pdf.fonttype'] = 42` (and `ps.fonttype = 42`), or use `text.usetex = True`. Never use fonttype 3.
- **Base-14/35 fonts not embedded by LaTeX:** set `pdftexDownloadBase14` and `dvipsDownloadBase35` to true in `updmap.cfg` (`updmap -sys` shows which file is used).
- **Quick fix without regenerating a figure:** re-distill it with Ghostscript, then recompile the paper:
  ```sh
  gs -q -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -dEmbedAllFonts=true -dSubsetFonts=true -sOutputFile=fig_fixed.pdf fig.pdf
  ```

### "Syntax Warning: Mismatch between font type and embedded font file"
This comes from poppler (`pdffonts`), not veraPDF, and it does not affect the result. It usually means matplotlib with `pdf.fonttype = 42` embedded a CFF-based `.otf` font (for example Linux Libertine O) but labeled it TrueType. Fix: use `text.usetex`, use a `.ttf` version of the font, or re-distill the figure with Ghostscript as above. Use `pdffonts -q` to silence it.

### check_format.py messages
These are text heuristics run on the first page and body. Check each one against `VLDB-formatting.md` before editing:
- **ISSN or PVLDB reference block missing:** wrong or outdated template.
- **Artifact block missing:** only an error if the paper must provide an artifact URL.
- **Default availability URL:** `URL_TO_YOUR_ARTIFACTS` from the template is still in `\vldbavailabilityurl{}`.
- **"Acknowledgments not complying to format":** use the template's acknowledgments environment, which produces the uppercase heading.

## Gotchas
- **`env: python3\r: No such file or directory`:** the script has Windows (CRLF) line endings. Convert it to LF, for example with `perl -pi -e 's/\r$//' check_*.py`.
- **The checks are not exhaustive.** A pass here does not guarantee acceptance, so also go through `VLDB-formatting.md`.
- **Online validators** (listed in `PDFA-how-to.md`) are a useful second opinion when veraPDF and another tool disagree.
