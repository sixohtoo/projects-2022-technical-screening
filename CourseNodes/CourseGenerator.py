import CourseNodes

"""
courses_list 
"""


def generate_course(condition):
    # print("gc:", condition)
    condition_str = ''
    if condition:
        for i, text in enumerate(condition):
            if text.lower() == "and":
                return CourseNodes.CourseAnd.CourseAnd(condition[:i], condition[i + 1:])
            if text.lower() == "or":
                return CourseNodes.CourseOr.CourseOr(condition[:i], condition[i + 1:])
            if text.lower() == "units":
                return CourseNodes.CourseLeafUnits.CourseLeafUnits(condition)
        condition_str = ' '.join(condition)
        # condition_str = ' '.join(condition)
        # open_bracket_pos = condition_str.find('(')
        # if open_bracket_pos != -1:
        #     close_bracket_pos = condition_str.rfind(')')
        #     condition_str = condition_str[:open_bracket_pos] \
        #         + condition_str[open_bracket_pos + 1: close_bracket_pos] \
        #         + condition_str[close_bracket_pos + 1:]
        # print("condtion:", condition_str)
        if not check_can_remove_outer_brackets(condition_str):
            # print("yeeted")
            return CourseNodes.CourseLeafUnits.CourseLeafUnits(seperate_blocks(condition_str))
        # print("condtion:", condition_str)
        condition_str = remove_outer_brackets(condition)
        # print("cs:", condition_str)
        condition = seperate_blocks(condition_str)
        # print("GC:", condition)
        for i, text in enumerate(condition):
            if text.lower() == "and":
                return CourseNodes.CourseAnd.CourseAnd(condition[:i], condition[i + 1:])
            if text.lower() == "or":
                return CourseNodes.CourseOr.CourseOr(condition[:i], condition[i + 1:])
            if text.lower() == "units":
                return CourseNodes.CourseLeafUnits.CourseLeafUnits(condition)

    # print("cs:", condition_str)
    # print("sb:", seperate_blocks(condition_str))
    if "units" in condition_str:
        return CourseNodes.CourseLeafUnits.CourseLeafUnits(seperate_blocks(condition_str))
    else:
        return CourseNodes.CourseLeafCode.CourseLeafCode(seperate_blocks(condition_str))


"""
    Checks if brackets are part of a 'units' statement.
    Returns true if bracket should not be removed and false if they should be.
    e.g.
        "6 units of credit in (COMP6443, COMP6843)" -> False because outer brackets are part of 'unit statement'
        "(COMP3121 and 12 units of credit in (COMP3311, COMP3331, COMP2041))" -> True because outer brackets are part of 'binary statement'
"""


def check_can_remove_outer_brackets(condition_str):
    # print("bean", condition_str)
    if "units" not in condition_str:
        return True
    elif "(" not in condition_str:
        return True
    # print("here")
    open_bracket_pos = condition_str.find('(')
    units_pos = condition_str.find('units')
    return open_bracket_pos < units_pos


def remove_outer_brackets(condition):
    condition_str = ' '.join(condition)
    open_bracket_pos = condition_str.find('(')
    if open_bracket_pos != -1:
        close_bracket_pos = condition_str.rfind(')')
        condition_str = condition_str[:open_bracket_pos] \
            + condition_str[open_bracket_pos + 1: close_bracket_pos] \
            + condition_str[close_bracket_pos + 1:]

    return condition_str


def seperate_blocks(condition):
    if not condition:
        return []

    condition_arr = condition.split()

    if len(condition_arr) == 1:
        return condition_arr

    final_arr = []

    index = 0
    in_brackets = 0
    skip_word = False
    for word in condition_arr:
        # Loop through word
        for letter in word:
            if letter == '(':
                in_brackets += 1
            elif letter == ')':
                in_brackets -= 1
                skip_word = True

        if in_brackets or skip_word:
            skip_word = False
            index += 1
            continue
        elif word.lower() == 'or':
            final_arr.append(' '.join(condition_arr[:index]))
            final_arr.append('or')
            condition_arr = condition_arr[index + 1:]
            index = -1
        elif word.lower() == 'and':
            final_arr.append(' '.join(condition_arr[:index]))
            final_arr.append('and')
            condition_arr = condition_arr[index + 1:]
            index = -1
        index += 1
    final_arr.append(' '.join(condition_arr))
    # print(final_arr)

    return final_arr
