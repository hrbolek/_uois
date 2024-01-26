import pytest
import logging
import jwt

@pytest.mark.asyncio
async def test_publickey(DemoFalse, FastAPIClient, Publickey):
    # logging.info(f"AccessToken is {AccessToken}")
    logging.info(f"Publickey is {Publickey}")
    # response = FastAPIClient.post("/gql", headers=headers, json=json)



@pytest.mark.asyncio
async def test_admintoken(DemoFalse, Publickey, AdminToken):
    # logging.info(f"AccessToken is {AccessToken}")
    logging.info(f"Publickey is {Publickey}")
    key = Publickey.replace('"', '').replace('\\n', '\n').encode("ascii")
    logging.info(f"AdminToken is {AdminToken}")
    # response = FastAPIClient.post("/gql", headers=headers, json=json)
    decodedjwt = jwt.decode(jwt=AdminToken, key=key, algorithms=["RS256"])
    logging.info(f"jwt is {decodedjwt}")
    userid = decodedjwt["user_id"]
    logging.info(f"userid is {userid}")


@pytest.mark.asyncio
async def test_app_index(DemoFalse, FastAPIClient):
    # logging.info(f"AccessToken is {AccessToken}")
    response = FastAPIClient.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_app_index(DemoTrue, FastAPIClient):
    # logging.info(f"AccessToken is {AccessToken}")
    response = FastAPIClient.get("/")
    assert response.status_code == 200



# pytest --cov-report term-missing --cov=server tests --log-cli-level=INFO -x
    
