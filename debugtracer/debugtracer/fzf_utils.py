from pathlib import Path

from pyfzf import FzfPrompt


class SFzfPrompt(FzfPrompt):
    def prompt(
        self,
        choices=[],
        multi=False,
        prompt_text=None,
        return_idx=False,
        extra_options="",
    ):
        fzf_options = ""
        if multi:
            fzf_options += "--multi "
        if not prompt_text is None:
            fzf_options += f'--prompt "{prompt_text} : "'
        fzf_options += extra_options
        if return_idx:
            return self.prompt_index(choices, fzf_options)
        else:
            return super().prompt(choices, fzf_options)

    def prompt_index(self, choices, fzf_options=""):
        choices_str = [str(x) for x in choices]
        selection = self.prompt(choices_str, fzf_options)
        indices = []
        for x in selection:
            indices.append(choices_str.index(x))
        return indices


CACHEPATH = Path(f"{__file__}/fzfcache/")


def get_recent_choices(name: str):
    cache_path = CACHEPATH / name
    if cache_path.exists():
        with open(cache_path, "r") as f:
            text = f.read()
        return text.split("\n")
    else:
        return []


def write_to_cache(name: str, item: str, max_length: int):
    cache_path = CACHEPATH / name

    # Read the existing cache if it exists
    if cache_path.exists():
        with open(cache_path, "r") as f:
            lines = f.readlines()
    else:
        lines = []

    # Append the new item to the cache
    lines.append(item)

    # If the cache exceeds the maximum length, drop older items
    if len(lines) > max_length:
        lines = lines[-max_length:]
    cache_path.parent.mkdir(exist_ok=True, parents=True)
    # Write the updated cache back to the file
    with open(cache_path, "w") as f:
        f.writelines(lines)


prompter = SFzfPrompt()


def prompt(
    choices=[],
    multi=False,
    prompt_text=None,
    return_idx=False,
    extra_options="",
    cachename=None,
):
    if not cachename is None:
        choices += get_recent_choices(cachename)
    if len(choices) == 1:
        if return_idx:
            choices = [0]
        if multi:
            return choices
        return choices[0]
    result = prompter.prompt(
        choices, multi, prompt_text, return_idx, extra_options=extra_options
    )
    if not cachename is None:
        for item in result:
            write_to_cache(cachename, item, 100)
    if len(result) == 0:
        return None
    if not multi:
        return result[0]
    else:
        return result
