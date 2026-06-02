# Rétropropagation du gradient

Sujet : « Rétropropagation du gradient » (backpropagation) dans les réseaux de neurones profonds.

Cadrage : comment un réseau de neurones profond apprend. Réseau comme composition de couches ;
passe avant (forward) puis calcul efficace des gradients par la règle de la chaîne couche par
couche (passe arrière / backward) ; descente de gradient et ses variantes (SGD, mini-batch) ;
fonctions d'activation et leurs dérivées ; problème du gradient qui s'évanouit/explose et
parades. Couvre le pourquoi de l'efficacité (réutilisation des calculs vs différentiation naïve)
et les limites. Second des deux runs ML (le premier : ensemble-learning).
