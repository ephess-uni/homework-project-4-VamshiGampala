# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new=[]
    for dates in old_dates:
        new.append(datetime.strptime(dates, "%Y-%m-%d").strftime("%d %b %Y"))
    return new

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    try:
        if isinstance(start, str) and isinstance(n, int):
            lis=[]
            for i in range(0,n):
                lis.append(datetime.strptime(start,"%Y-%m-%d")  + timedelta(days=i))
            return lis
    except TypeError:
        pass


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    lis=[]
    z=0
    for i in values:
        a=[]       
        a.append(datetime.strptime(start_date,"%Y-%m-%d")  + timedelta(days=z))
        a.append()
        lis.append(tuple(a))
        z+=1
    return lis


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile) as f:
        li=[]
        DictReader_obj = DictReader(f)
        for item in DictReader_obj:
            di={}
            day=datetime.strptime(item['date_returned'],'%m/%d/%Y')- datetime.strptime(item['date_due'],'%m/%d/%Y') 
            if(day.days>0):
                amount=day.days*0.25
                di["patron_id"]=item['patron_id']
                di["late_fees"]=day.days*0.25
                li.append(di)
    with open('output.csv',"w", newline="", encoding="utf-8-sig") as outfile:

        writer = DictWriter(outfile, ["patron_id", "late_fees"])

        writer.writeheader()

        writer.writerow(li)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
