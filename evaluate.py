import pandas as pd
t = pd.read_csv("vireo/out/tagged.csv").sample(50, random_state=7)
t[["ticket_id", "customer_message", "agent_notes"]].assign(true_tag="").to_csv("vireo/out/to_label.csv", index=False)
# Label 'true_tag' by hand in out/to_label.csv, save as out/labelled.csv, then:
# l = pd.read_csv("out/labelled.csv"); print("accuracy:", (l.root_cause == l.true_tag).mean())