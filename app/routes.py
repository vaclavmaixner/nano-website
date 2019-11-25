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
    return render_template('news-post.html', articles=[article])


@app.route('/edit-news', methods=['GET', 'POST'])
@login_required
def edit_news():
    news_article = Article.query.all()
    news_form = PostNewsArticle()

    if news_form.validate_on_submit():
        article = Article(heading=news_form.heading.data,
                          body=news_form.post.data)
        db.session.add(article)
        db.session.commit()
        flash('Your post is now live!')

    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, app.config['NEWS_ARTICLES_PER_PAGE'], False)
    next_url = url_for('edit_news', page=articles.next_num) \
        if articles.has_next else None
    prev_url = url_for('edit_news', page=articles.prev_num) \
        if articles.has_prev else None

    return render_template('edit-news.html', articles=articles.items, next_url=next_url,
                           prev_url=prev_url, news_form=news_form)


@app.route('/edit-news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news_article(id):
    news_article = Article.query.get_or_404(id)
    news_form = PostNewsArticle()

    if news_form.validate_on_submit():
        news_article.body = news_form.post.data
        news_article.heading = news_form.heading.data
        db.session.add(news_article)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('admin', id=news_article.id))

    news_form.post.data = news_article.body
    return render_template('edit-post.html', form=news_form)


@app.route('/delete-news/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_news(id):
    news_article = Article.query.get_or_404(id)

    db.session.delete(news_article)
    db.session.commit()
    flash('The post has been deleted.')

    return redirect(url_for('edit_news', id=news_article.id))


@app.route('/admin2', methods=['GET', 'POST'])
@login_required
def admin():
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

    return render_template('admin.html', news_form=news_form, human_form=human_form, humans=humans, articles=articles.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/create-news', methods=['GET', 'POST'])
def create_news():
    news_form = PostNewsArticle()

    if news_form.validate_on_submit():
        article = Article(heading=news_form.heading.data,
                          body=news_form.post.data)
        db.session.add(article)
        db.session.commit()
        flash('Your post is now live!')

    return render_template('edit-news.html', news_form=news_form)


@app.route('/create-human', methods=['GET', 'POST'])
def create_human():
    news_form = PostNewsArticle()
    human_form = CreateNewHuman()

    if human_form.validate_on_submit():
        new_human = Human(slug=human_form.slug.data,
                          full_name=human_form.full_name.data, full_name_cz=human_form.full_name_cz.data,
                          position=human_form.position.data,
                          email=human_form.email.data, telephone=human_form.telephone.data,
                          orcid=human_form.orcid.data, links=human_form.links.data,
                          researcher_id=human_form.researcher_id.data, scopus_id=human_form.scopus_id.data, about_text=human_form.about_text.data)
        db.session.add(new_human)
        db.session.commit()
        flash('Your new human is now alive!')
    else:
        flash('not validated')

    return render_template('admin.html', news_form=news_form, human_form=human_form)


@app.route('/delete-human/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_human(id):
    human = Human.query.get_or_404(id)

    db.session.delete(human)
    db.session.commit()
    flash('The person has been deleted.')

    return redirect(url_for('admin', id=human.id))


@app.route('/people-detail/<name>', methods=['GET', 'POST'])
def people_detail(name):
    human = Human.query.filter_by(slug=Human.slug).first_or_404()
    return render_template('people-detail.html', human=human)


@app.route('/research')
def research():
    return render_template('research.html')


@app.route('/research/catalysis')
def catalysis():
    return render_template('catalysis.html')


@app.route('/research/fuel-cells')
def fuel_cells():
    return render_template('fuel-cells.html')


@app.route('/instruments')
def instruments():
    return render_template('instruments.html')


@app.route('/instruments/napxps')
def napxps():
    return render_template('napxps.html')


@app.route('/ceric')
def ceric():
    return render_template('ceric.html')


@app.route('/opvvv')
def opvvv():
    return render_template('opvvv.html')


@app.route('/opvvv/splmsb')
def splmsb():
    return render_template('splmsb.html')


@app.route('/opvvv/pacng')
def pacng():
    return render_template('pacng.html')


@app.route('/publications')
def publications():
    return render_template('publications.html')


@app.route('/grants')
def grants():
    return render_template('grants.html')


@app.route('/for-students')
def for_students():
    return render_template('for-students.html')


@app.route('/summer-projects')
def summer_projects():
    return render_template('summer-projects.html')


@app.route('/bachelors-theses')
def bachelors_theses():
    return render_template('bachelors-theses.html')


@app.route('/masters-theses')
def masters_theses():
    return render_template('masters-theses.html')


@app.route('/doctoral-theses')
def doctoral_theses():
    return render_template('doctoral-theses.html')


@app.route('/about-us')
def about_us():
    return render_template('about-us.html')


@app.route('/people')
def people():
    people = Human.query.all()
    return render_template('people.html', people=people)


@app.route('/contact')
def contact():
    return render_template('contact.html')


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
