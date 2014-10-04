from datetime import timedelta, datetime

class EventTime:
    """
    The EventTime class.  The purpose of this class is to translate IceCube time,
    which constist of the year and tenths of nanoseconds since the beginning of the
    year, to a format that is more user-friendly.  This class uses python's
    datetime module.
    @todo: Implement math operations.
    @todo: Clean up the interface so the tenths of nanoseconds and datetime is more
    unified and integrated.
    """
    def __init__(self,year, daqTime):
        """
        The constructor takes a year and a DAQTime (i.e. number of tenths of nanoseconds
        since the beginning of the year).
        @param year: The time of year that was used to initialize the class.
        @param daqTime : Number of tenths of nanoseconds since the beginning of the year.
        """
        self.year = year
        """
        The year the event occured.
        """
        self.daqTime = daqTime
        """
        The number of tenths of nanoseconds the event occured since the beginning of the year.
        """

        dtpair = self._make_datetime_pair()
        self.dateTime = dtpair[0]
        """
        The datetime object 
        """
        self.utcTenthNanoSecond = dtpair[1]
        """
        The remainder of the tenths of nanoseconds from the creation of the datetime object
        """

    def _make_datetime_pair(self):
        """
        This method uses the year and daqTime to create a datetime object.  Since the highest precision
        of datetime is microseconds, the remaining tenths of nanoseconds is returned as well.
        @return: This method returns a tuple (datetime, int) where the first element is the datetime 
        object and the second element is the remaining tenths of nanoseconds.
        """
        microsec = long(self.daqTime * 10**-4)
        utcTenthNanoSecond = self.daqTime % 10000
        dt = timedelta(microseconds = microsec)
        dateTime = datetime(year = self.year, month = 1, day = 1) + dt
        return (dateTime,utcTenthNanoSecond)    
    
    def __str__(self):
        date_str = ""
        dateTime,tenthns = self._make_datetime_pair()
        if dateTime.microsecond == 0. :
            date_str = "%s.%010d" % (str(dateTime),tenthns)
        else:
            date_str = "%s%d" % (str(dateTime),tenthns)
        return date_str
