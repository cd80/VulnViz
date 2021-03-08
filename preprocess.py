"""
1. remove comments
2. trim whitespaces
"""
import re

def beautify(dirty_code):
    clean_code = dirty_code
    clean_code = remove_comments(clean_code)
    clean_code = trim_whitespaces(clean_code)
    return clean_code

# https://stackoverflow.com/a/18381470/6103202
def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)

def trim_whitespaces(string):
    """
        1. tab -> space
        2. double spaces -> single space
        3. double newline -> single newline
    """
    new_code = string
    new_code = new_code.replace("\t", " ")
    new_code = new_code.replace("\r", "")
    while new_code.find(" "*2) != -1:
        new_code = new_code.replace(" "*2, " ")
    while new_code.find(" \n") != -1:
        new_code = new_code.replace(" \n", "\n")
    while new_code.find("\n"*2) != -1:
        new_code = new_code.replace("\n"*2, "\n")
    
    new_code = '\n'.join([line for line in new_code.split("\n") if line.strip() != ""])
    return new_code