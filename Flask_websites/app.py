from flask import Flask, redirect, url_for, render_template, request, make_response

app = Flask(__name__)

#dynamic routing function for string value
@app.route('/profile/<name>')
def profile(name):
    return 'this profile belongs to %s' %name

#dynamic routing function for integer value
@app.route('/profile/<int:id>')
def integer(id):
    return 'this profile belongs to %d' %id

#dynamic routing function for Floating value
@app.route('/profile/<float:id>')
def floating(id):
    return 'this profile belongs to %f' % id

#routing programme for admin and guest

#login form and request value webpage to phython server

@app.route('/<string:page_name>/')
def render_static(page_name):
    #return render_template('hello.html')
    return render_template('%s.html' % page_name)

@app.route('/success/<name>')
def get_success(name):
    return "Welcome to %s" %name

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method =='POST':
       username =request.form["username"]
       print(username)
       return redirect(url_for('get_success', name=username))
    else:
        username =request.args.get('username')
        print(username)
        return redirect(url_for('get_success', name=username))

#login form and request value webpage to phython server

#Template passing data in flask
@app.route('/welcome/<username>')
def index(username):
    return render_template('hello.html', name=username)

#Template passing data in flask
#result will display in tabluar format
@app.route('/students')
def student():
    return render_template('student.html')
@app.route('/results',methods=["POST","GET"])
def result():
    if request.method == "POST":
       result=request.form
       return render_template('results.html', result=result)

#result will display in tabluar format

#cookie method in phython

@app.route('/cookie')
def cookie():
    return render_template('cookie.html')

@app.route('/setcookie',methods=["POST","GET"])
def setcookie():
    if request.method =="POST":
        user =request.form["userName"]
        resp =make_response(render_template('read_Cookie.html'))
        resp.set_cookie('userID',user)
        return resp

@app.route('/getcookie')
def getcookie():
    name =request.cookies.get('userID')
    return "<h1>Hello "+name+"</h1>"

#cookie method in phython


@app.route('/admin')
def hello_admin():
    return "<h2>Hello Admin</h2>"

@app.route('/guest/<guest>')
def hello_guest(guest):
    return 'Hello guest %s' %guest

@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
       return redirect(url_for('hello_admin'))
    else:
      return redirect(url_for('hello_guest',guest=name))

#routing programme for admin and guest

#normal routing
@app.route('/')
def hello():
    firstApp ="First Python Application running"
    return "<h1>"+firstApp+"</h1>"

@app.route('/about')
def about():
    return "<h2>New pages</h2>"

@app.route('/contact')
def contact():
    return "<h3>Contact Us</h3>"
#normal routing

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
