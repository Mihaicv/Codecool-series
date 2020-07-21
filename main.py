from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash,session,jsonify,json
from datetime import datetime

from data import queries

load_dotenv()
app = Flask('codecool_series')
app.secret_key = '123'
page = 0
count = 0
column='rating'

@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)



@app.route('/shows/most-rated')
def get_15_rated():
    active_page = page
    offset = page * 15
    most_rated=queries.get_15_most_rated(offset)
    return render_template('15_most_rated.html', most_rated=most_rated,active_page=active_page)

@app.route('/register', methods=['GET','POST'])
def register_user():
       if request.method=='POST':
           submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           name= request.form.get('username')
           password=request.form.get('password')
           user_registered= queries.register_user(submission_time,name,password)
           if user_registered==False:
                flash('This user exist')
                return redirect('/register')
           return redirect('/login')
       return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login_user():

    if 'name' in session:
        return redirect('/')
    if request.method=='POST':
        name=request.form.get('username')
        password=request.form.get('password')
        user=queries.check_user_exist(name)
        if queries.check_login_user(name,password):
            session['name']=name
            session['user_id']=user[0]['id']
            flash('User '+ name+' is logged in')
            return redirect('/')
        else:
            flash('Invalid email or password')
            return redirect('/login')
    return render_template('login.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    if 'name' not in session:
        flash('You are not logged in!')
    else:
        session.pop('name', None)
        session.pop('user_id', None)
        return redirect('/login')

@app.route('/show/<id>')
def show_details(id):
    user_id=session['user_id']
    show=queries.get_show_by_id(id)
    print(show)
    season_movie = queries.show_season_movie(id)
    comments = queries.get_comments(id,user_id)
    top_3_actors_from_movie=queries.actors_3_from_movie(id)

    user_favorites = queries.get_user_favorites(id, session['user_id'])

    if user_favorites:
        id_user_favorites = user_favorites[0]['show_id']
    else:
        id_user_favorites= ''
    return render_template('show_page.html', show=show, season_movie=season_movie,  id_user_favorites= id_user_favorites, comments=comments,top_3_actors_from_movie=top_3_actors_from_movie)

@app.route('/design')
def design():
    return render_template('design.html')

@app.route('/nextpage')
def next_page():
    global page
    global column
    page += 1
    return redirect('/shows/most-rated')


@app.route('/downpage')
def previous_page():
    global page
    global column
    if page != 0:
        page -= 1
    if page == 0:
        page = page
    return redirect('/shows/most-rated')

@app.route('/favorite/<id>', methods=['GET','POST'])
def favorite(id):
    favorite_show=queries.fav_show(id)
    return render_template('favorite.html',favorite_show=favorite_show)

@app.route('/add_favorite/<show_id>', methods=['GET','POST'])
def add_favorite(show_id):
        queries.add_favorite(session['user_id'], show_id)
        return redirect(request.referrer)

@app.route('/top_actors')
def top_actors():
    # top_10_actors=queries.top_10_actors()
    return render_template('/top_actors.html')

@app.route('/get_actors')
def get_actors():
    data = queries.top_10_actors()
    return jsonify(data)

@app.route('/add_comment/<show_id>', methods=['GET','POST'])
def add_comment(show_id):
    if request.method == 'POST':
        user_id=session['user_id']
        id_show=show_id
        text = request.form.get('comment')
        queries.add_comment(user_id,id_show,text)

        return redirect('/show/'+show_id)

    return render_template('show_page.html')

@app.route('/add_comment_JS', methods=['POST','GET'])
def add_commentJS():
    data=request.get_json()
    user_id=session['user_id']
    show_id=data['id_text']
    message=data['text']
    queries.add_comment(user_id,show_id,message)
    return 'comment added'

@app.route('/get_comment_JS/<show_id>')
def get_commentJS(show_id):
    user_id = session['user_id']
    show_id=show_id
    comments=queries.get_comments(show_id,user_id)
    return jsonify(comments)

@app.route('/edit_overview', methods=['GET','POST'])
def edit_overview():
   data=request.get_json()
   show_id=data['idOverview']
   show_overview=data['textOverview']
   queries.edited_overview(show_id,show_overview)
   return 'edited overview'



def main():
    app.run(debug=False,
            port=8003)


if __name__ == '__main__':
    main()
