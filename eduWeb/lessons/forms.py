from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from eduWeb.models import Course, Lesson
from wtforms import StringField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length
from flask_login import current_user


def choice_query():
    '''Get courses choices from db'''
    return Course.query


def get_user_courses():
    ''' Check if the user is logged in'''
    if current_user.is_authenticated:
        # Retrieve the courses associated with the logged-in user
        user_courses = Course.query.join(Lesson).filter_by(user_id=current_user.id).all()
        return user_courses
    else:
        # User is not logged in
        return None


class NewLessonForm(FlaskForm):
    '''Implementation for the NewLessonForm class'''
    course = QuerySelectField('Course', query_factory=choice_query, get_label="title")
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    slug = StringField(
        "Slug",
        validators=[DataRequired(), Length(max=32)],
        render_kw={
            "placeholder": "Descriptive short version of your title. SEO friendly"
        },
    )
    content = CKEditorField(
        "Lesson Content", validators=[DataRequired()], render_kw={"rows": "20"}
    )
    thumbnail = FileField('Thumbnail', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Post")


class LessonUpdateForm(NewLessonForm):
    '''Form for the update lesson'''
    thumbnail = FileField("Thumbnail", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")