import CourseNodes


class CourseAnd(CourseNodes.CourseBinary.CourseBinary):
    def __init__(self, left, right) -> None:
        # print("and left:", left)
        # print("and right:", right)
        super().__init__(left, right)

    def evaluate(self, course_list):
        return self.left.evaluate(course_list) and self.right.evaluate(course_list)
