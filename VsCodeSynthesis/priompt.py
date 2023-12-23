from pyfzf import FzfPrompt


def select_option_with_prompt(choices, prompt_text):
    fzf = FzfPrompt()
    selected_option = fzf.prompt(choices, f'--prompt "{prompt_text}"')
    return selected_option


# Example usage
if __name__ == "__main__":
    options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    prompt = "Select an option:"
    selected_option = select_option_with_prompt(options, prompt)

    if selected_option:
        print("Selected option:", selected_option[0])
    else:
        print("No option selected.")
