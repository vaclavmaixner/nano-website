from app import app
from app import db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, PostNewsArticle, CreateNewHuman
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Article, Human
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/news')
def news():
    #articles = Article.query.all()
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, app.config['NEWS_ARTICLES_PER_PAGE'], False)
    next_url = url_for('news', page=articles.next_num) \
        if articles.has_next else None
    prev_url = url_for('news', page=articles.prev_num) \
        if articles.has_prev else None
    return render_template('news.html', articles=articles.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/news/<int:id>')
def news_article(id):
    article = Article.query.get_or_404(id)
    return render_template('news_post.html', articles = [article])


@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit(id):
    article = Article.query.get_or_404(id)

    form = PostNewsArticle()
    if form.validate_on_submit():
        article.body = form.post.data
        db.session.add(article)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('admin', id=article.id))

    form.post.data = article.body
    return render_template('edit_post.html', form=form)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    users = User.query.all()
    humans = Human.query.all()

    news_form = PostNewsArticle()
    human_form = CreateNewHuman()
     # if form.validate_on_submit():
    #     article = Article(body=form.post.data)
    #     db.session.add(article)
    #     db.session.commit()
    #     flash('Your post is now live!')

    # if new_human_form.validate_on_submit():
    #     new_human = Human(name=new_human_form.name.data,
    #                       full_name=new_human_form.full_name.data, position=new_human_form.position.data,
    #                       email=new_human_form.email.data, telephone=new_human_form.telephone.data,
    #                       links=new_human_form.links.data, ids=new_human_form.ids.data)
    #     db.session.add(new_human)
    #     db.session.commit()
    #     flash('Your new human is now alive!')
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, app.config['NEWS_ARTICLES_PER_PAGE'], False)
    next_url = url_for('news', page=articles.next_num) \
        if articles.has_next else None
    prev_url = url_for('news', page=articles.prev_num) \
        if articles.has_prev else None

    return render_template('admin.html', users=users, news_form=news_form, human_form=human_form, humans=humans, articles=articles.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/create-news', methods=['GET', 'POST']) 
def create_news():
    news_form = PostNewsArticle()
    human_form = CreateNewHuman()

    if news_form.validate_on_submit():
        article = Article(body=news_form.post.data)
        db.session.add(article)
        db.session.commit()
        flash('Your post is now live!')
        
    return render_template('admin.html', news_form=news_form, human_form=human_form)


@app.route('/create-human', methods=['GET', 'POST']) 
def create_human():
    news_form = PostNewsArticle()
    human_form = CreateNewHuman()

    if human_form.validate_on_submit():
        new_human = Human(name=human_form.name.data,
                          full_name=human_form.full_name.data, position=human_form.position.data,
                          email=human_form.email.data, telephone=human_form.telephone.data,
                          links=human_form.links.data, ids=human_form.ids.data)
        db.session.add(new_human)
        db.session.commit()
        flash('Your new human is now alive!')

    return render_template('admin.html', news_form=news_form, human_form=human_form)


@app.route('/detail/<name>', methods=['GET', 'POST'])
def detail(name):
    human = Human.query.filter_by(name=name).first_or_404()
    return render_template('detail.html', human=human)


@app.route('/our-research')
def our_research():
    return render_template('our-research.html')


@app.route('/publications')
def publications():
    return render_template('publications.html')


@app.route('/for-students')
def for_students():
    return render_template('for-students.html')


@app.route('/about-us')
def about_us():
    return render_template('about-us.html')


@app.route('/people')
def people():
    return render_template('people.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
