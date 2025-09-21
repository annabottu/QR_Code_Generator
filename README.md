# QR Code Generator

Generates QR codes as PNG files with the inputed URL by user.

## Requirements

Install dependencies with:

pip install -r requirements.txt

## Usage

Interactive:

python qr_gui.py

CLI:

python qr_gui.py "https://example.com" --output my_qr.png

## Notes

- The module lazily imports `qrcode` so importing `qr_gui` doesn't require
  having dependencies installed if you only want to read the module.
