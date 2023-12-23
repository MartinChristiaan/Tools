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


prompter = SFzfPrompt()


def prompt(
    choices=[], multi=False, prompt_text=None, return_idx=False, extra_options=""
):
    if len(choices) == 1:
        if return_idx:
            choices = [0]
        if multi:
            return choices
        return choices[0]
    result = prompter.prompt(
        choices, multi, prompt_text, return_idx, extra_options=extra_options
    )
    if len(result) == 0:
        return None
    if not multi:
        return result[0]
    else:
        return result
