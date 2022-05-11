import CourseNodes

"""
    Binary boolean composite node that evaluates its left and right children with an 'and'
"""


class CourseAnd(CourseNodes.CourseBinary.CourseBinary):
    def __init__(self, left, right) -> None:
        super().__init__(left, right)

    def evaluate(self, course_list):
        return self.left.evaluate(course_list) and self.right.evaluate(course_list)
