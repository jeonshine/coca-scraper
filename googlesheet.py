from oauth2client.service_account import ServiceAccountCredentials
import gspread

def connect(file_name):

    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]
    json_file_name = 'lxper.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)

    return gc.open(file_name)

def write(worksheet, index, result):

    last_alphabet = chr(65 + len(result))

    try:
        worksheet.update(f"A{index}:{last_alphabet}{index}", [result])
    except:
        # over 50000 string in one cell ==> error
        # allow one data writing per a sec
        print(f"{index} index got error while writing")