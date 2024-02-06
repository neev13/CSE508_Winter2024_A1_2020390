import os
import re
import string

def preprocess_text(text):
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)
    tokens = [token for token in tokens if token not in stopwords]
    tokens = [token for token in tokens if token not in string.punctuation]
    tokens = [token for token in tokens if token.strip() != '']
    return tokens

with open("stopwords.txt", 'r') as stopword_file:
    stopwords = stopword_file.read().splitlines()

preprocessed_folder = "all_PreprocessedTextFiles"
if not os.path.exists(preprocessed_folder):
    os.makedirs(preprocessed_folder)

a=0
b=0
text_files_folder = "all_TextFiles"
for filename in os.listdir(text_files_folder):
    if filename == "stopwords.txt":
        continue
    if filename.endswith(".txt"):
        file_path = os.path.join(text_files_folder, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            if(a<251):
                print(f"Before preprocessing - {filename}:\n{content}\n")
                a+=50

            tokens = preprocess_text(content)

            if(b<251):
                print(f"After preprocessing - {filename}:\n{' '.join(tokens)}\n")
                b+=50

            preprocessed_path = os.path.join(preprocessed_folder, f"preprocessed_{filename}")
            with open(preprocessed_path, 'w', encoding='utf-8') as output_file:
                output_file.write(' '.join(tokens))