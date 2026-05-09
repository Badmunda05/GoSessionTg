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
        print("❌ Telethon is not installed.")
        print("Run: pip install telethon")
        sys.exit(1)


def banner():
    print("╔══════════════════════════════════════════╗")
    print("║  Telegram String Session Generator      ║")
    print("║  Powered by Telethon (Python)           ║")
    print("╚══════════════════════════════════════════╝")
    print()
    print("Get your API credentials at:")
    print("https://my.telegram.org/apps")
    print()


def get_api_id() -> int:
    while True:
        try:
            val = int(input("Enter your API ID: ").strip())

            if val > 0:
                return val

            print("❌ Must be a positive integer.")

        except ValueError:
            print("❌ Invalid input — enter numbers only.")

        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            sys.exit(0)


def get_api_hash() -> str:
    while True:
        try:
            val = input("Enter your API Hash: ").strip()

            if len(val) >= 10:
                return val

            print("❌ Invalid API Hash.")

        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            sys.exit(0)


async def generate_session():
    from telethon import TelegramClient
    from telethon.sessions import StringSession

    banner()

    api_id = get_api_id()
    api_hash = get_api_hash()

    print("\n🔗 Connecting to Telegram...")

    client = TelegramClient(
        StringSession(),
        api_id,
        api_hash
    )

    try:
        await client.start()

    except KeyboardInterrupt:
        print("\nAborted.")
        return

    except Exception as e:
        print(f"❌ Login failed: {e}")
        return

    # ── Generate Session ────────────────────────────────────────────
    session_string = client.session.save()

    print()
    print("╔══════════════════════════════════════════╗")
    print("║   ✅ YOUR STRING SESSION (Telethon)     ║")
    print("╚══════════════════════════════════════════╝")
    print()

    print(session_string)
    print()

    # ── Send Session to Saved Messages ──────────────────────────────
    try:
        message_text = (
            "✅ YOUR STRING SESSION (Telethon)\n\n"
            f"`{session_string}`\n\n"
            "⚠️ KEEP YOUR SESSION STRING SECRET!"
        )

        await client.send_message(
            "me",
            message_text,
            parse_mode="md"
        )

        print("📨 Session sent to Saved Messages.")

    except Exception as e:
        print(f"⚠️ Could not send message: {e}")

    # ── Account Info ────────────────────────────────────────────────
    try:
        me = await client.get_me()

        print()
        print("👤 Logged in as:")

        full_name = f"{me.first_name} {me.last_name or ''}".strip()

        print(f"    Name    : {full_name}")

        if me.username:
            print(f"    Username: @{me.username}")

        print(f"    User ID : {me.id}")
        print(f"    Phone   : +{me.phone}")

    except Exception as e:
        print(f"⚠️ Could not fetch account info: {e}")

    await client.disconnect()

    print()
    print("⚠️ KEEP YOUR SESSION STRING SECRET.")
    print("It gives full access to your Telegram account.")


if __name__ == "__main__":
    check_deps()

    try:
        asyncio.run(generate_session())

    except KeyboardInterrupt:
        print("\nAborted.")
