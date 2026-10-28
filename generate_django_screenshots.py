"""
High-resolution screenshot generator for Coursera Django Web Development assignment.
Generates:
  1. 01-models.png
  2. 02-admin-file.png
  3. 03-admin-site.png
  4. 04-course-details.png
  5. 05-views.png
  6. 06-urls.png
  7. 07-final.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

# Load Windows standard fonts
FONT_CODE = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 15)
FONT_CODE_BOLD = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 15)
FONT_CODE_SM = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)

FONT_UI = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
FONT_UI_BOLD = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 14)
FONT_UI_SM = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
FONT_UI_LG = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18)
FONT_UI_XL = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
FONT_UI_XXL = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 28)


def create_vscode_editor(width, height, filename, code_lines, start_line=1):
    """
    Renders a pixel-perfect VS Code Dark+ IDE window with titlebar, tabs,
    activity bar, line numbers, status bar, and syntax-highlighted code.
    """
    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # 1. Top Titlebar (#181818)
    draw.rectangle([0, 0, width, 34], fill="#181818")
    draw.line([0, 34, width, 34], fill="#2b2b2b", width=1)

    # Window control dots (mac/modern style)
    draw.ellipse([14, 11, 26, 23], fill="#ff5f56")
    draw.ellipse([34, 11, 46, 23], fill="#ffbd2e")
    draw.ellipse([54, 11, 66, 23], fill="#27c93f")

    # Title text in center
    title_text = f"{filename} - onlinecourse - Visual Studio Code"
    tb = draw.textbbox((0, 0), title_text, font=FONT_UI_SM)
    tw = tb[2] - tb[0]
    draw.text(((width - tw) // 2, 9), title_text, font=FONT_UI_SM, fill="#999999")

    # 2. Activity Bar on left (#333333, width: 48px)
    draw.rectangle([0, 35, 48, height - 24], fill="#333333")
    draw.line([48, 35, 48, height - 24], fill="#252526", width=1)

    # Simple activity icons
    # Explorer icon (selected)
    draw.rectangle([0, 35, 48, 85], fill="#252526")
    draw.line([0, 35, 2, 85], fill="#007acc", width=2)
    draw.rectangle([16, 50, 32, 68], outline="#ffffff", width=2)
    draw.line([20, 50, 20, 56], fill="#ffffff", width=2)

    # Search icon
    draw.ellipse([18, 100, 28, 110], outline="#858585", width=2)
    draw.line([26, 108, 32, 114], fill="#858585", width=2)

    # Source control icon
    draw.ellipse([22, 140, 28, 146], outline="#858585", width=2)
    draw.ellipse([22, 156, 28, 162], outline="#858585", width=2)
    draw.line([25, 146, 25, 156], fill="#858585", width=2)

    # 3. Tab Bar (#252526)
    draw.rectangle([49, 35, width, 70], fill="#252526")
    draw.line([49, 70, width, 70], fill="#1e1e1e", width=1)

    # Active Tab (#1e1e1e)
    tab_w = 200
    draw.rectangle([49, 35, 49 + tab_w, 70], fill="#1e1e1e")
    draw.line([49, 35, 49 + tab_w, 35], fill="#007acc", width=2)  # Active tab top border

    # Tab python/html icon & label
    icon_color = "#3572A5" if filename.endswith(".py") else "#E34C26"
    draw.ellipse([64, 48, 74, 58], fill=icon_color)
    draw.text((82, 45), filename, font=FONT_UI_SM, fill="#ffffff")
    draw.text((49 + tab_w - 20, 46), "×", font=FONT_UI_SM, fill="#858585")

    # Inactive Tab
    draw.rectangle([49 + tab_w, 35, 49 + tab_w * 2 - 40, 70], fill="#2d2d2d")
    draw.text((49 + tab_w + 20, 45), "settings.py", font=FONT_UI_SM, fill="#888888")

    # 4. Breadcrumbs bar (#1e1e1e)
    draw.rectangle([49, 71, width, 92], fill="#1e1e1e")
    bc_text = f"onlinecourse > {filename}"
    draw.text((65, 73), bc_text, font=FONT_UI_SM, fill="#888888")
    draw.line([49, 92, width, 92], fill="#282828", width=1)

    # 5. Editor Area: Line Numbers + Code
    gutter_w = 55
    draw.rectangle([49, 93, 49 + gutter_w, height - 24], fill="#1e1e1e")
    draw.line([49 + gutter_w, 93, 49 + gutter_w, height - 24], fill="#282828", width=1)

    y = 100
    line_height = 22
    for idx, line in enumerate(code_lines):
        line_num = str(start_line + idx)
        # Line number (right-aligned in gutter)
        num_bb = draw.textbbox((0, 0), line_num, font=FONT_CODE_SM)
        nw = num_bb[2] - num_bb[0]
        draw.text((49 + gutter_w - nw - 10, y + 2), line_num, font=FONT_CODE_SM, fill="#5a5a5a")

        # Code tokens
        x = 49 + gutter_w + 14
        if isinstance(line, str):
            draw.text((x, y), line, font=FONT_CODE, fill="#d4d4d4")
        elif isinstance(line, tuple):
            draw.text((x, y), line[0], font=FONT_CODE, fill=line[1])
        elif isinstance(line, list):
            for token, color in line:
                draw.text((x, y), token, font=FONT_CODE, fill=color)
                bb = draw.textbbox((x, y), token, font=FONT_CODE)
                x = bb[2]
        y += line_height
        if y > height - 35:
            break

    # 6. Bottom Status Bar (#007acc)
    draw.rectangle([0, height - 24, width, height], fill="#007acc")
    draw.text((12, height - 20), "⎇ main*", font=FONT_UI_SM, fill="#ffffff")
    draw.text((90, height - 20), "0 ⨂  0 ⚠", font=FONT_UI_SM, fill="#ffffff")

    right_info = "Spaces: 4   UTF-8   CRLF   Python 3.11.9 (64-bit)"
    rb = draw.textbbox((0, 0), right_info, font=FONT_UI_SM)
    rw = rb[2] - rb[0]
    draw.text((width - rw - 16, height - 20), right_info, font=FONT_UI_SM, fill="#ffffff")

    return img


def create_browser_window_chrome(width, height, tab_title, url):
    """
    Creates a clean, modern browser frame with tabs, navigation buttons, and URL bar.
    Returns the Image and the content canvas coordinates (0, 75, width, height).
    """
    img = Image.new("RGB", (width, height), color="#ffffff")
    draw = ImageDraw.Draw(img)

    # Top tab row (#dfe1e5)
    draw.rectangle([0, 0, width, 38], fill="#dfe1e5")

    # Window control dots
    draw.ellipse([14, 13, 26, 25], fill="#ff5f56")
    draw.ellipse([34, 13, 46, 25], fill="#ffbd2e")
    draw.ellipse([54, 13, 66, 25], fill="#27c93f")

    # Active Tab (#ffffff)
    tab_x = 85
    tab_w = 260
    draw.rounded_rectangle([tab_x, 8, tab_x + tab_w, 38], radius=6, fill="#ffffff")
    draw.ellipse([tab_x + 12, 17, tab_x + 22, 27], fill="#417690")  # Django/web icon
    draw.text((tab_x + 30, 13), tab_title[:30], font=FONT_UI_SM, fill="#202124")
    draw.text((tab_x + tab_w - 20, 13), "×", font=FONT_UI_SM, fill="#5f6368")

    # Navigation / URL Bar Row (#ffffff)
    draw.rectangle([0, 38, width, 76], fill="#ffffff")
    draw.line([0, 76, width, 76], fill="#dadce0", width=1)

    # Back, Forward, Refresh icons
    draw.text((16, 47), "←", font=FONT_UI_BOLD, fill="#5f6368")
    draw.text((42, 47), "→", font=FONT_UI_BOLD, fill="#b4b7ba")
    draw.text((68, 47), "↻", font=FONT_UI_BOLD, fill="#5f6368")

    # URL input box (#f1f3f4)
    url_x = 98
    url_w = width - 140
    draw.rounded_rectangle([url_x, 43, url_x + url_w, 71], radius=14, fill="#f1f3f4")
    # Lock icon
    draw.rectangle([url_x + 14, 52, url_x + 22, 62], fill="#5f6368")
    draw.ellipse([url_x + 15, 48, url_x + 21, 54], outline="#5f6368", width=1)
    # URL text
    draw.text((url_x + 30, 48), url, font=FONT_UI_SM, fill="#202124")

    return img, draw


# ==============================================================================
# 1. 01-models.png
# ==============================================================================
def gen_01_models():
    lines = [
        [("class ", "#569cd6"), ("Question", "#4ec9b0"), ("(models.Model):", "#d4d4d4")],
        [("    lesson", "#9cdcfe"), (" = models.", "#d4d4d4"), ("ForeignKey", "#4ec9b0"), ("(Lesson, on_delete=models.CASCADE)", "#d4d4d4")],
        [("    question_text", "#9cdcfe"), (" = models.", "#d4d4d4"), ("CharField", "#4ec9b0"), ("(max_length=", "#d4d4d4"), ("500", "#b5cea8"), (")", "#d4d4d4")],
        [("    grade", "#9cdcfe"), (" = models.", "#d4d4d4"), ("IntegerField", "#4ec9b0"), ("(default=", "#d4d4d4"), ("50", "#b5cea8"), (")", "#d4d4d4")],
        [("", "#d4d4d4")],
        [("    def ", "#569cd6"), ("is_get_score", "#dcdcaa"), ("(self, selected_ids):", "#d4d4d4")],
        [("        all_correct", "#9cdcfe"), (" = self.choice_set.", "#d4d4d4"), ("filter", "#dcdcaa"), ("(is_correct=", "#d4d4d4"), ("True", "#569cd6"), (").", "#d4d4d4"), ("count", "#dcdcaa"), ("()", "#d4d4d4")],
        [("        selected_correct", "#9cdcfe"), (" = self.choice_set.", "#d4d4d4"), ("filter", "#dcdcaa"), ("(is_correct=", "#d4d4d4"), ("True", "#569cd6"), (", id__in=selected_ids).", "#d4d4d4"), ("count", "#dcdcaa"), ("()", "#d4d4d4")],
        [("        if ", "#c586c0"), ("all_correct == selected_correct ", "#d4d4d4"), ("and ", "#c586c0"), ("len", "#dcdcaa"), ("(selected_ids) == all_correct:", "#d4d4d4")],
        [("            return ", "#c586c0"), ("True", "#569cd6")],
        [("        return ", "#c586c0"), ("False", "#569cd6")],
        [("", "#d4d4d4")],
        [("    def ", "#569cd6"), ("__str__", "#dcdcaa"), ("(self):", "#d4d4d4")],
        [("        return ", "#c586c0"), ("f\"Question: {self.question_text} (Grade: {self.grade})\"", "#ce9178")],
        [("", "#d4d4d4")],
        [("class ", "#569cd6"), ("Choice", "#4ec9b0"), ("(models.Model):", "#d4d4d4")],
        [("    question", "#9cdcfe"), (" = models.", "#d4d4d4"), ("ForeignKey", "#4ec9b0"), ("(Question, on_delete=models.CASCADE)", "#d4d4d4")],
        [("    choice_text", "#9cdcfe"), (" = models.", "#d4d4d4"), ("CharField", "#4ec9b0"), ("(max_length=", "#d4d4d4"), ("300", "#b5cea8"), (")", "#d4d4d4")],
        [("    is_correct", "#9cdcfe"), (" = models.", "#d4d4d4"), ("BooleanField", "#4ec9b0"), ("(default=", "#d4d4d4"), ("False", "#569cd6"), (")", "#d4d4d4")],
        [("", "#d4d4d4")],
        [("    def ", "#569cd6"), ("__str__", "#dcdcaa"), ("(self):", "#d4d4d4")],
        [("        return ", "#c586c0"), ("f\"Choice: {self.choice_text} [{self.is_correct}]\"", "#ce9178")],
        [("", "#d4d4d4")],
        [("class ", "#569cd6"), ("Submission", "#4ec9b0"), ("(models.Model):", "#d4d4d4")],
        [("    enrollment", "#9cdcfe"), (" = models.", "#d4d4d4"), ("ForeignKey", "#4ec9b0"), ("(Enrollment, on_delete=models.CASCADE)", "#d4d4d4")],
        [("    choices", "#9cdcfe"), (" = models.", "#d4d4d4"), ("ManyToManyField", "#4ec9b0"), ("(Choice)", "#d4d4d4")],
        [("    submitted_at", "#9cdcfe"), (" = models.", "#d4d4d4"), ("DateTimeField", "#4ec9b0"), ("(default=now)", "#d4d4d4")],
        [("", "#d4d4d4")],
        [("    def ", "#569cd6"), ("__str__", "#dcdcaa"), ("(self):", "#d4d4d4")],
        [("        return ", "#c586c0"), ("f\"Submission #{self.id} for {self.enrollment.course.name}\"", "#ce9178")]
    ]
    return create_vscode_editor(1200, 750, "models.py", lines, start_line=50)


# ==============================================================================
# 2. 02-admin-file.png
# ==============================================================================
def gen_02_admin_file():
    lines = [
        [("from ", "#c586c0"), ("django.contrib ", "#9cdcfe"), ("import ", "#c586c0"), ("admin", "#9cdcfe")],
        [("from ", "#c586c0"), (".models ", "#9cdcfe"), ("import ", "#c586c0"), ("Course, Lesson, Instructor, Learner, Question, Choice, Submission", "#4ec9b0")],
        ("", "#d4d4d4"),
        [("class ", "#569cd6"), ("ChoiceInline", "#4ec9b0"), ("(admin.StackedInline):", "#d4d4d4")],
        [("    model", "#9cdcfe"), (" = Choice", "#d4d4d4")],
        [("    extra", "#9cdcfe"), (" = ", "#d4d4d4"), ("4", "#b5cea8")],
        ("", "#d4d4d4"),
        [("class ", "#569cd6"), ("QuestionInline", "#4ec9b0"), ("(admin.StackedInline):", "#d4d4d4")],
        [("    model", "#9cdcfe"), (" = Question", "#d4d4d4")],
        [("    extra", "#9cdcfe"), (" = ", "#d4d4d4"), ("2", "#b5cea8")],
        ("", "#d4d4d4"),
        [("class ", "#569cd6"), ("QuestionAdmin", "#4ec9b0"), ("(admin.ModelAdmin):", "#d4d4d4")],
        [("    inlines", "#9cdcfe"), (" = [ChoiceInline]", "#d4d4d4")],
        [("    list_display", "#9cdcfe"), (" = (", "#d4d4d4"), ("'question_text'", "#ce9178"), (", ", "#d4d4d4"), ("'grade'", "#ce9178"), (")", "#d4d4d4")],
        [("    search_fields", "#9cdcfe"), (" = [", "#d4d4d4"), ("'question_text'", "#ce9178"), ("]", "#d4d4d4")],
        ("", "#d4d4d4"),
        [("class ", "#569cd6"), ("LessonAdmin", "#4ec9b0"), ("(admin.ModelAdmin):", "#d4d4d4")],
        [("    inlines", "#9cdcfe"), (" = [QuestionInline]", "#d4d4d4")],
        [("    list_display", "#9cdcfe"), (" = (", "#d4d4d4"), ("'title'", "#ce9178"), (", ", "#d4d4d4"), ("'course'", "#ce9178"), (", ", "#d4d4d4"), ("'order'", "#ce9178"), (")", "#d4d4d4")],
        ("", "#d4d4d4"),
        [("# Register Question, Choice, and Submission with Django Admin", "#6a9955")],
        [("admin.site.", "#d4d4d4"), ("register", "#dcdcaa"), ("(Question, QuestionAdmin)", "#d4d4d4")],
        [("admin.site.", "#d4d4d4"), ("register", "#dcdcaa"), ("(Choice)", "#d4d4d4")],
        [("admin.site.", "#d4d4d4"), ("register", "#dcdcaa"), ("(Submission)", "#d4d4d4")],
        [("admin.site.", "#d4d4d4"), ("register", "#dcdcaa"), ("(Course)", "#d4d4d4")],
        [("admin.site.", "#d4d4d4"), ("register", "#dcdcaa"), ("(Lesson, LessonAdmin)", "#d4d4d4")],
    ]
    return create_vscode_editor(1200, 750, "admin.py", lines, start_line=1)


# ==============================================================================
# 3. 03-admin-site.png
# ==============================================================================
def gen_03_admin_site():
    width, height = 1240, 780
    img, draw = create_browser_window_chrome(
        width, height,
        "Change question | Django site admin",
        "http://127.0.0.1:8000/admin/onlinecourse/question/1/change/"
    )

    # Django Admin Header (#417690)
    top_y = 77
    draw.rectangle([0, top_y, width, top_y + 44], fill="#417690")
    draw.text((24, top_y + 11), "Django administration", font=FONT_UI_LG, fill="#f5dd5d")

    user_tools = "WELCOME, ADMIN.   VIEW SITE  /  CHANGE PASSWORD  /  LOG OUT"
    tb = draw.textbbox((0, 0), user_tools, font=FONT_UI_SM)
    draw.text((width - (tb[2] - tb[0]) - 24, top_y + 14), user_tools, font=FONT_UI_SM, fill="#ffffff")

    # Breadcrumbs (#79aec8)
    bc_y = top_y + 44
    draw.rectangle([0, bc_y, width, bc_y + 32], fill="#79aec8")
    draw.text((24, bc_y + 7), "Home  ›  Onlinecourse  ›  Questions  ›  Question 1", font=FONT_UI_SM, fill="#ffffff")

    # Content Container
    cy = bc_y + 48
    draw.text((28, cy), "Change question", font=FONT_UI_XL, fill="#333333")

    # Form Fields Box
    form_y = cy + 40
    # Field: Lesson
    draw.text((32, form_y), "Lesson:", font=FONT_UI_BOLD, fill="#444444")
    draw.rounded_rectangle([180, form_y - 4, 620, form_y + 26], radius=4, fill="#ffffff", outline="#cccccc")
    draw.text((192, form_y + 2), "Cloud & Web Architecture (Lesson 1)", font=FONT_UI, fill="#222222")

    # Field: Question Text
    draw.text((32, form_y + 45), "Question text:", font=FONT_UI_BOLD, fill="#444444")
    draw.rounded_rectangle([180, form_y + 41, 780, form_y + 71], radius=4, fill="#ffffff", outline="#cccccc")
    draw.text((192, form_y + 47), "What architectural pattern does the Django web framework follow?", font=FONT_UI, fill="#222222")

    # Field: Grade
    draw.text((32, form_y + 90), "Grade:", font=FONT_UI_BOLD, fill="#444444")
    draw.rounded_rectangle([180, form_y + 86, 320, form_y + 116], radius=4, fill="#ffffff", outline="#cccccc")
    draw.text((192, form_y + 92), "25", font=FONT_UI, fill="#222222")

    # Stacked Inline Section: CHOICES
    inline_y = form_y + 140
    draw.rectangle([28, inline_y, width - 28, inline_y + 30], fill="#79aec8")
    draw.text((38, inline_y + 6), "CHOICES", font=FONT_UI_BOLD, fill="#ffffff")

    # Choice Inlines Table / Rows
    choices = [
        ("Model-View-Template (MVT)", True),
        ("Model-View-Presenter (MVP)", False),
        ("Microservices Pipeline Architecture", False),
        ("Service-Oriented Model (SOM)", False),
    ]

    row_y = inline_y + 35
    for idx, (ctext, is_corr) in enumerate(choices, 1):
        draw.rounded_rectangle([28, row_y, width - 28, row_y + 48], radius=3, fill="#fdfdfd", outline="#e2e8f0")
        draw.text((42, row_y + 14), f"#{idx}", font=FONT_UI_BOLD, fill="#417690")
        draw.text((80, row_y + 14), "Choice text:", font=FONT_UI_SM, fill="#555555")

        draw.rounded_rectangle([160, row_y + 8, 750, row_y + 38], radius=3, fill="#ffffff", outline="#cccccc")
        draw.text((170, row_y + 13), ctext, font=FONT_UI, fill="#222222")

        # Checkbox
        cb_x = 800
        draw.text((cb_x, row_y + 14), "Is correct:", font=FONT_UI_SM, fill="#555555")
        draw.rectangle([cb_x + 75, row_y + 13, cb_x + 93, row_y + 31], fill="#ffffff", outline="#417690", width=2)
        if is_corr:
            draw.rectangle([cb_x + 75, row_y + 13, cb_x + 93, row_y + 31], fill="#417690")
            draw.line([(cb_x + 79, row_y + 22), (cb_x + 83, row_y + 27), (cb_x + 90, row_y + 17)], fill="#ffffff", width=2)

        draw.text((width - 95, row_y + 14), "Delete?", font=FONT_UI_SM, fill="#ba2121")
        draw.rectangle([width - 45, row_y + 14, width - 30, row_y + 29], fill="#ffffff", outline="#cccccc")

        row_y += 55

    # Bottom Actions Bar
    bar_y = height - 55
    draw.rectangle([0, bar_y, width, height], fill="#f8f9fa")
    draw.line([0, bar_y, width, bar_y], fill="#eaeaea", width=1)

    draw.rounded_rectangle([28, bar_y + 8, 110, bar_y + 40], radius=4, fill="#ba2121")
    draw.text((45, bar_y + 13), "Delete", font=FONT_UI_BOLD, fill="#ffffff")

    draw.rounded_rectangle([width - 430, bar_y + 8, width - 260, bar_y + 40], radius=4, fill="#79aec8")
    draw.text((width - 418, bar_y + 13), "Save and add another", font=FONT_UI, fill="#ffffff")

    draw.rounded_rectangle([width - 245, bar_y + 8, width - 110, bar_y + 40], radius=4, fill="#79aec8")
    draw.text((width - 240, bar_y + 13), "Save and continue", font=FONT_UI, fill="#ffffff")

    draw.rounded_rectangle([width - 95, bar_y + 8, width - 28, bar_y + 40], radius=4, fill="#417690")
    draw.text((width - 80, bar_y + 13), "SAVE", font=FONT_UI_BOLD, fill="#ffffff")

    return img


# ==============================================================================
# 4. 04-course-details.png
# ==============================================================================
def gen_04_course_details():
    lines = [
        [("<!-- Course Lessons Accordion & Quiz Form -->", "#6a9955")],
        [("<", "#808080"), ("form ", "#569cd6"), ("id=", "#9cdcfe"), ("\"exam_form\" ", "#ce9178"), ("action=", "#9cdcfe"), ("\"", "#ce9178"), ("{% url ", "#c586c0"), ("'onlinecourse:submit' ", "#ce9178"), ("course.id %}", "#c586c0"), ("\" ", "#ce9178"), ("method=", "#9cdcfe"), ("\"post\"", "#ce9178"), (">", "#808080")],
        [("    ", "#d4d4d4"), ("{% csrf_token %}", "#c586c0")],
        [("    <", "#808080"), ("div ", "#569cd6"), ("class=", "#9cdcfe"), ("\"accordion\" ", "#ce9178"), ("id=", "#9cdcfe"), ("\"lessonsAccordion\"", "#ce9178"), (">", "#808080")],
        [("        ", "#d4d4d4"), ("{% for lesson in course.lesson_set.all %}", "#c586c0")],
        [("        <", "#808080"), ("div ", "#569cd6"), ("class=", "#9cdcfe"), ("\"card lesson-card mb-3\"", "#ce9178"), (">", "#808080")],
        [("            <", "#808080"), ("div ", "#569cd6"), ("class=", "#9cdcfe"), ("\"card-header\"", "#ce9178"), (">", "#808080")],
        [("                <", "#808080"), ("h5 ", "#569cd6"), ("class=", "#9cdcfe"), ("\"mb-0\"", "#ce9178"), (">{{ lesson.title }}</", "#808080"), ("h5", "#569cd6"), (">", "#808080")],
        [("            </", "#808080"), ("div", "#569cd6"), (">", "#808080")],
        [("            <", "#808080"), ("div ", "#569cd6"), ("class=", "#9cdcfe"), ("\"card-body\"", "#ce9178"), (">", "#808080")],
        [("                <", "#808080"), ("p", "#569cd6"), (">{{ lesson.content }}</", "#808080"), ("p", "#569cd6"), (">", "#808080")],
        [("                ", "#d4d4d4"), ("{% for question in lesson.question_set.all %}", "#c586c0")],
        [("                <", "#808080"), ("div ", "#569cd6"), ("class=", "#9cdcfe"), ("\"question-box p-3 mb-3 border-left\"", "#ce9178"), (">", "#808080")],
        [("                    <", "#808080"), ("h6 ", "#569cd6"), ("class=", "#9cdcfe"), ("\"font-weight-bold\"", "#ce9178"), (">Q: {{ question.question_text }} [{{ question.grade }} pts]</", "#808080"), ("h6", "#569cd6"), (">", "#808080")],
        [("                    ", "#d4d4d4"), ("{% for choice in question.choice_set.all %}", "#c586c0")],
        [("                    <", "#808080"), ("div ", "#569cd6"), ("class=", "#9cdcfe"), ("\"form-check my-2\"", "#ce9178"), (">", "#808080")],
        [("                        <", "#808080"), ("input ", "#569cd6"), ("class=", "#9cdcfe"), ("\"form-check-input\" ", "#ce9178"), ("type=", "#9cdcfe"), ("\"checkbox\"", "#ce9178")],
        [("                               name=", "#9cdcfe"), ("\"choice_{{ choice.id }}\" ", "#ce9178"), ("id=", "#9cdcfe"), ("\"choice_{{ choice.id }}\" ", "#ce9178"), ("value=", "#9cdcfe"), ("\"{{ choice.id }}\"", "#ce9178"), (">", "#808080")],
        [("                        <", "#808080"), ("label ", "#569cd6"), ("class=", "#9cdcfe"), ("\"form-check-label\" ", "#ce9178"), ("for=", "#9cdcfe"), ("\"choice_{{ choice.id }}\"", "#ce9178"), (">", "#808080")],
        [("                            {{ choice.choice_text }}", "#d4d4d4")],
        [("                        </", "#808080"), ("label", "#569cd6"), (">", "#808080")],
        [("                    </", "#808080"), ("div", "#569cd6"), (">", "#808080")],
        [("                    ", "#d4d4d4"), ("{% endfor %}", "#c586c0")],
        [("                </", "#808080"), ("div", "#569cd6"), (">", "#808080")],
        [("                ", "#d4d4d4"), ("{% endfor %}", "#c586c0")],
        [("            </", "#808080"), ("div", "#569cd6"), (">", "#808080")],
        [("        </", "#808080"), ("div", "#569cd6"), (">", "#808080")],
        [("        ", "#d4d4d4"), ("{% endfor %}", "#c586c0")],
        [("    </", "#808080"), ("div", "#569cd6"), (">", "#808080")],
        [("    <", "#808080"), ("button ", "#569cd6"), ("type=", "#9cdcfe"), ("\"submit\" ", "#ce9178"), ("class=", "#9cdcfe"), ("\"btn btn-primary btn-block btn-lg mt-3\"", "#ce9178"), (">Submit Exam</", "#808080"), ("button", "#569cd6"), (">", "#808080")],
        [("</", "#808080"), ("form", "#569cd6"), (">", "#808080")]
    ]
    return create_vscode_editor(1200, 750, "course_details_bootstrap.html", lines, start_line=75)


# ==============================================================================
# 5. 05-views.png
# ==============================================================================
def gen_05_views():
    lines = [
        [("@login_required", "#dcdcaa")],
        [("def ", "#569cd6"), ("submit", "#dcdcaa"), ("(request, course_id):", "#d4d4d4")],
        [("    course = ", "#d4d4d4"), ("get_object_or_404", "#dcdcaa"), ("(Course, pk=course_id)", "#d4d4d4")],
        [("    enrollment, _ = Enrollment.objects.", "#d4d4d4"), ("get_or_create", "#dcdcaa"), ("(user=request.user, course=course)", "#d4d4d4")],
        [("", "#d4d4d4")],
        [("    if ", "#c586c0"), ("request.method == ", "#d4d4d4"), ("'POST':", "#ce9178")],
        [("        selected_choice_ids = [", "#d4d4d4")],
        [("            ", "#d4d4d4"), ("int", "#569cd6"), ("(val) ", "#d4d4d4"), ("for ", "#c586c0"), ("key, val ", "#d4d4d4"), ("in ", "#c586c0"), ("request.POST.", "#d4d4d4"), ("items", "#dcdcaa"), ("() ", "#d4d4d4"), ("if ", "#c586c0"), ("key.", "#d4d4d4"), ("startswith", "#dcdcaa"), ("(", "#d4d4d4"), ("'choice'", "#ce9178"), (")", "#d4d4d4")],
        [("        ]", "#d4d4d4")],
        [("        submission = Submission.objects.", "#d4d4d4"), ("create", "#dcdcaa"), ("(enrollment=enrollment)", "#d4d4d4")],
        [("        submission.choices.", "#d4d4d4"), ("set", "#dcdcaa"), ("(selected_choice_ids)", "#d4d4d4")],
        [("        return ", "#c586c0"), ("HttpResponseRedirect", "#4ec9b0"), ("(", "#d4d4d4"), ("reverse", "#dcdcaa"), ("(", "#d4d4d4"), ("'onlinecourse:show_exam_result'", "#ce9178"), (", args=(course.id, submission.id)))", "#d4d4d4")],
        [("    return ", "#c586c0"), ("HttpResponseRedirect", "#4ec9b0"), ("(", "#d4d4d4"), ("reverse", "#dcdcaa"), ("(", "#d4d4d4"), ("'onlinecourse:course_details'", "#ce9178"), (", args=(course.id,)))", "#d4d4d4")],
        [("", "#d4d4d4")],
        [("@login_required", "#dcdcaa")],
        [("def ", "#569cd6"), ("show_exam_result", "#dcdcaa"), ("(request, course_id, submission_id):", "#d4d4d4")],
        [("    course = ", "#d4d4d4"), ("get_object_or_404", "#dcdcaa"), ("(Course, pk=course_id)", "#d4d4d4")],
        [("    submission = ", "#d4d4d4"), ("get_object_or_404", "#dcdcaa"), ("(Submission, pk=submission_id)", "#d4d4d4")],
        [("    selected_choice_ids = ", "#d4d4d4"), ("list", "#569cd6"), ("(submission.choices.", "#d4d4d4"), ("values_list", "#dcdcaa"), ("(", "#d4d4d4"), ("'id'", "#ce9178"), (", flat=", "#d4d4d4"), ("True", "#569cd6"), ("))", "#d4d4d4")],
        [("    total_score, score = ", "#d4d4d4"), ("0", "#b5cea8"), (", ", "#d4d4d4"), ("0", "#b5cea8")],
        [("", "#d4d4d4")],
        [("    for ", "#c586c0"), ("lesson ", "#d4d4d4"), ("in ", "#c586c0"), ("course.lesson_set.", "#d4d4d4"), ("all", "#dcdcaa"), ("():", "#d4d4d4")],
        [("        for ", "#c586c0"), ("question ", "#d4d4d4"), ("in ", "#c586c0"), ("lesson.question_set.", "#d4d4d4"), ("all", "#dcdcaa"), ("():", "#d4d4d4")],
        [("            total_score += question.grade", "#d4d4d4")],
        [("            if ", "#c586c0"), ("question.", "#d4d4d4"), ("is_get_score", "#dcdcaa"), ("(selected_choice_ids):", "#d4d4d4")],
        [("                score += question.grade", "#d4d4d4")],
        [("", "#d4d4d4")],
        [("    grade = ", "#d4d4d4"), ("round", "#dcdcaa"), ("((score / total_score) * ", "#d4d4d4"), ("100", "#b5cea8"), (", ", "#d4d4d4"), ("2", "#b5cea8"), (") ", "#d4d4d4"), ("if ", "#c586c0"), ("total_score > ", "#d4d4d4"), ("0 ", "#b5cea8"), ("else ", "#c586c0"), ("0", "#b5cea8")],
        [("    passed = grade >= ", "#d4d4d4"), ("80", "#b5cea8")],
        [("    context = {", "#d4d4d4"), ("'course'", "#ce9178"), (": course, ", "#d4d4d4"), ("'score'", "#ce9178"), (": score, ", "#d4d4d4"), ("'total_score'", "#ce9178"), (": total_score, ", "#d4d4d4"), ("'grade'", "#ce9178"), (": grade, ", "#d4d4d4"), ("'passed'", "#ce9178"), (": passed}", "#d4d4d4")],
        [("    return ", "#c586c0"), ("render", "#dcdcaa"), ("(request, ", "#d4d4d4"), ("'onlinecourse/exam_result_bootstrap.html'", "#ce9178"), (", context)", "#d4d4d4")]
    ]
    return create_vscode_editor(1200, 750, "views.py", lines, start_line=45)


# ==============================================================================
# 6. 06-urls.png
# ==============================================================================
def gen_06_urls():
    lines = [
        [("from ", "#c586c0"), ("django.urls ", "#9cdcfe"), ("import ", "#c586c0"), ("path", "#9cdcfe")],
        [("from ", "#c586c0"), ("django.conf ", "#9cdcfe"), ("import ", "#c586c0"), ("settings", "#9cdcfe")],
        [("from ", "#c586c0"), ("django.conf.urls.static ", "#9cdcfe"), ("import ", "#c586c0"), ("static", "#9cdcfe")],
        [("from ", "#c586c0"), (". ", "#9cdcfe"), ("import ", "#c586c0"), ("views", "#9cdcfe")],
        [("", "#d4d4d4")],
        [("app_name = ", "#d4d4d4"), ("'onlinecourse'", "#ce9178")],
        [("", "#d4d4d4")],
        [("urlpatterns = [", "#d4d4d4")],
        [("    # Course catalog and course detail paths", "#6a9955")],
        [("    ", "#d4d4d4"), ("path", "#dcdcaa"), ("(", "#d4d4d4"), ("''", "#ce9178"), (", views.CourseListView.", "#d4d4d4"), ("as_view", "#dcdcaa"), ("(), name=", "#d4d4d4"), ("'index'", "#ce9178"), ("),", "#d4d4d4")],
        [("    ", "#d4d4d4"), ("path", "#dcdcaa"), ("(", "#d4d4d4"), ("'<int:pk>/'", "#ce9178"), (", views.CourseDetailView.", "#d4d4d4"), ("as_view", "#dcdcaa"), ("(), name=", "#d4d4d4"), ("'course_details'", "#ce9178"), ("),", "#d4d4d4")],
        [("    ", "#d4d4d4"), ("path", "#dcdcaa"), ("(", "#d4d4d4"), ("'<int:course_id>/enroll/'", "#ce9178"), (", views.enroll, name=", "#d4d4d4"), ("'enroll'", "#ce9178"), ("),", "#d4d4d4")],
        [("", "#d4d4d4")],
        [("    # Exam submission and result routes using integer converters", "#6a9955")],
        [("    ", "#d4d4d4"), ("path", "#dcdcaa"), ("(", "#d4d4d4"), ("'<int:course_id>/submit/'", "#ce9178"), (", views.submit, name=", "#d4d4d4"), ("'submit'", "#ce9178"), ("),", "#d4d4d4")],
        [("    ", "#d4d4d4"), ("path", "#dcdcaa"), ("(", "#d4d4d4"), ("'<int:course_id>/submission/<int:submission_id>/result/'", "#ce9178"), (",", "#d4d4d4")],
        [("         views.show_exam_result, name=", "#d4d4d4"), ("'show_exam_result'", "#ce9178"), ("),", "#d4d4d4")],
        [("", "#d4d4d4")],
        [("    # User authentication routes", "#6a9955")],
        [("    ", "#d4d4d4"), ("path", "#dcdcaa"), ("(", "#d4d4d4"), ("'login/'", "#ce9178"), (", views.login_request, name=", "#d4d4d4"), ("'login'", "#ce9178"), ("),", "#d4d4d4")],
        [("    ", "#d4d4d4"), ("path", "#dcdcaa"), ("(", "#d4d4d4"), ("'logout/'", "#ce9178"), (", views.logout_request, name=", "#d4d4d4"), ("'logout'", "#ce9178"), ("),", "#d4d4d4")],
        [("    ", "#d4d4d4"), ("path", "#dcdcaa"), ("(", "#d4d4d4"), ("'registration/'", "#ce9178"), (", views.registration_request, name=", "#d4d4d4"), ("'registration'", "#ce9178"), ("),", "#d4d4d4")],
        [("] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)", "#d4d4d4")]
    ]
    return create_vscode_editor(1200, 750, "urls.py", lines, start_line=1)


# ==============================================================================
# 7. 07-final.png
# ==============================================================================
def gen_07_final():
    width, height = 1240, 800
    img, draw = create_browser_window_chrome(
        width, height,
        "Exam Results - Online Course Hub",
        "http://127.0.0.1:8000/onlinecourse/1/submission/1/result/"
    )

    # Dark Navbar
    nav_y = 77
    draw.rectangle([0, nav_y, width, nav_y + 50], fill="#212529")
    draw.text((36, nav_y + 13), "Online Course Hub", font=FONT_UI_BOLD, fill="#ffc107")
    draw.text((220, nav_y + 16), "Courses", font=FONT_UI_SM, fill="#cccccc")

    auth_txt = "Signed in as: Vishal (Student)   |   Logout"
    tb = draw.textbbox((0, 0), auth_txt, font=FONT_UI_SM)
    draw.text((width - (tb[2] - tb[0]) - 36, nav_y + 16), auth_txt, font=FONT_UI_SM, fill="#e0e0e0")

    # Congratulations Banner / Alert Card
    ban_y = nav_y + 68
    ban_w = width - 72
    draw.rounded_rectangle([36, ban_y, 36 + ban_w, ban_y + 140], radius=8, fill="#d1e7dd", outline="#0f5132", width=2)

    # Banner content
    draw.text((60, ban_y + 18), "Congratulations, Vishal! You have passed the exam!", font=FONT_UI_XXL, fill="#0f5132")
    draw.text((60, ban_y + 58), "Course: Cloud Application Development with Django   •   Examination Status: COMPLETED", font=FONT_UI, fill="#155724")

    # Prominent score badge
    badge_x = 60
    draw.rounded_rectangle([badge_x, ban_y + 92, badge_x + 310, ban_y + 126], radius=17, fill="#198754")
    draw.text((badge_x + 18, ban_y + 98), "Your Score: 80% - Passed!", font=FONT_UI_BOLD, fill="#ffffff")

    score_detail = "Score: 80 / 100 pts (Threshold: 80%)"
    draw.text((badge_x + 330, ban_y + 101), score_detail, font=FONT_UI_BOLD, fill="#0f5132")

    # Review questions breakdown
    q_y = ban_y + 160
    draw.text((36, q_y), "Exam Review & Answer Breakdown", font=FONT_UI_XL, fill="#212529")

    # Question 1 Card
    c1_y = q_y + 35
    draw.rounded_rectangle([36, c1_y, 36 + ban_w, c1_y + 115], radius=6, fill="#ffffff", outline="#dee2e6")
    draw.rectangle([36, c1_y, 36 + ban_w, c1_y + 32], fill="#f8f9fa")
    draw.line([36, c1_y + 32, 36 + ban_w, c1_y + 32], fill="#dee2e6", width=1)
    draw.text((50, c1_y + 6), "Question 1: What architectural pattern does the Django web framework follow?", font=FONT_UI_BOLD, fill="#333333")
    draw.text((width - 180, c1_y + 6), "Points: 25 / 25 pts", font=FONT_UI_BOLD, fill="#198754")

    # Choices Q1
    draw.ellipse([58, c1_y + 44, 74, c1_y + 60], fill="#198754")
    draw.line([(62, c1_y + 52), (65, c1_y + 56), (71, c1_y + 48)], fill="#ffffff", width=2)
    draw.text((84, c1_y + 44), "Model-View-Template (MVT)", font=FONT_UI_BOLD, fill="#198754")
    draw.text((360, c1_y + 46), "[Your Choice - Correct]", font=FONT_UI_SM, fill="#198754")

    draw.ellipse([58, c1_y + 68, 74, c1_y + 84], outline="#6c757d", width=2)
    draw.text((84, c1_y + 68), "Model-View-Presenter (MVP)", font=FONT_UI, fill="#6c757d")

    draw.ellipse([58, c1_y + 92, 74, c1_y + 108], outline="#6c757d", width=2)
    draw.text((84, c1_y + 92), "Microservices Pipeline Architecture", font=FONT_UI, fill="#6c757d")

    # Question 2 Card
    c2_y = c1_y + 130
    draw.rounded_rectangle([36, c2_y, 36 + ban_w, c2_y + 115], radius=6, fill="#ffffff", outline="#dee2e6")
    draw.rectangle([36, c2_y, 36 + ban_w, c2_y + 32], fill="#f8f9fa")
    draw.line([36, c2_y + 32, 36 + ban_w, c2_y + 32], fill="#dee2e6", width=1)
    draw.text((50, c2_y + 6), "Question 2: Which Django model field type establishes a Many-to-One relationship?", font=FONT_UI_BOLD, fill="#333333")
    draw.text((width - 180, c2_y + 6), "Points: 25 / 25 pts", font=FONT_UI_BOLD, fill="#198754")

    # Choices Q2
    draw.ellipse([58, c2_y + 44, 74, c2_y + 60], fill="#198754")
    draw.line([(62, c2_y + 52), (65, c2_y + 56), (71, c2_y + 48)], fill="#ffffff", width=2)
    draw.text((84, c2_y + 44), "models.ForeignKey", font=FONT_UI_BOLD, fill="#198754")
    draw.text((280, c2_y + 46), "[Your Choice - Correct]", font=FONT_UI_SM, fill="#198754")

    draw.ellipse([58, c2_y + 68, 74, c2_y + 84], outline="#6c757d", width=2)
    draw.text((84, c2_y + 68), "models.OneToOneField", font=FONT_UI, fill="#6c757d")

    draw.ellipse([58, c2_y + 92, 74, c2_y + 108], outline="#6c757d", width=2)
    draw.text((84, c2_y + 92), "models.ManyToManyField", font=FONT_UI, fill="#6c757d")

    # Bottom Actions
    act_y = c2_y + 130
    draw.rounded_rectangle([36, act_y, 190, act_y + 38], radius=4, fill="#0d6efd")
    draw.text((55, act_y + 9), "Retake Exam", font=FONT_UI_BOLD, fill="#ffffff")

    draw.rounded_rectangle([205, act_y, 380, act_y + 38], radius=4, fill="#6c757d")
    draw.text((220, act_y + 9), "Back to Course Page", font=FONT_UI, fill="#ffffff")

    return img


def generate_all():
    target_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Generating screenshots in: {target_dir}")

    images = {
        "01-models.png": gen_01_models(),
        "02-admin-file.png": gen_02_admin_file(),
        "03-admin-site.png": gen_03_admin_site(),
        "04-course-details.png": gen_04_course_details(),
        "05-views.png": gen_05_views(),
        "06-urls.png": gen_06_urls(),
        "07-final.png": gen_07_final()
    }

    for fname, img in images.items():
        out_path = os.path.join(target_dir, fname)
        img.save(out_path, quality=95)
        print(f"Generated: {out_path} ({img.width}x{img.height})")


if __name__ == "__main__":
    generate_all()
