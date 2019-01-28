'''
Created on 10-Sep-2017

@author: Suhaa
'''
import requests
from bs4 import BeautifulSoup as bs
import os
import regex as re
str = ' '
nstr = '\n'
rating = {'nfl': 'ranking', 'ncaaf': 'top25', 'nba': 'ranking', 'ncaab': 'top-25', 'mlb': None, 'nhl': None, 'wnba': None}
sports = ['nfl', 'ncaaf', 'nba', 'ncaab', 'mlb', 'nhl', 'wnba']
repeat_check = False

def get_Odds(url):
    ostr = ''
    page = requests.get (url)
    soup = bs (page.content, 'lxml')
    title = soup.find ('h1', class_='titleBar titleBarScoreOdds').getText ()
    ostr += title + nstr
    divs = soup.find_all ('div', class_='odds_gamesHolder')
    for div in divs:
        trs = div.find_all ('tr')
        for tr in trs:
            data = tr.getText (separator=str).strip ()
            data = " ".join (data.splitlines ())
            ostr += data + nstr
        ostr += nstr
    return ostr

def get_Injuries(url):
    ostr = ''
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    title = soup.find('h1', class_='titleBar').getText()
    ostr += title + nstr
    tables = soup.find_all('table', class_='statistics_table')
    for table in tables:
        trs = table.find_all('tr')
        for tr in trs:
            data = tr.getText(separator=str).strip()
            data = " ".join (data.splitlines ())
            ostr += data.replace('        ', ' ') + nstr
        ostr += nstr
    return ostr

def get_Ratings(url):
    ostr = ''
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    title = soup.find ('h1', class_='titleBar').getText()
    ostr += title + nstr
    iframe = soup.find('iframe', id='ctl00__FrmViewer')
    if iframe is None:
        return ostr
    iframe_src = iframe.get('src')
    page = requests.get(iframe_src)
    soup = bs(page.content, 'lxml')
    weekTitle = soup.find('span', id='weekTitle').getText()
    ostr += weekTitle + nstr
    trs = soup.find('table', class_='sdi-data-wide').find_all('tr')
    cnt = 0
    for tr in trs:
        tds = tr.find_all ('td')
        if cnt == 0:
            for td in tds:
                ostr += td.getText() + str
            ostr += nstr
            cnt += 1
        else:
            for td in tds:
                ostr += (td.find('input').get('value')) + str
            ostr += nstr
    return ostr

def get_Trends(url):
    ostr_list = {}
    ostr = ''
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    title = soup.find('h1', class_='titleBar').getText()
    ostr += title + nstr
    iframe = soup.find('iframe', id='ctl00__FrmViewer')
    if iframe is None:
        return ostr
    iframe_src = iframe.get('src')
    page = requests.get(iframe_src)
    soup = bs(page.content, 'lxml')
    trs = soup.find_all(['td', 'div'], {'class': ['sdi-so-title', 'sdi-datahead-sub', 'sdi-datacell']})
    cnt = 0
    teamname = None
    for tr in trs:
        if not tr.find('div') is None:
            cnt = 0
        elif tr.name == 'div':
            if not teamname is None:
                ostr_list[teamname] = ostr
                ostr = ''
            teamname = tr.getText()
            sobj = re.search(r'\d{4}-\d{2}-\d{2}', teamname)
            if not sobj is None:
                teamname = teamname[:sobj.start() - 1]
            ostr += tr.getText() + nstr
        else:
            cnt += 1
            ostr += tr.getText() + str
            if cnt == 5:
                ostr += nstr
                cnt = 0
    if not teamname is None:
        ostr_list[teamname] = ostr
    return ostr_list

def get_Offensive_Stats(url):
    ostr = ''
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    if soup.find('h1', class_='titleBar'):
        title = soup.find('h1', class_='titleBar').getText()
        ostr += title + nstr
    iframe = soup.find('iframe', id='ctl00__FrmViewer')
    if iframe is None:
        return ostr
    iframe_src = iframe.get('src')
    page = requests.get(iframe_src)
    soup = bs(page.content, 'lxml')
    if soup.find ('div', class_='sdi-so-title'):
        weekTitle = soup.find ('div', class_='sdi-so-title').getText ()
        ostr += weekTitle + nstr
    trs = soup.find('table', class_='sdi-data-wide').find_all('tr')
    cnt = 0
    for tr in trs:
        tds = tr.find_all('td')
        ostr += ' '.join(tr.getText().strip().splitlines())
        # for td in tds:
        #     ostr += td.getText().strip() + str
        ostr += nstr
    return ostr

def get_Weather(url):
    ostr = ''
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    title = soup.find('h1', class_='titleBar').getText()
    ostr += title + nstr
    iframe = soup.find('iframe', id='ctl00__FrmViewer')
    if iframe is None:
        return ostr
    iframe_src = iframe.get('src')
    page = requests.get(iframe_src)
    soup = bs(page.content, 'lxml')
    trs = soup.find_all('tr')
    cnt = 0
    for tr in trs:
        tds = tr.find_all('td', {'class': ['weathertop2', 'weathersubhead2', 'alt1left', 'weather4']})
        if cnt == 1:
            cnt = 0
            continue
        if len(tds) == 3:
            cnt = 1
        for td in tds:
            data = td.getText().strip().replace('\t', '')
            data = " ".join(data.splitlines())
            ostr += data + str
        ostr += nstr
    return ostr

def get_Standings(url):
    ostr = ''
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    title = soup.find('h1', class_='titleBar').getText()
    ostr += title + nstr
    iframe = soup.find('iframe', id='ctl00__FrmViewer')
    if iframe is None:
        return ostr
    iframe_src = iframe.get('src')
    page = requests.get(iframe_src)
    soup = bs(page.content, 'lxml')
    weekTitle = soup.find ('div', class_='sdi-title-page-who-sublinks').getText ()
    ostr += weekTitle + nstr
    divs = soup.find_all('div', class_='sdi-so')
    for div in divs:
        sotitle = div.find('div', class_='sdi-so-title').getText()
        ostr += sotitle + nstr
        trs = div.find_all('tr')
        cnt = 0
        for tr in trs:
            tds = tr.find_all('td')
            for td in tds:
                ostr += td.getText().strip() + str
            ostr += nstr
    return ostr

def get_Scores(url):
    ostr = ''
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    title = soup.find('h1', class_='titleBar titleBarScoreOdds').getText()
    ostr += title + nstr
    divs = soup.find_all('div', id='_DivOutput')
    for divv in divs:
        div = divv.find_all('tr')[3]
        trs = div.find_all('tr')
        for tr in trs:
            ostr += tr.getText(separator=str).strip().replace('\n', '').replace('                                       ', ' ') + nstr
        ostr += nstr
    return ostr

def wnba_get_Standings(url):
    ostr = ''
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    title = soup.find('h1', class_='titleBar').getText()
    ostr += title + nstr
    divs = soup.find_all('table', class_='datatable')
    if len(divs) != 2:
        return ostr
    trs = divs[1].find_all(['th', 'tr'], {'class': ['header1', 'header2', 'cell1', 'cell2']})
    cnt = 0
    for tr in trs:
        if tr.get('class')[0] == 'header1':
            if cnt == 0:
                cnt = 1
            elif tr.get('nowrap') == 'nowrap':
                ostr += nstr
            ostr += tr.getText() + str
        else:
            if cnt > 0:
                ostr += nstr
                cnt = 0
            ostr += tr.getText(separator=' ') + nstr
    return ostr

def wnba_get_Trends(url):
    ostr_dict = {}
    ostr = ''
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    title = soup.find('h1', class_='titleBar').getText()
    ostr += title + nstr
    divs = soup.find_all('table', class_='datatable')
    if len(divs) != 2:
        return ostr
    subtitle = soup.find('th', class_='header1').getText()
    ostr += subtitle + nstr
    trs = divs[1].find_all('td', {'class': ['lightBlueTitleCell', 'matchupCells', 'matchupHeader', 'matchupCells Text', 'copy']})
    cnt = 0
    title = None
    for tr in trs:
        if tr.get('class')[0] == 'lightBlueTitleCell':
            if not title is None:
                ostr_dict[title] = ostr
                ostr = ''
            title = tr.getText().strip()
            sobj = re.search(r'\d+/\d+/\d{4}', title)
            if not sobj is None:
                title = title[:sobj.start() - 3]
        ostr += tr.getText().strip() + nstr
    if not title is None:
        ostr_dict[title] = ostr
    return ostr_dict

def wnba_get_Offensive_Stats(url):
    ostr = ''
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    if soup.find('h1', class_='titleBar') is None:
        return 'None'
    ostr += soup.find('h1', class_='titleBar').getText()
    divs = soup.find_all('table', class_='datatable')
    if len(divs) != 2:
        return ostr
    trs = divs[1].find_all (['th', 'tr'], {'class': ['header1', 'header2', 'cell1', 'cell2']})
    cnt = 0
    for tr in trs:
        if tr.get ('class')[0] == 'header1':
            if cnt == 0:
                cnt = 1
            elif tr.get ('nowrap') == 'nowrap':
                ostr += nstr
            ostr += tr.getText () + str
            if len(tr.find_all(['b', 'a'])) > 0 and not tr.get('colspan') is None:
                ostr += nstr
        else:
            if cnt > 0:
                ostr += nstr
                cnt = 0
            ostr += tr.getText (separator=' ') + nstr
    return ostr

def mlb_get_Offensive_Stats(url):
    ostr = ''
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    title = soup.find('h1', class_='titleBar').getText()
    ostr += title + nstr
    iframe = soup.find ('iframe', id='ctl00__FrmViewer')
    if iframe is None:
        return ostr
    iframe_src = iframe.get ('src')
    page = requests.get(iframe_src)
    soup = bs (page.content, 'lxml')
    divs = soup.find_all('table', class_='datatable')
    if len(divs) != 2:
        return ostr
    trs = divs[1].find_all(['th', 'td'])
    cnt = 0
    for tr in trs:
        if not tr.get('nowrap') is None:
            ostr += tr.getText() + str
            continue
        elif (tr.get('class') is not None and tr.get('class')[0].find('cell') != -1) or cnt == 1:
            if tr.get('class') is not None:
                ostr += nstr
            ostr += tr.getText() + str
            cnt = 1
            continue
        else:
            ostr += tr.getText().strip() + nstr
    return ostr

def mlb_get_Trends(url):
    ostr_dict = {}
    ostr = ''
    page = requests.get(url)
    soup = bs(page.content, 'lxml')
    title = soup.find('h1', class_='titleBar').getText()
    ostr += title + nstr
    iframe = soup.find ('iframe', id='ctl00__FrmViewer')
    if iframe is None:
        return ostr
    iframe_src = iframe.get ('src')
    page = requests.get(iframe_src)
    soup = bs (page.content, 'lxml')
    divs = soup.find_all('table', class_='datatable')
    if len(divs) != 2:
        return ostr
    trs = divs[1].find_all(['th', 'td'], {'class': ['header1', 'lightBlueTitleCell', 'matchupHeader', 'matchupCells Text']})
    cnt = 0
    teamtitle = None
    for tr in trs:
        if tr.get('class')[0] == 'lightBlueTitleCell':
            if cnt == 0:
                cnt = 1
                if not teamtitle is None:
                    ostr_dict[teamtitle] = ostr
                    ostr = ''
                teamtitle = tr.getText()
                sobj = re.search(r'\d+:\d{2}', teamtitle)
                if not sobj is None:
                    teamtitle = teamtitle[:sobj.start () - 3]
            else:
                cnt = 0
        ostr += tr.getText() + nstr
    if not teamtitle is None:
        ostr_dict[teamtitle] = ostr
    return ostr_dict

def console_out(sport):
    print (get_Odds ('http://www.donbest.com/' + sport + '/odds/'))
    print (get_Injuries ('http://www.donbest.com/' + sport + '/injuries'))
    print (get_Scores ('http://www.donbest.com/' + sport + '/scores/'))
    print (get_Weather ('http://www.donbest.com/' + sport + '/weather/'))
    if not rating[sport] is None:
        print (get_Ratings ('http://www.donbest.com/' + sport + '/' + rating[sport] + '/'))
    if sport == 'wnba' or sport == 'nhl':
        print(wnba_get_Standings('http://www.donbest.com/' + sport + '/standing/'))
        print(wnba_get_Offensive_Stats('http://www.donbest.com/' + sport + '/defensive-stats/'))
        print(wnba_get_Offensive_Stats('http://www.donbest.com/' + sport + '/offensive-stats/'))
        print(wnba_get_Trends('http://www.donbest.com/' + sport + '/trends/'))
    elif sport == 'mlb':
        print (get_Standings ('http://www.donbest.com/' + sport + '/standing/'))
        print (mlb_get_Offensive_Stats ('http://www.donbest.com/' + sport + '/defensive-stats/'))
        print (mlb_get_Offensive_Stats ('http://www.donbest.com/' + sport + '/offensive-stats/'))
        print (mlb_get_Trends ('http://www.donbest.com/' + sport + '/trends/'))
    else:
        print (get_Standings ('http://www.donbest.com/' + sport + '/standing/'))
        print (get_Offensive_Stats ('http://www.donbest.com/' + sport + '/defensive-stats/'))
        print (get_Offensive_Stats ('http://www.donbest.com/' + sport + '/offensive-stats/'))
        print (get_Trends ('http://www.donbest.com/' + sport + '/trends/'))

ref_title = ['COLLEGE FOOTBALL', 'WNBA PLAYOFFS', 'MAJOR LEAGUE BASEBALL', 'NFL WEEK', 'Last Updated:', 'Current Line', 'Forecasted Game Time Conditions', 'Rank Team', 'CurrentRank LastWeek']

def check_title(title, sect):
    if re.search(r'\d+', title) is None or not re.search(r'\d{4}-\d{2}-\d{2}') is None:
        return True
    else:
        for ref in ref_title:
            if title.find(ref) != -1:
                return True
    return False

def get_diff(ndata, sport, sect, title):
    fname = sport + '_' + sect + title + '.txt'
    if os.path.isfile ('./' + fname) and repeat_check:
        with open (fname, 'r') as f:
            odata = f.read ()
        ndatas = ndata.splitlines ()
        ddata = ''
        for ldata in ndatas:
            if len (ldata.strip ()) == 0:
                ddata += ldata + nstr
            elif odata.find (ldata) == -1:
                ddata += ldata + nstr
            else:
                if check_title (ldata, sect):
                    ddata += ldata + nstr
        with open (fname, 'w') as f:
            print (ddata)
            # f.write(ddata)
    else:
        with open (fname, 'w', encoding='utf-8') as f:
            f.write (ndata)

def txtfile_save(ndata, sport, sect):
    if sect == 'trends':
        for key, value in ndata.items():
            get_diff(value, sport, sect, '_' + key)
    else:
        get_diff(ndata, sport, sect, '')

def file_out(sport):
    txtfile_save(get_Odds ('http://www.donbest.com/' + sport + '/odds/'), sport, 'odds')
    txtfile_save (get_Injuries ('http://www.donbest.com/' + sport + '/injuries'), sport, 'injuries')
    txtfile_save (get_Scores ('http://www.donbest.com/' + sport + '/scores/'), sport, 'scores')
    txtfile_save (get_Weather ('http://www.donbest.com/' + sport + '/weather/'), sport, 'weather')
    if not rating[sport] is None:
        txtfile_save (get_Ratings ('http://www.donbest.com/' + sport + '/' + rating[sport] + '/'), sport, 'rating')
    if sport == 'wnba' or sport == 'nhl':
        txtfile_save(wnba_get_Standings('http://www.donbest.com/' + sport + '/standing/'), sport, 'standing')
        txtfile_save(wnba_get_Offensive_Stats('http://www.donbest.com/' + sport + '/defensive-stats/'), sport, 'defensive_stats')
        txtfile_save(wnba_get_Offensive_Stats('http://www.donbest.com/' + sport + '/offensive-stats/'), sport, 'offensive_stats')
        txtfile_save(wnba_get_Trends('http://www.donbest.com/' + sport + '/trends/'), sport, 'trends')
    elif sport == 'mlb':
        txtfile_save (get_Standings ('http://www.donbest.com/' + sport + '/standing/'), sport, 'standing')
        txtfile_save (mlb_get_Offensive_Stats ('http://www.donbest.com/' + sport + '/defensive-stats/'), sport, 'defensive_stats')
        txtfile_save (mlb_get_Offensive_Stats ('http://www.donbest.com/' + sport + '/offensive-stats/'), sport, 'offensive_stats')
        txtfile_save (mlb_get_Trends ('http://www.donbest.com/' + sport + '/trends/'), sport, 'trends')
    else:
        txtfile_save (get_Standings ('http://www.donbest.com/' + sport + '/standing/'), sport, 'standing')
        txtfile_save (get_Offensive_Stats ('http://www.donbest.com/' + sport + '/defensive-stats/'), sport, 'defensive_stats')
        txtfile_save (get_Offensive_Stats ('http://www.donbest.com/' + sport + '/offensive-stats/'), sport, 'offensive_stats')
        txtfile_save (get_Trends ('http://www.donbest.com/' + sport + '/trends/'), sport, 'trends')

for sport in sports:
    # sport = 'wnba'
    file_out(sport)
