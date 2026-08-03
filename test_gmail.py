from auth import get_gmail_service

service = get_gmail_service()

# Get the latest 5 emails
results = service.users().messages().list(userId='me', maxResults=5).execute()
messages = results.get('messages', [])

print(f"Found {len(messages)} recent emails:\n")

for msg in messages:
    message = service.users().messages().get(userId='me', id=msg['id']).execute()
    headers = message['payload']['headers']
    
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
    
    print(f"From: {sender}")
    print(f"Subject: {subject}")
    print("-" * 50)
