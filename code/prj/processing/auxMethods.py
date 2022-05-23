
"""

A file with addictional methods

"""

def convert_array_to_string(arr):
    string = ""
    for i in range(len(arr)):
        string += str(arr[i]) + ";"

    return string
