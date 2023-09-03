from flask import Flask, request, jsonify
from langchain.text_splitter import RecursiveCharacterTextSplitter
import imaplib
import email
from email.header import decode_header
import openai
import os

app = Flask(__name__)

@app.route('/process_emails', methods=['GET'])
def process_emails():
    # Assuming you're going to pass Gmail credentials via URL parameters for this example
    email_user = request.args.get('email_user')
    email_password = request.args.get('email_password')

    # Initialize your original code's setup
    openai.api_key = openai.api_key = os.environ["OPENAI_API_KEY"]
    text_splitter2 = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)

    # Initialize IMAP and login
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_password)
    mailbox = "inbox"
    mail.select(mailbox)
    
    summaries_list = []
    
    status, email_ids = mail.search(None, "ALL")
    email_id_list = email_ids[0].split()[:5]
    for email_id in email_id_list:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        subject, encoding = decode_header(msg["subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        email_summary = {'From': msg["from"], 'Subject': subject, 'Summary': []}

        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if content_type == "text/plain":
                    email_body = payload.decode()
                    email_chunks = text_splitter2.split_text(email_body)
                    for chunk in email_chunks:
                        prompt = f"Summarize the following email content:\n{chunk}"
                        response = openai.Completion.create(
                            engine="text-davinci-003",
                            prompt=prompt,
                            max_tokens=150
                        )
                        summary = response.choices[0].text.strip()
                        email_summary['Summary'].append(summary)
        
        summaries_list.append(email_summary)

    mail.logout()
    
    return jsonify(summaries_list)

if __name__ == '__main__':
    app.run(debug=True)
