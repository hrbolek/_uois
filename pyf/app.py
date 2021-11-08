from fastapi import FastAPI, Request

import models.BaseEntities as BEntities
import models.BaseEntityTypes as BETypes
import sqlengine.sqlengine as SqlEngine

import fastapiapp
import graphqlapp

#app = FastAPI(root_path="/apif")
app = FastAPI()


fastapiapp.attachFastApi(app)
graphqlapp.attachGraphQL(app)
