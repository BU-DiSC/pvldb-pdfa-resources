# How to ensure PDF/A compliance

This is a collection of resources started as part of the PVLDB Vol 16 Publication Process. It primarily hosts tool to check PDF/A compliance and also include various resources and how-tos regarding achieving PDF/A compliance. 

> Note: This is a live document, so please check back for updated content and feel free to contribute as well.

## Getting started with the tools to check PDF/A compliance

### Set up the tools
The checking scripts need Python 3 with PyPDF2, poppler (for `pdffonts`) and veraPDF (which needs Java). On macOS (with Homebrew), Debian/Ubuntu or Fedora, one command installs everything:

```
./setup.sh
```

It asks for your password to install system packages and is safe to re-run. Run `./setup.sh -h` for options.

To install the tools by hand instead, follow [_tools/INSTALL_TOOLS.md](_tools/INSTALL_TOOLS.md).

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

If a check fails, [PDFA-how-to.md](PDFA-how-to.md) explains how to fix it. If your paper declares PDF/A-1b and fails, try declaring PDF/A-2b with `\hypersetup{pdfapart=2,pdfaconformance=b}`. PVLDB accepts PDF/A-2, which allows things PDF/A-1 forbids, such as transparency in figures. Then re-run the check.

## Proposed workflow: check your figures too
Font problems often come from a single figure. To find it, check the figures one by one:
```
cp /path/to/paper/figures/*.pdf _testdir/
./check_fonts_pdfa.py
```
Look for `contains Type 3 fonts` or `has N missing fonts`. For figures, ignore `not a valid PDF/A` and don't run `check_format.py`.

## How to prepare your PDF

[Click here](PDFA-how-to.md) to see a set of advice on how to prepare your PDF so that it is PDF/A compliant.

# AI Agents

AI coding agents can use the getting-started skill in [.claude/skills/pvldb-pdfa-getting-started/SKILL.md](.claude/skills/pvldb-pdfa-getting-started/SKILL.md), which also covers interpreting and fixing failures.
