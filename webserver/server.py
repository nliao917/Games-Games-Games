import os

from flask import Flask, abort, request, render_template, g, redirect, Response
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool



tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, instance_relative_config=True,template_folder=tmpl_dir)

DB_USER = "lz2803"
DB_PASSWORD = "1138"


DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"
DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/proj1part2"

#
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
    try:
        g.conn = engine.connect()
    except:
        print ("uh oh, problem connecting to database")
        import traceback; traceback.print_exc()
        g.conn = None

@app.teardown_request
def teardown_request(exception):
    try:
        g.conn.close()
    except Exception as e:
        pass

@app.route('/')
def index():
    print (request.args)
    cursor = g.conn.execute("SELECT gid, name FROM game")
    names = []
    for result in cursor:
        names.append(result)  # can also be accessed using result[0]
    cursor.close()
    context = dict(data = names)
    return render_template("index.html", **context)


@app.route('/screenshot')
def screeshot():
    print (request.args)
    cursor = g.conn.execute("SELECT picure FROM has_screenshot")
    names = []
    for result in cursor:
        names.append(result)  # can also be accessed using result[0]
    cursor.close()
    context = dict(data = names)
    return render_template("another.html", **context)


@app.route('/genre')
def genre():
    print (request.args)
    cursor = g.conn.execute("SELECT gname FROM Genre")
    names = []
    for result in cursor:
        names.append(result)  # can also be accessed using result[0]
    cursor.close()
    context = dict(data = names)
    return render_template("genre.html", **context)

def get_genre(genre):
    cursor = g.conn.execute('SELECT * from game g join has H on g.gid= h.gid WHERE h.gname =%s',genre)
    names = []
    for result in cursor:
        names.append(result)
    cursor.close()
    post = dict(data = names)
    if post is None:
        abort(404)
    return post


@app.route('/genre/<genre>')
def gen(genre):
    post = get_genre(genre)
    return render_template('genre1.html', **post)

@app.route('/platform')
def platform():
    print (request.args)
    cursor = g.conn.execute("SELECT distinct type FROM Platform")
    names = []
    for result in cursor:
        names.append(result)  # can also be accessed using result[0]
    cursor.close()
    context = dict(data = names)
    return render_template("platform.html", **context)

@app.route('/review')
def review():
    cursor = g.conn.execute("SELECT g.name,r.score, r.attitude,r.source,r.link FROM game g left join rate_rates r on g.gid=r.gid")
    names = []
    for result in cursor:
        if not result[2]:
            names.append([result[0],result[1],result[3],result[4]])
        else:
            names.append([result[0],result[2],result[3],result[4]])
    cursor.close()
    context = dict(data = names)
    return render_template("review.html", **context)

def get_platform(platform):
    cursor = g.conn.execute('SELECT distinct g.gid, g.name FROM game g left join release_on r on g.gid=r.gid join platform p on r.pname=p.pname WHERE p.type =%s',platform)
    names = []
    for result in cursor:
        names.append(result)
    cursor.close()
    post = dict(data = names)
    if post is None:
        abort(404)
    return post


@app.route('/platform/<platform>')
def plat(platform):
    post = get_platform(platform)
    return render_template('platform1.html', **post)



def get_post(id):
    cursor = g.conn.execute('SELECT * FROM game g left join release_on r on g.gid=r.gid left join platform p on r.pname=p.pname left join rate_rates rate on g.gid=rate.gid left join makes m on m.gid=g.gid WHERE g.gid =%s',id)
    names = []
    for result in cursor:
        names.append(result)
    cursor.close()
    post = dict(data = names)
    if post is None:
        abort(404)
    return post


@app.route('/<int:id>')
def post(id):
    post = get_post(id)
    return render_template('game.html', **post)

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using
        python server.py
    Show the help text using
        python server.py --help
    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()

    
