from flask import render_template, flash, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, models, db
from .forms import Login, Entry, Register, UserSearch, ChangePW
import datetime, time
import logging


@app.route('/', methods=['GET', 'POST'])
def home():
    form = Login()

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = models.Users.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Login failed, try again or register.')
            logging.warning('User failed to login')
            return redirect('/')
        else:
            logging.info('%s logged in'%user.username)
            session['user'] = user.id
            sessionflag = True
            return redirect('/userdiary')
    else:
        return render_template('home.html',
                            title='Login',
                            form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    users = models.Users.query.all()
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        password = request.form['password']

        user = models.Users.query.filter_by(username=username).first()

        if user:
            flash('Username already exists')
            logging.warning('User failed to register account')
            return redirect('/register',)
        else:
            newUser = models.Users(fname=fname, lname=lname, username=username, password=generate_password_hash(password, method='sha256'))

            db.session.add(newUser)
            db.session.commit()

            logging.info('user has created an account')

            return redirect('/')

    else:
        return render_template('register.html',
                                form=form,
                                title='Register',
                                users=users)


@app.route('/userdiary')
def userDiary():
    if not session.get('user'):
        return redirect('/')

    userid = session['user']
    entries = models.DiaryEntries.query.filter_by(user_id=userid)
    user = models.Users.query.filter_by(id=userid).first()

    return render_template("userDiary.html",
                            title='Your Diary',
                            entries=entries,
                            user=user)

@app.route('/entry', methods=['GET', 'POST'])
def diaryEntry():
    if not session.get('user'):
        return redirect('/')

    form = Entry()

    if request.method == "POST":
        dateBuf = request.form['date']

        dayStr, monthStr, yearStr = dateBuf.split("/", 2) #Parses the deadline into day, month, year

        if dayStr[0] == '0':    #day format = 0d
            day = int(dayStr[1])
        else:                   #day format = dd
            day = int(dayStr)

        if monthStr[0] == '0':  #month format = 0m
            month = int(monthStr[1])
        else:                   #month format = mm
            month = int(monthStr)

        year = int(yearStr)
        
        date = datetime.date(year, month, day)    #create new Date object
        event = request.form['event']
        feeling = request.form['feeling']
        comments = request.form['comments']
        summ = request.form['summ']
        if 'private' in request.form:
            state = True
        else:
            state = False

        newEntry = models.DiaryEntries(date=date, event=event, feeling=feeling, comments=comments, summ=summ, private=state, user_id=session['user'])

        db.session.add(newEntry)
        db.session.commit()

        user = models.Users.query.filter_by(id=session['user']).first()
        flash('Entry added successfully!')
        logging.info('%s added a new entry'%user.username)

        return redirect('/entry')
    
    else:
        return render_template('entry.html',
                                title='Diary Entry',
                                form=form)

@app.route('/logout')
def logout():
    if not session.get('user'):
        return redirect('/')

    user = models.Users.query.filter_by(id=session['user']).first()
    logging.info('%s logged out'%user.username)
    session.pop('user', None)
    sessionflag = False
    flash('Log out successful!')
    return redirect('/')

@app.route('/friends', methods = ['GET', 'POST'])
def friends():
    if not session.get('user'):
        return redirect('/')

    form = UserSearch()
    userid = session['user']
    user = models.Users.query.filter_by(id=userid).first()
    username = user.username
    friendLinks = models.Friends.query.filter_by(user1=username)
    friends = []
    for friend in friendLinks:
        k = models.Users.query.filter_by(username=friend.user2).first()
        friends.append(k)


    if request.method == "POST":
        newUsername = request.form['username']

        userCheck = models.Users.query.filter_by(username=newUsername).first()

        if userCheck:
            friendCheck = models.Friends.query.filter_by(user1=username, user2=newUsername).first()
            if friendCheck:
                flash('This user is already your friend!')
                return redirect('/friends')

            newFriend = models.Friends(user1=username, user2=newUsername)

            db.session.add(newFriend)
            db.session.commit()
            logging.info('%s added a friend'%username)
            flash('Friend added successfully!')


        else:
            logging.warning('%s failed to add a friend '%username)
            flash('User could not be found.')

        return redirect('/friends')
    else:
        return render_template('friends.html',
                                title='Friends',
                                form=form,
                                friends=friends)

@app.route('/changePassword', methods=['GET', 'POST'])
def passwordChange():
    if not session.get('user'):
        return redirect('/')

    form = ChangePW()

    userid = session['user']
    user = models.Users.query.filter_by(id=userid).first()
    
    if request.method == "POST":
        old = request.form['old']
        new = request.form['new']

        if not check_password_hash(user.password, old):
            logging.warning('%s failed to change their password'%user.username)
            flash('Old password is incorrect, please try again.')
        else:
            user.password = generate_password_hash(new, method='sha256')
            db.session.commit()
            logging.info('%s changed their password'%user.username)
            flash('Password changed successfully!')

        return redirect('/changePassword')

    else:
        return render_template('password.html',
                                title='Change Password',
                                form=form)

@app.route('/friendsDiary/<int:id>')
def friendDiary(id:int):
    if not session.get('user'):
        return redirect('/')

    entries = models.DiaryEntries.query.filter_by(user_id=id)
    user = models.Users.query.filter_by(id=id).first()

    return render_template('friendDiary.html',
                            title='Friends Diary',
                            user=user,
                            entries=entries)