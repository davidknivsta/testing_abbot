import os
import requests
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_message_from_google_docs(document_id, service_account_json):
    """Hämta meddelande från Google Docs"""
    try:
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(service_account_json),
            scopes=['https://www.googleapis.com/auth/documents.readonly']
        )
        service = build('docs', 'v1', credentials=credentials)
        document = service.documents().get(documentId=document_id).execute()
        content = document.get('body', {}).get('content', [])
        message_text = ""
        
        for element in content:
            if 'paragraph' in element:
                paragraph = element['paragraph']
                for text_run in paragraph.get('elements', []):
                    if 'textRun' in text_run:
                        message_text += text_run['textRun']['content']
        
        return message_text.strip()
    except Exception as e:
        print(f"❌ Fel vid hämtning från Google Docs: {e}")
        return None

def send_telegram_message(bot_token, chat_id, message, thread_id=None):
    """Skicka meddelande via Telegram Bot API med stöd för Topics"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    if thread_id:
        try:
            payload['message_thread_id'] = int(thread_id)
        except ValueError:
            pass # Ignorera om det inte är en siffra
            
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        if response.json().get('ok'):
            print(f"✅ Meddelande skickat!")
            return True
        else:
            print(f"❌ Telegram API fel: {response.json()}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Nätverksfel: {e}")
        return False

def main():
    print("🚀 Startar bot via Google Cloud Run...")
    
    bot_token = os.getenv('BOT_TOKEN')
    raw_chat_id = os.getenv('CHAT_ID')
    document_id = os.getenv('GOOGLE_DOC_ID')
    service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    fallback_message = os.getenv('DAILY_MESSAGE')
    
    if not bot_token or not raw_chat_id:
        print("❌ BOT_TOKEN eller CHAT_ID saknas i miljövariablerna.")
        exit(1)

    # Hantera Topic ID (om CHAT_ID innehåller ett kolon)
    if ':' in raw_chat_id:
        chat_id, thread_id = raw_chat_id.split(':')
        chat_id, thread_id = chat_id.strip(), thread_id.strip()
    else:
        chat_id, thread_id = raw_chat_id.strip(), None

    # Hämta meddelandet
    message = None
    if document_id and service_account_json:
        print("📄 Hämtar från Google Docs...")
        message = get_message_from_google_docs(document_id, service_account_json)
        
    if not message and fallback_message:
        print("📝 Använder DAILY_MESSAGE som fallback...")
        message = fallback_message
        
    if not message:
        print("⚠️ Inget meddelande hittades, använder standard...")
        message = "🌟 God kväll allihopa! Hoppas ni mår bra!"

    # Skicka
    success = send_telegram_message(bot_token, chat_id, message, thread_id)
    if not success:
        exit(1)

if __name__ == "__main__":
    main()
