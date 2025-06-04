import tensorflow as tf
from utils.conllu import read_conllu_dataset
from utils.data import Dataset
import numpy as np
import joblib

train_sentences = read_conllu_dataset("data/ro_rrt-ud-train.conllu")

dataset_dl = Dataset()
dataset_dl.fit(train_sentences, mode="chars", categorical_y=True)

dataset_hmm = Dataset()
dataset_hmm.fit(train_sentences, mode="word_id", categorical_y=False)

#print(dataset_hmm.word2id)

def predict_dl_fun(model):
    def predict_dl(sentences):
        X = dataset_dl.encode_x(sentences)
        y_pred = model([X])
        y_pred = y_pred[0]  # Get the first (and only) sentence prediction
        y_pred = np.argmax(y_pred, axis=-1)[:len(sentences[0])]
        y_pred = [dataset_dl.labels[i] for i in y_pred]
        return y_pred
    return predict_dl

def predict_hmm_fun(model_path="models/pos_hmm_model.joblib", mapping_path="models/pos_hmm_mappings.joblib"):
    model = joblib.load(model_path)
    mappings = joblib.load(mapping_path)
    
    def predict_hmm(sentences):
        # Convert words to IDs using the same mapping as during training
        word_ids = []
        for word, _ in sentences[0]:  # We only handle one sentence at a time
            word_id = mappings['word2id'].get(word, mappings['word2id'].get('UNK', 0))
            word_ids.append(word_id)
            
        # Reshape for HMM
        X = np.array(word_ids).reshape(-1, 1)
        lengths = [len(word_ids)]
        
        # Get predictions
        predicted_tags = model.decode(X, lengths)[1]
        
        # Convert tag IDs back to tag names
        return [mappings['id2label'][tag_id] for tag_id in predicted_tags]
    
    return predict_hmm


algorithms = {
    "lstm": predict_dl_fun(tf.keras.models.load_model("pos_lstm_model.keras")),
    "cnn1d": predict_dl_fun(tf.keras.models.load_model("pos_cnn1d_model.keras")),
    "hmm": predict_hmm_fun(),
}


def prepare_sentence(sentence: str):
    import re
    tokens = re.findall(r"\w+|[^\w\s]", sentence.strip())
    sentence = [(word, "X") for word in tokens]  # Assign a dummy UPOS tag
    return [sentence]


def inference(model_name:str, sentence:str):
    sentence = prepare_sentence(sentence)
    return algorithms[model_name](sentence)

def main():
    while True:
        user_input = input("Enter model name and sentence (e.g., 'lstm This is my sentence.'): ")
        if not user_input.strip():
            continue
        parts = user_input.split(maxsplit=1)
        if len(parts) < 2:
            print("Please provide a model name and a sentence.")
            continue
        model_name, sentence = parts[0], parts[1]
        
        if model_name not in algorithms:
            print(f"Model '{model_name}' not found. Available models: {list(algorithms.keys())}")
            continue
        
        predictions = inference(model_name, sentence)
        print(f"Predictions for '{sentence}': {predictions}")

main()
