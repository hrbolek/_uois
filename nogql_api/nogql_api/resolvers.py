from fastapi import FastAPI, File, UploadFile, Request, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from typing import List
import tempfile

from io import BytesIO
from tempfile import NamedTemporaryFile
import openpyxl
from copy import copy
import datetime


async def create_upload_files(files: List[UploadFile]):

    result = []
    for file in files:
        content = await file.read()
        memory = BytesIO(content)
        wb = openpyxl.load_workbook(filename=memory, read_only=True)
        ws = wb["DataCelyRok"]

        for index, row in enumerate(ws.rows):
            if index == 0:
                continue

            names = ["name", "month", "date", "desc", "hours"]
            newRow = dict(zip(names, map(lambda item: item.value, row)))
            if newRow["date"] is None:
                print("has no date", newRow)
            elif not isinstance(newRow["date"], datetime.datetime):
                print("date has bad type", newRow)
            else:
                result.append(newRow)

    with open("vzor.xlsx", "rb") as f:
        content = f.read()

    memory = BytesIO(content)
    resultFile = openpyxl.load_workbook(filename=memory)

    resultFileCelyRok = resultFile["DataCelyRok"]
    resultFileWs = resultFile["ProTisk"]

    prevName = None
    prevMonth = None
    rowIndex = 16
    for item in result:
        currentName = item["name"]
        currentMonth = item["date"].month
        if (currentName != prevName) or (currentMonth != prevMonth):
            # print(currentName, currentMonth)
            currentWs = resultFile.copy_worksheet(resultFileWs)
            currentWs.title = f"{currentName}_{currentMonth}"
            rowIndex = 16

            print(currentName)

            names = currentName.split(" ")
            currentWs[f"B10"] = names[0]
            currentWs[f"B11"] = names[1]

            currentWs[f"C12"] = datetime.datetime(
                year=item["date"].year, month=item["date"].month, day=1
            )
            if item["date"].month == 12:
                currentWs[f"E12"] = datetime.datetime(
                    year=item["date"].year + 1, month=1, day=1
                ) + datetime.timedelta(days=-1)
            else:
                currentWs[f"E12"] = datetime.datetime(
                    year=item["date"].year, month=item["date"].month + 1, day=1
                ) + datetime.timedelta(days=-1)

            prevName = currentName
            prevMonth = currentMonth

        # currentWs.insert_rows(rowIndex)
        currentWs[f"A{rowIndex}"] = item["date"]
        currentWs[f"B{rowIndex}"] = item["desc"]
        currentWs[f"F{rowIndex}"] = item["hours"]
        # for col in ['A', 'B', 'C', 'D', 'E', 'F']:
        #    currentWs[f'{col}{rowIndex}']._style = copy(currentWs[f'{col}{rowIndex+1}']._style)
        rowIndex = rowIndex + 1

        resultFileCelyRok.insert_rows(2)
        resultFileCelyRok["A2"] = currentName
        resultFileCelyRok["B2"] = item["date"].month
        resultFileCelyRok["C2"] = item["date"]
        resultFileCelyRok["D2"] = item["desc"]
        resultFileCelyRok["E2"] = item["hours"]
        for col in ["A", "B", "C", "D", "E", "F"]:
            resultFileCelyRok[f"{col}2"]._style = copy(
                resultFileCelyRok[f"{col}3"]._style
            )
        # resultFileCelyRok.append([currentName, item['month'], item['date'], item['desc'], item['hours']])

    with NamedTemporaryFile() as tmp:
        resultFile.save(tmp.name)
        tmp.seek(0)
        stream = tmp.read()
        headers = {"Content-Disposition": 'attachment; filename="VsechnyVykazy.xlsx"'}
        return Response(stream, media_type="application/vnd.ms-excel", headers=headers)


async def exportSchema():
    from sqlalchemy_schemadisplay import create_uml_graph
    from sqlalchemy import MetaData
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import create_engine

    from nogql_api.DBDefinitions import ComposeConnectionString

    Base = automap_base()
    connectionstring = ComposeConnectionString()
    connectionstring = connectionstring.replace(
        "postgresql+asyncpg", "postgresql+psycopg2"
    )
    engine = create_engine(connectionstring)

    print("Extracting metadata ...")
    Base.prepare(
        engine,
        reflect=True,
        # classname_for_table=fromTableToModelName,
        # name_for_collection_relationship=fromTableToRelationNName,
        # name_for_scalar_relationship=fromTableToRelation1Name
    )

    print("Creating graph for UML ...")

    def getModels(SQLAlchemyBase=Base):
        baseClasses = SQLAlchemyBase.classes
        result = []
        for item in dir(baseClasses):
            if item.startswith("_"):
                continue
            result.append(getattr(baseClasses, item))
        return result

    mappers = [cls.__mapper__ for cls in getModels(SQLAlchemyBase=Base)]
    graph = create_uml_graph(
        mappers,
        show_operations=False,  # not necessary in this case
        show_multiplicity_one=False,  # some people like to see the ones, some don't
    )
    print("Writing UML...")

    with NamedTemporaryFile() as tmp:
        # graph.write_png('/output/img/uml.png') # write out the file
        # graph.write_svg('/output/img/uml.svg') # write out the file
        # graph.write_svg('/output/img/uml.svg') # write out the file
        graph.write_svg(tmp.name)
        tmp.seek(0)
        stream = tmp.read()
        # headers = {
        #    'Content-Disposition': 'attachment; filename="uml.svg"'
        # }
        return Response(stream, media_type="image/svg+xml")  # , headers=headers)
