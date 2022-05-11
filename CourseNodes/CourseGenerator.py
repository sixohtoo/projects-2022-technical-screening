import CourseNodes

"""
courses_list 
"""

"""
    Factory function used to generate composite CourseNodes depending on what the condition is.
    e.g. 
        "COMP1511 or COMP1531" will return a CourseOr.
        "COMP1511 and COMP1531" will return a CourseAnd.
        "Prerequistite: COMP2041" will return a CourseLeafCode
        "36 units of credit in COMP courses" will return a CourseLeafUnits
"""


def generate_course(condition):
    condition_str = ''

    if condition:
        # Check if an 'and' or 'or' is outside of any brackets
        # which will generate a CourseAnd or CourseOr.
        for i, text in enumerate(condition):
            if text.lower() == "and":
                return CourseNodes.CourseAnd.CourseAnd(condition[:i], condition[i + 1:])
            if text.lower() == "or":
                return CourseNodes.CourseOr.CourseOr(condition[:i], condition[i + 1:])

        condition_str = ' '.join(condition)

        # Check if outer pair of brackets belong with a 'units of credit' statement.
        # If they do then these brackets shouldn't be removed.
        if not check_can_remove_outer_brackets(condition_str):
            return CourseNodes.CourseLeafUnits.CourseLeafUnits(seperate_blocks(condition_str))

        # Removes the outer brackets from the condition
        condition_str = remove_outer_brackets(condition)

        # Seperate condition back into an array which evaluates to booleans
        condition = seperate_blocks(condition_str)

        # Check if an 'and' or 'or' is outside of any brackets
        # whih will generate a CourseAnd or CourseOr
        for i, text in enumerate(condition):
            if text.lower() == "and":
                return CourseNodes.CourseAnd.CourseAnd(condition[:i], condition[i + 1:])
            if text.lower() == "or":
                return CourseNodes.CourseOr.CourseOr(condition[:i], condition[i + 1:])

    # Creates a composite leaf node which can be evaluated to either true or false
    # CourseLeafUnits is for any uoc requirement (e.g. "36 units of credit in COMP courses")
    # CourseLeafCode is for any course code requirement (e.g. "COMP3121")
    if "units" in condition_str:
        return CourseNodes.CourseLeafUnits.CourseLeafUnits(seperate_blocks(condition_str))
    else:
        return CourseNodes.CourseLeafCode.CourseLeafCode(seperate_blocks(condition_str))


"""
    Checks if brackets are part of a 'units' statement.
    Returns true uf brackets should be removed, and False if they shouldn't
    e.g.
        "6 units of credit in (COMP6443, COMP6843)" -> True because outer brackets are part of 'unit statement'
        "(COMP3121 and 12 units of credit in (COMP3311, COMP3331, COMP2041))" -> False because outer brackets are part of 'binary statement'
"""


def check_can_remove_outer_brackets(condition_str):
    if "units" not in condition_str:
        return True
    elif "(" not in condition_str:
        return True
    open_bracket_pos = condition_str.find('(')
    units_pos = condition_str.find('units')

    # Check if brackets is part of a 'units' statement.
    # If 'units' appears before the open bracket, then shouldn't remove the open brackets
    return open_bracket_pos < units_pos


"""
    Removes the outer brackets from a string.
    e.g. ["(A or B)"] -> "A or B"
"""


def remove_outer_brackets(condition):
    condition_str = ' '.join(condition)
    open_bracket_pos = condition_str.find('(')
    if open_bracket_pos != -1:
        close_bracket_pos = condition_str.rfind(')')
        condition_str = condition_str[:open_bracket_pos] \
            + condition_str[open_bracket_pos + 1: close_bracket_pos] \
            + condition_str[close_bracket_pos + 1:]

    return condition_str


"""
    Seperates a string into an array of conditions which evaluate down to booleans
    "A or B or C" -> ["A", "or", "B", "or", "C"]
    "A and (B or C)" -> ["A", "and", "(B or C)"]
"""


def seperate_blocks(condition):
    # If a course has an empty condition string (e.g. COMP1511), return empty array
    if not condition:
        return []

    condition_arr = condition.split()

    # If course only has 1 requirement (e.g. "MATH1081"), no need to split into blocks
    if len(condition_arr) == 1:
        return condition_arr

    final_arr = []

    index = 0
    in_brackets = 0
    skip_word = False
    # Loop through each word in condition statement
    for word in condition_arr:
        # Loop through each letter to check how many levels of brackets this word is in
        # Should leave anything in brackets in the same block (only split words outside of brackets)
        for letter in word:
            if letter == '(':
                in_brackets += 1
            elif letter == ')':
                in_brackets -= 1
                skip_word = True

        # Skip word if currently in brackets
        if in_brackets or skip_word:
            skip_word = False
            index += 1
            continue
        # If word is 'and' or 'or' then add left condition to the new array,
        # add the operation and then cut condition_arr to after this word
        elif word.lower() in ['or', 'and']:
            final_arr.append(' '.join(condition_arr[:index]))
            final_arr.append(word.lower())
            condition_arr = condition_arr[index + 1:]
            index = -1

        index += 1
    final_arr.append(' '.join(condition_arr))
    return final_arr
