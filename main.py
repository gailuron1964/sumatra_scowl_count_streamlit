from sumatra import Client
import streamlit as st
from env import setup_env

TOPOLOGY = """
event login

user := $.user as string
ip := $.ip as string
count := Count()
count_by_ip := Count(by ip)
count_by_ip_user := Count(by ip, user)
"""

setup_env()
sumatra = Client('console.qa.sumatra.ai')

sumatra.create_branch_from_scowl(TOPOLOGY)

sumatra.create_timeline_from_file('attack', 'attack.jsonl')
materialization = sumatra.materialize(timeline='attack')

logins = materialization.get_events("login")
st.write(logins[['user', 'ip', 'count', 'count_by_ip', 'count_by_ip_user']])
