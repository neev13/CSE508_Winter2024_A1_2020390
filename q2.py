import os
import pickle
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

stopwords_path = 'stopwords.txt'
dataset_path = 'all_PreprocessedTextFiles'

def read_stopwords(file_path):
    with open(file_path, 'r') as file:
        stopwords_list = file.read().splitlines()
    return set(stopwords_list)

def create_inverted_index(dataset_path, stop_words):
    inverted_index = {}
    total_docs = 0

    for filename in os.listdir(dataset_path):
        with open(os.path.join(dataset_path, filename), 'r', encoding='utf-8', errors='replace') as file:
            terms = word_tokenize(file.read())
            terms = [term.lower() for term in terms if term.isalpha() and term not in stop_words]

            for term in terms:
                if term not in inverted_index:
                    inverted_index[term] = [[filename], 1]
                else:
                    if filename not in inverted_index[term][0]:
                        inverted_index[term][0].append(filename)
                        inverted_index[term][1] += 1

        total_docs += 1

    return inverted_index, total_docs

def get_posting_list(term, inverted_index):
    if term in inverted_index:
        return inverted_index[term][0]
    else:
        return []

def get_posting_listsize(term, inverted_index):
    if term in inverted_index:
        return inverted_index[term][1]
    else:
        return 0

def and_query(term1, term2, inverted_index):
    posting_list1 = get_posting_list(term1, inverted_index)
    posting_list2 = get_posting_list(term2, inverted_index)
    posting_list1_size = get_posting_listsize(term1, inverted_index)
    posting_list2_size = get_posting_listsize(term2, inverted_index)
    return and_query_helper(posting_list1, posting_list1_size, posting_list2, posting_list2_size)

def and_query_helper(posting_list1, size1, posting_list2, size2):
    result = []
    count = 0
    i = 0
    j = 0

    while i < size1 and j < size2:
        count += 1
        if posting_list1[i] == posting_list2[j]:
            result.append(posting_list1[i])
            i += 1
            j += 1
        elif posting_list1[i] < posting_list2[j]:
            i += 1
        else:
            j += 1

    return result, count

def and_not_query(term1, term2, inverted_index):
    posting_list1 = get_posting_list(term1, inverted_index)
    posting_list2 = get_posting_list(term2, inverted_index)
    posting_list1_size = get_posting_listsize(term1, inverted_index)
    posting_list2_size = get_posting_listsize(term2, inverted_index)
    return and_not_query_helper(posting_list1, posting_list1_size, posting_list2, posting_list2_size)

def and_not_query_helper(posting_list1, size1, posting_list2, size2):
    result = []
    count = 0
    i = 0
    j = 0

    while i < size1 and j < size2:
        count += 1
        if posting_list1[i] == posting_list2[j]:
            i += 1
            j += 1
        elif posting_list1[i] < posting_list2[j]:
            result.append(posting_list1[i])
            i += 1
        else:
            j += 1

    while i < size1:
        count += 1
        result.append(posting_list1[i])
        i += 1

    return result, count

def or_query(term1, term2, inverted_index):
    posting_list1 = get_posting_list(term1, inverted_index)
    posting_list2 = get_posting_list(term2, inverted_index)
    posting_list1_size = get_posting_listsize(term1, inverted_index)
    posting_list2_size = get_posting_listsize(term2, inverted_index)
    return or_query_helper(posting_list1, posting_list1_size, posting_list2, posting_list2_size)

def or_query_helper(posting_list1, size1, posting_list2, size2):
    result = []
    count = 0
    i = 0
    j = 0

    while i < size1 and j < size2:
        count += 1
        if posting_list1[i] == posting_list2[j]:
            result.append(posting_list1[i])
            i += 1
            j += 1
        elif posting_list1[i] < posting_list2[j]:
            result.append(posting_list1[i])
            i += 1
        else:
            result.append(posting_list2[j])
            j += 1

    while i < size1:
        count += 1
        result.append(posting_list1[i])
        i += 1

    while j < size2:
        count += 1
        result.append(posting_list2[j])
        j += 1

    return result, count

def or_not_query(term1, term2, inverted_index, all_docs):
    posting_list1 = get_posting_list(term1, inverted_index)
    posting_list2 = get_posting_list(term2, inverted_index)
    posting_list1_size = get_posting_listsize(term1, inverted_index)
    posting_list2_size = get_posting_listsize(term2, inverted_index)
    return or_not_query_helper(posting_list1, posting_list1_size, posting_list2, posting_list2_size, all_docs)

def or_not_query_helper(posting_list1, size1, posting_list2, size2, all_docs):
    result = []
    count = 0
    i = 0
    j = 0
    diff = list(set(all_docs) - set(posting_list2))
    result, count = or_query_helper(posting_list1, size1, diff, len(diff))
    return result, count

def main():
    dataset_path = 'all_PreprocessedTextFiles'
    stopwords_file = 'stopwords.txt'
    with open(stopwords_file, 'r', encoding='utf-8') as stop_file:
        stop_words = set(word.strip() for word in stop_file)

    inverted_index, total_docs = create_inverted_index(dataset_path, stop_words)
    n = int(input("Enter the number of queries: "))
    for _ in range(n):
        input_sequence = input("Enter the input sequence: ")
        operations = input("Enter the operations (comma-separated): ")

        query = input_sequence.lower()
        tokens = word_tokenize(query)
        tokens = [w.lower() for w in tokens if w.isalpha() and w not in stop_words]
        query = set(tokens)

        ops = operations.split(',')
        result = get_posting_list(next(iter(query)), inverted_index)
        size = get_posting_listsize(next(iter(query)), inverted_index)

        for term, op in zip(list(query)[1:], ops):
            if op == 'AND':
                result, count = and_query_helper(result, size, get_posting_list(term, inverted_index),
                                                 get_posting_listsize(term, inverted_index))
            elif op == 'OR':
                result, count = or_query_helper(result, size, get_posting_list(term, inverted_index),
                                                get_posting_listsize(term, inverted_index))
            elif op == 'AND NOT':
                result, count = and_not_query_helper(result, size, get_posting_list(term, inverted_index),
                                                     get_posting_listsize(term, inverted_index))
            elif op == 'OR NOT':
                result, count = or_not_query_helper(result, size, get_posting_list(term, inverted_index),
                                                    get_posting_listsize(term, inverted_index), all_docs)

            size = len(result)

        print("\nQuery:", ' '.join([f"{term} {ops[i - 1]}" for i, term in enumerate(query)]))
        print("Number of documents retrieved:", len(result))
        print("Names of the documents retrieved:", result)

if __name__ == "__main__":
    main()