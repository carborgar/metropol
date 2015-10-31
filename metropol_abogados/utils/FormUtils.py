def add_extra_choices(original_choices, choices_to_add):
    original_choices.extend(choices_to_add)
    return original_choices


def get_sorted_choices(choices):
    return sorted(choices, key=lambda tup: str(tup[1]))
