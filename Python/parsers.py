b = birth[0].split(' ')
if len(b) == 4:
    mob = b[1]
    dob = int(b[2][:-1])
    yob = int(b[3])
    birthplace = birth[0].split(' in ')
    if len(birthplace) == 2:
        birthplace = birthplace[1]
    assert mob in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                   'October', 'November', 'December']
    assert dob in range(1, 31)
elif len(b) == 2:
    yob = int(b[1])


 d = death[0].split(' ')
            mod = d[1]
            dod = d[2][0:1]
            yod = d[3]
            if mod not in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                           'October', 'November', 'December']:
                mod = None
            if dod.isdigit() and int(dod) in range(1, 31):
                dod = int(dob)
            else:
                dod = None
            if len(yod) == 4 and yod.isdigit():
                yod = int(yod)
            else:
                yod = None
            deathplace = death[0].split(' in ')
            if len(deathplace) == 2:
                deathplace = deathplace[1]
            else:
                deathplace = None
        else:
            dod = None
            mod = None
            yod = None
            deathplace = None