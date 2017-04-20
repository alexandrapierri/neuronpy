# -*- coding: utf-8 -*-
"""Sage server customized for executing NEURON commands through a client/server
   interface.
   
   This code largely comes from the file: 
   sage/examples/ajax/simple_ajax_twisted_sage.py, by Alex Clemesha

   To execute from sage, 

   from neuronpy.server import neuronsageserver
   neuronsageserver.run()
"""
import os
from twisted.web2 import resource
from twisted.web2 import http_headers
from twisted.web2 import http
from twisted.web2 import channel
from twisted.web2 import server
from twisted.internet import reactor

from sage.interfaces import sage0

class Root(resource.Resource):

    addSlash = True

    def __init__(self):
        # Get the path to the module within the sage/python environment.
        neuronsageserver_path = os.path.dirname(__file__)
        with open(os.path.join(neuronsageserver_path,'sagetermTERM.html'), 'r') \
                as htmlfile:
            self.HTML = htmlfile.read()
        self.child_eval = EvalSomeSAGECode()

    def render(self, request):
        return http.Response(200, {'content-type': http_headers.MimeType( \
                'text', 'html')}, self.HTML) #'<html>empty</html>')

class EvalSomeSAGECode(resource.PostableResource):

    def render(self, request):
        code = request.args.get('code')[0]
        print code
        result = sage0.sage0.eval(code)
        print result
        return http.Response(200, {'content-type': http_headers.MimeType( \
                'text', 'html')}, result)

def run():
    site = server.Site(Root())
    factory = channel.HTTPFactory(site)
    reactor.listenTCP(8000, factory)
    print "\nOpen your browser to 'http://localhost:8000'\n"
    reactor.run()

if __name__ == "__main__":
    run()
