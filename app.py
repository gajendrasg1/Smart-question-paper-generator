from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import random

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

# ---------------- HOME PAGE ---------------- #

@app.route('/')
def home():
    return render_template('index.html')

# ---------------- GENERATE QUESTION PAPER ---------------- #

@app.route('/generate', methods=['POST'])
def generate():

    subject = request.form['subject'].strip()
    difficulty = request.form['difficulty']
    num_questions = int(request.form['num_questions'])

    # ---------------- VALID SUBJECTS ---------------- #

    valid_subjects = [

        "python",
        "java",
        "dbms",
        "ddco",
        "os",
        "operating system",
        "computer networks",
        "cn",
        "aiml",
        "artificial intelligence",
        "machine learning",
        "data science",
        "cyber security",
        "cloud computing",
        "web technology",
        "software engineering",
        "c programming",
        "c++",
        "javascript",
        "react",
        "flask",
        "mongodb",
        "biology",
        "physics",
        "chemistry",
        "mathematics",
        "electronics",
        "electrical",
        "mechanical",
        "civil engineering"

    ]

    # ---------------- VALIDATION ---------------- #

    if subject.lower() not in valid_subjects:

        return '''
        <h1 style="text-align:center;color:red;margin-top:50px;">
        Invalid Academic Subject
        </h1>

        <h2 style="text-align:center;">
        Please Enter Valid Subject Name
        </h2>
        '''

    # ---------------- QUESTION GENERATION ---------------- #

    starters = [

        "Explain",
        "Discuss",
        "Describe",
        "Analyze",
        "Evaluate",
        "Illustrate",
        "Compare",
        "Differentiate",
        "Summarize",
        "Write short notes on"

    ]

    topics = [

        f"core concepts of {subject}",
        f"applications of {subject}",
        f"modern technologies in {subject}",
        f"future scope of {subject}",
        f"industrial use of {subject}",
        f"security aspects of {subject}",
        f"advantages of {subject}",
        f"limitations of {subject}",
        f"algorithms used in {subject}",
        f"real-world implementation of {subject}",
        f"architecture of {subject}",
        f"workflow in {subject}",
        f"performance optimization in {subject}",
        f"ethical issues in {subject}",
        f"automation using {subject}",
        f"communication methods in {subject}",
        f"advanced concepts of {subject}",
        f"data processing in {subject}",
        f"research opportunities in {subject}",
        f"latest innovations in {subject}"

    ]

    endings = [

        "with examples.",
        "in detail.",
        "with suitable diagram.",
        "using real-time applications.",
        "with advantages and disadvantages.",
        "with case study.",
        "in modern industry.",
        "with technical explanation.",
        "with practical implementation.",
        "with comparison."

    ]

    # ---------------- GENERATE UNIQUE QUESTIONS ---------------- #

    generated_questions = set()

    max_possible = len(starters) * len(topics) * len(endings)

    num_questions = min(num_questions, max_possible)

    while len(generated_questions) < num_questions:

        question = (
            f"{random.choice(starters)} "
            f"{random.choice(topics)} "
            f"{random.choice(endings)}"
        )

        generated_questions.add(question)

    generated_questions = list(generated_questions)

    return render_template(
        'output.html',
        subject=subject,
        difficulty=difficulty,
        questions=generated_questions
    )

# ---------------- DOWNLOAD PDF ---------------- #

@app.route('/download_pdf', methods=['POST'])
def download_pdf():

    subject = request.form['subject']
    difficulty = request.form['difficulty']

    questions_list = request.form.getlist('questions')

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font('Arial', 'B', 18)

    pdf.cell(
        200,
        10,
        txt='SMART QUESTION PAPER',
        ln=True,
        align='C'
    )

    pdf.ln(10)

    pdf.set_font('Arial', '', 12)

    pdf.cell(
        200,
        10,
        txt=f'Subject: {subject}',
        ln=True
    )

    pdf.cell(
        200,
        10,
        txt=f'Difficulty: {difficulty}',
        ln=True
    )

    pdf.ln(10)

    for i, q in enumerate(questions_list, start=1):

        pdf.multi_cell(
            0,
            10,
            f'{i}. {q}'
        )

    pdf.output('question_paper.pdf')

    return send_file(
        'question_paper.pdf',
        as_attachment=True
    )

# ---------------- RUN APP ---------------- #

if __name__ == '__main__':
    app.run(debug=True)