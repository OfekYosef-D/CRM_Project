from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from app import app, db, login_manager
from app.models import Customer, User
from app.forms import CustomerForm, LoginForm, SignupForm


bcrypt = Bcrypt(app)
@app.route('/home')
@login_required
def home():
    total_customers = len(Customer.query.all())  # Example stat: total number of customers
    recent_customers = Customer.query.order_by(Customer.id.desc()).limit(5).all()  # Last 5 customers
    return render_template('dashboard.html', total_customers=total_customers, recent_customers=recent_customers)


@app.route('/customers', methods=['GET', 'POST'])
@login_required
def list_customers():
    form = CustomerForm() # Create an instance of the form
    search_query = request.args.get('search') # Get the search term from the url
    if search_query: # If the user used search function, display the current customer only.
        customers = Customer.query.filter(
            (Customer.name.ilike(f"%{search_query}%")) |
            (Customer.email.ilike(f"%{search_query}%")) |
            (Customer.phone.ilike(f"%{search_query}%"))
        ).all()
    else: # If the user didn't use the search function, displaying all customers.
        customers = Customer.query.all()

    if form.validate_on_submit(): # Checks if the form was submitted and valid
        # Add the new customer to the DB
        new_customer = Customer(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
        )
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('list_customers')) # Refresh the page to show changes

    return render_template('customers.html', form=form, customers=customers)

@app.route('/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = CustomerForm(obj=customer) # Fill the customer data before we change it

    if form.validate_on_submit():
        customer.name = form.name.data
        customer.email = form.email.data
        customer.phone = form.phone.data
        db.session.commit()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('list_customers'))

    return render_template('customers.html', form=form, customer=customer)

@app.route('/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('list_customers'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))  # Redirect to dashboard
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        new_customer = Customer(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data
        )
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_customer.html', form=form)

@app.route('/reports')
@login_required
def reports():
    flash('Reports page is under construction.', 'info')
    return redirect(url_for('home'))












