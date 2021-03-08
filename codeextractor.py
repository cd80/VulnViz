def badcode(code):
    # extract bad(vuln) from source
    if code.find("#ifndef OMITBAD") == -1:
        return []
    badcode = code.split("#ifndef OMITBAD")[1].split("#endif")[0]
    badcodes = get_func_bodies(badcode)
    return badcodes

def goodcode(code):
    # extract good(safe) from source
    if code.find("#ifndef OMITGOOD") == -1:
        return []
    goodcode = code.split("#ifndef OMITGOOD")[1].split("#endif")[0]
    goodcodes = get_func_bodies(goodcode)
    return goodcodes

def get_func_bodies(code):
    # omit function prototypes and just get their body blocks
    depth = 0
    cur_code = ''
    codes = []
    record = False
    for c in code:
        if c == '{':
            depth += 1
            if depth == 1:
                record = True
        elif c == '}':
            depth -= 1
            if depth == 0 and record == True:
                record = False
                codes.append(cur_code)
                cur_code = ''
        else:
            # print(c, record)
            if record:
                cur_code += c
    return codes