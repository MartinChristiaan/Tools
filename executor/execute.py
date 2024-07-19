import os
import sys

# Note
# May need to move to appropriate directory...


path = sys.argv[1]
extension = path.split(".")[-1]


def find_python_rootdir(path):
    root = "/".join(path.split("/")[:-1])
    while True:
        if "__init__.py" in os.listdir(root):
            break
        else:
            root = "/".join(root.split("/")[:-1])
        if len(root.split("/")) == 1:
            root = "/".join(path.split("/")[:-1])
            break
    return root


if extension == "py":
    root = find_python_rootdir(path)
    pypath = path.replace(root, "").replace(".py", "").replace("/", ".")
    if pypath.startswith("."):
        pypath = pypath[1:]
    cmd = f"cd {root} && python3 -m {pypath}"
    print(f"Executing {cmd}")
    os.system(f"cd {root} && python3 -m {pypath}")
else:
    root = "/".join(path.split("/")[:-1])
    bashpath = path.replace(root, "")[1:]
    os.system(f"cd {root} && bash {bashpath}")
