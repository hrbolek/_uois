from typing_extensions import Required

from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int, NonNull

#from models.GroupRelated.GroupModel import GroupModel
from graphqltypes.Utils import extractSession

from graphqltypes.Utils import createRootResolverById, createRootResolverByName

from models.AcreditationRelated.SubjectTopic import SubjectTopicModel
from models.AcreditationRelated.ProgramModel import ProgramModel
from models.AcreditationRelated.SubjectSemesterModel import SubjectSemesterModel
from models.AcreditationRelated.SubjectModel import SubjectModel

ProgramRootResolverById = createRootResolverById(ProgramModel)

class ProgramType(ObjectType):
    id = ID()
    name = String()

    lastchange = DateTime()
    externalId = String()

    subjects = List('graphqltypes.Subject.SubjectType')
    #users = List(lambda:Field('graphqltypes.User.UserType').type)
    def resolve_subjects(parent, info):
        session = extractSession(info)
        #groupRecord = session.query(GroupModel).get(parent.id)
        try:
            dbRecord = session.query(ProgramModel).filter_by(id=parent.id).one()
            result = dbRecord.subjects
        except Exception as e:
            print(e)
        return result
        


import random
class CreateRandomProgram(Mutation):
    class Arguments():
        pass

    result = Field('graphqltypes.Program.ProgramType')
    ok = Boolean()

    def mutate(root, info):
        session = extractSession(info)

        subjectNames = subjects()

        def randomTopic(subjectsemester, index, length):
            name = f'{subjectsemester.name} : Téma {index}'
            dbRecord = SubjectTopicModel(name=name)
            session.add(dbRecord)
            session.commit()
            return dbRecord

        def randomSubjectSemester(subject, index):
            name = f'{subject.name} / {index}'
            dbRecord = SubjectSemesterModel(name=name)
            session.add(dbRecord)
            session.commit()

            total = 0
            maximum = random.choice([40, 80, 120])
            index = 0
            while total < maximum:
                index = index + 1
                currentLength = random.choice([2, 4, 8])
                if total + currentLength > maximum:
                    currentLength = maximum - total
                total = total + currentLength
                randomTopic(dbRecord, index, currentLength).subjectsemester = dbRecord

            return dbRecord

        def randomSubject(program):
            name = random.choice(subjectNames)
            dbRecord = SubjectModel(name=name)
            session.add(dbRecord)
            session.commit()

            semesterCount = random.randint(1, 3)
            for index in range(semesterCount):
                randomSubjectSemester(dbRecord, index+1).subject = dbRecord

            return dbRecord

        def randomProgram():
            letters = ['B', 'C', 'D', 'E', 'F', 'G', 'H']
            typesA = ['Bc', 'Mgr', 'D']
            typesB = ['P', 'K']
            part1 = random.choice(letters) + random.choice(letters)
            part2 = random.choice(letters) + random.choice(letters)
            part3 = random.choice(letters) + random.choice(letters)
            part4 = random.choice(typesA) + '-' + random.choice(typesB) 
            part5 = random.choice(['2015', '2019', '2020'])
            name = f'{part1}-{part2}-{part3}-{part4}-{part5}'
            dbRecord = ProgramModel(name=name)
            session.add(dbRecord)
            session.commit()

            subjectCount = random.randint(10, 20)
            for index in range(subjectCount):
                randomSubject(dbRecord).program = dbRecord

            return dbRecord

        try:
            print('@CreateRandomProgram')
            result = randomProgram()
        except Exception as e:
            print('@CreateRandomProgram error')
            print(e)

        return CreateRandomProgram(ok=True, result=result)


def subjects():
    
    data = """3D optická digitalizace 1
Agentní a multiagentní systémy
Aktuální témata grafického designu
Algebra
Algoritmy
Algoritmy (v angličtině)
Analogová elektronika 1
Analogová elektronika 2
Analogová technika
Analýza a návrh informačních systémů
Analýza binárního kódu
Analýza systémů založená na modelech
Anglická konverzace na aktuální témata
Anglická konverzace na aktuální témata
Angličtina 1: mírně pokročilí 1
Angličtina 2: mírně pokročilí 2
Angličtina 3: středně pokročilí 1
Angličtina 3: středně pokročilí 1
Angličtina 4: středně pokročilí 2
Angličtina 4: středně pokročilí 2
Angličtina pro doktorandy
Angličtina pro Evropu
Angličtina pro Evropu
Angličtina pro IT
Angličtina pro IT
Angličtina: praktický kurz obchodní konverzace a prezentace
Aplikace paralelních počítačů
Aplikovaná herní studia - výzkum a design
Aplikované evoluční algoritmy
Architektura 20. století
Architektury výpočetních systémů
Audio elektronika
Automatizované testování a dynamická analýza
Autorská práva - letní
Bakalářská práce
Bakalářská práce Erasmus (v angličtině)
Bayesovské modely pro strojové učení (v angličtině)
Bezdrátové a mobilní sítě
Bezpečná zařízení
Bezpečnost a počítačové sítě
Bezpečnost informačních systémů
Bezpečnost informačních systémů a kryptografie
Bioinformatika
Bioinformatika
Biologií inspirované počítače
Biometrické systémy
Biometrické systémy (v angličtině)
Blockchainy a decentralizované aplikace
CCNA Kybernetická bezpečnost (v angličtině)
České umění 1. poloviny 20. století v souvislostech - zimní
České umění 2. poloviny 20. století v souvislostech - letní
Chemoinformatika
Číslicové zpracování akustických signálů
Číslicové zpracování signálů (v angličtině)
CNC obrábění / Roboti v umělecké praxi
Daňový systém ČR
Databázové systémy
Databázové systémy (v angličtině)
Dějiny a filozofie techniky
Dějiny a kontexty fotografie 1
Dějiny a kontexty fotografie 2
Dějiny designu 1 - letní
Dějiny designu 1 - zimní
Desktop systémy Microsoft Windows
Digitální forenzní analýza (v angličtině)
Digitální marketing a sociální média (v angličtině)
Digitální sochařství - 3D tisk 1
Digitální sochařství - 3D tisk 2
Diplomová práce
Diplomová práce (v angličtině)
Diplomová práce Erasmus (v angličtině)
Diskrétní matematika
Dynamické jazyky
Ekonomie informačních produktů
Elektroakustika 1
Elektronický obchod (v angličtině)
Elektronika pro informační technologie
Elektrotechnický seminář
Evoluční a neurální hardware
Evoluční výpočetní techniky
Filozofie a kultura
Finanční analýza
Finanční management pro informatiky
Finanční trhy
Formální analýza programů
Formální jazyky a překladače
Formální jazyky a překladače (v angličtině)
Funkcionální a logické programování
Funkční verifikace číslicových systémů
Fyzika 1 - fyzika pro audio inženýrství
Fyzika v elektrotechnice (v angličtině)
Fyzikální optika
Fyzikální optika (v angličtině)
Fyzikální seminář
Grafická a zvuková rozhraní a normy
Grafická uživatelská rozhraní v Javě
Grafická uživatelská rozhraní v Javě (v angličtině)
Grafická uživatelská rozhraní v X Window
Grafické a multimediální procesory
Grafové algoritmy
Grafové algoritmy (v angličtině)
Hardware/Software Codesign
Hardware/Software Codesign (v angličtině)
Herní studia
Informační systémy
Informační výchova a gramotnost
Inteligentní systémy
Inteligentní systémy
Internetové aplikace
Inženýrská pedagogika a didaktika
Inženýrská pedagogika a didaktika
Jazyk C
Klasifikace a rozpoznávání
Kódování a komprese dat
Komunikační systémy pro IoT
Konvoluční neuronové sítě
Kritická analýza digitálních her
Kruhové konzultace
Kryptografie
Kultura projevu a tvorba textů
Kultura projevu a tvorba textů
Kurz pornostudií
Lineární algebra
Lineární algebra
Logika
Makroekonomie
Management
Management projektů
Manažerská komunikace a prezentace
Manažerská komunikace a prezentace
Manažerské vedení lidí a řízení času
Manažerské vedení lidí a řízení času
Matematická analýza 1
Matematická analýza 2
Matematická logika
Matematické struktury v informatice (v angličtině)
Matematické výpočty pomocí MAPLE
Matematické základy fuzzy logiky
Matematický seminář
Matematický software
Matematika 2
Maticový a tenzorový počet
Mechanika a akustika
Mikroekonomie
Mikroprocesorové a vestavěné systémy
Mikroprocesorové a vestavěné systémy (v angličtině)
Mobilní roboty
Modelování a simulace
Modelování a simulace
Moderní matematické metody v informatice
Moderní metody zobrazování 3D scény
Moderní metody zpracování řeči
Moderní teoretická informatika
Moderní trendy informatiky (v angličtině)
Molekulární biologie
Molekulární genetika
Multimédia
Multimédia (v angličtině)
Multimédia v počítačových sítích
Návrh a implementace IT služeb
Návrh a realizace elektronických přístrojů
Návrh číslicových systémů
Návrh číslicových systémů (v angličtině)
Návrh kyberfyzikálních systémů (v angličtině)
Návrh počítačových systémů
Návrh vestavěných systémů
Návrh, správa a bezpečnost
Operační systémy
Optické sítě
Optika
Optimalizace
Optimalizační metody a teorie hromadné obsluhy
Optimální řízení a identifikace
Paralelní a distribuované algoritmy
Paralelní výpočty na GPU
Pedagogická psychologie
Pedagogická psychologie
Plošné spoje a povrchová montáž
Počítačová fyzika I
Počítačová fyzika II
Počítačová grafika
Počítačová grafika
Počítačová grafika (v angličtině)
Počítačová podpora konstruování
Počítačové komunikace a sítě
Počítačové vidění (v angličtině)
Počítačový seminář
Podnikatelská laboratoř
Podnikatelské minimum
Pokročilá bioinformatika
Pokročilá matematika
Pokročilá počítačová grafika (v angličtině)
Pokročilá témata administrace operačního systému Linux
Pokročilé asemblery
Pokročilé biometrické systémy
Pokročilé číslicové systémy
Pokročilé databázové systémy
Pokročilé databázové systémy (v angličtině)
Pokročilé informační systémy
Pokročilé komunikační systémy (v angličtině)
Pokročilé operační systémy
Pokročilé směrování v páteřních sítích (ENARSI)
Pokročilé techniky návrhu číslicových systémů
Pokročilý návrh a zabezpečení podnikových sítí
Praktické aspekty vývoje software
Praktické paralelní programování
Pravděpodobnost a statistika
Právní minimum
Právní minimum
Právo informačních systémů
Přenos dat, počítačové sítě a protokoly
Přenos dat, počítačové sítě a protokoly (v angličtině)
Principy a návrh IoT systémů
Principy programovacích jazyků a OOP
Principy programovacích jazyků a OOP (v angličtině)
Principy syntézy testovatelných obvodů
Programovací seminář
Programování na strojové úrovni
Programování v .NET a C#
Programování zařízení Apple
Projektová praxe 1
Projektová praxe 1
Projektová praxe 1 (v angličtině)
Projektová praxe 1 (v angličtině)
Projektová praxe 1 (v angličtině)
Projektová praxe 1 (v angličtině)
Projektová praxe 2
Projektová praxe 2
Projektová praxe 2 (v angličtině)
Projektová praxe 2 (v angličtině)
Projektová praxe 3
Projektování datových sítí
Projektový manažer
Prostředí distribuovaných aplikací
Rádiová komunikace
Regulované gramatiky a automaty
Rétorika
Rétorika
Řízení a regulace 1
Řízení a regulace 2
Robotika (v angličtině)
Robotika a manipulátory
Robotika a zpracování obrazu
Semestrální projekt
Semestrální projekt
Semestrální projekt (v angličtině)
Semestrální projekt Erasmus (v angličtině)
Semestrální projekt Erasmus (v angličtině)
Seminář C#
Seminář C++
Seminář diskrétní matematiky a logiky
Seminář Java
Seminář Java (v angličtině)
Seminář VHDL
Senzory a měření
Serverové systémy Microsoft Windows
Signály a systémy
Simulační nástroje a techniky
Síťová kabeláž a směrování (CCNA1+CCNA2)
Síťové aplikace a správa sítí
Skriptovací jazyky
Složitost (v angličtině)
Směrování a přepínání v páteřních sítích (ENCOR)
Soft Computing
Španělština: začátečníci 1/2
Španělština: začátečníci 2/2
Správa serverů IBM zSeries
Statická analýza a verifikace
Statistika a pravděpodobnost
Statistika, stochastické procesy, operační výzkum
Strategické řízení informačních systémů
Strojové učení a rozpoznávání
Systémová biologie
Systémy odolné proti poruchám
Systémy odolné proti poruchám
Systémy pracující v reálném čase (v angličtině)
Technologie sítí LAN a WAN (CCNA3+4)
Teoretická informatika
Teoretická informatika (v angličtině)
Teorie a aplikace Petriho sítí
Teorie her
Teorie kategorií v informatice
Teorie programovacích jazyků
Testování a dynamická analýza
Tvorba aplikací pro mobilní zařízení (v angličtině)
Tvorba uživatelských rozhraní
Tvorba uživatelských rozhraní (v angličtině)
Tvorba webových stránek
Tvorba webových stránek (v angličtině)
Typografie a publikování
Účetnictví
Ukládání a příprava dat
Umělá inteligence a strojové učení
Úvod do molekulární biologie a genetiky
Úvod do softwarového inženýrství
Uživatelská zkušenost a návrh rozhraní a služeb (v angličtině)
Vědecké publikování od A do Z
Vizualizace a CAD (v angličtině)
Vizuální styly digitálních her 1
Vizuální styly digitálních her 2
Vybraná témata z analýzy a překladu jazyků
Vybrané kapitoly z matematiky
Vybrané partie z matematiky I.
Vybrané partie z matematiky II.
Vybrané problémy informačních systémů
Výpočetní fotografie
Výpočetní geometrie
Výpočetní geometrie (v angličtině)
Vysoce náročné výpočty
Vysoce náročné výpočty
Vysoce náročné výpočty (v angličtině)
Výstavba překladačů (v angličtině)
Výtvarná informatika
Zabezpečovací systémy
Zahraniční odborná praxe
Zahraniční odborná praxe
Základy ekonomiky podniku
Základy financování
Základy herního vývoje
Základy hudební akustiky
Základy marketingu
Základy počítačové grafiky
Základy programování
Základy umělé inteligence
Základy umělé inteligence (v angličtině)
Získávání znalostí z databází
Zkouška z jazyka anglického pro Ph.D.
Zobrazovací systémy v lékařství
Zpracování a vizualizace dat v prostředí Python
Zpracování obrazu
Zpracování obrazu (v angličtině)
Zpracování přirozeného jazyka
Zpracování přirozeného jazyka (v angličtině)
Zpracování řeči a audia člověkem a počítačem
Zpracování řečových signálů
Zpracování řečových signálů (v angličtině)
Zvukový software"""
    
    return data.splitlines()