from flask import Flask, render_template_string, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

# The HTML content for your UI
html_content = """
<!DOCTYPE html>
<html>
<head><title>AI Translator</title></head>
<body style="font-family: sans-serif; padding: 40px;">
    <h2>CodeAlpha AI Translator</h2>
    <textarea id="text" style="width:100%; height:100px;"></textarea><br>
    <select id="lang">
        <option value="es">Spanish</option>
        <option value="fr">French</option>
        <option value="hi">Hindi</option>
    </select>
    <button onclick="translate()">Translate</button>
    <div id="result" style="margin-top:20px; padding:10px; background:#eee;"></div>
    <script>
        async function translate() {
            const text = document.getElementById('text').value;
            const target_lang = document.getElementById('lang').value;
            const res = await fetch('/translate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text, target_lang})
            });
            const data = await res.json();
            document.getElementById('result').innerText = data.translated_text;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_content)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    # Stability fix for current environment
    temp_translator = Translator()
    translation = temp_translator.translate(data['text'], dest=data['target_lang'])
    return jsonify({'translated_text': translation.text})

if __name__ == '__main__':
    app.run(debug=True)