from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username}, {self.occupation}"


class Course(models.Model):
    name = models.CharField(null=False, max_length=100, default='online course')
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True, default=now)
    instructors = models.ManyToManyField(Instructor, blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Enrollment',
        blank=True
    )
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description[:40]}..."


class Lesson(models.Model):
    title = models.CharField(max_length=200, default="Lesson Title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.course.name})"


class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'beta'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'Beta')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

    def __str__(self):
        return f"Enrollment: {self.user.username} in {self.course.name}"


class Question(models.Model):
    """
    Question model linked to Lesson (ForeignKey) with question_text, grade,
    and a method is_get_score(selected_ids) to evaluate whether selected
    choice IDs contain all correct answers and no incorrect answers.
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=50)

    def is_get_score(self, selected_ids):
        """
        Determines whether the provided selected choice IDs contain
        all correct choices and zero incorrect choices for this question.
        Handles both integer and string representations in selected_ids.
        """
        # Normalize selected_ids to integers
        if not selected_ids:
            return False

        try:
            selected_int_ids = [int(i) for i in selected_ids if str(i).isdigit()]
        except (ValueError, TypeError):
            return False

        # Count total correct choices belonging to this question
        all_correct_count = self.choice_set.filter(is_correct=True).count()
        # Count how many of the selected choices are correct
        selected_correct_count = self.choice_set.filter(is_correct=True, id__in=selected_int_ids).count()

        # Score is awarded only if all correct choices were selected and no extra incorrect choices were picked
        if all_correct_count > 0 and all_correct_count == selected_correct_count and len(selected_int_ids) == all_correct_count:
            return True
        return False

    def __str__(self):
        return f"Question: {self.question_text} (Grade: {self.grade})"


class Choice(models.Model):
    """
    Choice model linked to Question (ForeignKey) with choice_text and is_correct flag.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice: {self.choice_text} [Correct: {self.is_correct}]"


class Submission(models.Model):
    """
    Submission model linked to Enrollment (ForeignKey) with a ManyToManyField to Choice.
    """
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    submitted_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Submission #{self.id} - {self.enrollment.user.username} - {self.enrollment.course.name}"
