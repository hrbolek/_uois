docker build --tag build_js_doc --file DockerfileJsDoc .
REM docker run -i -t -v ./docs:/usr/src/app/docs --name  build_js_doc build_js_doc 
REM docker run -i -t -v ./docs:/usr/src/app/docs --name  build_js_doc --entrypoint sh build_js_doc 
docker run -i -t --mount source="docs",target="/usr/src/app/docs" --name  build_js_doc --entrypoint sh build_js_doc 
pause
docker rm build_js_doc 
pause