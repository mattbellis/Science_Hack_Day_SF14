from math import frexp, fabs, ldexp
import sys

"""
The purpose of this module is to provide functions that
perform operations that really should be part of the python
standard, but surprisingly are not.  Apparently file i/o
in python is controlled by one and only one module and
reads and writes string ONLY.  This was surprising.  So
below are functions that form the bit representation of
int, longs, and floats and converts them to a character
string for maxiumum efficiency.  Hard to get better
compression than this I think.
"""

def _frexp(f):    
    """
    This is q think wrapper around python's frexp that returns
    a mantissa and exponent in a form that is a little more
    convenient for the the fileio module.  Namely the exponent
    offset form is preferable since there's now only one sign
    to worry about.  This greatly simplifies file i/o.  The
    mantissa is converted to an integer (* 10**15 to minimize
    precision loss and fits into 52 bits) and the exponent is
    shifted by 1023 to guarantee it is an unsigned integer and
    fits into 11 bits.
    @param f: The float value to be coverted to be decomposed into mantissa and exponent.
    """
    (m,e) = frexp(f)
    mant = int( m * 10**15 )
    exponent = e + 1023
    return (mant,exponent)

def _ldexp(m,e):
    """
    This function performs the inverse of _frexp.  Given a
    mantissa and exponent, it returns the float representation.
    @param m: mantissa assumed to be type long.
    @param e: exponent assumed to be type int.
    """
    return ldexp(m / 10.**15, e - 1023)
    
def _bitstring_to_charstring(bit_string):
    """
    This function takes a bit_string (i.e. '10010011') and returns
    a string of characters ('\x93' in this example) that can be fed
    to python's file write method.
    """
    if not len(bit_string) % 8 :
        result = ""
        for chunk in [bit_string[n:n+8] for n in range(0,len(bit_string),8)]:
            result += "%c" % chr(int("%s"% chunk,2))
        return result
    else:
        raise Error('Malformed bit string.  Must be an integral number of bytes (i.e. 8 bits).')

def _charstring_to_bitstring(char_string):
    """
    This function takes a character string (i.e. '\x93') and returns
    a string of bits ('10010011' in this example) that can be converted
    to the correct type.
    """
    bit_str = ""
    for ch in char_string :
        bit_str += bin( ord(ch) ).lstrip('0b').zfill(8)
    return bit_str

def _encode_mantissa_as_bitstring(mant):
    """
    This is expecting an integer.  The purpose of this function is to
    return the bit_string representation of the mantissa.  The length
    of the string is 52 characters long and is meant to be combined
    with the 11 bit exponent and 1 sign bit to form a 64 bit string
    representation of a double precision float.
    """
    mant_bin_rep = [0 for j in range(52)]
    for n in reversed(range(52)):
        f,mant = divmod(mant,2**n)
        mant_bin_rep[n] = int(f)
    mant_bin_rep.reverse()
    result = ""
    for b in mant_bin_rep:
        result += "%d" % b
    return result

def _encode_exponent_as_bitstring(exponent):
    """
    This is expecting an integer.  The purpose of this function is to
    return the bit_string representation of the exponent.  The length
    of the string is 11 characters long and is meant to be combined
    with the 52 bit exponent and 1 sign bit to form a 64 bit string
    representation of a double precision float.
    """
    exp_bin_rep = [0 for j in range(11)]
    for n in reversed(range(11)):
        f,exponent = divmod(exponent,2**n)
        exp_bin_rep[n] = int(f)
    exp_bin_rep.reverse()
    result = ""
    for b in exp_bin_rep:
        result += "%d" % b
    return result

def encode_unsigned(i):
    """
    This function 'encodes' both int and long types and returns a string
    that can be fed to the pyhton file's write method.
    """
    if type(i) == type(int()):
        nbytes = 4
    if type(i) == type(long()):
        nbytes = 8 
    return _bitstring_to_charstring( bin(i).lstrip('0b').zfill(nbytes*8) )

def decode_unsigned(char_string):
    """
    The function decodes a string of characters and returns the integer (or long) value.
    """
    bit_str = _charstring_to_bitstring(char_string)
    if len(char_string) == 4 :
        return int(bit_str ,2)
    if len(char_string) == 8 :
        return long(bit_str,2)

def encode_float(f):
    """
    This function translates a float to its 8 byte
    character string repesentation so that python's
    file write method can write it. The 64 bit representation
    is a follows:
    1. 1 bit for the sign

    2. 11 birs for the exponent

    3. 52 bits for the mantissa

    So read as a string the SIGN is in the 0th position, the EXPONENT is 1-11,
    and the MANTISSA is 12-52.
    m / 10.**15, e - 1023
    f = (-1)**SIGN * (MANTISSA/10**15) * 2**(EXPONENT - 1023 )
    """
    if type(f) != type(float()):
        print "this is not a float"
        sys.exit()

    (m,e) = _frexp(fabs(f))

    if f < 0 : sign = 1
    else : sign = 0
    result = "%d" % sign
    result += _encode_exponent_as_bitstring(e)
    result += _encode_mantissa_as_bitstring( fabs(m) )
    return _bitstring_to_charstring(result)

def decode_float(s):
    """
    This function translates an 8 byte character string repesentation 
    to a float.  See the coreresponding _frexp function for the byte
    layout and interpretation.
    """
    if len(s) != 8 :
        print "this is not right - len('%s') = %d " % (s,len(s))
        sys.exit()
    bin_str = _charstring_to_bitstring(s)
    if bin_str[0] == '0' : sign = +1
    if bin_str[0] == '1' : sign = -1
    exponent = int(bin_str[1:12],2) 
    mantissa = long(bin_str[12:],2) 
    return sign * _ldexp(mantissa,exponent)
    


