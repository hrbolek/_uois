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
    query = 'query{programTypeById(id: "' + row['id'] + '''") { 
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
    resp = await schema.execute(query, context_value=context_value)
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
    query = 'query{programLanguageById(id: "' + row['id'] + '''") { 
        id
        name
        nameEn
        lastchange
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
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
    query = 'query{programFormById(id: "' + row['id'] + '''") { 
        id
        name
        nameEn
        lastchange
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
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
    query = 'query{programTitleById(id: "' + row['id'] + '''") { 
        id
        name
        nameEn
        lastchange
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
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
    query = 'query{programLevelById(id: "' + row['id'] + '''") { 
        id
        name
        nameEn
        lastchange
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
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
    query = 'query{acsubjectById(id: "' + row['id'] + '''") { 
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
    resp = await schema.execute(query, context_value=context_value)
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
    query = 'query{acsemesterById(id: "' + row['id'] + '''") { 
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
    resp = await schema.execute(query, context_value=context_value)
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
    query = 'query{acsemesterById(id: "' + row['id'] + '''") { 
        id
        classifications { 
            id
            lastchange
            user { id }
            level { id name nameEn }
            type { id name nameEn }
            semester { id }
        }
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
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
    query = 'query{actopicById(id: "' + row['id'] + '''") { 
        id
        name
        nameEn
        lastchange
        order
        semester { id }
        lessons { id }
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
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
    query = 'query{aclessonById(id: "' + row['id'] + '''") { 
        id
        count
        lastchange
        topic { id }
        type { id }
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
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
    query = 'query{aclessonTypeById(id: "' + row['id'] + '''") { 
        id
        name
        nameEn
        lastchange
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data
    data = data['aclessonTypeById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']
    #for topic in data['topics']:
    #    assert topic['semester']['id'] == row['id']
