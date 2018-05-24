from flask import Flask, url_for,render_template
from os import path


app = Flask(__name__)

DIR = path.dirname(__file__)


#console output will appear in /var/log/apache2/error.log

@app.route('/')
def root():
    print "=====================================\nConsole Message\n"
    print DIR + "\n====================================="
    return render_template('home.html')
'''
    body = "<h2> Posh some Pishes </h2>"
    body+= "DIR: " + DIR + "<br>"
    body+= '<img src="' + url_for('static', filename='img/posh.jpg') + '" width="500"</img>'
    return body
'''
 
if __name__ == '__main__':
    app.debug = True #DANGER DANGER! Set to FALSE before deployment!
    app.run()
