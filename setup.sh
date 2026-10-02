#!/usr/bin/env bash
# Install the tools needed by check_fonts_pdfa.py and check_format.py:
#   - Python 3 with PyPDF2 (>= 2, PdfReader API)
#   - poppler (pdffonts)
#   - Java (needed by veraPDF)
#   - veraPDF, installed into _tools/veraPDF
#
# Supported: macOS (Homebrew), Debian/Ubuntu (apt), Fedora/RHEL (dnf).
# Safe to re-run: anything already installed is left alone.

set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: ./setup.sh [--skip-system] [--reinstall-verapdf] [-h]

  --skip-system         Do not use the system package manager (brew/apt/dnf);
                        only install PyPDF2 and veraPDF.
  --reinstall-verapdf   Reinstall veraPDF even if _tools/veraPDF already works.
  -h, --help            Show this help.
USAGE
}

SKIP_SYSTEM=0
REINSTALL_VERAPDF=0
for arg in "$@"; do
  case "$arg" in
    --skip-system) SKIP_SYSTEM=1 ;;
    --reinstall-verapdf) REINSTALL_VERAPDF=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $arg"; usage; exit 1 ;;
  esac
done

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VERAPDF_DIR="$REPO_DIR/_tools/veraPDF"
VERAPDF_DOWNLOAD_DIR="$REPO_DIR/_tools/veraPDF-download"
VERAPDF_URL="https://software.verapdf.org/rel/verapdf-installer.zip"
VENV_DIR="$REPO_DIR/.venv"

info() { printf '\n==> %s\n' "$*"; }
warn() { printf '!!  %s\n' "$*" >&2; }
die()  { printf '!!  %s\n' "$*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

# Run a command as root (directly if we already are root).
as_root() {
  if [[ $(id -u) -eq 0 ]]; then "$@"
  elif have sudo; then sudo "$@"
  else die "Need root to run: $* (install sudo or run this script as root)"
  fi
}

java_ok() { java -version >/dev/null 2>&1; }

# ---------------------------------------------------------------------------
# 1. System packages
# ---------------------------------------------------------------------------
install_system_packages() {
  case "$(uname -s)" in
    Darwin)
      have brew || die "Homebrew not found. Install it from https://brew.sh and re-run."
      info "Installing packages with Homebrew"
      have python3  || brew install python
      have pdffonts || brew install poppler
      if ! java_ok; then
        brew install openjdk
        # Homebrew's openjdk is keg-only; macOS (and the veraPDF launcher) only
        # find a JDK registered under /Library/Java/JavaVirtualMachines.
        if ! /usr/libexec/java_home >/dev/null 2>&1; then
          info "Registering Homebrew's Java with macOS (asks for your password)"
          as_root ln -sfn "$(brew --prefix openjdk)/libexec/openjdk.jdk" \
            /Library/Java/JavaVirtualMachines/openjdk.jdk
        fi
      fi
      ;;
    Linux)
      if have apt-get; then
        info "Installing packages with apt"
        as_root apt-get update
        as_root apt-get install -y python3 python3-pip python3-venv \
          poppler-utils default-jre-headless curl unzip
      elif have dnf; then
        info "Installing packages with dnf"
        as_root dnf install -y python3 python3-pip poppler-utils curl unzip
        if ! java_ok; then
          as_root dnf install -y java-21-openjdk-headless \
            || as_root dnf install -y java-17-openjdk-headless
        fi
      else
        die "No apt-get or dnf found. Install python3, pip, poppler-utils, a Java runtime (11+), curl and unzip manually, then re-run with --skip-system."
      fi
      ;;
    *)
      die "Unsupported OS: $(uname -s). Follow _tools/INSTALL_TOOLS.md instead."
      ;;
  esac
}

if [[ $SKIP_SYSTEM -eq 0 ]]; then
  install_system_packages
else
  info "Skipping system packages (--skip-system)"
fi

for tool in python3 pdffonts curl unzip; do
  have "$tool" || die "'$tool' is not installed."
done
java_ok || die "Java is not working ('java -version' failed). veraPDF needs Java 11 or newer."

# ---------------------------------------------------------------------------
# 2. PyPDF2
# ---------------------------------------------------------------------------
pypdf2_ok() {
  "$1" -c 'import PyPDF2, sys; sys.exit(int(PyPDF2.__version__.split(".")[0]) < 2)' >/dev/null 2>&1
}

PYTHON_NOTE=""
if pypdf2_ok python3; then
  info "PyPDF2 already installed"
else
  info "Installing PyPDF2"
  if python3 -m pip install --user "PyPDF2>=3" && pypdf2_ok python3; then
    :
  else
    # Newer Debian/Ubuntu and Homebrew Python refuse pip installs outside a
    # virtual environment (PEP 668), so fall back to a venv in the repo.
    warn "pip could not install into the system Python; using a virtual environment in .venv instead"
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/python" -m pip install --quiet "PyPDF2>=3"
    pypdf2_ok "$VENV_DIR/bin/python" || die "Could not install PyPDF2."
    PYTHON_NOTE="Run 'source .venv/bin/activate' before using the check scripts."
  fi
fi

# ---------------------------------------------------------------------------
# 3. veraPDF
# ---------------------------------------------------------------------------
if [[ $REINSTALL_VERAPDF -eq 0 ]] && "$VERAPDF_DIR/verapdf" --version >/dev/null 2>&1; then
  info "veraPDF already installed in _tools/veraPDF"
else
  info "Downloading veraPDF"
  rm -rf "$VERAPDF_DOWNLOAD_DIR"
  mkdir -p "$VERAPDF_DOWNLOAD_DIR"
  curl -fL --progress-bar -o "$VERAPDF_DOWNLOAD_DIR/verapdf-installer.zip" "$VERAPDF_URL"
  unzip -q "$VERAPDF_DOWNLOAD_DIR/verapdf-installer.zip" -d "$VERAPDF_DOWNLOAD_DIR"

  installer_jar=$(find "$VERAPDF_DOWNLOAD_DIR" -name 'verapdf-izpack-installer-*.jar' | head -n 1)
  [[ -n "$installer_jar" ]] || die "veraPDF installer not found in the downloaded zip."

  info "Installing veraPDF into _tools/veraPDF"
  # Unattended IzPack install: the only option the installer asks for is the path.
  printf 'INSTALL_PATH=%s\n' "$VERAPDF_DIR" > "$VERAPDF_DOWNLOAD_DIR/install.properties"
  java -jar "$installer_jar" -options "$VERAPDF_DOWNLOAD_DIR/install.properties" </dev/null

  rm -rf "$VERAPDF_DOWNLOAD_DIR"
fi

# ---------------------------------------------------------------------------
# 4. Verify
# ---------------------------------------------------------------------------
info "Installed versions"
if [[ -x "$VENV_DIR/bin/python" ]] && ! pypdf2_ok python3; then
  py="$VENV_DIR/bin/python"
else
  py=python3
fi
echo "PyPDF2   $("$py" -c 'import PyPDF2; print(PyPDF2.__version__)')"
echo "poppler  $(pdffonts -v 2>&1 | head -n 1)"
echo "Java     $(java -version 2>&1 | head -n 1)"
echo "veraPDF  $("$VERAPDF_DIR/verapdf" --version 2>/dev/null | head -n 1)"

cat <<EOF

Setup complete. ${PYTHON_NOTE}
Try it:
  mkdir -p _testdir && cp /path/to/your-paper.pdf _testdir/
  ./check_fonts_pdfa.py
  ./check_format.py
EOF
