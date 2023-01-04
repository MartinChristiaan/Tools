
import os
import json

# convert file to snippet and add them to list!
# File content is body file name is prefix
home = os.path.expanduser('~')

folder = "snippets"
snippet_path = "python.json"

with open(snippet_path, 'r') as f:
	text = f.read()
snippet_dict = json.loads(text)


for filename in os.listdir(folder):
	with open(f'{folder}/{filename}', 'r') as f:
		body = f.read()
	
	snippets = body.split("#")
	print(snippets)
	for snippet in snippets:
		if len(snippet) == 0:
			continue
		
		body_lines = [x for x in snippet.split("\n") if len(x) > 0]
		prefix = body_lines[0].replace(' ',"")
		snippet = dict(
			prefix=prefix,
			scope="python",
			body=body_lines,
			description=prefix
		)
		snippet_dict[prefix] = snippet
out_string = json.dumps(snippet_dict,indent=4)
snippet_path_code = f"{home}/.config/Code/User/snippets/python.json"
print(snippet_path_code)
with open(snippet_path_code, 'w') as f:
	f.write(out_string)

