import json
from io import StringIO

st = StringIO()
df.to_csv(st, index=False, line_terminator="\n")

data = {
    "name": "essai1",
    "format": "df",
    "team": "5",
    "project": "tgtg",
    "password": "Ensae06CPdist",
    "content": st.getvalue(),
}
print(json.dumps(data))