# Online Course Platform with Quiz & Exam Features

A full-featured Django web application for an online learning platform. Features course management, lesson structures, interactive quizzes, automated grading with percentage calculation, and enrollment tracking.

## Core Features Implemented

1. **Database Models (`onlinecourse/models.py`)**:
   - `Course`, `Lesson`, `Instructor`, `Learner`, `Enrollment`.
   - `Question`: linked to `Lesson` (ForeignKey), includes `question_text`, `grade`, and method `is_get_score(selected_ids)` to evaluate whether selected choice IDs contain all correct answers and no incorrect answers.
   - `Choice`: linked to `Question` (ForeignKey), includes `choice_text` and `is_correct` (BooleanField).
   - `Submission`: linked to `Enrollment` (ForeignKey) with ManyToManyField to `Choice`.

2. **Django Admin (`onlinecourse/admin.py`)**:
   - `QuestionInline` (StackedInline) embedded in `LessonAdmin`.
   - `ChoiceInline` (StackedInline) embedded in `QuestionAdmin`.
   - Registered models with search fields and list displays for easy quiz administration.

3. **Bootstrap UI Templates (`onlinecourse/templates/onlinecourse/`)**:
   - `course_details_bootstrap.html`: Responsive Bootstrap 5 template with hero banner, lesson accordion, embedded quiz questions with choice checkboxes, and exam submission form.
   - `exam_result_bootstrap.html`: Clean result dashboard displaying score earned, total possible points, grade percentage, pass/fail badge (80% threshold), and detailed question-by-question review.

4. **Views & Business Logic (`onlinecourse/views.py`)**:
   - `submit`: Processes submitted exam choices via POST, extracts choice IDs, creates a `Submission` record for the user's `Enrollment`, and redirects to results.
   - `show_exam_result`: Computes user's score vs. maximum points across all lesson questions, calculates percentage, determines pass status, and renders the result view.

5. **Routing (`onlinecourse/urls.py`)**:
   - `<int:course_id>/submit/` -> `views.submit`
   - `<int:course_id>/submission/<int:submission_id>/result/` -> `views.show_exam_result`

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser (for Admin Access)**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```
   Navigate to `http://127.0.0.1:8000/` to view the course platform and `http://127.0.0.1:8000/admin/` to manage courses, questions, and choices.
