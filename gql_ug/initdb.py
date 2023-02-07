import asyncio
from main import RunOnceAndReturnSessionMaker
from gql_ug.GraphResolvers import importData
from gql_ug.DBDefinitions import ComposeConnectionString
import click


@click.command()
def init():
    print("local init")
    asyncio.run(RunOnceAndReturnSessionMaker())


async def goAndImport():
    sessionMaker = await RunOnceAndReturnSessionMaker()
    await importData(sessionMaker)


async def complexDBImport(modelIndex):
    import json
    from gql_ug.GraphResolvers import datetime_parser, putPredefinedStructuresIntoTable

    sessionMaker = await RunOnceAndReturnSessionMaker()

    print("asyncImport have DBModels", flush=True)
    with open("./extradata/ug_data.json", "r") as f:
        jsonData = json.load(f, object_hook=datetime_parser)
    print("data in json", flush=True)

    try:
        for tableName, DBModel in modelIndex.items():  # iterate over all models
            # get the appropriate data
            DBModel.__tablename__ = tableName  # reflexe tento atribut nema :(
            listData = jsonData.get(tableName, None)
            if listData is None:
                # data does not exists for current model
                print(f"table {tableName} has no data to import", flush=True)
                continue

            print("table", tableName, flush=True)
            # save data - all rows into a table, if a row with same id exists, do not save it nor update it
            try:
                await putPredefinedStructuresIntoTable(
                    sessionMaker, DBModel, lambda: listData
                )
                print(f"table {tableName} import finished", flush=True)
            except Exception as e:
                print("Exception", e, f"on table {tableName}")

    except Exception as e:
        print(e)
    print("*" * 30, flush=True)
    print("data in DB", flush=True)
    print("*" * 30, flush=True)


@click.command()
def loadall():
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import create_engine

    Base = automap_base()
    connectionstring = ComposeConnectionString()
    connectionstring = connectionstring.replace(
        "postgresql+asyncpg", "postgresql+psycopg2"
    )
    engine = create_engine(connectionstring)

    Base.prepare(engine, reflect=True)
    baseClasses = {}
    for item in dir(Base.classes):
        if item.startswith("_"):
            continue
        baseClasses[item] = getattr(Base.classes, item)

    order = [
        "roletypes",
        "grouptypes",
        "users",
        "groups",
        "memberships",
        "roletypes",
        "roles",
        "externalidtypes",
        "externalids",
        "eventtypes",
        "events",
    ]
    # 'answers',
    # 'authorizationgroups', 'authorizationroletypes', 'authorizations', 'authorizationusers', 'authors',
    # 'events', 'eventtypes', 'externalids', 'externalidtypes',
    # 'facilities', 'facilitytypes',
    # 'formitems', 'formparts', 'forms', 'formsections',
    # 'lessons',
    # 'personalitiesCertficates', 'personalitiesCertificateTypes', 'personalitiesMedalTypeGroups', 'personalitiesMedalTypes', 'personalitiesMedals', 'personalitiesRanks',
    # 'personalitiesRelatedDocs', 'personalitiesStudies', 'personalitiesWorkHistories',
    # 'projectFinanceTypes', 'projectFinances', 'projectMilestones', 'projectTypes', 'projects', 'publication_types', 'publications',
    # 'questionTypes', 'questions', 'roles', 'roletypes', 'subjects', 'surveys', 'users', 'workflows', 'workflowstateroletypes', 'workflowstates', 'workflowstateusers'

    orderedDBClasses = {}
    for item in order:
        orderedDBClasses[item] = baseClasses[item]

    print("start to load")
    asyncio.run(complexDBImport(orderedDBClasses))
    print("finished")
    pass


@click.command()
def load():
    print("load")
    asyncio.run(goAndImport())
    pass


@click.command()
def save():
    print("save")
    pass


@click.group()
def cli():
    pass


cli.add_command(init)
cli.add_command(load)
cli.add_command(loadall)
cli.add_command(save)


cli()
