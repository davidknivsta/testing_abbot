import os
import requests
from datetime import datetime
import pytz

def get_daily_message():
    """
    Använder inte denna funktion nu. Men den ligger kvar
    för att kunna användas i framtiden för att till exempel
    hämta dagens bön från ett Google document.
    (Orginalfunktion)
    Skapa dagens meddelande.
    Anpassa denna funktion för dina egna meddelanden!
    """
    # Sätt tidzon till svensk tid
    stockholm_tz = pytz.timezone('Europe/Stockholm')
    today = datetime.now(stockholm_tz)
    
    weekday = today.strftime('%A')
    date_str = today.strftime('%Y-%m-%d')
    
    # Översätt veckodagar till svenska
    weekdays = {
        'Monday': 'Måndag',
        'Tuesday': 'Tisdag', 
        'Wednesday': 'Onsdag',
        'Thursday': 'Torsdag',
        'Friday': 'Fredag',
        'Saturday': 'Lördag',
        'Sunday': 'Söndag'
    }
    
    swedish_weekday = weekdays.get(weekday, weekday)
    
    # Olika meddelanden för olika dagar
    messages = {
        0: f"🌟 God måndag kväll! Ny vecka, nya möjligheter! {date_str}",
        1: f"💪 Tisdag kväll - halvvägs genom veckan! {date_str}",
        2: f"🐪 Onsdag = kameldagen! Hoppas ni mår bra!",
        3: f"🎯 Torsdag kväll - snart helg! {date_str}",
        4: f"🎉 Fredag kväll! Äntligen helg! {date_str}",
        5: f"😎 Lördag kväll - njut av helgen! {date_str}",
        6: f"🌙 Söndag kväll - vila inför nya veckan! {date_str}"
    }
    
    day_index = today.weekday()
    return messages.get(day_index, f"✨ Trevlig {swedish_weekday}kväll! {date_str}")

def send_telegram_message(bot_token, chat_id, message):
    """
    Skicka meddelande via Telegram Bot API
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'  # Tillåter HTML-formatering
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        if response.json().get('ok'):
            print(f"✅ Meddelande skickat: {message}")
            return True
        else:
            print(f"❌ Telegram API fel: {response.json()}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Nätverksfel: {e}")
        return False

def main():
    """
    Huvudfunktion som körs av GitHub Actions
    Lägger dagens bön i main.
    """
       
    print("🚀 Startar daglig bot...")
    
    # Hämta secrets från GitHub Actions miljövariabler
    bot_token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    
    if not bot_token:
        print("❌ BOT_TOKEN saknas i GitHub Secrets")
        exit(1)
        
    if not chat_id:
        print("❌ CHAT_ID saknas i GitHub Secrets")
        exit(1)
    
    # Skapa och skicka meddelandet
    # message = get_daily_message()
    message = os.getenv('DAILY_MESSAGE')
    success = send_telegram_message(bot_token, chat_id, message)
    
    if success:
        print("🎉 Klart! Meddelandet har skickats.")
    else:
        print("💥 Något gick fel. Kolla loggarna ovan.")
        exit(1)

if __name__ == "__main__":
    main()
