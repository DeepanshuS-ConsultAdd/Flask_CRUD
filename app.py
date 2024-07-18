from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from email_validator import validate_email, EmailNotValidError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(100), nullable=False)

@app.route("/show", methods=["GET"])
def index():
    employees = Employee.query.all()
    return jsonify([{
        'id': employee.id,
        'name': employee.name,
        'salary': employee.salary,
        'email': employee.email,
        'role' : employee.role
    } for employee in employees])

@app.route("/show/<int:id>", methods=["GET"])
def check(id):
    print("heyhh")
    try:
        employee = Employee.query.get_or_404(id)
        return jsonify({
            'id': employee.id,
            'name': employee.name,
            'salary': employee.salary,
            'email': employee.email,
            'role': employee.role
        })
    except:
        return f"Sorry!, No Record Found for ID: {id}"

@app.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    name = data.get('name')
    salary = data.get('salary')
    email = data.get('email')
    roles = data.get('role')
    if('@' not in email):
        return "Invalid Email"
    if(not isinstance(salary, int)):
        return "Invalid Salary"
    new_employee = Employee(name=name, salary=salary, email=email, role=roles)
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'id': new_employee.id, 'name': new_employee.name, 'salary': new_employee.salary, 'email': new_employee.email, 'role': new_employee.role})

@app.route("/update/<int:id>", methods=["PUT"])
def update(id):
    try:
        employee = Employee.query.get_or_404(id)
        data = request.get_json()
        employee.name = data.get('name', f"{employee.name}")
        employee.salary = data.get('salary', f"{employee.salary}")
        employee.email = data.get('email', f"{employee.email}")
        employee.role = data.get('role', f"{employee.role}")
        db.session.commit()
        return jsonify({'id': employee.id, 'name': employee.name, 'salary': employee.salary, 'email': employee.email, 'role': employee.role})
    except:
        return f"Sorry!, No Record Found for ID: {id}"

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    try:
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'})
    except:
        return f'Sorry!, No Record Found for ID: {id}'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
