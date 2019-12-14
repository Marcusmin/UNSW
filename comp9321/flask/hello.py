from flask import Flask, escape, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def back():
    return 'hi, i am back~'

@app.route('/hello')
@app.route('/hello/<name>')
def hello_world(name = None):
    return render_template('hello.html', name = name)

@app.route('/user/<username>')
def show_user(username):
    return f'user name is {username}'
    #return 'user name is %s' % username

@app.route('/num/<int:num>')
def show_num(num):
    return f'the number is {num}'

with app.test_request_context():
    print(url_for('back'))
    print(url_for('hello_world'))
    print(url_for('hello_world', xxx = '1'))
    print(url_for('show_user', username = 'marcus'))
    print(url_for('show_num', num = 100))