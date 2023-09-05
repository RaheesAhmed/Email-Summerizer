# Email-Summerizer
The code provided is a Flask app that processes emails of their content using the OpenAI API. Here's a it works:

1. Import the   ```
   from flask import Flask,, jsonifychain.text_splitter import RecursiveCharacterTextSplitter
   import imaplib
   import email
   from email.header import decode_header
 openai
   import os
   ```

2. Initialize the Flask app:

   ```
   app = Flask(__   ``:

 ```
   @app.route('/process_emails', methods=['GET'])
   def process_emails():
   ```

4. Retrieve Gmail credentials from URL   ```
 = request.args.get('_password     open.api_key = os.environ["OPENAI_API_KEY"]
   text_splitter2 = RecursiveCharacterSplitter(chunk_size=1500, chunk)
  . Connect to the IMAP server and login to the email account:

lib.IMAP4_SSL("imap.gmail.com")
   mail.login(email_user)
   ``7. (in "inbox:

   ```
 = " mail.select(mailbox)
   `` Create to store email summaries:

  _list = []
   ```

9. Retrieve email IDs:

   ```
   status, email_ids = mail_ids[0].split()[:5  # Limit to 5 emails for this example
   ```

10. Iterate through the selected email IDs:

    ```
    for email_id in email_id_list:
 ```

11. Fetch the email data:

    ```
    status, = mail(email_id822)")
 msg = email.message_from_bytes(msg_data[0][1])
   `

. Decode the email subject:

       subject, encoding =_header(msgsubject)[0]
    if isinstance(subject, bytes):
        subject = subject.decode`

. Create a dictionary to store email summaries, parts of the email():
 ```

15. Check is not an    content.get if " chunks=True)
    if content_type == "        email_body = payload.decode()
        email_chunks = text_splitter2.split_text(email)
=prompt,
=150 summary = response.choices[0].text.strip()
        email_summary['Summary'].append(summary)
    ```

18. Append the email summary to the list:

    ```
    summaries_list.append(email_summary)
    ```

19. Logout from the    ```

20 list of summaries as a JSON response:

    ```
    return jsonify(summaries_list)
    the Flask app in debug mode:

 ```
    if __name__ ==main__':
       .run(debug=True)
    ```

To use this code, you need to have the required libraries installed, set up the OpenAI API key as an environment, and provide valid Gmail credentials as parameters when making a request to the `/process_emails` endpoint. The code will retrieve the specified number of emails from split their content into generate summaries using theAI API. The summaries will be returned as a JSON response.

<b>References:</b>
<span>[1] <a href='https://stackoverflow.com/questions/17640687/flask-how-do-i-read-the-raw-body-in-a-post-request-when-the-content-type-is-a' target='_blank' class='text-purple-1 underline'>Flask - How do I read the raw body in a POST request ...</a></span>
<span>[2] <a href='https://www.reddit.com/r/LangChain/comments/14x0lap/open_ai_chatbot_streaming/' target='_blank' class='text-purple-1 underline'>OPEN AI chatbot streaming : r/LangChain</a></span>
<span>[3] <a href='https://community.openai.com/t/how-to-use-fine-tune-model-using-python-flask/98454' target='_blank' class='text-purple-1 underline'>How to use fine tune model using python flask - API</a></span>
