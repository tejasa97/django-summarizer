from utils import (nlp,
                  find_sentences,
                  sanitize_for_model,
                  sanitize_original,
                  get_TFIDF,
                  load_data,
                  write_data)
import numpy as np
import time

"""
TODOS:
1. Convert this into a FastAPI API.
2. Test the algorithm better.
3. Better sanitization of text.
4. Figure out `threshold` for effective summarization.
5. Make it more effecient.
"""

FOLDER = 'test-2'
text = load_data(FOLDER)
start = time.time()
doc = nlp(text)

sentences = np.array([sanitize_original(sent.text) for sent in doc.sents])
sentences_for_tfidf = sanitize_for_model(sentences)


res = get_TFIDF(sentences_for_tfidf)
THRESHOLD = 1

summary = sentences[find_sentences(res, THRESHOLD)].tolist()
time_taken = time.time() - start

output = {
    'summary': summary,
    'time_taken': time_taken,
    'total_lines': len(sentences),
    'compressed_percent': round((len(summary) / len(sentences)) * 100, 2),
    'threshold_used': THRESHOLD
}
write_data('test-2', FOLDER)
