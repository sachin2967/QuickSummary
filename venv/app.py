from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        API_TOKEN = "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"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

        def query(payload):
            data = json.dumps(payload)
            response = requests.request("POST", API_URL, headers=headers, data=data)
            return response.json()

        
        maxL = int(request.form.get('maxL'))
        text = request.form.get('text')
        minL=maxL//4

        if minL is None:
            minL = 30
        if maxL is None:
            maxL = 100

        data = query(
            {
                "inputs": text,
                "parameters": {"min_length": minL, "max_length": maxL},
            }
        )
        summary_text = data[0]["summary_text"]
        return render_template('index.html', data=summary_text)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

