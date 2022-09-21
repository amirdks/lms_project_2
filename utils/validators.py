import re

from django.core.exceptions import ValidationError

import re


def is_valid_iran_code(input):
    if not re.search(r'^\d{10}$', input):
        raise ValidationError('لطفا کد ملی معتبر وارد کنید')
    check = int(input[9])
    s = sum(int(input[x]) * (10 - x) for x in range(9)) % 11
    return check == s if s < 2 else check + s == 11
