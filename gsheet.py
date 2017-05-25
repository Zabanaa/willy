import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Startups List").sheet1

def save_startup_to_spreadsheet(startup_info, index):

    try:
        sheet.insert_row(startup_info, index)
    except Exception as e:
        return False

    return True

for i in range(10):

    print("Saving startup {}".format(i))
    save_startup_to_spreadsheet(["Berlin", "Soundcloud", "Python", "https://weoijqw.com"], i)
    print("Startup Saved !")
    print("")
