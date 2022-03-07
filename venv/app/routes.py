from flask_bootstrap import Bootstrap
from app import DBfunc
import forms
import requests
from app import app
from app import leaguecalls
from flask import render_template, flash, redirect, url_for, request
import json
global leagueusername
global LogInUsername

'''

REMOVE RANDOM IMPORTS SOMETIMES
i have 0 clue but my stupid ide sometimes adds random imports that break the code
remove above from flask_bootstrap import Bootstrap

'''

@app.route('/', methods=['POST', 'GET'])
@app.route('/index')
def home():
    return redirect("/login")


# main page bascially, where u will be most of the time during testing.
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.loginInForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            global LogInUsername
            LogInUsername = request.form['username']
            LogInPassword = request.form['password']
            # not good variable name, but stays
            x = DBfunc.verifyLogin(LogInUsername,LogInPassword)
            if x == True:

                return redirect('/stattracker')

            else:

                flash(f"User {LogInUsername} not found")

    return render_template('login.html', title="Log In Page", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global signUpUsername
    global signUpPassword
    global signUpLeagueUser
    form = forms.signUpForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            signUpUsername = request.form['username']
            signUpPassword = request.form['password']
            signUpLeagueUser = request.form['chosenLeagueUsername']
            DBfunc.createUser(
                signUpUsername, signUpPassword, signUpLeagueUser)
            flash("signup succsefful")

    return render_template('signup.html', title="Sign Up Page", form=form)


@app.route('/stattracker', methods=['GET', 'POST'])
def stattracker():

    global leagueusername
    leagueusername = DBfunc.loadUsername(LogInUsername)


    print(leagueusername)
    leagueusername = leaguecalls.summonerInfo(leagueusername)
    currentGamer = leaguecalls.requestSummoner(leagueusername)
    currentGamer.requestfunc()
    currentGamer.parseResponse()
    matchidlist = currentGamer.getMatchHistory()
    leagueplayericon = str(leagueusername.getSummonerPictureID())
    print(matchidlist)
    playermanList = []
    kills = []
    deaths = []
    champname = []
    assists = []
    kdaNumber = []
    itemlist = [[]] #2d array, holds items for currently requested player over 5 games, to access index like: itemlist[game][item], e,g, itemlist[0][1] e.g. 2nd item from first game
    for matchID in matchidlist:
        curmatch = leaguecalls.MatchInfo(matchID)
        curmatch.getMatchInfo()
        chosenmatch = curmatch.getMatchResponse()
        playerMan = leaguecalls.PlayerManager()
        playerMan.populatePlayerInfo(chosenmatch)
        playermanList.append(playerMan)
    
    for x,currentPlayerManager in enumerate(playermanList):
        player = currentPlayerManager.getPlayerByName(leagueusername.getSummonerName())
        try:
            kills.append(player.getKills())
            deaths.append(player.getDeaths())
            champname.append(player.getPlayerChamp())
            assists.append(player.getAssists())
            kdaNumber.append(round(player.getKDA(),2))
            templist = []
            for item in player.getItemList():
                try:
                    templist.append(str(item))
                except IndexError:
                    pass
            itemlist.append(templist)
        except:
            pass
            
  
    itemlist.pop(0)
    print(itemlist)


    return render_template('stattracker.html', playericon = leagueplayericon, title="track stats", displayUser=LogInUsername,champname = champname, matchinfo="test", kills =kills, deaths =deaths,assists = assists,kdaNumber = kdaNumber,ingamename = leagueusername.getSummonerName(),items = itemlist)
