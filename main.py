from flask import Flask, request, jsonify
from agent import Agent 
from task import Task
from crew import Crew
from my_llm import call_llm
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

reader = Agent(
    name="TranscriptReader",
    role="Analyzer",
    goal="Identify one compelling insight, moment, or transformation that can be turned into a powerful LinkedIn story.",
    backstory=(
        "You are skilled at analyzing transcripts to spot a *single* strong narrative with emotional or intellectual depth. "
        "Even if the transcript contains multiple topics, your job is to find the **most impactful one** — a story worth telling. "
        "Focus on clear outcomes, transformation, learnings, or character arcs that readers can relate to. "
        "Do not list or extract all topics — pick the strongest insight that can become a powerful story."
    ),
    llm_fn=call_llm
)

writer = Agent(
    name="PostWriter",
    role="LinkedInWriter",
    goal="Craft a single compelling, real LinkedIn story that feels human, inspiring, and natural.",
    backstory=(
        "You are an expert at writing viral LinkedIn posts.\n"
        "You specialize in crafting stories that feel authentic and are written like real humans — not AI.\n\n"
        "Here's your story-building approach:\n"
        "1. Start with an emotionally engaging or curiosity-piquing opening line.\n"
        "2. Share a clear, detailed narrative with emotional ups and downs — third-person preferred.\n"
        "3. Highlight a challenge, the actions taken, and what was learned or changed.\n"
        "4. End with a reflective thought and a question to prompt comments.\n\n"
        "Important:\n"
        "- Only one story per post — even if the transcript has many topics.\n"
        "- Do NOT use section headings like Hook, Insight, Hashtags.\n"
        "- Use short paragraphs and line breaks for readability.\n"
        "- Include 3–5 hashtags at the end, but with no label.\n\n"
        "Also take the input from the reviewer and correct the post. Iterate it a couple of times to refine it."
    ),
    llm_fn=call_llm
)

reviewer = Agent(
    name="Reviewer",
    role="Editor and Content Optimizer",
    goal="Polish the LinkedIn post so it's clearer, more engaging, and feels like it was written by a real human.",
    backstory=(
        "You are a professional editor for LinkedIn content.\n"
        "Your job is to refine the post so it:\n"
        "1. Has a strong opening line.\n"
        "2. Flows naturally like a real story.\n"
        "3. Ends with a reflective CTA-style question.\n"
        "4. Contains 3–5 relevant hashtags (but no labels).\n"
        "Don't critique — directly return a better, more refined post."
    ),
    llm_fn=call_llm
)



task1 = Task("read", reader, "Read the transcript and find the best story.")
task2 = Task("write_post", writer, "Write the LinkedIn post based on that story.")
task3 = Task("review_post", reviewer, "Polish the LinkedIn post to improve clarity and tone. Return ONLY the final post without explanations or edit summaries.")

crew = Crew(
    agents=[reader, writer, reviewer],
    tasks=[task1, task2, task3],
    verbose=True
)

def generate_post(transcript):
    try:
        print("🚀 Running full crew pipeline...")
        print("📥 Received transcript:", transcript[:200])
        final_output = run_crew(transcript)
        print("✅ Final polished post:", final_output)
        return final_output
    except Exception as e:
        print("❌ Error in generate_post:", e)
        return "Error: Something went wrong."




@app.route("/", methods=["GET"])
def index():
    return "✅ API is live. Use POST to submit a transcript."

@app.route("/generate", methods=["POST"])
def handle_transcript():
    if "transcript" not in request.files:
        return jsonify({"error": "❌ No file uploaded"}), 400

    file = request.files["transcript"]
    if file.filename == "":
        return jsonify({"error": "❌ Empty file name"}), 400

    try:
        transcript = file.read().decode("utf-8")
        post = generate_post(transcript)
        if post:
            return jsonify({"post": post})
        else:
            return jsonify({"error": "❌ Something went wrong while generating the post."}), 500
    except Exception as e:
        print("❌ Exception during file handling:", e)
        return  jsonify({"error": "❌ Server error."}), 500

if __name__ == "__main__":
    app.run(debug=True)





