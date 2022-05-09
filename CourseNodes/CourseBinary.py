import CourseNodes


class CourseBinary(CourseNodes.Course.Course):
    # Left and right are arrays
    # presq: (a or b) and c
    def __init__(self, left, right) -> None:
        self.left = CourseNodes.CourseGenerator.generate_course(left)
        self.right = CourseNodes.CourseGenerator.generate_course(right)
