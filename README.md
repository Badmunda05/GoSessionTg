# Telegram String Session Generator

Generate a **Telegram String Session** from your account using two tools:

| Folder | Language | Library |
|--------|----------|---------|
| `go-session/` | Go | [gogram](https://github.com/amarnathcjd/gogram) |
| `python-session/` | Python | [Telethon](https://github.com/LonamiWebs/Telethon) |

A String Session lets userbot/bot scripts log in as your account on a VPS without
needing OTP every time.

---

## Step 0 — Get API Credentials

1. Open [https://my.telegram.org/apps](https://my.telegram.org/apps)
2. Log in with your phone number
3. Create a new app (any name is fine)
4. Copy your **App ID** (integer) and **App Hash** (32-char hex string)

---

## Option A — Python / Telethon (Easiest)

### Install

```bash
# Make sure Python 3.8+ is installed
python3 --version

# Install Telethon
pip install telethon
# or
pip install -r python-session/requirements.txt
```

### Run

```bash
cd python-session
python3 session_gen.py
```

### What happens

```
Enter your API ID: 12345678
Enter your API Hash: abcdef1234567890abcdef1234567890

🔗  Connecting to Telegram …
Please enter your phone (or bot token): +919876543210
Please enter the code you received: 12345
(2FA password if enabled): ••••••••

✅  YOUR STRING SESSION (Telethon)

1BQANOTREALxxxxxxxxxxxxxxx...

💾  Session saved to: telethon_session.txt
👤  Logged in as: John Doe  @johndoe  ID: 123456789
```

---

## Option B — Go / GoGram

### Install Go

**Ubuntu / Debian VPS:**
```bash
sudo apt update && sudo apt install -y golang-go
go version   # should print go1.21+
```

**Manual (latest Go):**
```bash
wget https://go.dev/dl/go1.22.4.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
```

### Run

```bash
cd go-session

# Download dependencies (only needed once)
go mod tidy

# Run
go run main.go
```

### Build a standalone binary (optional)

```bash
cd go-session
go build -o session-gen main.go

# Run without needing Go installed
./session-gen
```

---

## Using the Session String

### In a Telethon userbot/bot

```python
from telethon import TelegramClient
from telethon.sessions import StringSession

SESSION  = "YOUR_SESSION_STRING_HERE"
API_ID   = 12345678
API_HASH = "your_api_hash_here"

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def main():
    await client.start()
    me = await client.get_me()
    print(f"Logged in as: {me.first_name}")

import asyncio
asyncio.run(main())
```

### In a GoGram userbot/bot

```go
package main

import (
    "fmt"
    "github.com/amarnathcjd/gogram/telegram"
)

func main() {
    client, _ := telegram.NewClient(telegram.ClientConfig{
        AppID:   12345678,
        AppHash: "your_api_hash_here",
        StringSession: "YOUR_SESSION_STRING_HERE",
    })
    client.Conn()
    me, _ := client.GetMe()
    fmt.Println("Logged in as:", client.JSON(me, true))
    client.Idle()
}
```

---

## VPS Quick-Start (Copy-Paste)

### Python on a fresh Ubuntu VPS

```bash
sudo apt update && sudo apt install -y python3 python3-pip git
git clone https://github.com/YOUR_USERNAME/TgSessionGen.git
cd TgSessionGen/python-session
pip3 install telethon
python3 session_gen.py
```

### Go on a fresh Ubuntu VPS

```bash
sudo apt update && sudo apt install -y golang-go git
git clone https://github.com/YOUR_USERNAME/TgSessionGen.git
cd TgSessionGen/go-session
go mod tidy
go run main.go
```

---

## Project Structure

```
TgSessionGen/
├── go-session/
│   ├── main.go          ← Go session generator (GoGram)
│   └── go.mod           ← Go module / dependency file
├── python-session/
│   ├── session_gen.py   ← Python session generator (Telethon)
│   └── requirements.txt ← Python dependencies
└── README.md
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `go: command not found` | Install Go — see Option B above |
| `ModuleNotFoundError: telethon` | Run `pip install telethon` |
| OTP not arriving | Check Telegram app — code arrives as a message from Telegram |
| `PHONE_NUMBER_INVALID` | Use full international format: `+919876543210` |
| `AUTH_KEY_UNREGISTERED` | Session expired — generate a new one |
| 2FA password prompt | Enter your Telegram Two-Step Verification password |
| `go mod tidy` fails | Check internet connection; GitHub must be reachable |

---

## Security

- **Never share your session string** — it gives complete access to your Telegram account
- **Never commit it to GitHub** — add these to `.gitignore`:

```
session_string.txt
telethon_session.txt
*.session
```

- Store it as an **environment variable** when deploying:

```bash
export SESSION_STRING="your_session_here"
```

```python
import os
SESSION = os.environ["SESSION_STRING"]
```

---

## License

MIT — free to use, modify, and distribute.
