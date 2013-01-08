#! /usr/bin/env python
import os
from collections import Counter

from bottle import TEMPLATE_PATH, Bottle, run, static_file, request
from bottle import jinja2_template as template

def count_kmers(sequence, k):
    """
    Given a sequence S, return each kmer of size k
    and the number of times the kmer occurs in S.
    
    This function is case insentive.
    
    >>> kmer_counts = count_kmers('actgtgtac', 2)
    >>> for kmer in kmer_counts:
    >>>>    print kmer, kmer_counts[kmer]
    tg 2
    ac 2
    gt 2
    ta 1
    ct 1
    """
    sequence = sequence.lower()
    # be careful to not go beyond the end of the sequence.
    kmer_counts = Counter()
    for i in xrange((len(sequence) - k) + 1):
        kmer = sequence[i:i+k]
        kmer_counts[kmer] += 1

    return kmer_counts



base_dir = os.path.dirname(__file__)
TEMPLATE_PATH.append(os.path.abspath(os.path.join(base_dir, 'views' )))


app = Bottle()


# -- serve static files, files located in static 
static_folder = 'static'
_static_folder = os.path.join( os.path.dirname(__file__), static_folder)
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=_static_folder)




@app.route('/', method='GET')
def index():

    # the user clicked the "submit" button
    if request.GET.get('submit','').strip():

        # retrieve the values in the web form
        sequence = request.GET.get('sequence', '').strip()
        k        = str(request.GET.get('k', '').strip())

        # ignore if the user did not enter a sequence or a k
        # before clicking the submit button
        if len(sequence) == 0 or len(k) == 0: 
            return template('index')
        
        # count the kmers in the sequence
        kmer_counts = count_kmers(sequence, int(k))
        
        # send the kmer counts to the web page
        return template('index', kmer_counts=kmer_counts,
                                 sequence=sequence,
                                 k=k)
    else:
        return template('index')


run(app, host='localhost', port=8088, reloader=True)