import datetime
import urllib
import csv

'''
@function Craw historical stock data using google finance api. 
  The result is stored in a csv file under path "./data/" .
@parameter symbol: the company symbol.
@parameter start_date: the starting date in formate "yyyy-mm-dd".
@parameter end_date: the ending date in formate "yyyy-mm-dd". Default date is today.
'''
def get_hist_data(symbol, start_date, end_date = datetime.date.today().isoformat()):
  start = datetime.date(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
  end = datetime.date(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]))
  url = "http://www.google.com/finance/historical?q={0}".format(symbol.upper())
  url += "&startdate={0}&enddate={1}&output=csv".format(
    start.strftime('%b %d, %Y'),end.strftime('%b %d, %Y'))
  csv = urllib.urlopen(url).readlines()
  csv.reverse()

  filepath = "./input/{0}.csv".format(symbol) 
  with open(filepath,'wb') as csvfile:
    for bar in xrange(0,len(csv)-1):
      ds,open_,high,low,close,volume = csv[bar].rstrip().split(',')
      # open_,high,low,close = [float(x) for x in [open_,high,low,close]]
      dt = datetime.datetime.strptime(ds,'%d-%b-%y')
      line = [close]
      csvfile.write(",".join(line))
      csvfile.write('\n')

get_hist_data('aapl', "2001-01-01")