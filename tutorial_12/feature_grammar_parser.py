#NLTK code defining a simple grammar, and demonstrating some simple parsing and generating functions. 
#Alistair Knott, 10/5/2016

import nltk;
import nltk.parse.chart;
from nltk.parse.generate import generate;
from nltk.app import rdparser_app;
from nltk import load_parser


#demo_parse(string) finds all the parses of string permitted by the grammar that it loads.
#The function uses a type of parser called a chart parser,that can handle recursion, 
#and that finds all possible parses, reasonably efficiently.
#E.g. demo_parse("Fred thinks he loves the sheep")  
def demo_parse(string):

    #tokenise the input string
    tokens = string.split();

    #set trace=2 if you want to see what the parser is doing, step-by-step..
    # - N.B. NLTK caches grammars after they're loaded, unless told not to. 
    #   I've told it not to, so that the grammar can be changed during a session.
    cp = load_parser('file:///Users/zw/Documents/Otago/COSC343_Artificial_Intielligence/tutorial_12/feature_grammar.fcfg', trace=0, cache=False);

    #run the chart parser on the tokens
    for tree in cp.parse(tokens):
            print(tree);
            tree.draw();
    


