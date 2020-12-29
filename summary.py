from .utils import (nlp,
                  find_sentences,
                  sanitize_for_model,
                  sanitize_original,
                  get_TFIDF,
                  load_data,
                  write_data)
import numpy as np
import time



FOLDER = 'test-2'

def get_summary(data, debug = False, folder = False, THRESHOLD = 1):

    if debug:
        start = time.time()

    if folder:
        text = load_data(data)
    else:
        text = data
    doc = nlp(text)

    sentences = np.array([sanitize_original(sent.text) for sent in doc.sents])
    sentences_for_tfidf = sanitize_for_model(sentences)


    res = get_TFIDF(sentences_for_tfidf)

    summary = sentences[find_sentences(res, THRESHOLD)].tolist()
    if debug:
        time_taken = time.time() - start

        output = {
            'summary': summary,
            'total_lines': len(sentences),
            'compressed_percent': round((len(summary) / len(sentences)) * 100, 2),
            'threshold_used': THRESHOLD,
            'time_taken': time_taken,
        }
        if folder:
            write_data(data, output)
            return f'Data written to data/{FOLDER}/out.json'
        return output

    else:
        return summary
