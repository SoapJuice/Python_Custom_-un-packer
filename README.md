Florea Florin-Cosmin 3A3

Proiect - A 
Id - 7

Creati un tool de impachetare/despachetare fisiere. Tool-ul manipuleaza arhive create dupa
un format definit de dezvoltator. Un set minim de comenzi pe care va trebui sa le stie tool-ul
sunt: creare_arhiva ( cu param 1 fisier, 1 director sau o lista de fisiere) - creaza o arhiva
Listare_continut - va lista fisierele din interiorul arhivei si size-ul lor
Full_unpack ( cu parametru un folder destinatie ) - dezarhiveaza toata arhiva
Unpack ( lista de fisiere in folder de output ) - dezarhiveaza doar fisierele respective
!!! nu se vor folosi biblioteci python 3rd party si nu aveti voie sa folositi zipFile (nu este nevoie
de compresie)

INPUT:
Comenzile listare_continut, full_unpack, unpack

OUTPUT:
Arhiva si fisierele rezultate in urma comenzilor rulate
Logurile comenzilor executate precum si erorile aparute
