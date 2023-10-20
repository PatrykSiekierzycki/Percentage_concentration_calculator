import re


"""
Brief: check if in string are dot or minus. Also check at what index is for minus.
Param: string.
Return: bool or (bool + haw many minus are in string; minus for this minus; and how many dots are in string).
"""
def isNumberWithDotOrMinus(user_input):

    minusCounter = 0
    minusIndex = None
    dotCounter = 0
    buffor = ""

    for index, char in enumerate(user_input):

        if char == "-":
            minusCounter += 1
            minusIndex = index
        elif char == ".":
            dotCounter += 1
        else:
            buffor = buffor + char

    # Check is only one minus at front of "user_input" and is only one dot.
    if minusCounter <= 1 and dotCounter <= 1 and (minusIndex == 0 or minusIndex is None):
        numeric = buffor.isnumeric()
        if numeric is True:
            return True, minusCounter, minusIndex, dotCounter
        else:
            return False
    else:
        return False

"""
Brief: Function for prepere numeric input: remove all whitespace sign and change all "," to ".".
Param: user_input: string
Return: prepered input: string
"""
def prepereNumericInput(user_input):

    # Change all commas to dots in "user_input".
    user_input = user_input.replace(",", ".")

    # Get rid of whitespace character from "user_input".
    whitespace_list = [" ", "\t", "\n", "\v", "\f", "\r"]
    for space in whitespace_list:
        user_input = user_input.replace(space, "")

    return user_input

"""
Brief: Function check if str type variable "data" is a number and return it as int or float type.
Param:
    data: str type (string to check)
    dtype: data type of returned value.
Return:
    int: if string is a number and "dtype" is set at "int".
    float: : if string is a number and "dtype" is set at "float".
    False: if string is not a number.
"""
def isNumber(data):

    # Prepere data and check if argument has minus or dot.
    data = prepereNumericInput(data)
    if data.isnumeric():
        return int(data)
    else:
        pack = isNumberWithDotOrMinus(data)

        if type(pack) is tuple:
            number = pack[0]
            with_dot = pack[3]

            if number is True and with_dot != 0:
                return float(data)
            elif number is True and with_dot == 0:
                return int(data)

        if type(pack) is bool and pack is True:
            return int(data)
        else:
            return False

"""
Brief: function check if string is a proper RGB hexadecimal number
Param:
    data: str
Return:
    str: unchange argument
    bool: if is not a proper RGB hexadeciamal value.
"""
def is_a_hexadecimal_color(data):
    
    if type(data) is not str:
        return False
    
    if len(data) != 7:
        return False
    
    if data[0] != "#":
        return False
    
    proper_value = "[0-9 a-f A-F]"
    
    x = re.findall(proper_value, data[1:])

    if len(x) != 6:
        return False
    
    return data
