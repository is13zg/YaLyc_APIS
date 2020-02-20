def check_number(s):
    try:
        s = "".join(s.split())
        # s = s.replace(" ", "")
        if s.find("+7") != 0 and s.find("8") != 0:
            raise ValueError
        if s.find("8") == 0:
            s = s.replace("8", "+7", 1)

        if not all((s.split("-"))):
            raise ValueError
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
                raise ValueError
        if s2 != s1 or max(s2, s1) > 1:
            raise ValueError
        else:
            s = s.replace("(", "")
            s = s.replace(")", "")

    except Exception:
        return "неверный формат"

    try:
        if len(s) != 12:
            raise ValueError
    except Exception:
        return "неверное количество цифр"

    return s


print(check_number(input()))
