from nltk.tokenize import sent_tokenize, word_tokenize
from itertools import chain
from argparse import ArgumentParser, RawTextHelpFormatter
import numpy as np

MSG_DESCRIPTION = "Summarize text of a given file."


def tokenizeSentences(text):
    return [word_tokenize(i) for i in sent_tokenize(text)]


def SteinbergerAndJezek(sigma, v, K, N):
    sk = []

    for k in range(K):
        sum_ = 0
        for i in range(len(V[k])):
            sum_ += (V[k][i]) ** 2 * (sigma[i]) ** 2

        sk += [(np.sqrt(sum_), k)]

    sk_sorted = sorted(sk, key=lambda x: -x[0])

    index = [i[1] for i in sk_sorted[0:N]]

    for i in index:
        print(" ".join(sents[i]))


def Murray():
    return


if __name__ == "__main__":

    parser = ArgumentParser(
        description=MSG_DESCRIPTION, formatter_class=RawTextHelpFormatter
    )
    parser.add_argument("file", help="File containing the text to be summarized.")
    parser.add_argument(
        "method",
        help="""Method to summarize:\n\t0: Steinberg and Jezek;\n\t1: Murray""",
        choices=[0, 1],
        type=int,
    )
    parser.add_argument(
        "number_sentences", help="number of sentences on the summaty", type=int
    )

    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        text = f.read()

    sents = tokenizeSentences(text)

    words = set(chain.from_iterable(sents))
    word_index = {word: k for k, word in enumerate(words)}

    num_words = len(word_index)
    num_sents = len(sents)

    X = np.zeros((num_words, num_sents))
    for d, sent in enumerate(sents):
        for word in sent:
            w = word_index[word]
            X[w, d] += 1

    U, S, Vt = np.linalg.svd(X)
    V = Vt.transpose()

    if args.method:
        Murray()
    else:
        SteinbergerAndJezek(S, V, num_sents, args.number_sentences)
