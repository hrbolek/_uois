import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_granting")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_granting.GraphTypeDefinitions import schema

from shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
)


def createByIdTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        datarow = data[tableName][0]

        query = "query($id: ID!){" f"{queryEndpoint}(id: $id)" "{ id, name }}"
        context_value = await createContext(async_session_maker)
        variable_values = {"id": datarow["id"]}

        print(query, flush=True)
        print(variable_values, flush=True)

        resp = await schema.execute(
            query, context_value=context_value, variable_values=variable_values
        )  # , variable_values={"title": "The Great Gatsby"})

        respdata = resp.data[queryEndpoint]
        print(respdata, flush=True)

        assert resp.errors is None

        for att in attributeNames:
            assert respdata[att] == datarow[att]

    return result_test


def createPageTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()

        query = "query{" f"{queryEndpoint}" "{ id, name }}"
        print(query, flush=True)

        context_value = await createContext(async_session_maker)
        resp = await schema.execute(query, context_value=context_value)

        respdata = resp.data[queryEndpoint]
        print(respdata, flush=True)
        assert resp.errors is None

        datarows = data[tableName]
        for rowa, rowb in zip(respdata, datarows):
            for att in attributeNames:
                assert rowa[att] == rowb[att]

    return result_test

def createResolveReferenceTest(tableName, gqltype, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()

        data = get_demodata()
        table = data[tableName]
        for row in table:
            rowid = row['id']

            query = (
                'query { _entities(representations: [{ __typename: '+ f'"{gqltype}", id: "{rowid}"' + 
                ' }])' +
                '{' +
                f'...on {gqltype}' + 
                '{ id }'+
                '}' + 
                '}')

            context_value = await createContext(async_session_maker)

            resp = await schema.execute(query, context_value=context_value)
            data = resp.data
            print(data, flush=True)
            data = data['_entities'][0]

            assert data['id'] == rowid

    return result_test

test_reference_acprogramforms = createResolveReferenceTest(tableName='acprogramforms', gqltype='AcProgramFormTypeGQLModel')
test_reference_acprograms = createResolveReferenceTest(tableName='acprograms', gqltype='AcProgramGQLModel')
test_reference_acprograms_editor = createResolveReferenceTest(tableName='acprograms', gqltype='AcProgramEditorGQLModel')
test_reference_acprogramlanguages = createResolveReferenceTest(tableName='acprogramlanguages', gqltype='AcProgramLanguageTypeGQLModel')
test_reference_acprogramlevels = createResolveReferenceTest(tableName='acprogramlevels', gqltype='AcProgramLevelTypeGQLModel')
test_reference_acprogramtitles = createResolveReferenceTest(tableName='acprogramtitles', gqltype='AcProgramTitleTypeGQLModel')
test_reference_acclassificationtypes= createResolveReferenceTest(tableName='acclassificationtypes', gqltype='AcClassificationTypeGQLModel')

test_reference_acprogramtypes = createResolveReferenceTest(tableName='acprogramtypes', gqltype='AcProgramTypeGQLModel')
 
test_reference_acclassifications = createResolveReferenceTest(tableName='acclassifications', gqltype='AcClassificationGQLModel')
test_reference_acclassificationlevels = createResolveReferenceTest(tableName='acclassificationlevels', gqltype='AcClassificationLevelGQLModel')


test_reference_subjects = createResolveReferenceTest(tableName='acsubjects', gqltype='AcSubjectGQLModel')
test_reference_semesters = createResolveReferenceTest(tableName='acsemesters', gqltype='AcSemesterGQLModel')

    
test_reference_topics = createResolveReferenceTest(tableName='actopics', gqltype='AcTopicGQLModel')
test_reference_lessons = createResolveReferenceTest(tableName='aclessons', gqltype='AcLessonGQLModel')
test_reference_lesson_types = createResolveReferenceTest(tableName='aclessontypes', gqltype='AcLessonTypeGQLModel')
test_reference_users = createResolveReferenceTest(tableName='users', gqltype='UserGQLModel')
test_reference_groups = createResolveReferenceTest(tableName='groups', gqltype='GroupGQLModel')



test_query_classification_type_page = createPageTest(tableName="acclassificationtypes", queryEndpoint="acclassificationTypePage")


# test_query_request_by_id = createByIdTest(tableName="formrequests", queryEndpoint="requestById")
# test_query_request_page = createPageTest(tableName="formrequests", queryEndpoint="requestsPage")

# test_query_form_type_by_id = createByIdTest(tableName="formtypes", queryEndpoint="formTypeById")
# test_query_form_type_page = createPageTest(tableName="formtypes", queryEndpoint="formTypePage")
# test_query_form_category_by_id = createByIdTest(tableName="formcategories", queryEndpoint="formCategoryById")
# test_query_form_category_page = createPageTest(tableName="formcategories", queryEndpoint="formCategoryPage")

# test_query_item_by_id = createByIdTest(tableName="formitems", queryEndpoint="itemById")

# test_query_item_type_by_id = createByIdTest(tableName="formitemtypes", queryEndpoint="itemTypeById")
# test_query_item_type_page = createPageTest(tableName="formitemtypes", queryEndpoint="itemTypePage")
# test_query_item_category_by_id = createByIdTest(tableName="formitemcategories", queryEndpoint="itemCategoryById")
# test_query_item_category_page = createPageTest(tableName="formitemcategories", queryEndpoint="itemCategoryPage")

@pytest.mark.asyncio
async def test_query_program():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['acprograms']
    row = table[0]
    query = 'query{programById(id: "' + row['id'] + '''") { 
        id
        name
        nameEn
        lastchange
        type { id }
        subjects { id }
        editor { id }
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data
    data = data['programById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']
    assert data['type']['id'] == row['type_id']
    assert data['editor']['id'] == row['id']

@pytest.mark.asyncio
async def test_query_say_hello():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    query = 'query{sayHelloGranting(id: "123")}'

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data
    data = data['sayHelloGranting']

    
    assert resp.errors is None
    assert 'ello' in data

@pytest.mark.asyncio
async def test_query_program_type():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['acprogramtypes']
    row = table[0]
    id = row['id']
    query = '''query($id: ID!){
        programTypeById(id: $id) { 
            id
            name
            nameEn
            lastchange
            level { id }
            language { id }
            title { id }
            form { id }
    }}'''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    data = data['programTypeById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']
    assert data['level']['id'] == row['level_id']
    assert data['language']['id'] == row['language_id']
    assert data['title']['id'] == row['title_id']
    assert data['form']['id'] == row['form_id']


@pytest.mark.asyncio
async def test_query_program_language():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['acprogramlanguages']
    row = table[0]
    id = row['id']
    query = '''query($id: ID!){
        programLanguageById(id: $id) { 
            id
            name
            nameEn
            lastchange
    }}'''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    data = data['programLanguageById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']

@pytest.mark.asyncio
async def test_query_classification_type():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['acclassificationtypes']
    query = '''query{acclassificationTypePage { 
        id
        name
        nameEn
        lastchange
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    assert resp.errors is None
    data = resp.data
    data = data['acclassificationTypePage']

    print(data, flush=True)
    
    assert resp.errors is None


@pytest.mark.asyncio
async def test_query_program_form():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['acprogramforms']
    row = table[0]
    id = row['id']
    query = '''query($id: ID!){
        programFormById(id: $id) { 
            id
            name
            nameEn
            lastchange
    }}'''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    data = data['programFormById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']


@pytest.mark.asyncio
async def test_query_program_title():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['acprogramtitles']
    row = table[0]
    id = row['id']
    query = '''query($id: ID!){
        programTitleById(id: $id) { 
            id
            name
            nameEn
            lastchange
    }}'''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    data = data['programTitleById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']

@pytest.mark.asyncio
async def test_query_program_level():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['acprogramlevels']
    row = table[0]
    id = row['id']
    query = '''query($id: ID!){
        programLevelById(id: $id) { 
            id
            name
            nameEn
            lastchange
    }}'''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    data = data['programLevelById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']

@pytest.mark.asyncio
async def test_query_subject():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['acsubjects']
    row = table[0]
    id = row['id']
    query = '''query($id: ID!){
        acsubjectById(id: $id) { 
            id
            name
            nameEn
            lastchange
            program { id }
            semesters { 
                id 
                subject { id }
            }
    }}'''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    data = data['acsubjectById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']
    assert data['program']['id'] == row['program_id']

    for semester in data['semesters']:
        assert semester['subject']['id'] == row['id']


@pytest.mark.asyncio
async def test_query_semesters():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['acsemesters']
    row = table[0]
    id = row['id']
    query = '''query($id: ID!){
        acsemesterById(id: $id) { 
            id
            order
            credits
            lastchange
            subject { id }
            topics { 
                id 
                semester { id }
            }
    }}'''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    data = data['acsemesterById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']
    assert data['subject']['id'] == row['subject_id']
    for topic in data['topics']:
        assert topic['semester']['id'] == row['id']

@pytest.mark.asyncio
async def test_query_classification_via_semester():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['acsemesters']
    row = table[0]
    id = row['id']
    query = '''query($id: ID!){
        acsemesterById(id: $id) { 
            id
            classifications { 
                id
                lastchange
                user { id }
                level { id name nameEn }
                semester { id }
            }
        }
    }'''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    assert resp.data is not None
    data = resp.data
    data = data['acsemesterById']

    print(data, flush=True)
    print(row, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']
    # assert data['user']['id'] == row['user_id']
    # assert data['level']['id'] == row['classificationlevel_id']
    # assert data['type']['id'] == row['classificationtype_id']
    # assert data['semester']['id'] == row['semester_id']

@pytest.mark.asyncio
async def test_query_topic():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['actopics']
    row = table[0]
    id = row['id']
    query = '''query($id: ID!){
        actopicById(id: $id) { 
            id
            name
            nameEn
            lastchange
            order
            semester { id }
            lessons { id }
    }}'''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    data = data['actopicById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']
    assert data['semester']['id'] == row['semester_id']
    #for topic in data['topics']:
    #    assert topic['semester']['id'] == row['id']

@pytest.mark.asyncio
async def test_query_lesson():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['aclessons']
    row = table[0]
    id = row['id']
    query = '''query($id: ID!){
        aclessonById(id: $id) { 
            id
            count
            lastchange
            topic { id }
            type { id }
    }}'''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    data = data['aclessonById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']
    assert data['topic']['id'] == row['topic_id']
    assert data['type']['id'] == row['type_id']
    #for topic in data['topics']:
    #    assert topic['semester']['id'] == row['id']

@pytest.mark.asyncio
async def test_query_lesson_type():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['aclessontypes']
    row = table[0]
    id = row['id']
    query = '''query($id: ID!){
        aclessonTypeById(id: $id) { 
            id
            name
            nameEn
            lastchange
    }}'''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    data = data['aclessonTypeById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']
    #for topic in data['topics']:
    #    assert topic['semester']['id'] == row['id']


@pytest.mark.asyncio
async def test_program_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['acprogramtypes']
    row = table[0]
    id = row['id']

    name = "Program X"
    query = '''
            mutation(
                $type_id: ID!,
                $name: String!
                ) {
                programInsert(program: {
                    typeId: $type_id,
                    name: $name
                }){
                    id
                    msg
                    program {
                        id
                        name
                        lastchange
                        type { id }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {"name": name, "type_id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    
    print(resp, flush=True)

    assert resp.errors is None
    data = resp.data['programInsert']
    assert data["msg"] == "ok"
    data = data["program"]
    assert data["type"]["id"] == id
    assert data["name"] == name
   
    id = data["id"]
    lastchange = data["lastchange"]
    name = "NewName"
    query = '''
            mutation(
                $id: ID!,
                $lastchange: DateTime!
                $name: String!
                ) {
                programUpdate(program: {
                id: $id,
                lastchange: $lastchange
                name: $name
            }){
                id
                msg
                program {
                    id
                    name
                    lastchange
                }
            }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id, "name": name, "lastchange": lastchange}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None

    data = resp.data['programUpdate']
    assert data['msg'] == "ok"
    data = data["program"]
    assert data["name"] == name

    # lastchange je jine, musi fail
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data['programUpdate']
    assert data['msg'] == "fail"

    pass

@pytest.mark.asyncio
async def test_program_type_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    
    table = data["acprogramforms"]
    row = table[0]
    form_id = row["id"]

    table = data["acprogramlanguages"]
    row = table[0]
    language_id = row["id"]

    table = data["acprogramlevels"]
    row = table[0]
    level_id = row["id"]

    table = data["acprogramtitles"]
    row = table[0]
    title_id = row["id"]

    name = "Program X"
    query = '''
            mutation(
                $form_id: ID!,
                $language_id: ID!,
                $level_id: ID!,
                $title_id: ID!,
                $name: String!
                ) {
                programTypeInsert(programType: {
                    formId: $form_id,
                    languageId: $language_id,
                    levelId: $level_id,
                    titleId: $title_id,
                    name: $name,
                    nameEn: $name
                }){
                    id
                    msg
                    programType {
                        id
                        name
                        lastchange
                        form { id }
                        language { id }
                        level { id }
                        title { id }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {
        "name": name, 
        "form_id": form_id,
        "language_id": language_id,
        "title_id": title_id,
        "level_id": level_id
    }
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    
    print(resp, flush=True)

    assert resp.errors is None
    data = resp.data['programTypeInsert']
    assert data["msg"] == "ok"
    data = data["programType"]
    assert data["form"]["id"] == form_id
    assert data["language"]["id"] == language_id
    assert data["title"]["id"] == title_id
    assert data["level"]["id"] == level_id
    assert data["name"] == name
   
    id = data["id"]
    lastchange = data["lastchange"]
    name = "NewName"
    query = '''
            mutation(
                $id: ID!,
                $lastchange: DateTime!
                $name: String!
                ) {
                programTypeUpdate(programType: {
                id: $id,
                lastchange: $lastchange
                name: $name
            }){
                id
                msg
                programType {
                    id
                    name
                    lastchange
                }
            }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id, "name": name, "lastchange": lastchange}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None

    data = resp.data['programTypeUpdate']
    assert data['msg'] == "ok"
    data = data["programType"]
    assert data["name"] == name

    # lastchange je jine, musi fail
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data['programTypeUpdate']
    assert data['msg'] == "fail"

    pass

@pytest.mark.asyncio
async def test_subject_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    
    table = data["acprograms"]
    row = table[0]
    id = row["id"]

    name = "Subject X"
    query = '''
            mutation(
                $id: ID!,
                $name: String!
                ) {
                operation: subjectInsert(subject: {
                    programId: $id,
                    name: $name,
                    nameEn: $name
                }){
                    id
                    msg
                    entity: subject {
                        id
                        name
                        lastchange
                        program { id }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {
        "name": name, 
        "id": id,
    }
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    
    print(resp, flush=True)

    assert resp.errors is None
    data = resp.data['operation']
    assert data["msg"] == "ok"
    data = data["entity"]
    assert data["program"]["id"] == id
    assert data["name"] == name
    
   
    id = data["id"]
    lastchange = data["lastchange"]
    name = "NewName"
    query = '''
            mutation(
                $id: ID!,
                $lastchange: DateTime!
                $name: String!
                ) {
                operation: subjectUpdate(subject: {
                id: $id,
                lastchange: $lastchange
                name: $name
            }){
                id
                msg
                entity: subject {
                    id
                    name
                    lastchange
                }
            }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id, "name": name, "lastchange": lastchange}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None

    data = resp.data['operation']
    assert data['msg'] == "ok"
    data = data["entity"]
    assert data["name"] == name

    # lastchange je jine, musi fail
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data['operation']
    assert data['msg'] == "fail"

    pass

@pytest.mark.asyncio
async def test_semester_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    
    table = data["acsubjects"]
    row = table[0]
    id = row["id"]

    table = data["acclassificationtypes"]
    row = table[0]
    classification_id = row["id"]


    name = "Semester X"
    query = '''
            mutation(
                $id: ID!,
                $classification_id: ID!
                ) {
                operation: semesterInsert(semester: {
                    subjectId: $id,
                    classificationtypeId: $classification_id
                }){
                    id
                    msg
                    entity: semester {
                        id
                        lastchange
                        subject { id }
                        classificationType { id }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {
        "id": id,
        "classification_id": classification_id
    }
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    
    print(resp, flush=True)

    assert resp.errors is None
    data = resp.data['operation']
    assert data["msg"] == "ok"
    data = data["entity"]
    assert data["subject"]["id"] == id
    assert data["classificationType"]["id"] == classification_id
    #assert data["name"] == name
    
   
    id = data["id"]
    lastchange = data["lastchange"]
    name = "NewName"
    query = '''
            mutation(
                $id: ID!,
                $lastchange: DateTime!
                $order: Int!
                ) {
                operation: semesterUpdate(semester: {
                id: $id,
                lastchange: $lastchange
                order: $order
            }){
                id
                msg
                entity: semester {
                    id
                    order
                    lastchange
                }
            }
            }
        '''
    order = 2
    context_value = await createContext(async_session_maker)
    variable_values = {"id": id, "order": order, "lastchange": lastchange}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None

    data = resp.data['operation']
    assert data['msg'] == "ok"
    data = data["entity"]
    assert data["order"] == order

    # lastchange je jine, musi fail
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data['operation']
    assert data['msg'] == "fail"

    pass
