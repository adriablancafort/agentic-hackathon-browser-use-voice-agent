#!/bin/sh
set -e

REPO="browser-use/profile-use-releases"
BINARY_NAME="profile-use"
WORK_DIR="${TMPDIR:-$HOME/.cache/profile-use-installer}"

cleanup() {
    [ -f "$TMP_FILE" ] && rm -f "$TMP_FILE"
}

trap cleanup EXIT INT TERM

detect_os() {
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    case "$OS" in
        linux*)   OS='linux' ;;
        darwin*)  OS='darwin' ;;
        msys*|mingw*|cygwin*) OS='windows' ;;
        *)
            echo "Error: Unsupported OS: $(uname -s)" >&2
            exit 1
            ;;
    esac
}

detect_arch() {
    ARCH=$(uname -m)
    case "$ARCH" in
        x86_64|amd64) ARCH='amd64' ;;
        aarch64|arm64) ARCH='arm64' ;;
        *)
            echo "Error: Unsupported architecture: $(uname -m)" >&2
            exit 1
            ;;
    esac
}

get_latest_version() {
    VERSION=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    if [ -z "$VERSION" ]; then
        echo "Error: Failed to fetch latest version" >&2
        exit 1
    fi
}

download_and_run() {
    mkdir -p "$WORK_DIR"
    
    BINARY_URL="https://github.com/$REPO/releases/download/$VERSION/${BINARY_NAME}-${OS}-${ARCH}"
    
    if [ "$OS" = "windows" ]; then
        BINARY_URL="${BINARY_URL}.exe"
        TMP_FILE="$WORK_DIR/${BINARY_NAME}.exe"
    else
        TMP_FILE="$WORK_DIR/$BINARY_NAME"
    fi
    
    if command -v curl >/dev/null 2>&1; then
        if ! curl -fsSL --retry 3 --retry-delay 1 -o "$TMP_FILE" "$BINARY_URL"; then
            echo "Error: Download failed from $BINARY_URL" >&2
            exit 1
        fi
    elif command -v wget >/dev/null 2>&1; then
        if ! wget -q -O "$TMP_FILE" "$BINARY_URL"; then
            echo "Error: Download failed from $BINARY_URL" >&2
            exit 1
        fi
    else
        echo "Error: curl or wget required" >&2
        exit 1
    fi

    chmod +x "$TMP_FILE" 2>/dev/null || true
    
    [ "$OS" = "darwin" ] && xattr -d com.apple.quarantine "$TMP_FILE" 2>/dev/null || true
    
    # Pass BROWSER_USE_API_KEY if set
    if [ -n "${BROWSER_USE_API_KEY:-}" ]; then
        export BROWSER_USE_API_KEY
    fi
    
    "$TMP_FILE" </dev/tty
}

main() {
    detect_os
    detect_arch
    
    if [ -n "${PROFILE_USE_VERSION:-}" ]; then
        VERSION="$PROFILE_USE_VERSION"
    else
        get_latest_version
    fi
    
    download_and_run
}

main