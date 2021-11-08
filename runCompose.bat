set COMPOSE_CONVERT_WINDOWS_PATHS=1
docker-compose -p app2 up -d --build
pause
docker-compose -p app2 down
