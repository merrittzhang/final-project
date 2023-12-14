"""
database.py
Authors: Merritt Zhang, Sam Sanft
"""

import contextlib
import sqlite3


DATABASE_URL = 'file:reg.sqlite?mode=ro'


def get_classes(dept="", coursenum="", area="", title=""):
    """
    Returns a list of dictionary objects that correspond to classes.
    Returns all classes by default, keyword args can be used to specify
    which classes to return.
    """
    with sqlite3.connect(DATABASE_URL, isolation_level=None,
                         uri=True) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            courses = []
            # Get data from database
            stmt = "SELECT classid, classes.courseid, dept, " \
                   "coursenum, area, title "
            stmt += "FROM classes, courses, crosslistings "
            stmt += "WHERE classes.courseid = courses.courseid "
            stmt += "AND classes.courseid = crosslistings.courseid "
            args = []

            # Check flags
            if dept:
                dept = dept.replace("%", "\\%").replace("_", "\\_")
                stmt += 'AND dept LIKE ? '
                args.append("%" + dept + "%")
            if coursenum:
                num = coursenum.replace("%", "\\%").replace("_", "\\_")
                stmt += 'AND coursenum LIKE ? '
                args.append("%" + num + "%")
            if area:
                area = area.replace("%", "\\%").replace("_", "\\_")
                stmt += 'AND area LIKE ? '
                args.append("%" + area + "%")
            if title:
                title = title.replace("%", "\\%").replace("_", "\\_")
                stmt += 'AND title LIKE ? '
                args.append("%" + title + "%")

            if len(args) > 0:
                stmt += 'ESCAPE "\\" '

            stmt += "ORDER BY dept, coursenum "

            # Return result
            cursor.execute(stmt, args)
            for entry in cursor.fetchall():
                courses.append({"classid": entry[0],
                                "courseid": entry[1],
                                "dept": entry[2],
                                "coursenum": entry[3],
                                "area": entry[4],
                                "title": entry[5]})
            return courses


def get_class_info(classid):
    """
    Returns a dictionary object that correspond to class info for
    classid.
    """
    with sqlite3.connect(DATABASE_URL, isolation_level=None,
                         uri=True) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            info = {}

            # Get data from classes
            stmt = "SELECT courseid, days, starttime, endtime, bldg, " \
                   "roomnum "
            stmt += "FROM classes WHERE classid = ?"
            cursor.execute(stmt, [classid])
            result = cursor.fetchall()

            if len(result) == 0:
                return None
            courseid = result[0][0]
            info.update({"courseid": result[0][0],
                         "days": result[0][1],
                         "starttime": result[0][2],
                         "endtime": result[0][3],
                         "bldg": result[0][4],
                         "roomnum": result[0][5]})

            # Get data from courses
            stmt = "SELECT area, title, descrip, prereqs "
            stmt += f"FROM courses WHERE courseid = {courseid}"
            cursor.execute(stmt)
            result = cursor.fetchall()
            info.update({"area": result[0][0],
                         "title": result[0][1],
                         "descrip": result[0][2],
                         "prereqs": result[0][3]})

            # Get data from crosslistings
            depts = []
            nums = []
            stmt = "SELECT dept, coursenum "
            stmt += f"FROM crosslistings WHERE courseid = {courseid} "
            stmt += "ORDER BY dept, coursenum"
            cursor.execute(stmt)
            result = cursor.fetchall()
            for entry in result:
                depts.append(entry[0])
                nums.append(entry[1])
            info.update({"dept": depts, "coursenum": nums})

            # Get data from coursesprofs
            stmt = "SELECT profname "
            stmt += "FROM coursesprofs, profs "
            stmt += f"WHERE courseid = {courseid} "
            stmt += "AND coursesprofs.profid = profs.profid "
            stmt += "ORDER BY profname"
            cursor.execute(stmt)
            result = cursor.fetchall()
            profs = [entry[0] for entry in result]
            info.update({"prof": profs})

            return info
