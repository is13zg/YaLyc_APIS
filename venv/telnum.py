def check_number(s):
    er = "error"
    s = str(s)
    s = "".join(s.split())
    # s = s.replace(" ", "")
    if s.find("+7") != 0 and s.find("8") != 0:
        return er
    if s.find("8") == 0:
        s = s.replace("8", "+7", 1)

    if not all((s.split("-"))):
        return er
    else:
        s = s.replace("-", "")

    s1 = 0
    s2 = 0
    for c in s:
        if c == "(":
            s1 += 1
        elif c == ")":
            s2 += 1
        if s2 > s1:
            return er
    if s2 != s1 or max(s2, s1) > 1:
        return er
    else:
        s = s.replace("(", "")
        s = s.replace(")", "")

    if len(s) != 12:
        return er
    else:
        return s


print(check_number(input()))
