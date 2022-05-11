import CourseNodes
import re

"""
	Object that evaluates course condition statements that require a certain number of units.
"""


class CourseLeafUnits(CourseNodes.CourseLeaf.CourseLeaf):
    def __init__(self, course) -> None:
        rules = {}

        course_str = ' '.join(course)
        pattern = re.compile("(\d+)\s+units")

        # rules["uoc"] stores number of units needed
        rules["uoc"] = int(pattern.findall(course_str)[0])

        pattern = re.compile("(\d+)?\s+([A-Z]{4})\s+courses")
        result = pattern.findall(course_str)

        # Deal with any conditions that are only valid with a subset of courses
        # e.g. "18 units oc credit in (COMP9417, COMP9418, COMP9444, COMP9447)"
        if '(' in course_str:
            # Regex to extract text from inside the brackets
            pattern = re.compile("\((.*)\)")
            allowed_courses_str = pattern.findall(course_str)[0]
            # rules["allowed_courses"] is a set of all valid courses for the condition
            # e.g. set("COMP6443",  "COMP6843", "COMP6445", "COMP6845", "COMP6447")
            rules["allowed_courses"] = set(
                re.split(',\s*', allowed_courses_str))
            # Deal with any conditions where only faculty/type is specified
            # e.g. "36 units of credit in COMP courses"
        elif result and len(result[0]) == 1:
            rules["level"] = ""
            rules["type"] = result[0][0]
            # Deal with any conditions where type and level are specified
            # e.g. "12 units of credit in level 3 COMP courses"
        elif result and len(result[0]) == 2:
            rules["level"] = result[0][0]
            rules["type"] = result[0][1]

        super().__init__(rules)

    def evaluate(self, course_list):
        units = 0

        # Evaluate conditions that require a certain level/prefix.
        if "level" in self.course:
            allowed = self.course["type"] + self.course["level"]
            units = len([x for x in course_list if x.startswith(allowed)]) * 6
            # Evaluate condition that require a certain subset of courses
        elif "allowed_courses" in self.course:
            units = len(
                [x for x in course_list if x in self.course["allowed_courses"]]) * 6
            # Evaluate condition that only requires a certain number of units
        else:
            units = len(course_list) * 6

        return units >= self.course["uoc"]
