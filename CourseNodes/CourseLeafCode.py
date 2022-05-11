import re
import CourseNodes

"""
	Object that evaluates course condition statements that require a certain course code prerequisite.
"""


class CourseLeafCode(CourseNodes.CourseLeaf.CourseLeaf):
    def __init__(self, course) -> None:
        course_name = ''
        # if course condition is empty (e.g. COMP1511), do nothing
        if len(course) > 0:
            # Filter out any unessecary words
            # e.g. "Prerequisite: COMP3121" -> COMP3121
            for phrase in course:
                for word in phrase.split():
                    if re.match(r'\D*\d\d\d\d\D*', word):
                        course_name = word

        super().__init__(course_name)

    # Determines whether a certain course has been done already
    def evaluate(self, course_list):
        # If condition is empty, return True
        if not self.course:
            return True
        # If course code is in the course_list, return True
        elif self.course.lower() in ' '.join(course_list).lower():
            return True
        # If course number is in course_list, return True
        elif self.course[3:] in ' '.join(course_list):
            return True
        # Course has not been done, return False
        return False
