from flask import Flask, render_template, flash, request
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from wtforms import Form, TextField, validators, SubmitField

# App config
DEBUG=True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = "c0c1023497cc1da362047b607777c1306f8e089155df2148da045ac6b78c86ff659ae050619a51864253308937700682"
esclient = Elasticsearch(['http://localhost:5555'])

# Search Form
class SearchForm(Form):
    query = TextField("Search FOI", validators=[validators.required()])


def mlk_query(query):
    fields = ['call_id', 'service_request_log', 'assigned_to', 'call_topic_category_1', 'call_topic_category_2', 'call_topic_category_3', 'call_opened_date_time', 'call_resolved', 'details', 'agent']
    es = Search(using=esclient, index='logstash-*')
    q = Q('multi_match', query=query,  fields=['service_request_log', 'details'])
    q = es.query(q).source(fields)
    results = q.execute()
    return(results)

# App
@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm(request.form)
    print(form.errors)

    ### Blank results for no search
    results = None
    if request.method == "POST":
        query = request.form["query"]
        ### Set up es
        results = mlk_query(query)
        print(results)
        print(len(results))
        ### Validate form

    return render_template('index.html', form=form, results =results)


#Kill caching in the browser
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

