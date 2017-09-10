
def student_check(user):
    return not user.is_anonymous and user.staff == 'S'


def teacher_check(user):
    return not user.is_anonymous and user.staff == 'T'
