#! /usr/bin/env python
import os
from collections import Counter

from bottle import TEMPLATE_PATH, Bottle, run, static_file, request
from bottle import jinja2_template as template

def count_kmers(sequence, k):
    """
    Given a sequence S, return a dictionary of 
    each kmer of size k and the number of times 
    the kmer occurs in S.
    
    This function is case insensitive.
    
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
    kmer_counts = Counter()
    
    # grab each, overlapping kmer of size k, while
    # being careful to not go beyond the end of the sequence.
    for i in xrange((len(sequence) - k) + 1):
        kmer = sequence[i:i+k]
        kmer_counts[kmer] += 1

    return kmer_counts


# create a new Bottle app instance
app = Bottle()

# add the views directory to Bottle's list of directories in which
# to search for HTML templates.
base_dir = os.path.dirname(__file__)
TEMPLATE_PATH.append(os.path.abspath(os.path.join(base_dir, 'views' )))

# serve static files, such as Bootstrap's CSS
# expects file to be located in static 
static_folder = 'static'
_static_folder = os.path.join( os.path.dirname(__file__), static_folder)
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=_static_folder)

# Bind "http://localhost:8088/" to the index function below.
# This is the key concept behind Bottle.  URLs are explicitly
# bound to Python functions.  When you navigate to that URL,
# Bottle will execute the function.
@app.route('/', method='GET')
def index():
    """
    This function will be called when navigating to:
    http://localhost:8088/.
    
    This function:
    1. Extracts the sequence and k values from the form using
       the request.GET.get() functions.
    2. Calls count_kmers() (see above) to count the kmers
    3. Sends the kmer_counts dictionary to the index.html
       Jinja template.  The Jinja-ed Python code in the template 
       processes the kmer_counts and prints to the web page
       as an HTML table.
    """
    # the user clicked the "submit" button
    if request.GET.get('submit','').strip():

        # retrieve the values in the web form
        seq = request.GET.get('seq', '').strip()
        k   = str(request.GET.get('k', '').strip())

        # ignore if the user did not enter a sequence or a k
        # before clicking the submit button
        if len(seq) == 0 or len(k) == 0: 
            return template('index')
        
        # count the kmers in the sequence
        kmer_counts = count_kmers(seq, int(k))
        
        # send the kmer counts to the web page
        return template('index', kmer_counts=kmer_counts, seq=seq, k=k)
                                 
    # nothing has happened.  just serve a page with no results.
    else:
        return template('index')


run(app, host='localhost', port=8088, reloader=True)
