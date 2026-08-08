import pandas as pd
import pyautogui
import time
import urllib.parse
import webbrowser
from datetime import datetime

FILE = "rent.xlsx"

# Timing
LOAD_TIME = 8
BEFORE_ENTER = 1
AFTER_SEND = 3
BETWEEN_MESSAGES = 2

# Read Excel
df = pd.read_excel(FILE)

# Make Status a text column
df["Status"] = df["Status"].fillna("").astype(str)

for index, row in df.iterrows():

    # Skip already sent
    if str(row["Status"]).strip():
        continue

    name = str(row["Name"]).strip()

    phone = (
        str(row["Phone number"])
        .replace("+", "")
        .replace(" ", "")
        .replace(".0", "")
    )

    message = f"Hi, {name} Your rent for the month is pending."
    encoded_message = urllib.parse.quote(message)

    print(f"Sending to {name}...")

    # Open WhatsApp chat
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"
    webbrowser.open(url)

    # Wait for WhatsApp to load
    time.sleep(LOAD_TIME)

    # Click message box
    screen_width, screen_height = pyautogui.size()

    pyautogui.click(
        screen_width // 2,
        screen_height - 80
    )

    time.sleep(BEFORE_ENTER)

    # Send message
    pyautogui.press("enter")

    # Wait for WhatsApp to process
    time.sleep(AFTER_SEND)

    # Update Excel
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    df.at[index, "Status"] = f"Sent on {timestamp}"

    # Save immediately
    df.to_excel(FILE, index=False)

    print(f"✓ Sent to {name}")

    # Close WhatsApp tab
    pyautogui.hotkey("ctrl", "w")

    time.sleep(BETWEEN_MESSAGES)

print("\nAll messages processed.")