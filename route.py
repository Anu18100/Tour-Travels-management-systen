from werkzeug.wrappers import Request
from managment import app , db , encode
from datetime import date
import secrets
import os
from PIL import Image
from flask import render_template , url_for , flash , redirect , request
from managment.form import *
from managment.datbase import User , Tour , Review
from flask_login import login_user , current_user , logout_user , login_required


@app.route('/home')
@app.route('/')
def home():
    rev = Review.query.all()
    user = User
    if current_user.is_authenticated:
        image_file = url_for('static' , filename = 'pp/' + current_user.image_file)
        tour = Tour
        return render_template('home_page.html' , image_file= image_file , rev = rev  , user = user , tour = tour)
    return render_template('home_page.html',rev = rev , user = user )


@app.route('/registration',methods=['GET', 'POST'])
def regi():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = redistrationform()
    if form.validate_on_submit():
        encoded_pass = encode.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first = form.fn.data ,middle = form.mn.data , last = form.ln.data , email = form.email.data , user_type = form.user_type.data , password=encoded_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.fn.data}','success')
        return redirect(url_for('login'))
    return render_template('registration.html' , form=form)





@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and encode.check_password_hash(user.password, form.password.data):
            login_user(user , remember= form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful , Please check the email and Password','danger')
    return render_template('login_page.html' , form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))





def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path , 'static/pp' , picture_fn)
    outout_size = (300,300)
    i = Image.open(form_picture)
    i.thumbnail(outout_size)
    i.save(picture_path)
    return picture_fn




@app.route('/account' ,methods=['GET', 'POST'])
@login_required
def account():
    form = Accountform()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first = form.fn.data
        current_user.middle = form.mn.data
        current_user.last = form.ln.data
        current_user.email = form.email.data
        current_user.add1 = form.add1.data
        current_user.add2 = form.add2.data
        current_user.add3 = form.add3.data
        current_user.add4 = form.add4.data
        current_user.state = form.add5.data
        current_user.city = form.add6.data
        current_user.pincode = form.pincode.data
        db.session.commit()
        flash("Your Account is Updated!", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.fn.data = current_user.first
        form.mn.data = current_user.middle
        form.ln.data = current_user.last
        form.email.data = current_user.email
        form.add1.data = current_user.add1
        form.add2.data = current_user.add2
        form.add3.data = current_user.add3
        form.add4.data = current_user.add4
        form.add5.data = current_user.state
        form.add6.data = current_user.city
        form.pincode.data = current_user.pincode
    image_file = url_for('static' , filename = 'pp/' + current_user.image_file)
    return render_template('account.html' ,  image_file = image_file , form = form)





@app.route('/plantour' , methods=[ 'GET', 'POST'])
@login_required
def tour():
    form = tourform()
    if form.validate_on_submit():
        ptour = Tour(place = form.place.data , doj = form.doj.data , total_amt = form.total_amt.data , package_amt = form.package_amt.data , nop = form.nop.data , traveler = current_user)
        db.session.add(ptour)
        db.session.commit()
        flash('Your trip is Booked' , 'success')
        return redirect(url_for('home'))
    return render_template('tour.html' ,  form = form)


@app.route('/plantour/<pid>' , methods=[ 'GET', 'POST'])
@login_required
def ptour(pid):
    form = tourform()
    pk = Packages.query.get_or_404(pid)
    form.place.data = pk.destination
    form.package_amt.data = pk.amt
    form.doj.data = date.today()
    if form.validate_on_submit():
        ptour = Tour(place = form.place.data , doj = form.doj.data , total_amt = form.total_amt.data , package_amt = form.package_amt.data , nop = form.nop.data , traveler = current_user)
        db.session.add(ptour)
        db.session.commit()
        flash('Your trip is Booked' , 'success')
        return redirect(url_for('packagelist'))
    return render_template('tour.html' ,  form = form , pid = pid)



@app.route('/review' , methods=[ 'GET', 'POST'] )
@login_required
def review():
    d = date.today()
    form = reviewform()
    rev = Review
    if form.validate_on_submit():
        rev = Review(title = form.title.data , review = form.review.data ,date_review = d , rver = current_user.id)
        db.session.add(rev)
        db.session.commit()
        flash( 'Review is created' , 'success' )
        return redirect(url_for('home'))
    return render_template('review.html' ,  form = form , rev = rev)


@app.route('/packages' , methods=[ 'GET', 'POST'] )
@login_required
def package():
    form = Packageform()
    pk = Packages.query.all()
    if form.validate_on_submit():
        package = Packages(destination = form.destiantion.data , duration = form.duration.data , amt =   form.amt.data)
        db.session.add(package)
        db.session.commit()
        flash( 'Package added' , 'success' )
        return redirect(url_for('package'))
    return render_template('pakage.html' , form = form , pk = pk )


@app.route('/upackage/<pid>' , methods=[ 'GET', 'POST'] )
@login_required
def upackage(pid):
    form = Packageform()
    pk = Packages.query.get_or_404(pid)
    if form.validate_on_submit():
        pk.amt = form.amt.data
        db.session.commit()
        flash( 'Package is updated' , 'success' )
        return redirect(url_for('package'))
    form.amt.data = pk.amt
    form.destiantion.data = pk.destination
    form.duration.data = pk.duration
    return render_template('pakage.html' ,  form = form , pk = pk , pid= pid)


@app.route('/udelete/<pid>' , methods=['GET', 'POST'] )
@login_required
def udelete(pid):
    db.session.delete(Packages.query.get_or_404(pid))
    db.session.commit()
    flash( 'Package is Deleted' , 'success' )
    return redirect(url_for('package'))


@app.route('/buses' , methods=[ 'GET', 'POST'] )
@login_required
def buses():
    form = busesform()
    bus = Buses.query.all()
    if form.validate_on_submit():
        bus_1 = Buses(driver_name = form.driver_name.data, contact = form.contact.data, status =form.status.data )
        db.session.add(bus_1)
        db.session.commit()
        flash( 'bus added' , 'success' )
        return redirect(url_for('buses' ))
    return render_template('buses.html' , form = form , bus =bus)


@app.route('/ubus/<pid>' , methods=[ 'GET', 'POST'] )
@login_required
def ubus(pid):
    form = busesform()
    bus = Buses.query.get_or_404(pid)
    if form.validate_on_submit():
        bus.driver_name = form.driver_name.data
        bus.contact = form.contact.data 
        bus.status = form.status.data 
        db.session.commit()
        flash( 'Bus is updated' , 'success' )
        return redirect(url_for('buses'))
    form.driver_name.data = bus.driver_name
    form.contact.data = bus.contact
    form.status.data = bus.status
    return render_template('buses.html' ,  form = form , bus = bus , pid= pid)


@app.route('/bdelete/<pid>' , methods=['GET', 'POST'] )
@login_required
def bdelete(pid):
    db.session.delete(Buses.query.get_or_404(pid))
    db.session.commit()
    flash( 'Bus is Deleted' , 'success' )
    return redirect(url_for('buses'))



@app.route('/busallocation' , methods=[ 'GET', 'POST'] )
@login_required
def busallocation():
    form = fform()
    tour = Tour
    user = User
    if form.validate_on_submit():
       return redirect(url_for('allot' , place = form.destiantion.data))
    return render_template('busallocation.html' , form = form ,tour = tour , user = user )



@app.route('/allot/<string:place>' , methods=[ 'GET', 'POST'] )
@login_required
def allot(place):
    form = tform()
    if form.validate_on_submit():
        Tour.query.get_or_404(place).bus_id = form.alloate_bus.data
        db.session.commit()
        return redirect(url_for('busallocation'))
    tour = Tour
    user = User
    return render_template('allot.html' , form = form ,tour = tour , user = user , place= place )


'''@app.route('/abus/<string:place>/<bid>' , methods=[ 'GET', 'POST'] )
@login_required
def abus(place , bid):
    tour = Tour.query.get_or_404(place)
    tour.bus_id = bid
    db.session.commit()
    return redirect(url_for('busallocation'))'''
    


@app.route('/packagelist' , methods=[ 'GET', 'POST'] )
def packagelist():
    pk = Packages
    tour = Tour
    return render_template('packagelist.html' , pk = pk , tour =tour)


@app.route('/tupdate/<pid>' , methods=[ 'GET', 'POST'] )
@login_required
def tupdate(pid):
    form = tourform()
    tour = Tour.query.get_or_404(pid)
    if form.validate_on_submit():
        tour.place = form.place.data
        tour.doj = form.doj.data
        tour.total_amt = form.total_amt.data
        tour.package_amt = form.package_amt.data
        tour.nop = form.nop.data
        db.session.commit()
        flash( 'Trip is updated' , 'success' )
        return redirect(url_for('packagelist'))
    form.total_amt.data = tour.total_amt
    form.package_amt.data = tour.package_amt
    form.place.data = tour.place
    form.nop.data = tour.nop
    form.doj.data = tour.doj
    return render_template('tour.html' , form = form , tour =tour)


@app.route('/tdelete/<pid>' , methods=['GET', 'POST'] )
@login_required
def tdelete(pid):
    db.session.delete(Tour.query.get_or_404(pid))
    db.session.commit()
    flash( 'Trip is Deleted' , 'success' )
    return redirect(url_for('packagelist'))


@app.route('/update/<rid>' , methods=[ 'GET', 'POST'] )
@login_required
def update(rid):
    form = reviewform()
    rev = Review.query.get_or_404(rid)
    if form.validate_on_submit():
        rev.title = form.title.data
        rev.review = form.review.data
        db.session.commit()
        flash( 'Review is updated' , 'success' )
        return redirect(url_for('review'))
    form.title.data = rev.title
    form.review.data = rev.review 
    return render_template('review.html' ,  form = form , rev = rev)


@app.route('/delete/<rid>' , methods=['GET', 'POST'] )
@login_required
def delete(rid):
    db.session.delete(Review.query.get_or_404(rid))
    db.session.commit()
    flash( 'Review is Deleted' , 'success' )
    return redirect(url_for('review'))


@app.route('/reviews' , methods=[ 'GET', 'POST'] )
def reviewlist():
    rev = Review.query.all()
    user = User
    return render_template('reviews.html' , rev = rev , user =user)
