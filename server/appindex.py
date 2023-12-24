import json
from fastapi import Request
from fastapi.responses import HTMLResponse

def loadMD(relativeFileName):
    from .main import dirName
    fullName = dirName + "/htmls/" + relativeFileName
    lines = []
    try:
        with open(fullName, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        pass
    return ''.join(lines)

def createCard(link, data):
    result = f"""<div class="card">
  <h2 class="card-header"><a href="/{link}/">{data["title"]}</a></h2>
  <div class="card-body">
    <md-block>{loadMD(data["markdownfile"])}</md-block>
  </div>
  <div class="card-footer">
    By {data["authors"]}
  </div>
</div>"""
    return result

async def createIndexResponse(request: Request):
    from .main import configFile
    body = ""
    with open(configFile, "r", encoding="utf-8") as f:
        config = json.load(f)
        for key, value in config.items():
            body = body + f'<div class="col col-md-3">{createCard(key, value)}</div>'

    result = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>IS Index</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>    
    <script type="module" src="https://md-block.verou.me/md-block.js"></script>
  </head>
  <body>
    <div class="container-fluid">
        <div class="row">
            {body}
        </div>    
    </div>    
  </body>
</html>
"""
    return HTMLResponse(result)