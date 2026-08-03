from agent import app, get_email_body
from auth import get_gmail_service

def process_recent_emails(max_emails=5):
    service = get_gmail_service()
    
    results = service.users().messages().list(userId='me', maxResults=max_emails, q="is:unread").execute()
    messages = results.get('messages', [])
    
    if not messages:
        print("No unread emails found.")
        return
    
    print(f"Processing {len(messages)} unread emails...\n")
    
    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = message['payload']['headers']
        
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        body = get_email_body(service, msg['id'])
        
        print(f"Processing: {subject}")
        
        result = app.invoke({
            "email_id": msg['id'],
            "subject": subject,
            "sender": sender,
            "body": body,
            "category": "",
            "action_taken": ""
        })
        
        print(f"→ Category: {result['category']}")
        print(f"→ Action: {result['action_taken']}")
        print("-" * 60)

if __name__ == "__main__":
    process_recent_emails()
