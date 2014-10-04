from event import Event
from encoder import encode_unsigned, decode_unsigned
from encoder import encode_float, decode_float
import sys

import gzip

FLOAT_SIZE = 8
INT_SIZE = 4
LONG_SIZE = 8

def write(file_handle, ev):
    """
    The write function is responsible for writing an event to a file.
    @param file_handle: The file_handle is a file object and can be a standard
    file, a gzip file handle, or anything with a write method really.
    @param ev: The Event object to be written to the frame.  There is some type checking
    performed since it's critical that the bytestream be consistent and well-defined.
    """
    if type(ev.runID) == type(int()) :
        file_handle.write( encode_unsigned(ev.runID) )
    else:
        raise TypeError('runID is not an int')

    if type(ev.year) == type(int()) :
        file_handle.write( encode_unsigned(ev.year) )
    else:
        raise TypeError('year is not an int')

    if type(ev.startTime) == type(long()) or \
           type(ev.startTime) == type(int()) :
        file_handle.write( encode_unsigned(long(ev.startTime)) )
    else:
        raise TypeError('startTime is not a long')

    if type(ev.eventLength) == type(float()) :
        file_handle.write( encode_float(ev.eventLength) )
    else:
        raise TypeError('eventLength is not a float')

    # now for the triggers
    # for decoding we need the number of triggers
    file_handle.write( encode_unsigned( long(len(ev.triggers))) )
    for ttime, tname in ev.triggers :
        file_handle.write( encode_float(ttime) )
        file_handle.write( encode_unsigned( int(len(tname)) ) )
        file_handle.write( tname )
        
    # now for the hits
    file_handle.write( encode_unsigned( long(len(ev.hits))) )
    for q,t,x,y,z in ev.hits :
        file_handle.write( encode_float(q) )
        file_handle.write( encode_float(t) )
        file_handle.write( encode_float(x) )
        file_handle.write( encode_float(y) )
        file_handle.write( encode_float(z) )

    #print ev

def read(file_handle):
    """
    This function is responsible for reading an event from a file and
    returning an Event object.  The order is assumed to be correct as
    well as the file type.  Otherwise this function will load garbage
    without warning. Since it's assuming a simple well-defined bytestream
    there's no way of verifying it's well-formed and uncorrupted.  What
    would be better is a dedicated serialization library that stores
    type and class information along with the data.  This should be the
    next thing to do.  The byte stream is assumed as follows in this order:
    1. 4 bytes - runID(unsigned int)
    
    2. 4 bytes - year(unsigned int)
    
    3. 8 bytes - startTime (long) - Number of tenths of nanoseconds since
    the beginning of the year.

    4. 8 bytes - eventLength(float) - Units of microseconds.

    5. 4 bytes - (long) - Number of triggers.  This is not a member
    of the Event class, since it's simply the size of the trigger list.
    For each trigger the byte structure is given as :
        - 8 bytes - trigger time (float) - Time of the trigger with respect
        to the start of the event.
        - 4 bytes - nchar (int) - Number of characters in the trigger name.
        - nchar * 1 byte - The characters that make up the trigger name.

    6. 8 bytes - nhits (long) - Number of hits in the event.  The next set
    consists of nhits*5*8 bytes (one chunk of 8 bytes for each float of q,t,x,y,z).

    @todo: Make a robust serialization library that stores the type information
    so that it is more generic and robust.  Something closer to boost's
    serialization library.  We won't regret it.
    """
    ev = Event()

    # when the end of the file is reached an empty string is returned
    # so we read a chunk of data and if an empty string is retrieved
    # return None, otherwise it's safe to decode that as the beginning
    # of the next event.
    data = file_handle.read(INT_SIZE)
    if data == '' : 
        # EOF, so return None
        return None
    else :
        ev.runID = decode_unsigned( data )
   
    ev.year = decode_unsigned( file_handle.read(INT_SIZE) )
    ev.startTime = decode_unsigned( file_handle.read(LONG_SIZE) )
    ev.eventLength = decode_float( file_handle.read(FLOAT_SIZE) )

    # now for the triggers
    # for decoding we need the number of triggers
    ntriggers = decode_unsigned( file_handle.read( LONG_SIZE ) )
    for n in range(ntriggers) :
        ttime = decode_float( file_handle.read( FLOAT_SIZE ) )
        tname = ""
        nchar = decode_unsigned( file_handle.read( INT_SIZE ) )
        for m in range(nchar) :
            tname += file_handle.read( 1 )
        ev.triggers.append( (ttime,tname) )

    # now for the hits
    nhits = decode_unsigned( file_handle.read( LONG_SIZE ) )
    for n in range(nhits) :
        q = decode_float( file_handle.read( FLOAT_SIZE ) )
        t = decode_float( file_handle.read( FLOAT_SIZE ) ) 
        x = decode_float( file_handle.read( FLOAT_SIZE ) ) 
        y = decode_float( file_handle.read( FLOAT_SIZE ) ) 
        z = decode_float( file_handle.read( FLOAT_SIZE ) )
        ev.hits.append( (q,t,x,y,z) )

    return ev
