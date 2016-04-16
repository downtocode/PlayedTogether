import requests
import lxml
from lxml import html
import time
from datetime import date, datetime

# Gets the page for a player given the player's full name
def getPage(playerName):
    searchTerm = '+'.join(playerName.split())
    return requests.get('http://www.soccerbase.com/players/home.sd?search=' + searchTerm)

# Takes the two player pages and returns two dictionaries for the two players as a tuple
def buildDictionaries(page1, page2):
    tree1 = html.fromstring(page1.content)
    tree2 = html.fromstring(page2.content)
    allrows = tree1.xpath('//*[@id="cpm"]/div[3]/table[1]/tbody/*')
    allrowsB = tree2.xpath('//*[@id="cpm"]/div[3]/table[1]/tbody/*')
    no_teams = len(allrows) - 2
    no_teamsB = len(allrowsB) - 2
    Defoe = {}
    Bassong = {}
    for i in range(1,no_teams+1):
        xpth = '//*[@id="cpm"]/div[3]/table[1]/tbody/tr[' + str(i) + ']'
        teamName = tree1.xpath(xpth + '/td[1]/a')[0].text.strip()
        frm = tree1.xpath(xpth + '/td[2]')[0].text.strip()
        frm = datetime.strptime(frm, "%d %b, %y")
        to = tree1.xpath(xpth + '/td[3]')[0].text.strip()
        if to == '':
            to = date.today().strftime("%d %b, %y")
        to = datetime.strptime(to, "%d %b, %y")
        if teamName not in Defoe:
            Defoe[teamName] = [(frm,to)]
        else:
            Defoe[teamName].append((frm,to))

    for i in range(1,no_teamsB+1):
        xpth = '//*[@id="cpm"]/div[3]/table[1]/tbody/tr[' + str(i) + ']'
        teamName = tree2.xpath(xpth + '/td[1]/a')[0].text.strip()
        frm = tree2.xpath(xpth + '/td[2]')[0].text.strip()
        frm = datetime.strptime(frm, "%d %b, %y")
        to = tree2.xpath(xpth + '/td[3]')[0].text.strip()
        if to == '':
            to = date.today().strftime("%d %b, %y")
        to = datetime.strptime(to, "%d %b, %y")
        if teamName not in Bassong:
            Bassong[teamName] = [(frm,to)]
        else:
            Bassong[teamName].append((frm,to))

    return (Defoe,Bassong)

# Return a dictionary of teams where player1 and player2 played together
# key is teamName, value is tuple of dates played together
# {team: (from, to)}
def overlap(player1, player2):
    teams = {}
    for team in player1:
        if team in player2:
            for dates in player1[team]:
                for dates2 in player2[team]:
                    s1 = dates[0]
                    e1 = dates[1]
                    s2 = dates2[0]
                    e2 = dates2[1]
                    if s2 <= e1 and s1 <= e2:
                        frm = max(s1,s2).strftime("%d %b, %y")
                        to = min(e1,e2).strftime("%d %b, %y")
                        teams[team] = (frm, to)
    return teams

# Get args from the command line
print 'Enter name of the first player: '
p1 = raw_input()
print 'Enter name of the second player: '
p2 = raw_input()
page1 = getPage(p1)
page2 = getPage(p2)
Defoe,Bassong = buildDictionaries(page1, page2)
print p1 + ' and ' + p2 + ' were teammates at: '
ans = overlap(Defoe, Bassong)
for key in ans:
    print '* ' + key + ' from ' + ans[key][0] + ' to ' + ans[key][1]
