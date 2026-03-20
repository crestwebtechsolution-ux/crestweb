from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'crestweb2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    business = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    name = request.form['name']
    phone = request.form['phone']
    new_lead = Lead(name=name, phone=phone)
    db.session.add(new_lead)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['admin_id'] == 'admin' and request.form['password'] == 'crestweb123':
            session['admin_logged_in'] = True
            return redirect(url_for('view_leads'))
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Admin Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-primary p-5">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h3 class="text-center mb-4">🔐 Admin Login</h3>
                            <form method="POST">
                                <div class="mb-3">
                                    <input class="form-control" name="admin_id" value="admin" placeholder="admin">
                                </div>
                                <div class="mb-3">
                                    <input class="form-control" type="password" name="password" placeholder="crestweb123">
                                </div>
                                <button class="btn btn-success w-100">Login → Leads</button>
                            </form>
                            <small class="text-muted mt-2 d-block text-center">
                                ID: admin | Pass: crestweb123
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/admin-logout')
def admin_logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/view-leads')
def view_leads():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin-login'))
    
    leads = Lead.query.order_by(Lead.timestamp.desc()).all()
    html = '''
    <!DOCTYPE html>
    <html>
    <head><title>View Leads</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="p-4">
        <div class="container">
            <div class="d-flex justify-content-between mb-4">
                <h2>📊 Leads (''' + str(len(leads)) + ''')</h2>
                <a href="/admin-logout" class="btn btn-danger">Logout</a>
            </div>
            '''
    
    if leads:
        html += '<table class="table table-striped"><tr><th>ID</th><th>Name</th><th>Phone</th><th>Date</th></tr>'
        for lead in leads:
            html += f'<tr><td>{lead.id}</td><td>{lead.name}</td><td>{lead.phone}</td><td>{lead.timestamp}</td></tr>'
        html += '</table>'
    else:
        html += '<div class="alert alert-info">No leads yet</div>'
    
    html += '''
        </div>
    </body>
    </html>
    '''
    return html

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
