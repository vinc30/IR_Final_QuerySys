# -*- coding: UTF-8  -*-  

# Code for tagging temporal expressions in text
# For details of the TIMEX format, see http://timex2.mitre.org/

from __future__ import print_function
from __future__ import unicode_literals

import re
import string
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from datetime import datetime, date, time

# Requires eGenix.com mx Base Distribution
# http://www.egenix.com/products/python/mxBase/
try:
    from mx.DateTime import *
except ImportError:
    print("""
Requires eGenix.com mx Base Distribution
http://www.egenix.com/products/python/mxBase/""")

# Predefined strings.
numbers = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten| \
          eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen| \
          eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty| \
          ninety|hundred|thousand)"
day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday|星期一|星期二|星期三|星期四|星期五|星期六|星期天|週一|週二|週三|週四|週五|週六|週日)"
week_day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday|星期一|星期二|星期三|星期四|星期五|星期六|星期天|週一|週二|週三|週四|週五|週六|週日)"
month = "(january|february|march|april|may|june|july|august|september| \
          october|november|december|一月|二月|三月|四月|五月|六月|七月|八月|九月|十月|十一月|十二月)"
dmy = "(year|day|week|month|年|日|周|月|週|禮拜|天)"
rel_day = "(today|yesterday|tomorrow|tonight|tonite|今天|明天|今日|今晚|昨|頭七)"
exp1 = "(before|after|earlier|later|ago|上個|下個|前|上|下|前)"
exp2 = "(this|next|last|上個|下個|上|下|前|今)"
iso = "\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+"
year = "((?<=\s)\d{4}|^\d{4})"
regxp1 = "((\d+|(" + numbers + "[-\s]?)+) " + dmy + "s? " + exp1 + ")"
regxp2 = "(" + exp2 + "(" + dmy + "|" + week_day + "|" + month + "))"
#regxp2 = "(" + exp2 + " (" + dmy + "|" + week_day + "|" + month + "))"
#regxp3 = "(\d{2}月)(\d{2}日)"
#regxp3 = "(\d+?月)(\d+?日)"
regxp3 = '((\d{2}年)?(\d{1,2}月)?(\d{1,2}日))|((\d{2}年)?(\d{1,2}月)(\d{1,2}日)?)'
reg1 = re.compile(regxp1, re.IGNORECASE)
reg2 = re.compile(regxp2, re.IGNORECASE)
reg3 = re.compile(rel_day, re.IGNORECASE)
reg4 = re.compile(iso)
#reg5 = re.compile(year)
reg6 = re.compile(regxp3)
def tag(text):

    # Initialization
    timex_found = []

    # re.findall() finds all the substring matches, keep only the full
    # matching string. Captures expressions such as 'number of days' ago, etc.
    found = reg1.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    # Variations of this thursday, next year, etc
    found = reg2.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
	
        timex_found.append(timex)

    # today, tomorrow, etc
    found = reg3.findall(text)
    for timex in found:
        timex_found.append(timex)

    # ISO
    found = reg4.findall(text)
    for timex in found:
        timex_found.append(timex)

    # Year
    """found = reg5.findall(text)
    for timex in found:
        timex_found.append(timex)
    """
     #*月*日
    found = reg6.findall(text)
    founded=[]
    for a in found:
	founded.append(sorted(a, key=lambda x:len(x), reverse=True)[0])
   # found = [a[0] for a in found if len(a) > 1]
   # print(found)
    #found = reg6.findall(text)
    for timex in founded:
        timex_found.append(timex)
    
    # Tag only temporal expressions which haven't been tagged.
    for timex in timex_found:
        text = re.sub(timex + '(?!</TIMEX2>)', '<TIMEX2>' + timex + '</TIMEX2>', text)

    return text

# Hash function for week days to simplify the grounding task.
# [Mon..Sun] -> [0..6]
hashweekdays = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6,
    '星期一':0,
    '星期二':1,
    '星期三':2,
    '星期四':3,
    '星期五':4,
    '星期六':5,
    '星期天':6,
    '星期日':6}

# Hash function for months to simplify the grounding task.
# [Jan..Dec] -> [1..12]
hashmonths = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12}

# Hash number in words into the corresponding integer value
def hashnum(number):
    if re.match(r'one|^a\b', number, re.IGNORECASE):
        return 1
    if re.match(r'two', number, re.IGNORECASE):
        return 2
    if re.match(r'three', number, re.IGNORECASE):
        return 3
    if re.match(r'four', number, re.IGNORECASE):
        return 4
    if re.match(r'five', number, re.IGNORECASE):
        return 5
    if re.match(r'six', number, re.IGNORECASE):
        return 6
    if re.match(r'seven', number, re.IGNORECASE):
        return 7
    if re.match(r'eight', number, re.IGNORECASE):
        return 8
    if re.match(r'nine', number, re.IGNORECASE):
        return 9
    if re.match(r'ten', number, re.IGNORECASE):
        return 10
    if re.match(r'eleven', number, re.IGNORECASE):
        return 11
    if re.match(r'twelve', number, re.IGNORECASE):
        return 12
    if re.match(r'thirteen', number, re.IGNORECASE):
        return 13
    if re.match(r'fourteen', number, re.IGNORECASE):
        return 14
    if re.match(r'fifteen', number, re.IGNORECASE):
        return 15
    if re.match(r'sixteen', number, re.IGNORECASE):
        return 16
    if re.match(r'seventeen', number, re.IGNORECASE):
        return 17
    if re.match(r'eighteen', number, re.IGNORECASE):
        return 18
    if re.match(r'nineteen', number, re.IGNORECASE):
        return 19
    if re.match(r'twenty', number, re.IGNORECASE):
        return 20
    if re.match(r'thirty', number, re.IGNORECASE):
        return 30
    if re.match(r'forty', number, re.IGNORECASE):
        return 40
    if re.match(r'fifty', number, re.IGNORECASE):
        return 50
    if re.match(r'sixty', number, re.IGNORECASE):
        return 60
    if re.match(r'seventy', number, re.IGNORECASE):
        return 70
    if re.match(r'eighty', number, re.IGNORECASE):
        return 80
    if re.match(r'ninety', number, re.IGNORECASE):
        return 90
    if re.match(r'hundred', number, re.IGNORECASE):
        return 100
    if re.match(r'thousand', number, re.IGNORECASE):
      return 1000

# Given a timex_tagged_text and a Date object set to base_date,
# returns timex_grounded_text
def ground(tagged_text, base_date):
    global month
    # Find all identified timex and put them into a list
    timex_regex = re.compile(r'<TIMEX2>.*?</TIMEX2>', re.DOTALL)
    timex_found = timex_regex.findall(tagged_text)
    timex_found = [re.sub(r'</?TIMEX2.*?>', '', timex) for timex in timex_found]

    # Calculate the new date accordingly
    for timex in timex_found:
        timex_val = 'UNKNOWN' # Default value

        timex_ori = timex   # Backup original timex for later substitution

        # If numbers are given in words, hash them into corresponding numbers.
        # eg. twenty five days ago --> 25 days ago
        if re.search(numbers, timex, re.IGNORECASE):
            split_timex = re.split(r'\s(?=days?|months?|years?|weeks?|月?|日?|年?)', \
                                                              timex, re.IGNORECASE)
            value = split_timex[0]
            unit = split_timex[1]
            num_list = [hashnum(s) for s in re.findall(numbers + '+', \
                                          value, re.IGNORECASE)]
            timex = repr(sum(num_list)) + ' ' + unit

        # If timex matches ISO format, remove 'time' and reorder 'date'
        if re.match(r'\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+', timex):
            dmy = re.split(r'\s', timex)[0]
            dmy = re.split(r'/|-', dmy)
            timex_val = str(dmy[2]) + '-' + str(dmy[1]) + '-' + str(dmy[0])

        # Specific dates
  #      elif re.match(r'\d{4}', timex):
   #         timex_val = str(timex)

        # Relative dates
        elif re.match(r'tonight|tonite|today|今天|今晚|今日|今', timex, re.IGNORECASE):
            timex_val = str(base_date)
        elif re.match(r'yesterday|昨日|昨天|昨晚|昨', timex, re.IGNORECASE):
            timex_val = str(base_date + RelativeDateTime(days=+1))
        elif re.match(r'前天|前日|前晚', timex, re.IGNORECASE):
            timex_val = str(base_date + RelativeDateTime(days=+2))
        elif re.match(r'tomorrow|明天|明日', timex, re.IGNORECASE):
            timex_val = str(base_date + RelativeDateTime(days=-1))
        elif re.match(r'後天', timex, re.IGNORECASE):
            timex_val = str(base_date + RelativeDateTime(days=-2))
        
        # Weekday in the following week.
        elif re.match(r'next ' + week_day, timex, re.IGNORECASE):
            day = hashweekdays[timex.split()[1]]
            timex_val = str(base_date + RelativeDateTime(weeks=-1, \
                            weekday=(day,0)))

        # Weekday in the current week.
        elif re.match(r'this ' + week_day, timex, re.IGNORECASE):
            day = hashweekdays[timex.split()[1]]
            timex_val = str(base_date + RelativeDateTime(weeks=0, \
                            weekday=(day,0)))

	# Weekday in the previous week.
        elif re.match(r'last ' + week_day, timex, re.IGNORECASE):
            day = hashweekdays[timex.split()[1]]
            timex_val = str(base_date + RelativeDateTime(weeks=+1, \
                              weekday=(day,0)))

        # Last, this, next week.
        elif re.match(r'next week|下週|下禮拜|下星期|下周', timex, re.IGNORECASE):
            year = (base_date + RelativeDateTime(weeks=-1)).year

            # iso_week returns a triple (year, week, day) hence, retrieve
            # only week value.
	    timex_val = str(base_date + RelativeDateTime(weeks=-1))
            #change
	  #  week = (base_date + RelativeDateTime(weeks=-1)).iso_week[1]
          #  timex_val = str(year) + 'W' + str(week)
        elif re.match(r'this week|本週|這禮拜|本周', timex, re.IGNORECASE):
            year = (base_date + RelativeDateTime(weeks=0)).year
	    
	    timex_val = str(base_date + RelativeDateTime(weeks=0))
	    #change
            #week = (base_date + RelativeDateTime(weeks=0)).iso_week[1]
            #timex_val = str(year) + 'W' + str(week)
        elif re.match(r'last week|上週|頭七|上禮拜|上星期|上周', timex, re.IGNORECASE):
            year = (base_date + RelativeDateTime(weeks=+1)).year
	    timex_val = str(base_date + RelativeDateTime(weeks=+1))
	    #change
            #week = (base_date + RelativeDateTime(weeks=+1)).iso_week[1]
            #timex_val = str(year) + 'W' + str(week)

        # Month in the following year.
        elif re.match(r'next ' + month, timex, re.IGNORECASE):
            month = hashmonths[timex.split()[1]]
            timex_val = str(base_date.year - 1) + '-' + str(month)

        # Month in the current year.
        elif re.match(r'this ' + month, timex, re.IGNORECASE):
            month = hashmonths[timex.split()[1]]
            timex_val = str(base_date.year) + '-' + str(month)

        # Month in the previous year.
        elif re.match(r'last ' + month, timex, re.IGNORECASE):
            month = hashmonths[timex.split()[1]]
            timex_val = str(base_date.year + 1) + '-' + str(month)
        elif re.match(r'next month|下個月|下月', timex, re.IGNORECASE):
            # Handles the year boundary.
            if base_date.month == 1:
                timex_val = str(base_date.year - 1) + '-' + '12'
            else:
                timex_val = str(base_date.year) + '-' + str(base_date.month - 1)
        elif re.match(r'this month|這個月', timex, re.IGNORECASE):
                timex_val = str(base_date.year) + '-' + str(base_date.month)
        elif re.match(r'上個月|上月', timex, re.IGNORECASE):
            # Handles the year boundary.
            if base_date.month == 12:
                timex_val = str(base_date.year + 1) + '-' + '1'
            else:
                timex_val = str(base_date.year) + '-' + str(base_date.month + 1)
        elif re.match(r'last year|去年', timex, re.IGNORECASE):
            timex_val = str(base_date.year + 1)
        elif re.match(r'this year|今年', timex, re.IGNORECASE):
            timex_val = str(base_date.year)
        elif re.match(r'next year|明年', timex, re.IGNORECASE):
            timex_val = str(base_date.year - 1)
        elif re.match(r'前年', timex, re.IGNORECASE):
            timex_val = str(base_date.year + 2)
#following do not change
        elif re.match(r'\d+ days? (ago|earlier|before)', timex, re.IGNORECASE):

            # Calculate the offset by taking '\d+' part from the timex.
            offset = int(re.split(r'\s', timex)[0])
            timex_val = str(base_date + RelativeDateTime(days=-offset))
        elif re.match(r'\d+ days? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = str(base_date + RelativeDateTime(days=+offset))
        elif re.match(r'\d+ weeks? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            year = (base_date + RelativeDateTime(weeks=-offset)).year
            timex_val = str(base_date + RelativeDateTime(weeks=-offset))
	    #week = (base_date + RelativeDateTime(weeks=-offset)).iso_week[1]
            #timex_val = str(year) + 'W' + str(week)
        elif re.match(r'\d+ weeks? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            year = (base_date + RelativeDateTime(weeks=+offset)).year
            
            timex_val = str(base_date + RelativeDateTime(weeks=+offset))
	    #change
            #week = (base_date + RelativeDateTime(weeks=+offset)).iso_week[1]
            #timex_val = str(year) + 'W' + str(week)
        elif re.match(r'\d+ months? (ago|earlier|before)', timex, re.IGNORECASE):
            extra = 0
            offset = int(re.split(r'\s', timex)[0])

            # Checks if subtracting the remainder of (offset / 12) to the base month
            # crosses the year boundary.
            if (base_date.month - offset % 12) < 1:
                extra = 1

            # Calculate new values for the year and the month.
            year = str(base_date.year - offset // 12 - extra)
            month = str((base_date.month - offset % 12) % 12)

            # Fix for the special case.
            if month == '0':
                month = '12'
            timex_val = year + '-' + month
        elif re.match(r'\d+ months? (later|after)', timex, re.IGNORECASE):
            extra = 0
            offset = int(re.split(r'\s', timex)[0])
            if (base_date.month + offset % 12) > 12:
                extra = 1
            year = str(base_date.year + offset // 12 + extra)
            month = str((base_date.month + offset % 12) % 12)
            if month == '0':
                month = '12'
            timex_val = year + '-' + month
        elif re.match(r'\d+ years? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = str(base_date.year - offset)
        elif re.match(r'\d+ years? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = str(base_date.year + offset)
#do not change upper
	#new 
	#%y年%b月%d日
	elif re.match(r'(\d{2}年)(\d{1,2}月)(\d{1,2}日)',timex):
	    dt =datetime.strptime(timex.encode('utf8'), "%y年%m月%d日")
	    timex_val = str(dt.strftime('%Y-%m-%d'))
	#%y年%月
	elif re.match(r'(\d{2}年)(\d{1,2}月)',timex):
	    dt =datetime.strptime(timex.encode('utf8'), "%y年%m月")
	    timex_val = str(dt.strftime('%Y-%m'))
	#月日
	elif re.match(r'(\d{1,2}月)(\d{1,2}日)',timex):
	    dt =datetime.strptime(timex.encode('utf8'), "%m月%d日")
	    timex_val = str(dt.strftime('%m-%d'))
	#日
	elif re.match(r'(\d{1,2}日)',timex):
	    dt =datetime.strptime(timex.encode('utf8'), "%d日")
	    timex_val = str(base_date.month)+'-'+str(dt.strftime('%d'))
	    
        #月
	elif re.match(r'(\d{1,2}月)',timex):
	    dt =datetime.strptime(timex.encode('utf8'), "%m月")
	    timex_val = str(dt.strftime('%m'))+'-01' 
	# Remove 'time' from timex_val.
        # For example, If timex_val = 2000-02-20 12:23:34.45, then
        # timex_val = 2000-02-20
        timex_val = re.sub(r'\s.*', '', timex_val)

        # Substitute tag+timex in the text with grounded tag+timex.
        tagged_text = re.sub('<TIMEX2>' + timex_ori + '</TIMEX2>', '<TIMEX2 val=\"' \
            + timex_val + '\">' + timex_ori + '</TIMEX2>', tagged_text)

    return tagged_text

####

def demo():
    import nltk
    text = nltk.corpus.abc.raw('rural.txt')[:10000]
    print(tag(text))

if __name__ == '__main__':
    demo()
