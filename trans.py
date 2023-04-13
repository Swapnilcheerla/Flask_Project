from flask import Flask, render_template, request
from main1 import *
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("cindex.html")


@app.route("/", methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        input = request.form.get("input_text")
        selected_lang = request.form.get("selected_language", None)
        if selected_lang is not None:
            lang = selected_lang
            translate = do_translate(input, selected_lang)
            sentiment = do_sentiment_analysis(input)
            # pospeech = detect_pos(input)
            # detect_ent = detect_entity(input)
            # label = generate_detect_label

        return render_template("cindex.html", input=input, lang=lang, translate=translate, sentiment=sentiment)


if __name__ == "__main__":
    app.run(debug=True)
