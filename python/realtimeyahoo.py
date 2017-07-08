#!/usr/bin/env python

from yahoo_finance import Share
import pandas as pd
from datetime import datetime

filepath='../../'
filename='Russell3000cleanlist.xls'
russell3000=pd.read_excel(filepath+filename)
russell3000.columns=['Company','Ticker']
russell3000['Price']=pd.Series(-1,index=russell3000.index)
russell3000['Change']=pd.Series(-1,index=russell3000.index)
russell3000['Volume']=pd.Series(-1,index=russell3000.index)
russell3000['Open']=pd.Series(-1,index=russell3000.index)
russell3000['Average daily volume']=pd.Series(-1,index=russell3000.index)
russell3000['Market cap']=pd.Series('N/A',index=russell3000.index)
russell3000['Book value']=pd.Series(-1,index=russell3000.index)
russell3000['Ebitda']=pd.Series('N/A',index=russell3000.index)
russell3000['Dividend share']=pd.Series(-1,index=russell3000.index)
#russell3000['Dividend yield']=pd.Series(-1,index=russell3000.index)
russell3000['Earnings share']=pd.Series(-1,index=russell3000.index)
russell3000['Year high']=pd.Series(-1,index=russell3000.index)
russell3000['Year low']=pd.Series(-1,index=russell3000.index)
russell3000['50 days MA']=pd.Series(-1,index=russell3000.index)
russell3000['200 days MA']=pd.Series(-1,index=russell3000.index)
russell3000['Price earnings ratio']=pd.Series(-1,index=russell3000.index)
russell3000['Price earnings growth ratio']=pd.Series(-1,index=russell3000.index)
russell3000['Price sales']=pd.Series(-1,index=russell3000.index)
russell3000['Price book']=pd.Series(-1,index=russell3000.index)
russell3000['Short ratio']=pd.Series(-1,index=russell3000.index)
russell3000.set_index('Ticker',inplace=True)
for s in russell3000.index.values:
	print "Retrieving data for", s
	try:
		shy=Share(s)
	except:
		continue
	try:
		russell3000.set_value(s,'Price',shy.get_price())
	except:
		pass
	try:
		russell3000.set_value(s,'Change',shy.get_change())
	except:
		pass
	try:
		russell3000.set_value(s,'Volume',shy.get_volume())
	except:
		pass
	try:
		russell3000.set_value(s,'Open',shy.get_open())
	except:
		pass
	try:
		russell3000.set_value(s,'Average daily volume',shy.get_avg_daily_volume())
	except:
		pass
	try:
		russell3000.set_value(s,'Market cap',shy.get_market_cap())
	except:
		pass
	try:
		russell3000.set_value(s,'Book value',shy.get_book_value())
	except:
		pass
	try:
		russell3000.set_value(s,'Ebitda',shy.get_ebitda())
	except:
		pass
	try:
		russell3000.set_value(s,'Dividend share',shy.get_dividend_share())
	except:
		pass
	#try:
	#	russell3000.set_value(s,'Divident yield',shy.get_dividend_yield())
	#except:
	#	pass
	try:
		russell3000.set_value(s,'Earnings share',shy.get_earnings_share())
	except:
		pass
	try:
		russell3000.set_value(s,'Year high',shy.get_year_high())
	except:
		pass
	try:
		russell3000.set_value(s,'Year low',shy.get_year_low())
	except:
		pass
	try:
		russell3000.set_value(s,'50 days MA',shy.get_50day_moving_avg())
	except:
		pass
	try:
		russell3000.set_value(s,'200 days MA',shy.get_200day_moving_avg())
	except:
		pass
	try:
		russell3000.set_value(s,'Price earnings ratio',shy.get_price_earnings_ratio())
	except:
		pass
	try:
		russell3000.set_value(s,'Price earnings growth ratio',shy.get_price_earnings_growth_ratio())
	except:
		pass
	try:
		russell3000.set_value(s,'Price sales',shy.get_price_sales())
	except:
		pass
	try:
		russell3000.set_value(s,'Price book',shy.get_price_book())
	except:
		pass
	try:
		russell3000.set_value(s,'Short ratio',shy.get_short_ratio())
	except:
		pass
u=datetime.now()
ofn='r3alldata'+str(u)[0:4]+str(u)[5:7]+str(u)[8:10]+'.xls'
russell3000.to_excel(ofn)
