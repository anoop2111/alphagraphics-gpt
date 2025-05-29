from flask import Flask, request, jsonify, render_template_string
import requests
from bs4 import BeautifulSoup
import openai
import os

# Set your OpenAI API key here or use an environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY", "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")




app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>AlphaGraphics GPT Tool</title></head>
<body>
  <h2>AlphaGraphics GPT Competitive Content Tool</h2>
  <form method="post">
    <label>Enter Competitor URL:</label><br>
    <input name="url" style="width:400px"/><br><br>
    <button type="submit">Analyze & Rewrite</button>
  </form>
  {% if original %}
    <h3>Original Content (from URL):</h3>
    <p>{{ original }}</p>
    <h3>Summarized:</h3>
    <p>{{ summary }}</p>
    <h3>Rewritten (AlphaGraphics-Style):</h3>
    <p>{{ rewritten }}</p>
    <h3>Suggested Google Post Headlines:</h3>
    <ul>{% for h in headlines %}<li>{{ h }}</li>{% endfor %}</ul>
    <h3>Offer Ideas:</h3>
    <ul>{% for o in offers %}<li>{{ o }}</li>{% endfor %}</ul>
  {% endif %}
</body>
</html>
'''

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

def gpt(prompt, temperature=0.7, max_tokens=500):

    response = openai.chat.completions.create(sss
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response['choices'][0]['message']['content'].strip()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        text = extract_text_from_url(url)[:3000]  # Limit to avoid overload

        summary = gpt(f"Summarize the following in 100 words:\n{text}")
        rewritten = gpt(f"Rewrite this for AlphaGraphics Carrollton in a friendly, persuasive, local-business tone:\n{summary}")
        headlines = gpt("Give 5 Google My Business post headlines based on this:\n" + summary).split("\n")
        offers = gpt("Suggest 5 promotional offers or campaign ideas for AlphaGraphics based on this:\n" + summary).split("\n")

        return render_template_string(
            HTML_TEMPLATE,
            original=text,
            summary=summary,
            rewritten=rewritten,
            headlines=headlines,
            offers=offers
        )
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

