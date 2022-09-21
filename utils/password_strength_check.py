from django import forms


def password_strength_check(password):
    password1 = password

    # At least MIN_LENGTH long
    if len(password1) < 8:
        raise forms.ValidationError('رمز عبور نمیتواند کمتر از 8 کارکتر باشد')

    # At least one letter and one non-letter
    first_isalpha = password1[0].isalpha()
    if all(c.isalpha() == first_isalpha for c in password1):
        raise forms.ValidationError("رمز عبور شما باید حداقل از یک حرف بزرگ و یا حرف خاص تشکیل شده باشد")

    # ... any other validation you want ...
    return password1
