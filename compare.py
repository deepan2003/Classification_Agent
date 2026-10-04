import pandas as pd
l = pd.read_csv("vireo/out/labelled.csv")
ai = pd.read_csv("vireo/out/tagged.csv")[["ticket_id", "root_cause"]]
m = l.merge(ai, on="ticket_id")
print("accuracy:", (m.root_cause == m.true_tag).mean())
print(m[m.root_cause != m.true_tag][["ticket_id", "true_tag", "root_cause"]])