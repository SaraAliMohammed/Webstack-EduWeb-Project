"""
Forms
"""
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from eduWeb.models import User, Course
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_ckeditor import CKEditorField


class RegistrationForm(FlaskForm):
    '''Implementation for the RegistrationForm class'''
    fname = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=25)]
    )
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$"
            ),
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        ''' Validates unique username'''
        user = User.query.filter_by(username=username.data)
        if user:
            raise ValidationError('username already exists! please choose a different one')

    def validate_email(self, email):
        ''' Validates unique email'''
        user = User.query.filter_by(email=email.data)
        if user:
            raise ValidationError('email already exists! please choose a different one')


class LoginForm(FlaskForm):
    '''Implementation for the LoginForm class'''
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class UpdateProfileForm(FlaskForm):
    '''Implementation for the UpdateProfileForm class'''
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    bio = TextAreaField("Bio")
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        ''' Validates unique username'''
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Username already exists! Please chosse a different one"
                )

    def validate_email(self, email):
        ''' Validates unique email'''
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "Email already exists! Please chosse a different one"
                )


def choice_query():
    '''Get courses choices from db'''
    return Course.query


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


class NewCourseForm(FlaskForm):
    title = StringField("Course Name", validators=[DataRequired(), Length(max=50)])
    description = TextAreaField(
        "Course Description", validators=[DataRequired(), Length(max=150)]
    )
    icon = FileField("Icon", validators=[DataRequired(), FileAllowed(["jpg", "png"])])
    submit = SubmitField("Create")

    def validate_title(self, title):
        course = Course.query.filter_by(title=title.data).first()
        if course:
            raise ValidationError(
                "Course name already exists! Please choose a different one"
            )


class LessonUpdateForm(NewLessonForm):
    thumbnail = FileField("Thumbnail", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")