# This program gets the historical and realtime stock data from goolglefinance 
# vheck the time delay from website: https://www.google.co.in/googlefinance/disclaimer/

from urllib2 import Request, urlopen 
import json
import csv

# get realtime data ----------------------------------------------------------
FullName = {
    u'id'     : u'ID',
    u't'      : u'StockSymbol',
    u'e'      : u'Index',
    u'l'      : u'LastTradePrice',
    u'l_cur'  : u'LastTradeWithCurrency',
    u'ltt'    : u'LastTradeTime',
    u'lt_dts' : u'LastTradeDateTime',
    u'lt'     : u'LastTradeDateTimeLong',
    u'div'    : u'Dividend',
    u'yld'    : u'Yield',
    u's'      : u'LastTradeSize',
    u'c'      : u'Change',
    u'c'      : u'ChangePercent',
    u'el'     : u'ExtHrsLastTradePrice',
    u'el_cur' : u'ExtHrsLastTradeWithCurrency',
    u'elt'    : u'ExtHrsLastTradeDateTimeLong',
    u'ec'     : u'ExtHrsChange',
    u'ecp'    : u'ExtHrsChangePercent',
    u'pcls_fix': u'PreviousClosePrice'
}
url = "http://finance.google.com/finance/info?client=ig&q=NASDAQ%3AAAPL"


# get historical data --------------------------------------------------------
url = "http://www.google.com/finance/historical?q=GOOG&histperiod=daily&startdate=Apr+1+2014&enddate=Apr+15+2014&output=csv"

MonthAbbr = {
	1:'Jan',
	2:'Feb',
	3:'Mar',
	4:'Apr',
	5:'May',
	6:'Jun',
	7:'Jul',
	8:'Aug',
	9:'Sep',
	10:'Oct',
	11:'Nov',
	12:'Dec',
}

r_MonthAbbr = {
	'Jan':'01',
	'Feb':'02',
	'Mar':'03',
	'Apr':'04',
	'May':'05',
	'Jun':'06',
	'Jul':'07',
	'Aug':'08',
	'Sep':'09',
	'Oct':'10',
	'Nov':'11',
	'Dec':'12',	
}

MonthAbbrList = r_MonthAbbr.keys()

def form_date(year,month,date):
	res = "{0}+{1}+{2}".format(MonthAbbr[int(month)], date, year)
	return res
def bulid_url(symbol, start, end):
	return "http://www.google.com/finance/historical?\
q={0}&histperiod=daily&startdate={1}&enddate={2}&output=csv".format(symbol, start, end)

def get_historical_data(symbol, start_year, start_month, start_date, end_year, end_month, end_date):
	start = form_date(start_year, start_month, start_date)
	end = form_date(end_year, end_month, end_date)
	url = bulid_url(symbol, start, end)

	req = Request(url)
	res = urlopen(req)

	return res.read()

def form_csv(s, filepath):
	res = ''
	pin =0
	record = False
	for i in range(len(s)):
		if not record:
			res += s[i]
		if s[i] == '\n':
			start = i+1
			record = True
			pin = i+1
		if s[i] == '-':		
			if s[pin:i] in MonthAbbrList:
				mon = r_MonthAbbr[s[pin:i]]
			else:
				day = '0'+s[pin:i] if pin+1==i else s[pin:i]
			pin = i+1		
		if record and s[i] == ',':
			year = '20' + s[pin:i]
			res += year + '-' + mon + '-' + day + ',' 
			record = False
			pin = i+1
	with open(filepath,"wb") as fo:
		fo.write(res)

def update_hist_data(symbol, filepath, start_year=2015, start_month=1, start_date=1, end_year=2017, end_month=1, end_date=1):
	res = get_historical_data(symbol, start_year, start_month, start_date, end_year, end_month, end_date)
	form_csv(res, filepath)


