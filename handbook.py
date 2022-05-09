"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: We do not expect you to come up with a perfect solution. We are more interested
in how you would approach a problem like this.
"""
import json
from pprint import pprint
from CourseNodes.CourseGenerator import generate_course, seperate_blocks

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()


def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.

    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """

    """
    Tree will be a dictionary of courses. The key is the course name, the value is an array
    where if any element is 'evaluated' to true, then the course is unlockable
    e.g.
    {
        "COMP1511" : [True],
        "COMP2511" : ["COMP1511", "DPST1091", "COMP1917", "COMP1921"],
        "COMP2511" : []
    }
    """

    target_condition = CONDITIONS[target_course]
    if not target_condition:
        return True

    condition_arr = seperate_blocks(target_condition)
    # print("a:", condition_arr)
    target = generate_course(condition_arr)

    # print("hb:", courses_list)
    return target.evaluate(courses_list)


if __name__ == "__main__":
    print(is_unlocked(["COMP1511", "COMP6841",
          "COMP6443", "COMP6447"], "COMP9302"))
