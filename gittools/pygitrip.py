# %%
import subprocess


# Execute gitrip and get output
def gitrip(*args):
    return subprocess.check_output(["bash", "gitrip.sh"]).decode("utf-8")


print(gitrip())
