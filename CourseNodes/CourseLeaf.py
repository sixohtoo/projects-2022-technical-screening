import re
import CourseNodes


class CourseLeaf(CourseNodes.Course.Course):
    def __init__(self, course) -> None:
        super().__init__()
        self.course = course
