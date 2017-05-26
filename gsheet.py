import gspread
from oauth2client.service_account import ServiceAccountCredentials
from celery import Celery

app     = Celery("tasks", backend="amqp", broker="amqp://localhost//")

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Startups List").sheet1

@app.task
def insert_row_to_spreadsheet(startup_info, index):

    try:
        sheet.insert_row(startup_info, index)
        print("Inserting Row ...")
    except Exception as e:
        return False

    print("Row inserted !")

def delete_rows():

    try:
        all_records = sheet.get_all_records()
    except IndexError as e:
        print("Worksheet Already Empty")
        return

    sheet.clear()
