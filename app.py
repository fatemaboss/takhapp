from flask import Flask, request, send_file, render_template_string
import json, io, os, sys

app = Flask(__name__)

# Read the HTML template
HTML_PATH = os.path.join(os.path.dirname(__file__), 'index.html')

@app.route('/')
def index():
    with open(HTML_PATH) as f:
        return f.read()

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    its = data.get('its', 'form')

    # Import and call the generator
    from generate_pdf import generate_pdf
    out_path = f'/tmp/Misaaq_Takhmeen_{its}.pdf'
    generate_pdf(data, out_path)

    return send_file(
        out_path,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Misaaq_Takhmeen_{its}.pdf'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
