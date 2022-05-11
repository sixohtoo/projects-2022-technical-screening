import CourseNodes

"""
    Binary composite parent node. Children are either CourseAnd or CourseOr.
"""


class CourseBinary(CourseNodes.Course.Course):
    # Left and right are arrays of booleans and operators
    def __init__(self, left, right) -> None:
        self.left = CourseNodes.CourseGenerator.generate_course(left)
        self.right = CourseNodes.CourseGenerator.generate_course(right)
