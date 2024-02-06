import pickle
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

dataset_folder = 'all_PreprocessedTextFiles'

def preprocess(filename):
    with open(os.path.join(dataset_folder, filename), 'r', encoding='latin1', errors='replace') as f:
        text = f.read()
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    tokens = [w for w in tokens if w.isalpha() or '-' in w]
    tokens = [w for w in tokens if w.strip()]
    return tokens

positional_index = {}

for filename in os.listdir(dataset_folder):
    tokens = preprocess(filename)
    for i, token in enumerate(tokens):
        if token in positional_index:
            if filename in positional_index[token]:
                positional_index[token][filename].append(i)
            else:
                positional_index[token][filename] = [i]
        else:
            positional_index[token] = {filename: [i]}

output_folder = './'
positional_file_path = os.path.join(output_folder, 'positional.pickle')

with open(positional_file_path, 'wb') as f:
    pickle.dump(positional_index, f)

def positional_query(query, positional_index):
    query = query.lower()
    tokens = word_tokenize(query)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    tokens = [w for w in tokens if w.isalpha() or '-' in w]
    tokens = [w for w in tokens if w.strip()]

    result = set()

    for token in tokens:
        if token in positional_index:
            if not result:
                result = set(positional_index[token])
            else:
                result = result.intersection(positional_index[token])

    result = list(result)
    result.sort()
    return result

def main():
    with open(positional_file_path, 'rb') as f:
        db = pickle.load(f)

    n = int(input("Enter the number of queries: "))
    queries = []
    for j in range(n):
        s = input("Enter query {}: ".format(j+1))
        queries.append(s)

    for i in range(n):
        query_result = positional_query(queries[i], db)
        print("Number of documents retrieved for query {} using positional index: {}".format(i+1, len(query_result)))
        print("Names of documents retrieved for query {} using positional index: {}".format(i+1, query_result))

if __name__ == "__main__":
    main()
