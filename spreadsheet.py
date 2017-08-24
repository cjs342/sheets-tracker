"""
Boilerplate login code taken from the gspread tutorial at:
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
"""

from oauth2client.service_account import ServiceAccountCredentials
import private
import gspread #make sure this is BELOW oauth2client import. NO IDEA why this is needed for Heroku to work
import time

def writeToSpreadsheet(cat_key, cat_name, amount):#(row,col,x):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sht_name = private.getSheetName()
    sheet1 = client.open(sht_name).sheet1

    # Extract and print all of the values
    #list_of_hashes = sheet.get_all_records()
    #print(list_of_hashes)

    # Write to the sheet
    #sheet.update_cell(1,1,"Hello, World!")
    row = 2
    #if sheet1.row_values(row)[0] != None:
    #    amount = "ERROR"
    while sheet1.row_values(row)[0] != '':
        row+=1

    #columns = private.getColumns()
    time_now = time.strftime("%H:%M:%S")
    date = time.strftime("%m/%d/%Y")

    sheet1.update_cell(row,1,date)
    sheet1.update_cell(row,2,time_now)
    sheet1.update_cell(row,3,cat_name)
    sheet1.update_cell(row,4,amount)

def getLastEntry():
    """TO DO: Return the last entered category + amount"""
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sht_name = private.getSheetName()
    sheet1 = client.open(sht_name).sheet1

    row = 2
    while sheet1.row_values(row)[0] != '':
        row+=1
    row-=1
    cat = sheet1.row_values(row)[2]
    val = sheet1.row_values(row)[3]
    return cat,val
