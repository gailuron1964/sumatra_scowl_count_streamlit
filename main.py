import textwrap
from sumatra import Client
import streamlit as st
import pandas as pd
from style import customize_styling

BRANCH_NAME = "tmp_workshop"

client = Client('console.qa.sumatra.ai')

@st.cache
def setup():
  try:
    client.get_branch(BRANCH_NAME)
  except Exception:
    client.create_branch_from_scowl(textwrap.dedent("""
      event login
      user := $.user as string
      ip := $.ip as string
    """), BRANCH_NAME)
    client.create_timeline_from_file('attack', 'attack.jsonl')

setup()

query = """
query EnrichTimelineQuery($id: String!, $features: [String]!, $defs: [Def]!, $start: DateTime!, $end: DateTime!) {{
  timeline(id: $id) {{
    enrich(
      branch: "{0}"
      features: $features
      defs: $defs
      filters: []
      hidden: []
      start: $start
      end: $end
    ) {{
      times
      features {{
        id
        values
        errors
      }}
    }}
  }}
}}
""".format(BRANCH_NAME)

default_value = st.experimental_get_query_params().get("scowl", ["CountUnique(user by ip)"])[0]
scowl = st.text_input(label="Scowl Expression", value=default_value)

variables = {
  'id': 'attack',
  'features': ['login.ip', 'login.user', 'login._'],
  'defs': [{'name': 'login.user', 'definition': '$.user as string'}, {'name': 'login.ip', 'definition': '$.ip as string'}, {'name': 'login._', 'definition': scowl}],
  'start': '2021-04-12T22:43:45Z',
  'end': '2021-04-12T22:44:20Z'
}

cols = {}
ret = client._gql_client.execute(query=query, variables=variables)
if 'errors' in ret:
  st.write(ret['errors'][0]['message'])
else:
  for feature in ret['data']['timeline']['enrich']['features']:
    name = feature['id'].split('.')[1]
    if name == '_':
      name = scowl
    cols[name] = feature['values']
  df = pd.DataFrame(cols, index=ret['data']['timeline']['enrich']['times'])[['ip', 'user', scowl]]
  st.write(df)

customize_styling()
