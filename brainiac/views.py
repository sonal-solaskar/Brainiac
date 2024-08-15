from flask import Blueprint, render_template, request, jsonify
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import instructor
from groq import Groq

load_dotenv()

views = Blueprint("views", __name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)
class Output(BaseModel):
    latex: str

client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

def get_LaTeX(query):
    prompt = f"""
    You are a tool which takes in natural language descriptions and give out LaTeX according to the instructions in the input.
    Output LaTeX for the following:
    {query}
    """
    resp = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_model=Output,
    )
    return resp.latex

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
    return render_template("prompt2latex.html")

@views.route("/generate_latex", methods=["POST"])
def generate_latex():
    data = request.json
    query = data.get("query")
    if query:
        latex_code = get_LaTeX(query)
        return jsonify({"latex": latex_code})
    else:
        return jsonify({"error": "Invalid input"}), 400

