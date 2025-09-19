# TPC1 - Expressão Regular

Neste TPC,foi nos proposto durante a aula teórica criar uma expressão regular sobre cadeias binárias que __não incluíssem a subcadeia "011"__.

Dado que se trata da representação dum binário, sabe-se que qualquer binário é iniciado por __uma sequência com pelo menos um dígito "1"__. Como a expressão não pode incluir a subcadeia "011", tem-se que __após a possível introdução dum dígito "0" ou mais__, apenas pode ser introduzido __um dígito "1" não seguido doutro dígito "1"__.Assim, pode-se utilizar este método de construção para deduzir a expressão regular. 

Obtendo a expressão regular:
^1+(0|01)*$

Após a realização de alguns __testes no [regex](https://regex101.com/r/9UAPvR/1)__, foi possível concluir que a expressão regular engloba todas as cadeias binárias que não contem a subcadeia "011".