import zeep
from zeep import Client

###
#
# Examples of how to pull data from the Georgia General Assembly's API
# using Python and a module called Zeep.
#
# More on Zeep: https://python-zeep.readthedocs.io/en/master/
# Which is by Michael van Tellingen
# And available free under MIT License
# https://github.com/mvantellingen/python-zeep
#
###

# GET SESSION SCHEDULES BACK TO 2001
#
# First, run this in your terminal. It's going to print kind of a menu of what you can get out of this endpoint:
#
# python -mzeep http://webservices.legis.ga.gov/GGAServices/Session/Service.svc?wsdl
#
# Part of the result is this:
#
# Service: SessionService
#      Port: BasicHttpBinding_SessionFinder (Soap11Binding: {http://www.legis.ga.gov/2009/01/01/services/}BasicHttpBinding_SessionFinder)
#          Operations:
#             GetSessionSchedule(SessionId: xsd:int, Chamber: ns0:Chamber) -> GetSessionScheduleResult: ns0:SessionCalendar
#             GetSessions() -> GetSessionsResult: ns0:ArrayOfSession
#             GetYears() -> GetYearsResult: ns0:ArrayOfYear
#
# It's saying: here are the operations you can do and the parameters you'll need.

wsdl = 'http://webservices.legis.ga.gov/GGAServices/Session/Service.svc?wsdl'
client = Client(wsdl)

# For example, GetSessions() doesn't need any parameters
sessions = client.service.GetSessions()
print(sessions)

# Neither does GetYears()
years = client.service.GetYears()
print(years)

# But pay attention to the 'Id' field in GetSessions(). You'll need it as a parameter to GetSessionSchedule()
sked = client.service.GetSessionSchedule(27, 'House')
print(sked)

# turn the schedule into an Ordered Dict if you like
py_sked = zeep.helpers.serialize_object(sked)
print(type(py_sked))

#####

# GET MEMBER LISTS BACK TO 2001
#
# Use a different endpoint, see choices by putting this in your terminal
# python -mzeep http://webservices.legis.ga.gov/GGAServices/Members/Service.svc?wsdl
#
# This is interesting:
#
# GetMembersBySession(SessionId: xsd:int) -> GetMembersBySessionResult: ns0:ArrayOfMemberListing


wsdl = 'http://webservices.legis.ga.gov/GGAServices/Members/Service.svc?wsdl'
client = Client(wsdl)

# Who were members *at any time* in the 2015-2016 regular session? It's Id No 24:

membs1516 = client.service.GetMembersBySession(24)
py_membs1516 = zeep.helpers.serialize_object(membs1516)
for i in range(len(py_membs1516)):
    print(py_membs1516[i]['Name'])


# There are a total six endpoints *that I know of*
# I'm not aware of any documentation, but if you find any, send it my way!
# Nor am I aware of any API for bill text

# http://webservices.legis.ga.gov/GGAServices/Votes/Service.svc?wsdl
# http://webservices.legis.ga.gov/GGAServices/Committees/Service.svc?wsdl
# http://webservices.legis.ga.gov/GGAServices/Members/Service.svc?wsdl
# http://webservices.legis.ga.gov/GGAServices/Legislation/Service.svc?wsdl
# http://webservices.legis.ga.gov/GGAServices/Session/Service.svc?wsdl
# http://webservices.legis.ga.gov/GGAServices/Members/Service.svc?wsdl


## NOTE
#
# OpenStates.org has an API with all this data back to 2017.  So if you don't need older data, you may
# like their API better.
#