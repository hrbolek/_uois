import main
import uvicorn
main.connectionString = "sqlite+aiosqlite:///:memory:"

app = main.app
uvicorn.run(app)