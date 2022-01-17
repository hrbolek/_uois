from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
import datetime
from functools import cache

import sqlengine.sqlengine as SqlEngine

from . import BaseModel

@cache # funny thing, it makes from this function a singleton
def GetModels(BaseModel=BaseModel.getBaseModel(), unitedSequence=Sequence('all_id_seq')):
    """create elementary models for information systems

    Parameters
    ----------
    BaseModel
        represents the declarative_base instance from SQLAlchemy
    unitedSequence : Sequence
        represents a method for generating keys (usually ids) for database entities

    Returns
    -------
    (UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel)
        tuple of models based on BaseModel, table names are hardcoded

    """

    #assert not(unitedSequence is None), "unitedSequence must be defined"
    print('Base models definition (ProgramModel, SubjectModel, SubjectSemesterModel, TopicModel)')
    class ProgramModel(BaseModel):
        __tablename__ = 'programs'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
        lastchange = Column(DateTime, default=datetime.datetime.now)
        externalId = Column(BigInteger, index=True)


    class SubjectModel(BaseModel):
        __tablename__ = 'subjects'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
        lastchange = Column(DateTime, default=datetime.datetime.now)
        externalId = Column(String, index=True)
        
    class SubjectSemesterModel(BaseModel):
        __tablename__ = 'subjectsemesters'

        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
        lastchange = Column(DateTime, default=datetime.datetime.now)

    class TopicModel(BaseModel):
        __tablename__ = 'topics'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
    class SubjectUserRoleModel(BaseModel):
        __tablename__ = 'subjectuserroles'
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)

    class SubjectUserRoleTypeModel(BaseModel):
        __tablename__ = 'subjectuserroletypes'
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)

    class ProgramUserRoleTypeModel(BaseModel):
        __tablename__ = 'programuserroletypes'
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)

    return ProgramModel, SubjectModel, SubjectSemesterModel, TopicModel, SubjectUserRoleModel, SubjectUserRoleTypeModel, ProgramUserRoleTypeModel


from . import Relations 
from . import BaseEntities
@cache
def BuildRelations():
    UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel = BaseEntities.GetModels()
    ProgramModel, SubjectModel, SubjectSemesterModel, TopicModel, SubjectUserRoleModel, SubjectUserRoleTypeModel, ProgramUserRoleTypeModel = GetModels()
    print('building relations between base models')

    Relations.defineRelation1N(ProgramModel, SubjectModel) 
    Relations.defineRelation1N(SubjectModel, SubjectSemesterModel)
    Relations.defineRelation1N(SubjectSemesterModel, TopicModel)

    Relations.defineRelationNM(UserModel, SubjectModel, tableAItemName='grantingsubjects', tableBItemName='guarantors')

    print('building relations between base models finished')
    #defineRelationNM(BaseModel, EventModel, UserModel, 'teachers', 'events')

    pass

from types import MappingProxyType

@cache
def ensureData(SessionMaker):
    def ensureDataItem(session, Model, name):
        itemRecords = session.query(Model).filter(Model.name == name).all()
        itemRecordsLen = len(itemRecords)
        if itemRecordsLen == 0:
            itemRecord = Model(name=name)
            session.add(itemRecord)
            session.commit()
        else:
            assert itemRecordsLen == 1, f'Database has inconsistencies {Model}, {name}'
            itemRecord = itemRecords[0]
        return itemRecord.id

    ProgramModel, SubjectModel, SubjectSemesterModel, TopicModel, SubjectUserRoleModel, SubjectUserRoleTypeModel, ProgramUserRoleTypeModel = GetModels()
    session = SessionMaker()
    try:
        guaranteeSubjectTypeId = ensureDataItem(session, SubjectUserRoleTypeModel, 'guarantee')
        teacherTypeId = ensureDataItem(session, SubjectUserRoleTypeModel, 'teacher')
        guaranteeDeputySubjectTypeId =  ensureDataItem(session, SubjectUserRoleTypeModel, 'guarantee deputy')

        guaranteeProgramTypeId = ensureDataItem(session, ProgramUserRoleTypeModel, 'guarantee')
        guaranteeDeputyProgramTypeId =  ensureDataItem(session, ProgramUserRoleTypeModel, 'guarantee deputy')

        result = {
            'guaranteeSubjectTypeId': guaranteeSubjectTypeId,
            'teacherTypeId': teacherTypeId,
            'guaranteeDeputySubjectTypeId': guaranteeDeputySubjectTypeId,
            'guaranteeProgramTypeId': guaranteeProgramTypeId,
            'guaranteeDeputyProgramTypeId': guaranteeDeputyProgramTypeId
        }    
    finally:
        session.close()
    return MappingProxyType(result)

import random
def PopulateRandomData(SessionMaker):
    session = SessionMaker()

    ProgramModel, SubjectModel, SubjectSemesterModel, TopicModel = GetModels()

    def randomizedTopic(subject, semester, index):
        randomName = f'{subject.name}-{semester.name}-{index+1}'
        record = TopicModel(name=randomName)
        session.add(record)
        session.commit()
        pass

    def randomizedSemester(subject):
        record = SubjectSemesterModel(name='')
        session.add(record)
        session.commit()

        semesterCount = random.randrange(1, 3)
        for _ in range(semesterCount):
            randomizedTopic(subject, record)
        
        session.commit()
        pass

    subjectNames = randomSubjectNames()
    def randomizedSubject(program):
        subjectRecord = SubjectModel(name=random.choice(subjectNames))
        session.add(subjectRecord)
        program.subjects.append(subjectRecord)
        session.commit()
        
        semestersCount = random.randrange(10, 15)
        for _ in range(semestersCount):
            randomizedSemester(subjectRecord)
        
        
        pass


    strsA = ['IT', 'EL', 'MIL', 'GEO', 'ST']
    strsB = ['Bc', 'Mgr', 'Dr']
    strsC = ['P', 'K', 'O']
    def randomizedProgram():
        year = random.randrange(2015, 2020)
        randomName = f'{random.choice(strsA)}-{random.choice(strsB)}-{random.choice(strsC)}/{year}'
        programRecord = ProgramModel(name=randomName)
        session.add(programRecord)
        session.commit()
        subjectsCount = random.randrange(10, 15)
        for _ in range(subjectsCount):
            randomizedSubject(programRecord)
        pass

    try:
        randomizedProgram()
        pass
    finally:
        session.close()

    pass

def randomSubjectNames():
    data = randomSubjectNamesStr()
    result = data.replace(' (v angličtině)', '').split('/n')
    resultArray = [item[:-1] if item[-1] in ['1', '2'] else item for item in result]
    return resultArray

def randomSubjectNamesStr():
    return """3D optická digitalizace 1
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