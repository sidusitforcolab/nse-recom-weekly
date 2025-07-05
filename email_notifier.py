import os
import yagmail

sender = os.environ.get("EMAIL_USER")
password = os.environ.get("EMAIL_PASS")
receiver = sender  # or change to another email

attachment = "output/weekly_top_stocks.csv"

subject = "📊 Weekly NSE Stock Picks"
body = "Hi,\n\nHere are the recommended stocks for this week.\n\nCheers,\nYour Recommender Bot"

yag = yagmail.SMTP(sender, password)
yag.send(to=receiver, subject=subject, contents=body, attachments=attachment)
print("📧 Email sent!")