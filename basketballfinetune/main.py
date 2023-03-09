import csv
import json

with open('basketball_data.csv') as f:
    reader = csv.DictReader(f)
    prompt_completion_pairs = []
    for row in reader:
        prompt = f"Generate a summary for {row['Player']}'s performance in the {row['Team']} team."
        completion = f"{row['Player']} played {row['GP  Games played']} games and started in {row['GS  Games started']} of them. They averaged {row['MPG  Minutes Per Game']} minutes per game ."

        prompt_completion_pairs.append({"prompt": prompt, "completion": completion})

with open('basketball_summary.json', 'w') as f:
    json.dump(prompt_completion_pairs, f)
