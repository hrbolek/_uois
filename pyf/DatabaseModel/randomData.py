import random
from unicodedata import name
from DatabaseModel.models import *
from DatabaseModel.myDevTools import *
from DatabaseModel.models import PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel

def randomUser(mod='main'):
    surNames = [
        'Novák', 'Nováková', 'Svobodová', 'Svoboda', 'Novotná',
        'Novotný', 'Dvořáková', 'Dvořák', 'Černá', 'Černý', 
        'Procházková', 'Procházka', 'Kučerová', 'Kučera', 'Veselá',
        'Veselý', 'Horáková', 'Krejčí', 'Horák', 'Němcová', 
        'Marková', 'Němec', 'Pokorná', 'Pospíšilová','Marek'
    ]

    names = [
        'Jiří', 'Jan', 'Petr', 'Jana', 'Marie', 'Josef',
        'Pavel', 'Martin', 'Tomáš', 'Jaroslav', 'Eva',
        'Miroslav', 'Hana', 'Anna', 'Zdeněk', 'Václav',
        'Michal', 'František', 'Lenka', 'Kateřina',
        'Lucie', 'Jakub', 'Milan', 'Věra', 'Alena'
    ]

    name1 = random.choice(names)
    name2 = random.choice(names)
    name3 = random.choice(surNames)
    email = f'{name1}.{name2}.{name3}@{mod}.university.world'
    return {'name': f'{name1} {name2}', 'surname': name3, 'email': email}

def GetStudyPrograms():
    options = ["Kyberneticka bezpecnost", "Protivzdusna obrana", "Elektro", "Strojni", "Pruzkum",
               "Zbrane a munice", "Velitel tankovych vojsk", "Zpravodajske zabezpeceni", "Vseobecne lekarstvi",
               "Zubni lekarstvi", "Pilot", "Ridici letoveho provozu"]
    return options

def preloadData(session):
    print("generating data - preloadData function")
    TypeFaculty = GroupTypeModel(name = "fakulta")
    TypeDepartment = GroupTypeModel(name = "katedra")
    TypeStudyGroup = GroupTypeModel(name = "studijni skupina")
    TypeAllStudentsGroup = GroupTypeModel(name = "studenti_UO")
    TypeAllTeachersGroup = GroupTypeModel(name = "ucitele_UO")

    AddToSessionAndCommit(TypeFaculty, session)
    AddToSessionAndCommit(TypeDepartment, session)
    AddToSessionAndCommit(TypeStudyGroup, session)
    AddToSessionAndCommit(TypeAllStudentsGroup, session)
    AddToSessionAndCommit(TypeAllTeachersGroup, session)

    print(TypeAllTeachersGroup)

    allTeachersGroup = GroupModel(name='teachers')
    allStudentsGroup = GroupModel(name='students')
    TypeAllStudentsGroup.groups.append(allStudentsGroup)
    TypeAllTeachersGroup.groups.append(allTeachersGroup)
    session.add(allTeachersGroup)
    session.add(allStudentsGroup)
    session.commit()

    studyPrograms = GetStudyPrograms()
    studyProgramsIds = []
    for program in studyPrograms:
        programRecord = ProgramModel(name = program)
        session.add(programRecord)
        session.commit()
        studyProgramsIds.append(programRecord.id)

        print(f'Subjects for {program}')        
        subjectList = [f'{program} / Předmět {i+1}' for i in range(9)]
        for subject in subjectList:
            subjectRecord = SubjectModel(name=subject, program=programRecord)
            session.add(subjectRecord)

            topicList = [f'Téma {i+1}' for i in range(19)]
            for index, topic in enumerate(topicList):
                topicRecord = LessonModel(topic=topic)
                topicRecord.subject = subjectRecord
                session.add(topicRecord)
        session.commit()
    
    def RandomizedStudents(faculty, studyGroup, count=10):
        for _ in range(count):
            student = randomUser(mod=faculty.name)
            personRecord = PersonModel(name = student["name"], surname = student["surname"], email = student["email"])
            studentRecord = StudentModel(program_id = random.choice(studyProgramsIds))
            personRecord.students.append(studentRecord)
            session.add(studentRecord)
            session.add(personRecord)
            faculty.people.append(personRecord)
            studyGroup.people.append(personRecord)
            allStudentsGroup.people.append(personRecord)
        session.commit()
    
    def RandomizedStudyGroup(faculty):
        name = f"{faculty.name}5-{random.choice([1, 2, 3, 4, 5])}{random.choice(['B', 'C', 'K'])}{random.choice(['A', 'E', 'I'])}"
        studyGroupRecord = GroupModel(name=name)
        TypeStudyGroup.groups.append(studyGroupRecord)
        session.add(studyGroupRecord)
        session.commit()
        RandomizedStudents(faculty, studyGroupRecord, count=random.randint(5, 15))
        pass
    
    def RandomizedTeachers(faculty, department, count=10):
        for _ in range(count):
            teacher = randomUser(mod=faculty.name)
            teacherRecord = PersonModel(name = teacher["name"], surname = teacher["surname"], email = teacher["email"])
            session.add(teacherRecord)
            faculty.people.append(teacherRecord)
            department.people.append(teacherRecord)
            allTeachersGroup.people.append(teacherRecord)
        session.commit()
        print('RandomizedTeachers', teacherRecord.id)
        
    def RandomizedDepartment(faculty, index): #faculty is type facultyGroup
        name = f"{faculty.name}_{index+1}_{random.choice(['B', 'C', 'K'])}{random.choice(['A', 'E', 'I'])}"
        departmentRecord = GroupModel(name=name)
        TypeDepartment.groups.append(departmentRecord)
        session.add(departmentRecord)
        session.commit()
        RandomizedTeachers(faculty, departmentRecord, count=random.randint(5, 20))
        pass
    
    def RandomizedFaculty(index):
        facultyGroup = GroupModel(name=f'F{index+1}')
        TypeFaculty.groups.append(facultyGroup)
        session.add(facultyGroup)
        session.commit()
        departmentCount = random.randrange(4, 14)
        for _ in range(departmentCount):
            RandomizedDepartment(facultyGroup, index=_)
        studyGroupCount = random.randrange(20, 40)
        for _ in range(studyGroupCount):
            RandomizedStudyGroup(facultyGroup)
        session.commit()
    
    def RandomizedUniversity():
        facultyCount = random.randrange(3, 7)
        for index in range(facultyCount):
            RandomizedFaculty(index)
        session.commit()
        
    RandomizedUniversity()
    session.commit()
    session.close()

def rooms(mySession, buildingRecord):
    # print("generating data - buildings function")
    for index in range(random.randrange(10, 15)):
        roomRecord = RoomModel(name=buildingRecord.name + ' / ' + str(index + 1), building_id=buildingRecord.id)
        AddToSession(roomRecord, mySession)

    CommitSession(mySession)
    pass

def buildings(mySession):
    print("generating data - buildings function")

    """
    studentsGroup = GroupModel(name = "Studenti_UO")
    teachersGroup = GroupModel(name = "ucitele")
    departmentGroup = GroupModel(name = "K-209")
    
    TypeDepartment = GroupTypeModel(name = "katedra")
    TypeDepartment.groups.append(departmentGroup)
    
    adam = PersonModel(name = "Adam", surname = "Novotny", address = "Brno", email = "adam@unob.cz")
    petr = PersonModel(name = "Petr", surname = "Veliky", address = "Petrohrad", email = "petr@unob.cz")
    studentsGroup.people.append(petr)
    adam.groups.append(teachersGroup)
    petr.groups.append(departmentGroup)
    """
    
    area1 = AreaModel(name = "Kasárna Šumavská")
    area2 = AreaModel(name = "Kasárna Jana Babáka")
    building1 = BuildingModel(name = "Jídelna")
    building2 = BuildingModel(name = "Katedra Informatiky")
    building3 = BuildingModel(name = "Brana KJB")
    building4 = BuildingModel(name = "Katedra matematiky")
    building5 = BuildingModel(name = "Internát Chodská")
    
    
    area1.buildings.append(building1)
    area1.buildings.append(building2)
    area1.buildings.append(building4)

    area2.buildings.append(building3)
    area2.buildings.append(building5)
    
    #AddToSession(adam, mySession)
    #AddToSession(studentsGroup, mySession)
    AddToSession(area1, mySession)
    AddToSession(area2, mySession)
    AddToSession(building1, mySession)
    AddToSession(building2, mySession)
    AddToSession(building3, mySession)
    AddToSession(building4, mySession)
    AddToSession(building5, mySession)
    CommitSession(mySession)

    rooms(mySession, building1)
    rooms(mySession, building2)
    rooms(mySession, building3)
    rooms(mySession, building4)
    rooms(mySession, building5)
 
def lekce(mySession):
    print("generating data - lekce function")
    cviceni = LessonTypeModel(name = "laboratorni cviceni")
    prednaska = LessonTypeModel(name = "prednaska na ucebne")

    l1 = LessonModel(topic = "lekce cviceni")
    l2 = LessonModel(topic = "lekce prednaska")

    cviceni.lessons.append(l1)
    prednaska.lessons.append(l2)

    AddToSession(cviceni, mySession)
    AddToSession(prednaska, mySession)
    AddToSession(l1, mySession)
    AddToSession(l2, mySession)
    mySession.commit()