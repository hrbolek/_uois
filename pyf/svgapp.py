#uvicorn main:app --reload

from fastapi.responses import Response
import fastapi.responses
from typing import Optional
from fastapi import FastAPI

import json
#from IPython.display import SVG

import datetime
import hashlib

def getMonday(fromDate=None):
    if fromDate is None:
        fromDate = datetime.datetime.now()
    if int(fromDate.strftime("%w")) == 0 or int(fromDate.strftime("%w")) == 6:
        y = fromDate + datetime.timedelta(days = int(int(fromDate.strftime("%w")) / 6 + 1))
    else:
        y = fromDate - datetime.timedelta(days = int(fromDate.strftime("%w")) - 1)
    return y

def calendarPositionTime(time):
    hours = time['hours']
    minutes = time['minutes']
    if hours < 8:
        hours = 8
    elif hours > 13:
        minutes += 50
    hours -= 8
    output = (minutes + hours*60) / 110
    return output

def SemestrPositionTime(time):
    hours = time['hours']
    minutes = time['minutes']
    if hours < 8:
        hours = 8
    if hours > 16:
        hours = 15
        minutes = 20
    elif hours > 13:
        hours -= 1
    hours -= 8
    output = (minutes + hours*60) / 110
    return output

def calendarPositionDate(date):
    return int(datetime.datetime(date['year'], date['month'], date['day']).strftime("%w"))-1

def getInicials(teacher):
    teach = teacher.split(", ")
    if(teach != []):
        if(len(teach) > 1):
            teach = teach[0][:1] + teach[1][:1]
        else:
            teach = teach[0][:1]
    else:
        teach = ""
    return teach[:5]

def hashColor(name):
    cmin = 128
    coe = 127
    f = hashlib.sha1(name.encode("utf-8")).hexdigest()[:6]
    R = f[:2]
    G = f[2:4]
    B = f[4:6]
    if int(R, 16) < cmin:
        R = str(hex(int(int(R, 16) +coe)))[2:4]
    if int(G, 16) < cmin:
        G = str(hex(int(int(G, 16) +coe)))[2:4]
    if int(B, 16) < cmin:
        B = str(hex(int(int(B, 16) +coe)))[2:4]
    Color = '#' + R + G + B
    return Color

def subShortcut(subject):
    sub = subject.split(" ")
    ret = ""
    for item in sub:
        ret = ret + item[:1]
    return ret

def CompareFF(a, b):
    return lambda item: a(item) and b(item)

def separateData(item):
    less = {'startTime': item['startTime'],'endTime': item['endTime'],
    'date': item['date'],'groupsNames': item['groupsNames'],
    'teachersIds': item['teachersIds'], 'classroomsIds': item['classroomsIds']}

    if item['classroomsNames'] == []:
        less['classroomsNames'] = ['']
    else:
        less['classroomsNames'] = item['classroomsNames']
    if item['teachersNames'] == []:
        less['teachersNames'] = ['']
    else:
        less['teachersNames'] = item['teachersNames']
    if 'subjectName' in item:
        less['subjectName'] = item['subjectName']
    elif 'subtopic' in item:
        less['subjectName'] = item['subtopic']
    else:
        less['subjectName'] = ''
    if 'topic'in item:
        less['topic'] = item['topic']
    else:
        less['topic'] = ''
    return less

def displayItem(item, col, subRow, name1, name2, name3, name4, color, rowNumber=4, widt=220, link1 = "", link2 = "", link3 = "", link4 = ""):
    smallRowHeight = 25
    bigRowHeight = rowNumber * 25
    colWidth = widt
    leftUpperX = (col) * (colWidth + 2) + 80
    leftUpperY = smallRowHeight + smallRowHeight + subRow * (bigRowHeight + 2)
    if color == '':
        Color = hashColor(item[name1])
    else:
        Color = color
    rectangle1 = f'<rect x="{leftUpperX}" y="{leftUpperY}" width="{colWidth}" height="{bigRowHeight}" stroke="#000000" stroke-width="1.33333" stroke-miterlimit="8"/>'
    rectangle2 = (f'<rect x="{leftUpperX}" y="{leftUpperY}" width="{colWidth}" height="{bigRowHeight}" stroke="{Color}" stroke-width="1.33333" stroke-miterlimit="8" fill="{Color}">'
        #+ '<animate attributeName="rx" values="0;15;0" dur="10s" repeatCount="indefinite" />'
        + '</rect>')
    
    text = (
        f'''<text font-family="Calibri,Calibri_MSFontService,sans-serif" font-weight="600" font-size="18" transform="translate({5+leftUpperX} {20+leftUpperY})">''' +
        f'''<a href="{link1}" target="_top">{item[name1]}</a>''' +
        f'''<tspan font-size="15" font-weight="400" x="-0.0424118" y="23"><a href="{link2}" target="_top">{item[name2]}</a></tspan>''' +
        f'''<tspan font-size="15" font-weight="400" x="1.04089" y="45"><a href="{link3}" target="_top">{item[name3]}</a></tspan>''' +
        f'''<tspan font-size="15" font-weight="400" x="1.04089" y="70"><a href="{link4}" target="_top">{item[name4]}</a></tspan></text>'''
        )

    return rectangle1 + rectangle2 + text

def displayItemS(item, col, subRow, name1, name2, name3, rowNumber=3, Color = '#FFFFFF', link1 = "", link2 = "", link3 = "", widt = 33):
    smallRowHeight = 15
    bigRowHeight = rowNumber * smallRowHeight
    colWidth = widt
    leftUpperX = (col) * (33 + 1) + 10
    leftUpperY = smallRowHeight + smallRowHeight + subRow * (smallRowHeight)
    rectangle1 = f'<rect x="{leftUpperX}" y="{leftUpperY}" width="{colWidth}" height="{bigRowHeight-1}" stroke="#000000" stroke-width="1.33333" stroke-miterlimit="8"/>'
    rectangle2 = (f'<rect x="{leftUpperX}" y="{leftUpperY}" width="{colWidth}" height="{bigRowHeight-1}" stroke="{Color}" stroke-width="1.33333" stroke-miterlimit="8" fill="{Color}">'
        #+ '<animate attributeName="rx" values="0;15;0" dur="10s" repeatCount="indefinite" />'
        + '</rect>')
    
    text = (
        f'''<text font-family="Calibri,Calibri_MSFontService,sans-serif" font-weight="400" font-size="14" transform="translate({1+leftUpperX} {11+leftUpperY})">''' +
        f'''<a href="{link1}" target="_top">{item[name1]}</a>''' +
        f'''<tspan font-size="14" font-weight="400" x="-0.0424118" y="16"><a href="{link2}" target="_top">{item[name2]}</a></tspan>''' +
        f'''<tspan font-size="14" font-weight="400" x="1.04089" y="32"><a href="{link3}" target="_top">{item[name3]}</a></tspan></text>''' 
        )

    return rectangle1 + rectangle2 + text


import json

def loadEvents(sourceFile='data.json'):
    with open(sourceFile, encoding="utf8") as inputFile:
        data = json.load(inputFile)
    return data

events = []
def getEvents():
    if len(events) == 0:
        data = loadEvents()
        for item in data['events']:         #kopie bez jakéhokoliv propojení (jedno změním druhé se nemění)
            events.append(separateData({**item}))
    return events

#startDate = datetime(2021, 10, 31)

def fromEventsToLessons(filterFunc, events):
    filteredEvents = filter(filterFunc, events)

    lessons = []
    for index, item in enumerate(filteredEvents):
        lessons.append(separateData(item))
    return lessons

def fromLessonsToSVGNavirators_1(timetableType, lessons, filteringText, filteringID, startDate):
    data = ''
    data = data + displayItem({'sbj': filteringText, 'top': '', 'tch': '', 'clsr': ''}, 2, 20, 'sbj', 'top', 'tch', 'clsr', '#00BBFF',1)
    data = data + displayItem({'sbj': 'Předchozí týden', 'top': '', 'tch': '', 'clsr': ''}, 1, 20, 'sbj', 'top', 'tch', 'clsr', '#00DFFF',
        1,220,"./?start=" + str(startDate - datetime.timedelta(days = 7)))

    data = data + displayItem({'sbj': 'Příští týden', 'top': '', 'tch': '', 'clsr': ''}, 3, 20, 'sbj', 'top', 'tch', 'clsr', '#00DFFF',
        1,220,"./?start=" + str(startDate + datetime.timedelta(days = 7)))
    return data

#def fromLessonsToSVG(lessons=lessons, filteringText=filteringText, filteringID=filteringID, startDate=startDate):
def fromLessonsToSVG_1(timetableType, lessons, filteringText, filteringID, startDate, showNavigator=False):

    baseUrl = '/ui'
    teacherBaseUrl = baseUrl + '/users/teacher'
    roomBaseUrl = baseUrl + '/areals/room'
    groupBaseUrl = baseUrl + '/groups/group'
    subjectBaseUrl = baseUrl + '/studyprograms/subject'

    SVGHeader = '<svg width="1500" height="700" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" overflow="hidden">'
    SVGFooter = '</svg>'

    data = (SVGHeader + '<g>')
    data = data + displayItem({'sbj': '8:00', 'top': '', 'tch': '', 'clsr': ''}, 0, -1, 'sbj', 'top', 'tch', 'clsr', '#FFFFFF',1) 
    data = data + displayItem({'sbj': '9:50', 'top': '', 'tch': '', 'clsr': ''}, 1, -1, 'sbj', 'top', 'tch', 'clsr', '#FFFFFF',1) 
    data = data + displayItem({'sbj': '11:40', 'top': '', 'tch': '', 'clsr': ''}, 2, -1, 'sbj', 'top', 'tch', 'clsr', '#FFFFFF',1)
    data = data + displayItem({'sbj': '', 'top': '', 'tch': '', 'clsr': ''}, 3, -1, 'sbj', 'top', 'tch', 'clsr', '#FFFFFF',1)
    data = data + displayItem({'sbj': '14:30', 'top': '', 'tch': '', 'clsr': ''}, 4, -1, 'sbj', 'top', 'tch', 'clsr', '#FFFFFF',1)
    data = data + displayItem({'sbj': '16:20', 'top': '', 'tch': '', 'clsr': ''}, 5, -1, 'sbj', 'top', 'tch', 'clsr', '#FFFFFF',1)

    datumForName = startDate
    dayList = ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne']
    for i in range(5):
        datumForName = datumForName + datetime.timedelta(days = 1)
        data = data + displayItem({
            'sbj': str(datumForName.day) + '.' + str(datumForName.month) + '.', 'top': dayList[datumForName.weekday()], 'tch': '', 'clsr': ''},
            -1, i, 'sbj', 'top', 'tch', 'clsr', '#FFFFFF',4,60)

    for index, item in enumerate(lessons):
        data = data + displayItem({
            'sbj': item['subjectName'][:27], 'top': item['topic'][:32], 'tch': item['teachersNames'][0],'clsr': item['classroomsNames'][0]},
            calendarPositionTime(item['startTime']), calendarPositionDate(item['date']),
            #'sbj', 'top', 'tch', 'clsr', '', 4, 220, "","","/teacher/?id="+str(item['teachersIds'][0]),"")
            'sbj', 'top', 'tch', 'clsr', '', 4, 220, subjectBaseUrl + "/1", subjectBaseUrl + "/1", teacherBaseUrl + "/1", roomBaseUrl + "/1")

    if showNavigator:
        data = data + fromLessonsToSVGNavirators_1(timetableType, lessons, filteringText, filteringID, startDate)
    data = data + ('</g>' + SVGFooter)

    return data

def resultGet_1(type: str, filterID: int, start: Optional[datetime.datetime] = None, showNavigator=False):
    if start is None:
        startDate = getMonday(start)
    else:
        startDate = start

    startDate = startDate - datetime.timedelta(days = 1)     #posun na neděli protože datatime má někdy problém s rovností v >= 
    endDate = startDate + datetime.timedelta(days = 6)
    filteringID = filterID

    filterFunc1 = lambda item: True

    if type == 'student':
        filteringGroup = 'groupsNames'      #pak upravit na groupsId - nějaký velký programátor který mě nechce potkat nechápe že věci mají mít ID
        filteringID = '23-5KB'
        filterFunc1 = lambda item: filteringID in item[filteringGroup]
    elif type == 'teacher':
        filteringGroup = 'teachersIds'      #občas chyba - učitele někdy nemají ID
        filterFunc1 = lambda item: filteringID in item[filteringGroup]
    elif type == 'room':
        filteringGroup = 'classroomsIds'    #nefunguje - proč asi, ne všechny učebny mají ID
        filterFunc1 = lambda item: filteringID in item[filteringGroup]

    filteringText = filteringID             #pak předělat na hledání názvu filtrované věci podle filteringGroupe a filteringID

    #filterFunc1 = lambda item: filteringID in item[filteringGroup]
    filterFunc2 = lambda item: (
        (datetime.datetime(item['date']['year'], item['date']['month'], item['date']['day']) >= startDate)
        and (datetime.datetime(item['date']['year'], item['date']['month'], item['date']['day']) <= endDate)
    )
    
    lessons = fromEventsToLessons(filterFunc=CompareFF(filterFunc1,filterFunc2), events=getEvents())

    if (filteringID == '23-5KB'):           #pak odstranit jen dočasný fix protože učební skupiny nemají ID
        filteringID = 10

    data = fromLessonsToSVG_1(timetableType=type, lessons=lessons, filteringText=filteringText, filteringID=filteringID, startDate=startDate, showNavigator=showNavigator)
    
    return data


def leftLargeBorder():
    data = ''
    for i in range(4):
        data = data + displayItemS({'sbj': '8:00', 'tch': '', 'clsr': ''}, 1, 2 + i*16, 'sbj', 'tch', 'clsr', 3,'#AACCFF')
        data = data + displayItemS({'sbj': '9:50', 'tch': '', 'clsr': ''}, 1, 5 + i*16, 'sbj', 'tch', 'clsr', 3,'#AACCFF') 
        data = data + displayItemS({'sbj': '11:40', 'tch': '', 'clsr': ''}, 1, 8 + i*16, 'sbj', 'tch', 'clsr', 3,'#AACCFF')
        data = data + displayItemS({'sbj': '14:30', 'tch': '', 'clsr': ''}, 1, 11 + i*16, 'sbj', 'tch', 'clsr', 3,'#AACCFF')
        data = data + displayItemS({'sbj': '16:20', 'tch': '', 'clsr': ''}, 1, 14 + i*16, 'sbj', 'tch', 'clsr', 3,'#AACCFF')
    data = data + displayItemS({'sbj': '8:00', 'tch': '', 'clsr': ''}, 1, 2 + 64, 'sbj', 'tch', 'clsr', 3,'#AACCFF')
    data = data + displayItemS({'sbj': '9:50', 'tch': '', 'clsr': ''}, 1, 5 + 64, 'sbj', 'tch', 'clsr', 3,'#AACCFF') 
    data = data + displayItemS({'sbj': '11:40', 'tch': '', 'clsr': ''}, 1, 8 + 64, 'sbj', 'tch', 'clsr', 3,'#AACCFF')

    dayList = ['Po', 'Út', 'St', 'Čt', 'Pá']
    for i in range(4):
        data = data + displayItemS({
            'sbj': dayList[i], 'tch': '', 'clsr': ''},
            0, i * 16 + 2, 'sbj', 'tch', 'clsr', 15,'#00FFAA')
    data = data + displayItemS({
            'sbj': dayList[4], 'tch': '', 'clsr': ''},
            0, 4 * 16 + 2, 'sbj', 'tch', 'clsr', 9,'#00FFAA')    
    return data

def largeBorder():
    return leftLargeBorder()
    pass

def defineDatumColumns():
    pass

def fromLessonsToSVG_2(startDate, endDate, lessons):
    SVGHeader = '<svg width="1500" height="1400" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" overflow="hidden">'
    SVGFooter = '</svg>'

    data = (SVGHeader + '<g>')
    data = data + leftLargeBorder()

    datumColumn = {}
    sloupcePrvnichMesicu = []
    datumForSemestr = startDate + datetime.timedelta(days = 1)
    sloupec = 2
    while(datumForSemestr <= endDate):
        if datumForSemestr.day == 1 or sloupec == 2:
            if int(datumForSemestr.strftime("%w")) == 1:
                data = data + displayItemS({'sbj': str(datumForSemestr.month) + '/' + str(datumForSemestr.year)[2:], 'tch': '', 'clsr': ''},
                    sloupec, 0, 'sbj', 'tch', 'clsr', 1,'#FFAA00')
                sloupcePrvnichMesicu.append(sloupec)
            else:
                data = data + displayItemS({'sbj': str(datumForSemestr.month) + '/' + str(datumForSemestr.year)[2:], 'tch': '', 'clsr': ''},
                    sloupec+1, 0, 'sbj', 'tch', 'clsr', 1,'#FFAA00')
                sloupcePrvnichMesicu.append(sloupec+1)
        if int(datumForSemestr.strftime("%w")) == 6:
            datumForSemestr = datumForSemestr + datetime.timedelta(days = 1)
            continue
        elif int(datumForSemestr.strftime("%w")) == 0:
            datumForSemestr = datumForSemestr + datetime.timedelta(days = 1)
            sloupec = sloupec + 1
            continue
        data = data + displayItemS({'sbj': datumForSemestr.day, 'tch': '', 'clsr': ''},
            sloupec, (int(datumForSemestr.strftime("%w"))-1) * 16 + 1, 'sbj', 'tch', 'clsr', 1,'#FFFF00')
        datumColumn[datumForSemestr] = sloupec
        hours = 0
        if int(datumForSemestr.strftime("%w")) == 5:
            hours = 3
        else:
            hours = 5
        for i in range(hours):
            if(sloupec in sloupcePrvnichMesicu):
                color = '#FFCCAA'
            else:
                color = '#FFFFFF'
            data = data + displayItemS({'sbj': '', 'tch': '', 'clsr': ''},
                sloupec, (int(datumForSemestr.strftime("%w"))-1) * 16 + i*3 + 2, 'sbj', 'tch', 'clsr', 3, color)

        datumForSemestr = datumForSemestr + datetime.timedelta(days = 1)

    inicials = {}
    shortcuts = {}
    for index, item in enumerate(lessons):
        date = item['date']

        column = datumColumn[datetime.datetime(date['year'], date['month'], date['day'])]
        row = calendarPositionDate(item['date']) * 16 + SemestrPositionTime(item['startTime']) * 3 + 2
        teachInicials = str(getInicials(item['teachersNames'][0]))
        subjectShortcut = str(subShortcut(item['subjectName']))
        if(teachInicials != ""):
            inicials[teachInicials] = item['teachersNames'][0]          #ošetřit duplicitní iniciály
        if(subjectShortcut != ""):
            shortcuts[subjectShortcut] = item['subjectName']
        if(column in sloupcePrvnichMesicu):
            color = '#FFCCAA'
        else:
            color = '#FFFFFF'

        data = data + displayItemS({
            'sbj': subjectShortcut, 'tch': teachInicials,'clsr': item['classroomsNames'][0][:4]},
            column , row, 'sbj', 'tch', 'clsr', 3, color, '.', '.', '.')

    rowOfLegend = 76
    for item in shortcuts:
        data = data + displayItemS({'sbj': item, 'tch': '', 'clsr': ''},
            0, rowOfLegend, 'sbj', 'tch', 'clsr', 1,'#A0DAFF')
        data = data + displayItemS({'sbj': shortcuts[item], 'tch': '', 'clsr': ''},
            1, rowOfLegend, 'sbj', 'tch', 'clsr', 1,'#B0FFFF', link1 = "", link2 = "", link3 = "", widt = 231)
        rowOfLegend += 1

    rowOfLegend = 76
    for item in inicials:
        data = data + displayItemS({'sbj': item, 'tch': '', 'clsr': ''},
            9, rowOfLegend, 'sbj', 'tch', 'clsr', 1,'#55FFAA')
        data = data + displayItemS({'sbj': inicials[item], 'tch': '', 'clsr': ''},
            10, rowOfLegend, 'sbj', 'tch', 'clsr', 1,'#AAFF00', link1 = "", link2 = "", link3 = "", widt = 231)
        rowOfLegend += 1

    data = data + ('</g>' + SVGFooter)
    return data

def resultGet_2(start: Optional[datetime.datetime] = None):
    if start is None:
        startDate = datetime.datetime(2021, 9, 1)
        startDate = startDate - datetime.timedelta(days = 1)
    else:
        startDate = start
        
    endDate = datetime.datetime(2022, 3, 7)
    filteringGroup = 'groupsNames'
    filteringText = '23-5KB'

    filterFunc1 = lambda item: filteringText in item[filteringGroup]
    filterFunc2 = lambda item: (
        (datetime.datetime(item['date']['year'], item['date']['month'], item['date']['day']) >= startDate) 
        and (datetime.datetime(item['date']['year'], item['date']['month'], item['date']['day']) <= endDate)
    )
    
    lessons = fromEventsToLessons(filterFunc=CompareFF(filterFunc1,filterFunc2), events=getEvents())
    data = fromLessonsToSVG_2(startDate, endDate, lessons)
    
    return data

def fromDateToDateTime(start):
    if start is None:
        start = getMonday()
    return datetime.datetime(year=start.year, month=start.month, day=start.day)

def attachSVGApp(app, bindPoint='/svg'):
    apiapp = FastAPI()

    @apiapp.get('/ping')
    async def ping():
        return {'msg': 'ping'}

    @apiapp.get('/student/{id}/')
    async def resultGetStudent(id: int, start: Optional[datetime.date] = None):
        data = resultGet_1(type='student', filterID=id, start=fromDateToDateTime(start), showNavigator=False)
        return Response(content=data, media_type="image/svg+xml")

    @apiapp.get('/teacher/{id}/')
    async def resultGetTeacher(id: int, start: Optional[datetime.date] = None):
        data = resultGet_1(type='teacher', filterID=id, start=fromDateToDateTime(start), showNavigator=False)
        return Response(content=data, media_type="image/svg+xml")

    @apiapp.get('/room/{id}/')
    async def resultGetRoom(id: int, start: Optional[datetime.date] = None):
        data = resultGet_1(type='room', filterID=id, start=fromDateToDateTime(start), showNavigator=False)
        return Response(content=data, media_type="image/svg+xml")

    @apiapp.get('/nav/student/{id}/')
    async def resultGetStudent(id: int, start: Optional[datetime.date] = None):
        data = resultGet_1(type='student', filterID=id, start=fromDateToDateTime(start), showNavigator=True)
        return Response(content=data, media_type="image/svg+xml")

    @apiapp.get('/nav/teacher/{id}/')
    async def resultGetTeacher(id: int, start: Optional[datetime.date] = None):
        data = resultGet_1(type='teacher', filterID=id, start=fromDateToDateTime(start), showNavigator=True)
        return Response(content=data, media_type="image/svg+xml")

    @apiapp.get('/nav/room/{id}/')
    async def resultGetRoom(id: int, start: Optional[datetime.date] = None):
        data = resultGet_1(type='room', filterID=id, start=fromDateToDateTime(start), showNavigator=True)
        return Response(content=data, media_type="image/svg+xml")

    # @apiapp.get('/svg/')
    # async def resultGet(type: str, filterID: int, start: Optional[datetime.datetime] = None):
    #     data = resultGet_1(type, filterID, start)
    #     return Response(content=data, media_type="image/svg+xml")

    # if type == 'student':
    #     filteringGroup = 'groupsNames'      #pak upravit na groupsId - nějaký velký programátor který mě nechce potkat nechápe že věci mají mít ID
    #     filteringID = '23-5KB'
    # elif type == 'teacher':
    #     filteringGroup = 'teachersIds'      #občas chyba - učitele někdy nemají ID
    # elif type == 'room':


    @apiapp.get('/A4/')
    async def resultGetA4(start: Optional[datetime.date] = None):
        data = resultGet_2(start)    
        return Response(content=data, media_type="image/svg+xml")

    print('SVG attached')
    app.mount(bindPoint, apiapp)