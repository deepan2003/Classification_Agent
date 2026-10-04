import pandas as pd
t = pd.read_csv("vireo/out/tagged.csv")
used = pd.read_csv("vireo/out/labelled.csv").ticket_id
t = t[~t.ticket_id.isin(used)].sample(40, random_state=99)
t[["ticket_id", "customer_message", "agent_notes"]].assign(true_tag="").to_csv("vireo/out/to_label_holdout.csv", index=False)