
def fiscal_year(data):
    date_sp             = data.split("-")
    year                = date_sp[0]
    nextyear            = int(date_sp[0])
    nextyear            = str(nextyear + 1)
    return f"{year[1:]}/{nextyear[2:]}"


def endDateFiscaYear(date):
    date_sp             = date.split("-")
    year                = int(date_sp[0])+1
    if year % 4 == 0 or year % 4 == 3:
        return f"{year}-03-32"
    else:
        return f"{year}-03-31"