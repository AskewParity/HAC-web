from flask.globals import g
import mechanize
from mechanize import _http

from bs4 import BeautifulSoup
import math


class Access:
    def __init__(self, username, password) :
        self.username = username
        self.password = password
        #Goes to the login URL  

        br = mechanize.Browser()
        count = 0
        while True:
            if count == 20:
                break
            try:
            # Browser options
                br.set_handle_equiv(True)
                br.set_handle_redirect(True)
                br.set_handle_gzip(True)
                br.set_handle_referer(True)
                br.set_handle_robots(False)
                br.set_handle_refresh(_http.HTTPRefreshProcessor(), max_time=2)
                br.addheaders = [('User-Agent', 'Mozilla/5.0')]
                br.open('https://homeaccess.katyisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f')
                br.select_form(nr=0)
                if not br.geturl() == 'https://homeaccess.katyisd.org/HomeAccess/Home/WeekView':
                    br.form['LogOnDetails.UserName'] = self.username
                    br.form['LogOnDetails.Password'] = self.password

                    br.submit()

                br.open('https://homeaccess.katyisd.org/HomeAccess/Content/Student/Assignments.aspx') 
                self.response = br.response().read()
                break
            except Exception as e: 
                print(e)
                count += 1
     

           
        self.doc = BeautifulSoup(self.response, "html.parser")
        self.info = Agg(self.doc).list_classes()
        
    def add_grade(self, grade, course, category, **kwargs):
        others = self.info[course].grade_agg
        remove = None
        for e in others:
            if e.type == category:
                remove = e
                others.remove(e)
                break
        
        others_agg = 0
        for e in others:
            others_agg += float(e.actual)
        
        if not kwargs :
            c = remove
        else:
            c = kwargs["lst"]  
        sum_grade = float(c.credit) + float(grade)
        total = float(c.total) + 100
        weighted_grade = float(c.weight) * sum_grade / total
        new_avg = weighted_grade + others_agg
        print(f"New Average {new_avg}")
        new_grade = Grade(category, sum_grade, total, round(100 * sum_grade / total, 2), float(c.weight), round(weighted_grade, 2))
        self.info[course].assignments.append(Assignment('GRADE', '00/00/0000', category, 1, grade, 100, grade))
        
        others.append(new_grade)
        self.info[course].totalgrade = round(sum([float(e.actual) for e in self.info[course].grade_agg]) * 100 / sum(float(e.weight) for e in self.info[course].grade_agg))
        return (new_grade, new_avg)
    
    #BROKEN
    def grade_needed(self, goal, course, category, **kwargs):
        others = self.info[course].grade_agg
        remove = None
        
        total = 0
        for e in others:
            total += float(e.weight)
        for e in others:
            if e.type == category:
                remove = e
                others.remove(e)

        others_agg = 0
        for e in others:
            others_agg += float(e.actual)
        
        if not kwargs :
            c = remove
        else:
            c = kwargs["lst"] 

        remove_other = float(goal * total / 100) - others_agg

        if remove_other > float(c.weight) :
            others.append(remove)
            return None

        lst = []
        temp = c
        while float(temp.actual) < remove_other :
            needed = math.ceil((remove_other * (float(temp.total) + 100)) / float(temp.weight)) - float(temp.credit)
            if needed > 100 : needed = 100
            temp = self.add_grade(needed, course, category, lst=temp)[0]
            lst.append(needed)
        return lst
class Agg:
    def __init__(self, doc):
        self.doc = doc

    def list_classes(self):
        #Sections the individual classes
        rawClassList = self.doc.findAll('div', attrs={"class": "AssignmentClass"})
        lst = []
        for i in rawClassList:
            lst.append(Course(i))
        return lst

class Course:
    def __init__(self, doc):
        self.doc = doc
        self.title = self.get_title()
        self.assignments = self.get_assignments()
        self.grade_agg = self.get_course_avgs()
        if self.grade_agg:
            self.totalgrade = round(sum([float(e.actual) for e in self.grade_agg]) * 100 / sum(float(e.weight) for e in self.grade_agg))
        else:
            self.totalgrade = 0

    def get_title(self):
        raw_title = self.doc.findAll('a', attrs={"class": "sg-header-heading"})
        return raw_title[0].text.strip()

    def get_assignments(self):
        lst = []
        assignment_list = self.doc.findAll("tr", attrs={"class": "sg-asp-table-data-row"})
        for e in assignment_list:
            temp = []
            string = e.findAll("a")
            if len(string) > 0:
                grades = e.findAll("td", attrs={"class": "sg-view-quick"})
                label = e.findAll("td")
                temp.append(label[0].text)
                temp.append(label[3].text)         
                for e in grades:
                    temp.append(e.text)
                assignment = Assignment(string[0].text.strip(), temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
                lst.append(assignment)
        return lst
    
    def get_course_avgs(self):
        dir = []
        assignment_list = self.doc.findAll("tr", attrs={"class": "sg-asp-table-data-row"})
        for e in assignment_list:
            data = e.findAll("td")
            if len(data) == 6:
                label = ""
                lst = []
                for i, e in enumerate(data):
                    if i == 0:
                        label = e.text
                    else:
                        lst.append(e.text)
                gr = Grade(label, lst[0], lst[1], lst[2], lst[3], lst[4])
                dir.append(gr)
        return dir

class Assignment():
    def __init__(self, title, date, type, quant, credit, total, percent):
        self.title = title
        self.date = date
        self.type = type
        self.quant = quant
        self.credit = credit
        self.total = total
        self.percent = percent

class Grade():
    def __init__(self, type, credit, total, percent, weight, actual):
        self.type = type
        self.credit = credit
        self.total = total
        self.percent = percent
        self.weight = weight
        self.actual = actual