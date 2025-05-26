import os

import requests  # type: ignore
import toml

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "env.toml")
config = toml.load(ENV_PATH)

HASURA_ENDPOINT = config["hasura"]["HASURA_ENDPOINT"]
HASURA_ADMIN_SECRET = config["hasura"]["HASURA_ADMIN_SECRET"]


def get_user_scores_with_category_names(user_id):
    """Return a dictionary of areas and scores for a user."""
    # user_id = "00000000-0000-0000-0000-000000000001"
    query = """
    query ObtenerPuntajes($createdBy: uuid!) {
      userQuestionAnswers(
        where: {
          createdBy: { _eq: $createdBy },
          selection: { _eq: true }
        }
      ) {
        question {
          skillCategoryCatalog {
            description
          }
        }
      }
    }
    """
    variables = {"createdBy": user_id}

    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": HASURA_ADMIN_SECRET,
    }

    response = requests.post(
        HASURA_ENDPOINT, json={"query": query, "variables": variables}, headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"Hasura error: {response.status_code} {response.text}")

    data = response.json()

    # Contar respuestas por nombre de categoría
    category_scores = {}
    answers = data["data"]["userQuestionAnswers"]

    for answer in answers:
        category_name = answer["question"]["skillCategoryCatalog"]["description"]
        if category_name in category_scores:
            category_scores[category_name] += 1
        else:
            category_scores[category_name] = 1

    return category_scores
