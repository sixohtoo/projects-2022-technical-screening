import CourseNodes
import re


class CourseLeafUnits(CourseNodes.CourseLeaf.CourseLeaf):
    def __init__(self, course) -> None:
        # print("units leaf course:", course)
        rules = {}

        course_str = ' '.join(course)
        pattern = re.compile("(\d+)\s+units")

        rules["uoc"] = int(pattern.findall(course_str)[0])

        pattern = re.compile("(\d+)?\s+([A-Z]{4})\s+courses")
        result = pattern.findall(course_str)
        # print("result:", result)
        if '(' in course_str:
            pattern = re.compile("\((.*)\)")
            # print("yee", course_str)
            allowed_courses_str = pattern.findall(course_str)[0]
            rules["allowed_courses"] = set(
                re.split(',\s*', allowed_courses_str))
        elif result and len(result[0]) == 1:
            rules["level"] = ""
            rules["type"] = result[0][0]
        elif result and len(result[0]) == 2:
            rules["level"] = result[0][0]
            rules["type"] = result[0][1]

        super().__init__(rules)

    def evaluate(self, course_list):
        units = 0
        if "level" in self.course:
            # print("type:", self.course["type"])
            # print("level:", self.course["level"])
            allowed = self.course["type"] + self.course["level"]
            units = len([x for x in course_list if x.startswith(allowed)]) * 6
            # for course in course_list:
            #     if course.startswith(allowed):
            #         units += 6
        elif "allowed_courses" in self.course:
            # print("been")
            units = len(
                [x for x in course_list if x in self.course["allowed_courses"]]) * 6
            # for course in course_list:
            #     if course in self.rules["allowed_courses"]:
            #         units += 6
            # print("UNITS ARE", units)
        else:
            units = len(course_list) * 6

        return units >= self.course["uoc"]
