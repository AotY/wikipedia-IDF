import logging
import json
import re
import os
import sys
import math
import csv
import nltk
import jieba
from opencc import OpenCC
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from bz2 import BZ2File
from multiprocessing import Pool
from argparse import ArgumentParser
from collections import Counter

DROP_TOKEN_RE = re.compile("^\W*$")

nltk.download("punkt")
parser = ArgumentParser()
parser.add_argument("-i", "--input", required=True,
                    type=str,  help="data dir")

parser.add_argument("-lang", "--language", type=str)

parser.add_argument("-s", "--stem", action='store_true')

parser.add_argument("-o", "--output", metavar="OUT_BASE",
                    required=True, help="Output CSV files base")

parser.add_argument("-l", "--limit", metavar="LIMIT",
                    type=int, help="Stop after reading LIMIT articles.")

parser.add_argument("-c", "--cpus", default=1, type=int,
                    help="Number of CPUs to employ.")

args = parser.parse_args()
if args.language == 'chinese':
    cc = OpenCC('t2s')

def filter_tokens(tokens):
    for t in tokens:
        if not DROP_TOKEN_RE.match(t):
            yield t.lower()


def stem(tokens):
    global stemmer
    stems = []
    token_to_stem_mapping = dict()

    for t in tokens:
        s = stemmer.stem(t)
        stems.append(s)
        if s not in token_to_stem_mapping:
            token_to_stem_mapping[s] = Counter()
        token_to_stem_mapping[s][t] += 1

    return set(stems), token_to_stem_mapping


def get_file_reader(filename):
    if filename.endswith(".bz2"):
        return BZ2File(filename)
    else:
        return open(filename)


def get_lines(data_dir):
    print('data_dir: ', data_dir)
    bz_dirs = os.listdir(data_dir)
    if bz_dirs[0].endswith('.bz2'):
        for filename in bz_dirs:
            file_path = os.path.join(data_dir, filename)
            with get_file_reader(file_path) as f:
                for line in f:
                    yield line
    else:
        for bz_dir in bz_dirs:
            bz_dir_path = os.path.join(data_dir, bz_dir)
            for filename in os.listdir(bz_dir_path):
                file_path = os.path.join(bz_dir_path, filename)
                with get_file_reader(file_path) as f:
                    for line in f:
                        yield line


def process_line(line):
    article_json = json.loads(line)
    if args.language == 'chinese':
        text = cc.convert(article_json["text"])
        tokens = list(jieba.cut(text))
        tokens = [token for token in tokens if len(token.split()) > 0]
    else:
        tokens = set(filter_tokens(word_tokenize(article_json["text"])))
    if args.stem:
        stems, token_to_stem_mapping = stem(tokens)
        return tokens, stems, token_to_stem_mapping
    else:
        return tokens, None, None


def main():
    global stemmer
    if args.stem and args.language in SnowballStemmer.languages:
        args.stem = True
    else:
        args.stem =False

    if args.stem:
        stemmer = SnowballStemmer(args.language)

    tokens_c = Counter()
    stems_c = Counter()
    token_to_stem_mapping = dict()
    articles = 0
    pool = Pool(processes=args.cpus)

    for tokens, stems, t_to_s_mapping in pool.imap_unordered(process_line, get_lines(args.input)):
        tokens_c.update(tokens)

        if args.stem:
            stems_c.update(stems)
            for token in t_to_s_mapping:
                if token not in token_to_stem_mapping:
                    token_to_stem_mapping[token] = Counter()
                token_to_stem_mapping[token].update(t_to_s_mapping[token])

        articles += 1
        if not (articles % 100):
            logging.info("Done %d articles.", articles)
        if articles == args.limit:
            break

    # 5761000
    pool.terminate()

    with open(os.path.join(args.output, "terms.csv"), "w") as o:
        w = csv.writer(o)
        w.writerow(("token", "frequency", "total", "idf"))
        for token, freq in tokens_c.most_common():
            w.writerow(
                [token, freq, articles, math.log(float(articles) / freq)])

    if args.stem:
        with open(os.path.join(args.output, "stems.csv"), "w") as o:
            w = csv.writer(o)
            w.writerow(("stem", "frequency", "total", "idf", "most_freq_term"))
            for s, freq in stems_c.most_common():
                w.writerow([s, freq, articles, math.log(
                    articles / (1.0 + freq)), token_to_stem_mapping[s].most_common(1)[0][0]])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
