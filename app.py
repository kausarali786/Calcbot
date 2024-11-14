from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from tensorflow.keras.models import load_model
import json
import random
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

lemmatizer = WordNetLemmatizer()
model = load_model('./modal/chatbot_model.h5')
intents = json.loads(open('./modal/intents.json').read())
words = pickle.load(open('./modal/words.pkl', 'rb'))
classes = pickle.load(open('./modal/classes.pkl', 'rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"Found in bag: {w}")
    return np.array(bag)


def predict_class(sentence):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def get_response(ints, intents_json):
    if not ints:
        return "I'm sorry, I didn't understand that."
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(msg):
    ints = predict_class(msg)
    res = get_response(ints, intents)
    return res


class Chat(Resource):
    def post(self):
        try:
            user_input = request.json.get('message')

            if not user_input:
                return {"error": "No input provided"}, 400

            response = chatbot_response(user_input)

            return jsonify({
                'status': 'success',
                'response': response
            })

        except Exception as e:
            return {"error": str(e)}, 500


api.add_resource(Chat, '/chat')

if __name__ == "__main__":
    app.run(debug=True)
