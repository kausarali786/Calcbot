import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random

words = []
classes = []
documents = []
ignore_words = ['?', '!']
data_file = open('../modal/intents.json').read()
intents = json.loads(data_file)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # take each word and tokenize it
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # adding documents
        documents.append((w, intent['tag']))

        # adding classes to our class list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

print(len(documents), "documents")
print(len(classes), "classes", classes)
print(len(words), "unique lemmatized words", words)

pickle.dump(words, open('../modal/words.pkl', 'wb'))
pickle.dump(classes, open('../modal/classes.pkl', 'wb'))

# initializing training data
training = []
output_empty = [0] * len(classes)
for doc in documents:
    # initializing bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # create our bag of words array with 1, if word match found in current pattern
    bag = [1 if w in pattern_words else 0 for w in words]

    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = [0] * len(classes)
    output_row[classes.index(doc[1])] = 1

    # Check the lengths
    if len(bag) != len(words):
        print(f"Bag length error: {len(bag)} != {len(words)}")
    if len(output_row) != len(classes):
        print(f"Output row length error: {len(output_row)} != {len(classes)}")

    training.append([bag, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)

# Separate the training data into X and y
train_x = np.array([entry[0] for entry in training])
train_y = np.array([entry[1] for entry in training])

print("Training data created")

# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
# model = Sequential()
# model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(64, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(len(train_y[0]), activation='softmax'))

from tensorflow.keras.optimizers import Adam

# Create model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model with Adam optimizer
model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])

# Train model
hist = model.fit(train_x, train_y, epochs=200, batch_size=32, validation_split=0.2, verbose=1)
model.save('../modal/chatbot_model.h5', hist)

print("model created")
