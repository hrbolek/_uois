# ReadME
# Tento soubor slouží jako diář, do kterého budeme naše zapisovat postupy v projektu 


##### #### ZADÁNÍ #### #### 
Vytvořte datové struktury popisující obecný plán studia, program studia, garanty programu (osoby. viz 1.), předmět studia, garanty předmětu, zástupci garanta, semestry předmětu, témata předmětu (název, vyučující, délky a typy výuky v tématu).

# 12.10.2022 
Proběhla konzultace s prof. Štefkem.
Ujasnění zadání, entit a jejich atributů

#18.10.2022
Další konzultace s prof. Štefkem kvůli dopřesnění atributů entit a řešení jejich vzájemných vazeb.
Vytvoření vlastního kontejneru gql_granting
Do kontejneru jsme poté zkopírovali z gql_ug DPDefinitions.py až po GraphTypeDefinitions
DPDefinitions.py jsme si upravili podle našeho diagramu.

# 3.-14.11.2022 
Nadefinovali jsme si datové struktury s atributy v DBDefinitions, které jsme poté po několika diskuzích s prof. Štefkem upravili tak, aby měli patřičnou logiku.

# 27.11.2022
Nadefinovali jsme resolvery v GraphResolvers. Tento krok nám reálně trval několik dnů, protože jsme si nebyli úplně jisti korektností kódu, po další konzultaci nám ukázal správnou metodu a mohli jsme pokračovat dál.

# 10.12.2022
Nadefinovali jsme gql modely v GraphTypeDefinitions na základě datových struktur v DBDefinitions.

# 22.1.2023
Proběhlo posledních pár úprav ve vazbách mezi entitami.

#  12.3-16.3.2023
Po další konzultaci se nám podařilo vytvořit editory a feeder.
