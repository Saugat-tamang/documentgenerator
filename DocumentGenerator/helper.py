import nepali_datetime
from user.models import *
from nepali_date_converter import nepali_to_english_converter

def nep_to_eng_date_con(data):
    date_sp                 = data.split(".")
    year                    = int(date_sp[0])
    month                   = int(date_sp[1])
    day                     = int(date_sp[2])
    return nepali_to_english_converter(year,month,day)

def fiscal_year():
    today                   = str(nepali_datetime.date.today())
    date_sp                 = today.split("-")
    year                    = int(date_sp[0])
    month                   = int(date_sp[1])
    day                     = int(date_sp[2])
    if (month < 4):
        return f"{year-1}/{year}"
    else :
        return f"{year}/{year+1}"

def endDateFiscaYear(date):
    date_sp                 = date.split("-")
    year                    = int(date_sp[0])+1
    if year % 4 == 0 or year % 4 == 3:
        return f"{year}-03-32"
    else:
        return f"{year}-03-31"
    
def fiscal_year(data):
    date_sp                 = data.split("-")
    year                    = date_sp[0]
    nextyear                = int(date_sp[0])
    nextyear                = str(nextyear + 1)
    return f"{year[1:]}/{nextyear[2:]}"