from event_time import EventTime
import sys

class Event:
    '''
    The Event class. This is a simple container
    for the event information and has the following
    member variables.

    runID - The Run ID
    year - The year the event triggered
    startTime - The number tenths of nanoseconds since the beginning
         of the year.
    eventLength - The length of the event in units of tenths of nanoseconds
    triggers - A list of triggers in the event.  This is a list of tuples where
         the first entry of the tuple is the time of the trigger with respect
         to the earliest trigger in the event.
    hits - A list of hits in the event.  A hit is simply a 5-tuple where the elements
        0-4 are charge, time, x, y, and z respectively.
    '''
    def __init__(self):
        # int
        self.runID = None
        # int
        self.year = None
        # long
        self.startTime = None
        # float
        self.eventLength = None
        # list, tuple, float, string
        self.triggers = list()
        # list, tuple, float, float, float, float, float
        self.hits = list()

    def event_time(self):
        return EventTime(self.year, self.startTime)

    def __str__(self):
        string = "RunID : " + str(self.runID) + '\n'
        string += str("Start Time : %s" % self.event_time() ) + '\n'
        string += str("Event Length : %f microsec" % self.eventLength) + '\n'
        string += "Triggers : " + str(self.triggers) + '\n'
        string += "Hits : " + str(self.hits) + '\n'
        return string
