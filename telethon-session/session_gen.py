"""
Telegram String Session Generator — Python (Telethon)
======================================================
Requirements:  pip install telethon
Usage:         python3 session_gen.py
"""

import asyncio
import sys


def check_deps():
    try:
        import telethon  # noqa
    except ImportError:
        print("❌  Telethon is not installed.\n    Run: pip install telethon")
        sys.exit(1)


def banner():
    print("╔══════════════════════════════════════════╗")
    print("║  Telegram String Session Generator       ║")
    print("║  Powered by Telethon (Python)            ║")
    print("╚══════════════════════════════════════════╝")
    print()
    print("Get your API credentials at: https://my.telegram.org/apps")
    print()


def get_api_id() -> int:
    while True:
        try:
            val = int(input("Enter your API ID: ").strip())
            if val > 0:
                return val
            print("❌  Must be a positive integer.")
        except ValueError:
            print("❌  Invalid input — enter a number.")
        except (KeyboardInterrupt, EOFError):
            print("\nAborted."); sys.exit(0)


def get_api_hash() -> str:
    while True:
        try:
            val = input("Enter your API Hash: ").strip()
            if len(val) >= 10:
                return val
            print("❌  Too short — should be a 32-character hex string.")
        except (KeyboardInterrupt, EOFError):
            print("\nAborted."); sys.exit(0)


async def generate_session():
    from telethon import TelegramClient
    from telethon.sessions import StringSession

    banner()
    api_id   = get_api_id()
    api_hash = get_api_hash()

    print("\n🔗  Connecting to Telegram …")

    client = TelegramClient(StringSession(), api_id, api_hash)

    try:
        await client.start()
    except KeyboardInterrupt:
        print("\nAborted."); return
    except Exception as e:
        print(f"❌  Login failed: {e}"); return

    session_string = client.session.save()

    print()
    print("╔══════════════════════════════════════════╗")
    print("║    ✅  YOUR STRING SESSION (Telethon)    ║")
    print("╚══════════════════════════════════════════╝")
    print()
    print(session_string)
    print()

    try:
        with open("telethon_session.txt", "w") as f:
            f.write(session_string + "\n")
        print("💾  Session saved to: telethon_session.txt")
    except OSError as e:
        print(f"⚠️   Could not save: {e}")

    try:
        me = await client.get_me()
        print()
        print("👤  Logged in as:")
        print(f"    Name    : {me.first_name} {me.last_name or ''}".rstrip())
        if me.username:
            print(f"    Username: @{me.username}")
        print(f"    User ID : {me.id}")
        print(f"    Phone   : +{me.phone}")
    except Exception as e:
        print(f"⚠️   Could not fetch account info: {e}")

    await client.disconnect()
    print()
    print("⚠️   KEEP YOUR SESSION STRING SECRET — it gives full access to your account!")


if __name__ == "__main__":
    check_deps()
    try:
        asyncio.run(generate_session())
    except KeyboardInterrupt:
        print("\nAborted.")
