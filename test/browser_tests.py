''' Adapted from: https://github.com/mbithenzomo/flask-selenium-webdriver-part-two/blob/master/tests/test_front_end.py'''
import os
import time
import unittest
import urllib.request
from os.path import join

from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from cscourses import db
from cscourses.models import Course, Student, Teacher, Grade

s1 = dict(uni_id="CS1234567", name="Ahmet Roth", title="mr", role='student', email='cs1234567@ucl.ac.uk',
          password='cs1234567', confirm='cs1234567')
t1 = dict(email="ct0000123@ucl.co.uk", role="teacher", uni_id="CT0000123", title="dr", name="Lewis Baird",
          password="ct0000123", confirm="ct0000123")


class TestBase(LiveServerTestCase):

    def create_app(self):
        from cscourses import create_app
        app = create_app('config.TestConfig')
        return app

    def setUp(self):
        """Setup the test driver and create test users"""
        # Chromedriver saved in the `test` directory (not included in the repo as you need to install the correct
        # version for your version of Chrome and operating system)
        self.driver = webdriver.Chrome(join(os.getcwd() + '/chromedriver'))
        self.driver.get(self.get_server_url())

        db.session.commit()
        db.drop_all()
        db.create_all()

        self.student1 = Student(email=s1.get('email'), student_ref=s1.get('uni_id'), name=s1.get('name'))
        self.student1.set_password(s1.get('password'))
        self.student2 = Student(email="cs1234568@ucl.co.uk", user_type="student", student_ref="CS1234568",
                                name="Elsie-Rose Kent")
        self.student2.set_password("cs1234568")
        self.student3 = Student(email="cs1234569@ucl.co.uk", user_type="student", student_ref="CS1234569",
                                name="Willem Bull")
        self.student3.set_password("cs1234569")
        self.teacher1 = Teacher(email=t1.get('email'), user_type=t1.get('role'), teacher_ref=t1.get('uni_id'),
                                title=t1.get('title'), name=t1.get('name'))
        self.teacher1.set_password(t1.get('password'))
        self.teacher2 = Teacher(email="ct0000124@ucl.co.uk", user_type="teacher", teacher_ref="uclcs0006", title="Prof",
                                name="Elif Munro")
        self.teacher2.set_password("ct0000124")
        self.teacher3 = Teacher(email="ct0000125@ucl.co.uk", user_type="teacher", teacher_ref="uclcs0010", title="Ms",
                                name="Aleyna Bonilla")
        self.teacher3.set_password("ct0000125")

        self.course1 = Course(course_code="COMP0015", name="Introduction to Programming")
        self.course2 = Course(course_code="COMP0034", name="Software Engineering")
        self.course3 = Course(course_code="COMP0035", name="Web Development")

        self.grade1 = Grade(grade="B-")
        self.grade2 = Grade(grade="C")
        self.grade3 = Grade(grade="B+")
        self.grade4 = Grade(grade="A+")
        self.grade5 = Grade(grade="A+")
        self.grade6 = Grade(grade="D+")

        self.student1.grades.append(self.grade1)
        self.student1.grades.append(self.grade4)
        self.student2.grades.append(self.grade2)
        self.student2.grades.append(self.grade5)
        self.student3.grades.append(self.grade3)
        self.student3.grades.append(self.grade6)

        self.course1.grades.append(self.grade1)
        self.course1.grades.append(self.grade2)
        self.course1.grades.append(self.grade3)
        self.course2.grades.append(self.grade4)
        self.course2.grades.append(self.grade5)
        self.course2.grades.append(self.grade6)

        self.teacher1.courses.append(self.course1)
        self.teacher2.courses.append(self.course2)
        self.teacher3.courses.append(self.course3)

        db.session.add_all([self.student1, self.student2, self.student3])
        db.session.add_all([self.teacher1, self.teacher2, self.teacher3])
        db.session.commit()

    def tearDown(self):
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


class TestRegistration(TestBase):

    def test_registration_succeeds(self):
        """
        Test that a user can create an account using the signup form if all fields are filled out correctly, and that
        they will be redirected to the index page
        """

        # Click signup menu link
        self.driver.find_element_by_id("signup-link").click()
        time.sleep(1)

        # Test person
        email = "cs1234570@ucl.co.uk"
        password = "cs1234570"
        confirm = "cs1234570"
        role = "Student"
        uni_id = "CS1234570"
        name = "Jago Curtis"
        title = "mr"

        # Fill in registration form
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("name").send_keys(name)
        self.driver.find_element_by_id("title").send_keys(title)
        self.driver.find_element_by_id("uni_id").send_keys(uni_id)
        role_select = Select(self.driver.find_element_by_id("role"))
        role_select.select_by_visible_text(role)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("confirm").send_keys(confirm)
        self.driver.find_element_by_id("submit").click()
        self.driver.implicitly_wait(10)

        # Assert that browser redirects to index page
        self.assertIn(url_for('main.index'), self.driver.current_url)

        # Assert success message is flashed on the index page
        success_message = self.driver.find_element_by_class_name("alert-warning").text
        self.assertIn("Signup succeeded", success_message)

    def test_login_succeeds_with_valid_user(self):
        """
        Write a test that logs in in a valid user with email="cs1234567@ucl.ac.uk" and password="cs1234567”
        """


if __name__ == '__main__':
    unittest.main()
