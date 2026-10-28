from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-pub_date')[:10]


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_enrolled = False
        if user.is_authenticated:
            is_enrolled = Enrollment.objects.filter(user=user, course=self.object).exists()
        context['is_enrolled'] = is_enrolled
        return context


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment, created = Enrollment.objects.get_or_create(
        user=user,
        course=course,
        defaults={'mode': 'audit'}
    )
    if created:
        course.total_enrollment += 1
        course.save()
    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))


@login_required
def submit(request, course_id):
    """
    Processes submitted exam choices (POST request) and creates a
    Submission record linked to the user's Enrollment.
    """
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    # Retrieve or create enrollment for the logged-in user
    enrollment, created = Enrollment.objects.get_or_create(
        user=user,
        course=course,
        defaults={'mode': 'audit'}
    )
    if created:
        course.total_enrollment += 1
        course.save()

    if request.method == 'POST':
        # Collect selected choice IDs from POST parameters
        # Checks both choice_<id> keys and general choices/choice list fields
        selected_choice_ids = []

        for key, value in request.POST.items():
            if key.startswith('choice'):
                try:
                    selected_choice_ids.append(int(value))
                except (ValueError, TypeError):
                    pass

        # Check fallback names if standard keys were not used
        if not selected_choice_ids:
            for item in request.POST.getlist('choices') + request.POST.getlist('choice'):
                if str(item).isdigit():
                    selected_choice_ids.append(int(item))

        # Create a new Submission entry
        submission = Submission.objects.create(enrollment=enrollment)
        if selected_choice_ids:
            submission.choices.set(selected_choice_ids)

        return HttpResponseRedirect(
            reverse('onlinecourse:show_exam_result', args=(course.id, submission.id))
        )

    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))


@login_required
def show_exam_result(request, course_id, submission_id):
    """
    Calculates total points earned versus maximum possible score,
    determines if the user passed, and renders the results context.
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    # Get all choice IDs selected in this submission
    selected_choice_ids = list(submission.choices.values_list('id', flat=True))

    total_score = 0
    score = 0

    # Calculate total course score and user score based on each question's evaluation
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            total_score += question.grade
            if question.is_get_score(selected_choice_ids):
                score += question.grade

    # Calculate percentage grade (avoid division by zero)
    grade = round((score / total_score) * 100, 2) if total_score > 0 else 0
    # Passing threshold is 80%
    passed = grade >= 80

    context = {
        'course': course,
        'submission': submission,
        'score': score,
        'total_score': total_score,
        'grade': grade,
        'passed': passed,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)


# Authentication Views
def registration_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully for {user.username}!")
            return redirect('onlinecourse:index')
        else:
            messages.error(request, "Unsuccessful registration. Please verify invalid information.")
    else:
        form = UserCreationForm()
    return render(request, 'onlinecourse/register.html', {'form': form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('onlinecourse:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'onlinecourse/login.html', {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('onlinecourse:index')
