# Necessary Imports

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
from logger import Lg

logger = Lg('inscraplog').getlog()


class Sitescrapper:

    def __init__(self, web_url):
        self.web_url = web_url

    def getscript_data(self):
        """Function scraps and gives the end json data named as script_data"""
        try:
            uclient = uReq(self.web_url)
            logger.info("Given input URL is requested from internet and webpage is opened")
            ineuron_page = uclient.read()
            logger.info("(getscript_data) Reading the Webpage Successful")
            uclient.close()
            logger.info("(getscript_data) Connection to the web server is closed")
            ineuron_html = bs(ineuron_page, "html.parser")
            logger.info("(getscript_data) Parsing the webpage as html")
            tag_data = ineuron_html.findAll("script", {"id": "__NEXT_DATA__"})
            script_data = json.loads(tag_data[0].string)
            logger.info("(getscript_data) tag data formatted to end json type")
            return script_data

        except Exception as e:
            logger.error("(getscript_data) error occurred while scrapping data" + str(e))

    def list_of_courses(self):
        """Function returns list of courses available from script data scrapped"""
        try:
            script_data = self.getscript_data()
            courses = script_data['props']['pageProps']['initialState']['init']['courses'].keys()
            course_list = list(courses)
            logger.info("(list_of_courses) course_list gathered")
            return course_list

        except Exception as e:
            logger.error("(list_of_courses) unable to fetch courses" + str(e))

    def course_url(self):
        """Function return respective url's of the courses"""
        try:
            course_url = []
            course_list = self.list_of_courses()
            for i in range(len(course_list)):
                course_url.append(self.web_url + course_list[i].replace(" ", "-"))
            logger.info("(course_url) all url's gathered")
            return course_url

        except Exception as e:
            logger.error("(course_url) error in url to be gathered" + str(e))

    def getcoursesscriptdata(self, course_url):
        """Function returns individual course script data scrapped from individual course url page"""
        try:
            uclient = uReq(course_url)
            logger.info("Given input URL is requested from internet and webpage is opened")
            course_webpage = uclient.read()
            logger.info("(getcoursesscriptdata) Reading the Webpage Successful")
            uclient.close()
            logger.info("(getcoursesscriptdata) Connection to the web server is closed")
            course_html = bs(course_webpage, "html.parser")
            logger.info("(getcoursesscriptdata) Parsing the webpage as html")
            tag_data = course_html.findAll("script", {"id": "__NEXT_DATA__"})
            course_webdata = json.loads(tag_data[0].string)
            logger.info("(getcoursesscriptdata) tag data formatted to end json type")
            return course_webdata

        except Exception as e:
            logger.error("(getcoursesscriptdata) error in scrapping course wise web page" + str(e))

    def course_whole_data(self):
        """Function iterates for whole course url and returns whole course web pages json data"""
        try:
            course_url = self.course_url()
            all_course_data = []
            for i in range(len(course_url)-50):
                course_data = self.getcoursesscriptdata(course_url[i])
                all_course_data.append(course_data)
            logger.info("(course_whole_data) individual course script data captured")
            return all_course_data

        except Exception as e:
            logger.error("(course_whole_data) error occurred in individual course script data capture" + str(e))

    def course_curriculum_title(self, course_data):
        """Function returns course curriculum titles"""
        try:
            course_curriculum_title = []
            length_iter = len(list(course_data['props']['pageProps']['data']['meta']['curriculum'].keys()))
            iter_list = list(course_data['props']['pageProps']['data']['meta']['curriculum'].keys())
            for i in range(length_iter):
                course_curriculum_title.append(course_data['props']['pageProps']['data']['meta']['curriculum'][iter_list[i]]['title'])
            logger.info("(course_curriculum_title) all course curriculum titles gathered")
            return course_curriculum_title

        except Exception as e:
            logger.error("(course_curriculum_title) error in all course curriculum titles fetch" + str(e))

    def course_curriculum(self, course_data):
        """Function returns course curriculum"""
        try:
            course_curriculum = []
            length_iter = len(list(course_data['props']['pageProps']['data']['meta']['curriculum'].keys()))
            iter_list = list(course_data['props']['pageProps']['data']['meta']['curriculum'].keys())
            for i in range(length_iter):
                length_iter_2 = len(list(course_data['props']['pageProps']['data']['meta']['curriculum'][iter_list[i]]['items']))
                for j in range(length_iter_2):
                    course_curriculum.append(course_data['props']['pageProps']['data']['meta']['curriculum'][iter_list[i]]['items'][j]['title'])
                logger.info("(course_curriculum) all course_curriculum data gathered")
            return course_curriculum

        except Exception as e:
            logger.error("(course_curriculum) error in all course_curriculum data fetch" + str(e))

    def course_details(self):
        """Function returns respective course description"""
        try:
            all_course_data = self.course_whole_data()
            course_info = []
            for i in range(len(all_course_data)):
                title = all_course_data[i]['props']['pageProps']['data']['title']
                description = all_course_data[i]['props']['pageProps']['data']['details']['description']
                if 'meta' in all_course_data[i]['props']['pageProps']['data'].keys():
                    course_curriculum_title = self.course_curriculum_title(course_data=all_course_data[i])
                    course_curriculum = self.course_curriculum(course_data=all_course_data[i])
                    learn = all_course_data[i]['props']['pageProps']['data']['meta']['overview']['learn']
                    requirements = all_course_data[i]['props']['pageProps']['data']['meta']['overview']['requirements']
                    features = all_course_data[i]['props']['pageProps']['data']['meta']['overview']['features']
                else:
                    continue
                if all_course_data[i]['props']['pageProps']['data']['details']['pricing']['isFree']:
                    pricing = 0
                else:
                    pricing = all_course_data[i]['props']['pageProps']['data']['details']['pricing']['IN']
                mydict = {"title":title, "description":description, "course_curriculum_title": course_curriculum_title,
                          "course_curriculum": course_curriculum, "learn": learn, "requirements": requirements,
                          "features": features, "price": pricing}
                course_info.append(mydict)
            logger.info("(course_details) course_info gathered")
            return course_info

        except Exception as e:
            logger.error("(course_details) error in course_info fetch" + str(e))
