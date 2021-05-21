from nltk.tokenize import sent_tokenize, word_tokenize
from itertools import chain
from argparse import ArgumentParser, RawTextHelpFormatter
import numpy as np

MSG_DESCRIPTION = "Summarize text of a given file."


def createInputMatrixAndSVD(sents):
    words = set(chain.from_iterable(sents))
    word_index = {word: k for k, word in enumerate(words)}

    num_words = len(word_index)
    num_sents = len(sents)
    # Input Matrix Creation
    X = np.zeros((num_words, num_sents))
    for d, sent in enumerate(sents):
        for word in sent:
            w = word_index[word]
            X[w, d] += 1
    # Singular Value Decomposition (SVD)
    U, S, Vt = np.linalg.svd(X)
    V = Vt.transpose()
    return U, S, Vt, V, num_sents


def tokenizeSentences(text):
    return [word_tokenize(i) for i in sent_tokenize(text)]


def SteinbergerAndJezek(sigma, V, K, N, sents, c):
    sk = []
    for k in range(K):
        sum_ = 0
        for i in range(c):
            sum_ += (V[k][i]) ** 2 * (sigma[i]) ** 2

        sk += [(np.sqrt(sum_), k)]

    sk_sorted = sorted(sk, key=lambda x: -x[0])

    index = [i[1] for i in sk_sorted[0:N]]

    for i in sorted(index):
        print(" ".join(sents[i]))


def CrossMethod(Vt, N, sents, c):
    # Pre processing step
    Vt = np.abs(Vt)
    avgs = []
    for concept in Vt:
        avgs += [np.mean(concept)]

    for i in range(c):
        for j in range(len(Vt[i])):
            Vt[i][j] = Vt[i][j] if Vt[i][j] > avgs[i] else 0

    # length of sentences = sum of Vt collumns
    l = Vt.sum(axis=0)

    length = []
    for i in range(len(l)):
        length += [(l[i], i)]

    length_sorted = sorted(length, key=lambda x: -x[0])
    index = [i[1] for i in length_sorted[0:N]]

    # using sorted to keep the original text order
    for i in sorted(index):
        print(" ".join(sents[i]))


if __name__ == "__main__":

    parser = ArgumentParser(
        description=MSG_DESCRIPTION, formatter_class=RawTextHelpFormatter
    )
    parser.add_argument("file", help="File containing the text to be summarized.")
    parser.add_argument(
        "method",
        help="""Method to summarize (default: 0):\n\t0: Steinberg and Jezek;\n\t1: Murray""",
        choices=[0, 1],
        type=int,
        default=0,
        nargs="?",
    )
    parser.add_argument(
        "number_sentences",
        help="number of sentences on the summary (default: 3)",
        type=int,
        default=3,
        nargs="?",
    )

    parser.add_argument(
        "number_concepts",
        help="number of concepts (default: max)",
        type=int,
        default=-1,
        nargs="?",
    )

    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        text = f.read()

    sents = tokenizeSentences(text)

    U, S, Vt, V, num_sents = createInputMatrixAndSVD(sents)

    if args.number_concepts == -1 or args.number_concepts > len(Vt):
        c = len(Vt)
    else:
        c = args.number_concepts

    if args.method:
        CrossMethod(Vt, args.number_sentences, sents, c)
    else:
        SteinbergerAndJezek(S, V, num_sents, args.number_sentences, sents, c)
