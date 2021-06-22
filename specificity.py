# Sept 27, 2019
#

import os
import configparser
import csv
import sys
import time
from operator import getitem
from scipy.stats import hypergeom


if __name__=='__main__':

    t0 = time.time()

    #---CHECK INPUT---#
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'input.ini')):
        sys.exit("No input.ini file in the current folder. Exiting")

    if len(sys.argv) == 1:
        sys.exit("I'm expecting the name of a section of the input.ini file as input. Exiting")

    config = configparser.ConfigParser()
    config.read('input.ini')

    if sys.argv[1] not in config.sections():
        sys.exit('Section {} does not exist in input.ini. Exiting'.format(sys.argv[1]))

    input_file = config.get(sys.argv[1], 'file_input', fallback = False)
    output_file = config.get(sys.argv[1], 'file_output', fallback = False)
    T  = int(config.get(sys.argv[1], 'word_corpus', fallback = False))
    t = int(config.get(sys.argv[1], 'word_subcorpus', fallback = False))

    




    #---SETUP OUTPUT/LOG DIRS AND FILES---#
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'Output')):
        os.makedirs(os.path.join(os.path.dirname(__file__), 'Output'))
        os.makedirs(os.path.join(os.path.dirname(__file__), 'Output', 'Results'))
        os.makedirs(os.path.join(os.path.dirname(__file__), 'Output', 'Logs'))

    output_id = "{}".format(output_file)
    outfilename = os.path.join(os.path.dirname(__file__), 'Output', 'Results', 'collocs_{}.csv'.format(output_id))
    outlogname = os.path.join(os.path.dirname(__file__), 'Output', 'Logs', 'log_{}.txt'.format(output_id))

    logfile = open(outlogname, 'w')
    sys.stdout = logfile

    #---THE PROGRAM STARTS---#
    print("The program will run with the following input:\n")
    print("input_file: {}".format(input_file))
    print("output_file: {}".format(output_file))
    print("T : {}".format(T ))
    print("t: {}".format(t))
    print("---")

    t1 = time.time()


    dict_result= {}
    # OUVERTURE FICHIER
    with open(input_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        ### POUR CHAQUE LIGNE
        for row in spamreader:
            f=int(row[1]) # F : frequence du mot dans le corpus global
            F=int(row[2]) # f : frequence du mot dans le sous-corpus
            k=(F*t)/T # CALCUL DE K
            
            # ESTIMATION LOG(P(X=K)) VIA DECOMPOSITION ET FORMULE STIRLING
           
            # CALCUL DIRECT VIA LIBRAIRIE STATISTIQUE
            prb_f_est1 = hypergeom.cdf(f, T, F, t)
            
            
            # CAS SIGNIFICATIVITE POSITIVE
            if(f>k):
                # DONNE PROBAS DE k à F-1
                
                sign=1
                # INVERSE POUR AVOIR P(X>f)
                S_est1=1-prb_f_est1
            # CAS SIGNIFICATIVITE NEGATIVE
            else:
                sign=-1
                # 
                S_est1=prb_f_est1
            
            k=round(k)
           
            ###### CALCUL DE l'INDICE DE SPECIFICITE
            idx_est1=(0.5-S_est1)/0.5
            idx_final_est1=idx_est1*10*sign
            #ENRIGISTREMENT DANS LE DICO
            dict_result[row[0]]={"F":F,"f":f,"k":k,"sign":sign,"Prob_est1":prb_f_est1,"S_est1":S_est1,"indice_final_est1":idx_final_est1}



        print("{} terms specificity cumputed in {} seconds".format(len(dict_result.keys()), time.time()-t1))

        t2 = time.time()
        
        # ENREGISTREMENT DES RESULTATS
        final=sorted(dict_result.items(),key=lambda x:getitem(x[1],'indice_final_est1'), reverse=True)
        print("output_file > "+output_file)
        with open(outfilename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["word","F","f","k","sign","Prob_est1","S_est1","indice_final_est1"])
            for row in final:
                spamwriter.writerow([row[0], row[1]["F"], row[1]["f"], row[1]["k"], row[1]["sign"], row[1]["Prob_est1"], row[1]["S_est1"],row[1]["indice_final_est1"]])
         
    
        print("{} result file obtained from the corpus in {} seconds".format(len(final), time.time()-t2))

        t_final = time.time()

        print('---')
        print('The program has run in {} seconds '.format(t_final-t0))
        print('Output file: {}'.format(outfilename))
