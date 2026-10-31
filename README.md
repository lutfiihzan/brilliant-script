# BrillianScript

Kumpulan skrip utilitas BrillianLabs.

Repo: [github.com/BrillianLabs/BrillianScript](https://github.com/BrillianLabs/BrillianScript)

| Folder | Deskripsi |
|--------|-----------|
| [script-laporan-bulanan](script-laporan-bulanan/) | Generator laporan bulanan Tenaga Teknis (Python + Word) |
| [script-spmb-bot](script-spmb-bot/) | Bot registrasi & login SPMB Kab. Bogor (JS + Python) |
| [script-decoder](script-decoder/) | Decoder PHP terenkripsi (php-encryptor) |
| [script-getcontact](script-getcontact/) | Bot cek tag GetContact (Web + CLI) |

## Quick start

### Laporan bulanan

```powershell
cd script-laporan-bulanan
pip install -r generator/requirements.txt
python laporan.py report 202610   # alur lengkap: script-laporan-bulanan/README.md
```

### SPMB bot

```powershell
# JavaScript
cd script-spmb-bot/javascript
copy .data.example .data
.\run.ps1 --check-login

# Python
cd script-spmb-bot/python
copy .data.example .data
python spmb_bot.py --audit
```

Dokumentasi: [script-spmb-bot/README.md](script-spmb-bot/README.md)

### PHP decoder

```powershell
cd script-decoder
python script/decode_php.py
```

Dokumentasi: [script-decoder/README.md](script-decoder/README.md)

### GetContact bot

```powershell
# Web (interaktif)
cd script-getcontact/web
pip install -r requirements.txt
python app.py
# buka http://localhost:5050

# CLI (PHP)
cd script-getcontact
php script/bot.php
```

Dokumentasi: [script-getcontact/README.md](script-getcontact/README.md)
