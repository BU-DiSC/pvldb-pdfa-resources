# Install tools to check PDF/A compliance and fonts

This process has been tested with macOS 13.3.

## Configuring Tools 
+ install python
+ Install PyPDF2 (needed for pdf-import.py)

```
pip3 install PyPDF2
```

## Java (needed by veraPDF)
+ macOS: `brew install openjdk && sudo ln -sfn "$(brew --prefix openjdk)/libexec/openjdk.jdk" /Library/Java/JavaVirtualMachines/openjdk.jdk`
+ Linux: `sudo apt install default-jre-headless` (Debian/Ubuntu) or `sudo dnf install java-21-openjdk-headless` (Fedora/RHEL)

## VeraPDF
Needs Java (see above). `./setup.sh` does this for you. To do it by hand, run from the repo root:

```
mkdir -p _tools/veraPDF-download && cd _tools/veraPDF-download
curl -LO https://software.verapdf.org/rel/verapdf-installer.zip && unzip -q verapdf-installer.zip
echo "INSTALL_PATH=$(cd .. && pwd)/veraPDF" > install.properties
java -jar verapdf-greenfield-*/verapdf-izpack-installer-*.jar -options install.properties
cd ../.. && rm -rf _tools/veraPDF-download
_tools/veraPDF/verapdf --version
```

This installs veraPDF into `_tools/veraPDF` without any prompts. Both `_tools/veraPDF` and `_tools/veraPDF-download` are in `.gitignore`.

## Setup Poppler 
+ Install poppler-utils (e.g., `brew install poppler`) (for checking embedded fonts)

