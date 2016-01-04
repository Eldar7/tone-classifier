#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from psycopg2 import connect
from pymystem3 import Mystem
from inspect import getsourcefile
from os.path import abspath, dirname
import vec

sys.path.insert(0, dirname(abspath(getsourcefile(lambda:0))) + '/../aux')
from vocs import TermVocabulary, DocVocabulary
from features import Features
from msg import Message
import pconf
import twits
import prob
import json

argc = len(sys.argv)
if (argc == 1):
    print """%s\n%s\n%s\n%s\n%s\n%s"""%(
        "Usage: baseline_bank <database> <train_table> <output>",
        "<task> -- task type",
        "<database> -- database to connect for training data",
        "<train_table> -- table with training data for bank",
        "<vocabulary> -- vocabulary",
        "<output> -- file to save tonality vectors")
    exit(0)

arguments = {'task_type' : sys.argv[1], 'database' : sys.argv[2],
    'train_table' : sys.argv[3], 'vocabulary' : sys.argv[4],
    'output' : sys.argv[5]
}

# Initialize config files
with open("conn.conf", "r") as f:
    conn_config = json.load(f, encoding='utf-8')

features = Features("features.conf")

# Connect to a database
connSettings = "dbname=%s user=%s password=%s host=%s"%( arguments['database'],
    conn_config["user"], conn_config["password"], conn_config["host"])

conn = connect(connSettings)
cursor = conn.cursor()

# make a term vocabulary
mystem = Mystem(entire_input=False)
term_voc = TermVocabulary(arguments['vocabulary'])
doc_voc = DocVocabulary()
problem = []
limit = sys.maxint # no limits
vectors = []
for score in [-1, 0, 1]:
    # getting twits with the same score
    twits.get(arguments['task_type'], cursor,
        arguments['train_table'], score, limit)
    # processing twits
    row = twits.next_row(cursor, score, 'train')
    count = 0
    while row is not None:
        text = row[0]
        index = row[1]

        message = Message(text=text, mystem=mystem, configpath="msg.conf")
        message.process()
        terms = message.get_terms()
        # feature: name: value
        doc_voc.add_doc(terms)
        vectors.append( { 'score': score, 'terms' : terms,
            'features': features.create(terms) } )
        # next row
        row = twits.next_row(cursor, score, 'train')
        count += 1

    print "class %d: %d"%(score, count)

# make problem
for vector in vectors:
    problem.append(vec.train_vector(vector['score'],
        term_voc, doc_voc, vector['terms'], vector['features']))

#save problem
prob.save(problem, arguments['output'])
