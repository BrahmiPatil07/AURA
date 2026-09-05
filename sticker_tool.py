import os
import re

STICKER_FOLDER = "stickers"


# Exact sticker filenames from your stickers folder
STICKER_MAP = {
    "math": "math.png",
    "research": "research.png",
    "time": "time.png",
    "document": "document.png",
    "coding": "coding.png",
    "learning": "learning.png",
    "confused": "confuse.png",
    "problem": "frustration.png",
    "task": "task.png",
    "general": "smart.png",
    "happy": "happy.png",
    "bye": "bye.png",
    "thank_you": "thank you.png",
    "sorry": "sorry.png",
    "celebration": "celebration.png",
    "intelligent": "intelligent.png",
    "shock": "shock.png",
    "good_work": "good work.png",
}


def get_sticker(category):
    """
    Return the sticker path for a category.
    """

    filename = STICKER_MAP.get(category)

    if not filename:
        return None

    path = os.path.join(STICKER_FOLDER, filename)

    if os.path.exists(path):
        return path

    return None


def classify_question(question):
    """
    Detect the type of user message and select
    an appropriate sticker category.
    """

    text = question.lower().strip()
    text = re.sub(r"\s+", " ", text)

    # -------------------------
    # MATH
    # -------------------------
    math_patterns = [
        r"\bcalculate\b",
        r"\bcalculation\b",
        r"\bcalculator\b",
        r"\bmultiply\b",
        r"\bmultiplication\b",
        r"\bdivide\b",
        r"\bdivision\b",
        r"\baddition\b",
        r"\bsubtraction\b",
        r"\bpercentage\b",
        r"\bpercent\b",
        r"\baverage\b",
        r"\bsum\b",
        r"\bsubtract\b",
        r"\bplus\b",
        r"\bminus\b",
        r"\bmathematics\b",
        r"\bmath\b",
    ]

    if any(re.search(pattern, text) for pattern in math_patterns):
        return "math"

    # Detect expressions like:
    # 25 + 15
    # 100 / 5
    # 8 * 9
    if re.search(r"\d+\s*[\+\-\*\/]\s*\d+", text):
        return "math"


    # -------------------------
    # TIME
    # -------------------------
    time_patterns = [
        r"\bwhat time\b",
        r"\bcurrent time\b",
        r"\btime now\b",
        r"\btime is it\b",
        r"\bwhat date\b",
        r"\bcurrent date\b",
        r"\btoday'?s date\b",
        r"\bwhat day is it\b",
        r"\bcurrent day\b",
    ]

    if any(re.search(pattern, text) for pattern in time_patterns):
        return "time"


    # -------------------------
    # RESEARCH / WEB SEARCH
    # -------------------------
    research_patterns = [
        r"\bresearch\b",
        r"\blatest\b",
        r"\brecent news\b",
        r"\bcurrent news\b",
        r"\bnews\b",
        r"\bsearch online\b",
        r"\bsearch the web\b",
        r"\bweb search\b",
        r"\blook it up\b",
        r"\blook up\b",
        r"\bfind online\b",
        r"\bon the internet\b",
        r"\bwhat happened\b",
    ]

    if any(re.search(pattern, text) for pattern in research_patterns):
        return "research"


    # -------------------------
    # DOCUMENT
    # -------------------------
    document_patterns = [
        r"\bpdf\b",
        r"\bdocument\b",
        r"\bfile\b",
        r"\buploaded file\b",
        r"\bread this file\b",
        r"\bread the file\b",
        r"\bsummarize this file\b",
        r"\bsummarize the file\b",
        r"\bsummary of this file\b",
        r"\bexplain this document\b",
        r"\bwhat does this document\b",
    ]

    if any(re.search(pattern, text) for pattern in document_patterns):
        return "document"


    # -------------------------
    # CODING
    # -------------------------
    coding_patterns = [
        r"\bpython\b",
        r"\bjava\b",
        r"\bjavascript\b",
        r"\bhtml\b",
        r"\bcss\b",
        r"\bsql\b",
        r"\bprogramming\b",
        r"\bprogram\b",
        r"\bcoding\b",
        r"\bcode\b",
        r"\bfunction\b",
        r"\bvariable\b",
        r"\bclass\b",
        r"\bapi\b",
        r"\bdatabase\b",
        r"\bgithub\b",
        r"\bgit\b",
        r"\bcompiler\b",
        r"\bcompile\b",
        r"\bsyntax\b",
        r"\bdebug\b",
        r"\bdebugging\b",
        r"\bwrite code\b",
        r"\bwrite a program\b",
    ]

    if any(re.search(pattern, text) for pattern in coding_patterns):
        return "coding"


    # -------------------------
    # PROBLEM / ERROR
    # -------------------------
    problem_patterns = [
        r"\berror\b",
        r"\bbug\b",
        r"\bissue\b",
        r"\bproblem\b",
        r"\bnot working\b",
        r"\bdoesn't work\b",
        r"\bdoesnt work\b",
        r"\bfailed\b",
        r"\bfailure\b",
        r"\bfix this\b",
        r"\bhelp me fix\b",
        r"\bi am stuck\b",
        r"\bi'm stuck\b",
        r"\bstuck\b",
        r"\bfrustrated\b",
        r"\bfrustration\b",
    ]

    if any(re.search(pattern, text) for pattern in problem_patterns):
        return "problem"


    # -------------------------
    # CONFUSED
    # -------------------------
    confused_patterns = [
        r"\bi don't understand\b",
        r"\bi dont understand\b",
        r"\bdon't understand\b",
        r"\bdont understand\b",
        r"\bconfused\b",
        r"\bnot clear\b",
        r"\bunclear\b",
        r"\bcan you clarify\b",
        r"\bclarify this\b",
        r"\bwhat do you mean\b",
    ]

    if any(re.search(pattern, text) for pattern in confused_patterns):
        return "confused"


    # -------------------------
    # LEARNING
    # -------------------------
    learning_patterns = [
        r"^what is\b",
        r"^what are\b",
        r"^who is\b",
        r"^why is\b",
        r"^why does\b",
        r"^how does\b",
        r"^how do\b",
        r"\bexplain\b",
        r"\bteach me\b",
        r"\bmeaning of\b",
        r"\bdefine\b",
        r"\bdefinition\b",
        r"\bdifference between\b",
        r"\bin simple words\b",
        r"\bsimple explanation\b",
    ]

    if any(re.search(pattern, text) for pattern in learning_patterns):
        return "learning"


    # -------------------------
    # TASK / CREATION
    # -------------------------
    task_patterns = [
        r"\bcreate\b",
        r"\bbuild\b",
        r"\bgenerate\b",
        r"\bdesign\b",
        r"\bdevelop\b",
        r"\bprepare\b",
        r"\bplan\b",
        r"\bmake\b",
        r"\borganize\b",
    ]

    if any(re.search(pattern, text) for pattern in task_patterns):
        return "task"


    # -------------------------
    # THANK YOU
    # -------------------------
    if re.search(
        r"\b(thank you|thanks|thank u|thx)\b",
        text
    ):
        return "thank_you"


    # -------------------------
    # GOODBYE
    # -------------------------
    if re.search(
        r"\b(bye|goodbye|see you|see ya)\b",
        text
    ):
        return "bye"


    # -------------------------
    # SORRY
    # -------------------------
    if re.search(
        r"\b(sorry|apologize|apologies)\b",
        text
    ):
        return "sorry"


    # -------------------------
    # GENERAL
    # -------------------------
    # Personal/general conversations use smart.png
    return "general"