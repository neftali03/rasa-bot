import os

import requests  # type: ignore
import toml

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "env.toml")
config = toml.load(ENV_PATH)

HASURA_ENDPOINT = config["hasura"]["HASURA_ENDPOINT"]
HASURA_ADMIN_SECRET = config["hasura"]["HASURA_ADMIN_SECRET"]


def fetch_questions():
    """Get the questions from the database."""
    query = """
        query {
            questions {
                id
                description
            }
        }
    """

    headers = {
        "Content-Type": "application/json",
    }

    if HASURA_ADMIN_SECRET:
        headers["x-hasura-admin-secret"] = HASURA_ADMIN_SECRET

    response = requests.post(HASURA_ENDPOINT, json={"query": query}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "data" in data and "questions" in data["data"]:
            return data["data"]["questions"]
        else:
            raise Exception(f"Respuesta inesperada de Hasura: {data}")
