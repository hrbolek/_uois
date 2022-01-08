docker build --tag tools .
REM docker run --name tools --rm -v ./output:/output -a stdout -a stderr tools
docker run --name tools --rm -v C:\develop\_docker\_uois\tools\output:/output -a stdout -a stderr tools

pause