from flask import Blueprint, render_template

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/Tools")
def tools():
    return render_template("aitools.html")


@views.route("/About")
def about():
    return render_template("aboutus.html")


@views.route("/Tool2")
def tool2():
    return render_template("tool2.html")


@views.route("/Prompt2Latex")
def prompt2latex():
    return render_template("promptToLaTeX.html")

    return render_template('tool2.html')

@views.route('/prompt2latex')
def prompt2latex():
    return render_template('prompt2latex.html')