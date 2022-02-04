set COMPOSE_CONVERT_WINDOWS_PATHS=1
docker-compose -p docs -f docker-compose.doc.yml up -d --build 
pause
docker-compose -p docs -f docker-compose.doc.yml down 
