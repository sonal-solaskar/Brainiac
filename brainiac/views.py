from flask import Blueprint, render_template, request, jsonify
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import instructor
from groq import Groq
from PyPDF2 import PdfReader

load_dotenv()

views = Blueprint("views", __name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


class LatexOutput(BaseModel):
    latex: str


class SummaryOutput(BaseModel):
    summary: str


client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)


def get_LaTeX(query: str) -> str:
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
        response_model=LatexOutput,
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


@views.route("/Summary")
def summary():
    return render_template("summary.html")


@views.route("/summarize_pdf", methods=["POST"])
def summarize_pdf_route():
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF file uploaded"}), 400

    pdf_file = request.files["pdf"]

    if not pdf_file.filename.endswith(".pdf"):
        return jsonify({"error": "Invalid file format. Please upload a PDF file."}), 400

    pdf_path = os.path.join("/tmp", pdf_file.filename)
    pdf_file.save(pdf_path)

    try:
        summary = summarize_pdf(pdf_path)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


def summarize_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    prompt = f"Summarize the following PDF content:\n\n{full_text}"

    resp = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_model=None,
    )
    return resp.choices[0].message.content


@views.route("/generate_latex", methods=["POST"])
def generate_latex():
    data = request.json
    query = data.get("query")
    if query:
        latex_code = get_LaTeX(query)
        return jsonify({"latex": latex_code})
    else:
        return jsonify({"error": "Invalid input"}), 400
