from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from auth import get_gmail_service
import base64
from email.mime.text import MIMEText

# Define the state
class EmailState(TypedDict):
    email_id: str
    subject: str
    sender: str
    body: str
    category: str
    action_taken: str

# Initialize LLM (using Ollama so it’s free)
llm = ChatOllama(model="llama3.2", temperature=0)

def get_email_body(service, msg_id):
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = message['payload']
    
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                break
    else:
        data = payload['body'].get('data', '')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    
    return body[:2000]  # Limit length

def classify_email(state: EmailState):
    prompt = ChatPromptTemplate.from_template("""
You are an expert email assistant. Classify the following email into exactly one of these categories:

1. Reply Now - Urgent or important emails that need a quick response
2. Reply Later - Important but not urgent
3. No Action - Newsletters, promotions, notifications, or low priority

Email:
From: {sender}
Subject: {subject}
Body: {body}

Reply with ONLY the category name (Reply Now, Reply Later, or No Action).
""")
    
    chain = prompt | llm
    result = chain.invoke({
        "sender": state["sender"],
        "subject": state["subject"],
        "body": state["body"]
    })
    
    category = result.content.strip()
    return {"category": category}

def apply_label(state: EmailState):
    service = get_gmail_service()
    category = state["category"]
    
    # Map categories to Gmail labels
    label_map = {
        "Reply Now": "Reply Now",
        "Reply Later": "Reply Later",
        "No Action": "No Action"
    }
    
    label_name = label_map.get(category, "No Action")
    
    # Create label if it doesn't exist
    try:
        labels = service.users().labels().list(userId='me').execute().get('labels', [])
        label_id = None
        for label in labels:
            if label['name'] == label_name:
                label_id = label['id']
                break
        
        if not label_id:
            new_label = service.users().labels().create(
                userId='me',
                body={'name': label_name, 'labelListVisibility': 'labelShow', 'messageListVisibility': 'show'}
            ).execute()
            label_id = new_label['id']
        
        # Apply the label
        service.users().messages().modify(
            userId='me',
            id=state["email_id"],
            body={'addLabelIds': [label_id]}
        ).execute()
        
        return {"action_taken": f"Labeled as {label_name}"}
    except Exception as e:
        return {"action_taken": f"Error: {str(e)}"}

# Build the graph
workflow = StateGraph(EmailState)

workflow.add_node("classify", classify_email)
workflow.add_node("apply_label", apply_label)

workflow.set_entry_point("classify")
workflow.add_edge("classify", "apply_label")
workflow.add_edge("apply_label", END)

app = workflow.compile()
