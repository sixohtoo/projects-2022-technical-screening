import re
import CourseNodes


class CourseLeafCode(CourseNodes.CourseLeaf.CourseLeaf):
    def __init__(self, course) -> None:
        # prereqdfsg: | dfgkdf: | COMP1511
        # print('clc:', course)
        # print("code leaf course:", course)
        course_name = ''
        if len(course) > 0:
            for phrase in course:
                # print("word:", word)
                # print("p:", phrase)
                for word in phrase.split():
                    if re.match(r'\D*\d\d\d\d\D*', word):
                        # print('yobnyob')
                        course_name = word
        super().__init__(course_name)
        # print(self.course)

    def evaluate(self, course_list):
        # print('hey bucko', self.course)
        if not self.course:
            return True
        elif self.course.lower() in ' '.join(course_list).lower():
            return True
        elif self.course[3:] in ' '.join(course_list):
            return True
        return False
