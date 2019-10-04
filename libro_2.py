#conta le lettere in un libro
import matplotlib.pyplot as plt
import time
import os
import argparse
import logging                                                      # è un print intelligente
logging.basicConfig(level=logging.INFO)    



_description = 'questo programma conta la frequenza delle lettere all interno di un file .txt e fa altre magie '                      #boh????? 


def contalettere(file_path):        
    #basic sanity checks
    
    assert file_path.endswith('.txt')
    assert os.path.isfile(file_path)

    logging.info('opening file %s...', file_path)                 # mi dice se sta aprendo il file

    with open(file_path) as imput_file:                           #leggo il file che gli ho dato                              
        data=imput_file.read()
    logging.info('Done. %d character(s) found', len(data))         # PERCHE USA S E D?, PERCHE HO BISOGNO DI CHIAMARLO IMUT FILE?

    lettere='abcdefghijklmnopqrstuvwxyz'
    dizionario={}

    for i in lettere:
        dizionario[i]=0
    for i in data.lower():
        if i in lettere:
            dizionario[i]+=1

    #ora normalizzio

    lettere_tot=float(sum(dizionario.values()))                 #.values() mi dà un vettore con le componenti uguali al numero di lettere trrovate

    for i in lettere:
        dizionario[i]=dizionario[i]/lettere_tot

    print (dizionario)

    keys = dizionario.keys()
    keys_values = dizionario.values()

    plt.bar(keys,keys_values)
    '''plt.show()'''


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description =_description)
    parser.add_argument('infile', help= 'nome del file che si vuole analizzare')
    parser.add_argument('-i','--histo',help='fa listogramma',action='store_true' )
    args = parser.parse_args()
    contalettere(args.infile)       #ricorda che quando lo richiami devi mettere args.nome del paramettro!!!


    if args.histo:
        
        plt.show()
    else:
        print (dizionario)



