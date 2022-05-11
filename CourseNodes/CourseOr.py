import CourseNodes

"""
    Binary boolean composite node that evaluates its left and right children with an 'or'
"""


class CourseOr(CourseNodes.CourseBinary.CourseBinary):
    def __init__(self, left, right) -> None:
        # print("or left:", left)
        # print("or right:", right)
        super().__init__(left, right)

    def evaluate(self, course_list):
        return self.left.evaluate(course_list) or self.right.evaluate(course_list)
