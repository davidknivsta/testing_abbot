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
    message = """Bön för Israel och Ukraina.
Far i Himlen!
Vi ber om beskydd för Israel, dess folk, land och gränser.
Vi ber för alla oskyldiga, både judar och araber, som lider i kriget mellan Israel och Hamas. 
Vi ber att terrorism och antisemitism upphör. 
Vi ber att gisslan friges.
Vi ber om beskydd från falsk medierapportering, att sanningen kommer fram. 
Vi ber att Israel inte ska användas som en bricka i storpolitiskt spel. 
Vi önskar Jerusalem frid och att världens kristna skall vara Israels vänner och stöd. 
Vi ber att vi kristna ska älska både judar och araber. 
Vi ber om ett rättfärdigt styre över Gaza och Västbanken.

Herre, vi ber fortsatt för Ukraina, och för alla - både ukrainare och ryssar - som lider av kriget. Vi ber om fred.
Vi ber för alla dem som tvingas till fronterna.
Vi ber för alla hjälparbetare, att de ska vara beskyddade.
Vi ber om insikt, mod och handlingskraft hos politiker och ledare att gå fredens väg.
Vi ber för kyrkor och församlingar, att de ska få vara redskap för fred och försoning.
Vi ber även för världsekonomin.

Herre, kom med din frid, hjälp oss hålla fred. 
Jesus Kristus, ge oroliga hjärtan ro. 
I Jesu välsignade namn.
Amen!"""
    success = send_telegram_message(bot_token, chat_id, message)
    
    if success:
        print("🎉 Klart! Meddelandet har skickats.")
    else:
        print("💥 Något gick fel. Kolla loggarna ovan.")
        exit(1)

if __name__ == "__main__":
    main()
