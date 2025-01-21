from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Customer
from app.forms import CustomerForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customers', methods=['GET', 'POST'])
def list_customers():
    form = CustomerForm() # Create an instance of the form
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

    customers = Customer.query.all()
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


















