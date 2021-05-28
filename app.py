from flask import Flask, render_template, request
from tfidf_search import tfidf_search


results = []
sample = ["https://www.ics.uci.edu/", "https://www.ics.uci.edu/about/about_deanmsg.php", "https://forms.communications.uci.edu/uci-feedback/", "https://academicplanning.uci.edu/uci-accreditation/", "https://dsc.uci.edu/"]
query = ""

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def searchEngine():
    global results
    print(request.form.get("query"))
    query = request.form.get("query")
    if (query!=None and query.strip() != ""):
        results = tfidf_search(query)
    return render_template("searchEngine.jinja2", prev_query = query, entries=results)