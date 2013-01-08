This is a simple demonstration of combining bottle.py with Twitter Boostrap
for exposing Python code as web applications.

Installation
============
1. First install bottle.py::

    pip install bottle
	
2. Now clone this repository and navigate to the source directory::

	git clone git://github.com/arq5x/toy_bottle_bootstrap_app.git
	cd toy_bottle_bootstrap_app	


Usage
============
1. From the `toy_bottle_bootstrap_app` directory, fire up the web app::
   
    python kmer-browser.py
	
2. Open a web browser to http://localhost:8088/

If you enter 'gattaca' as the sequence and '2' as the kmer size, 
you should see something like:

    .. image:: https://raw.github.com/arq5x/toy_bottle_bootstrap_app/master/app.png