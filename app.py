from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

sheet = None
try:
    # Google Sheets API setup
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)

    # Open spreadsheet (CHANGE 'UserData' to your sheet name if needed)
    sheet = client.open("UserData").sheet1
    print("[INFO] ✅ Connected to Google Sheets successfully.")

except Exception as e:
    print("[ERROR] ❌ Failed to connect to Google Sheets:", e)
    sheet = None

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        user_id = request.form.get("user_id")
        found = False

        if sheet:
            try:
                rows = sheet.get_all_records()
                for row in rows:
                    # Handle messy header by finding the first key
                    first_key = list(row.keys())[0]
                    if str(row.get(first_key)) == str(user_id):
                        message = f"Welcome {row.get('name')}! Your email is {row.get('email')}."
                        found = True
                        break
                if not found:
                    message = "User ID not found."
            except Exception as e:
                message = f"Error reading data from Google Sheets: {e}"
        else:
            message = "Error: Could not connect to Google Sheets."

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
