from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SearchForm(FlaskForm):
    job_fields = StringField('job search fields',
                            validators=[DataRequired()])
    #location = StringField('Location (OPTIONAL)')

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ResumeForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone_number = StringField('Phone', validators=[DataRequired(), Length(10)])
    #education section with major and gpa 
    education = StringField('Education/School', validators=[DataRequired(), Length(min=2, max=20)])
    major = StringField('Major(s)')
    gpa = StringField('GPA')
    skill_title1 = StringField('Skill1', validators=[DataRequired()])
    skill_description1 = StringField('SkillDescription1', validators=[DataRequired()])
    skill_title2 = StringField('Skill2')
    skill_description2 = StringField('SkillDescription2')
    skill_title3 = StringField('Skill1')
    skill_description3 = StringField('SkillDescription3')
    #relevant skills
    relevant_skill1 =  StringField('RelevantSkill1', validators=[DataRequired()])
    relevant_skill2 =  StringField('RelevantSkill2', validators=[DataRequired()])
    relevant_skill3 =  StringField('RelevantSkill3', validators=[DataRequired()])
    relevant_skill4 =  StringField('RelevantSkill4')
    relevant_skill5 =  StringField('RelevantSkill5')
    relevant_skill6 =  StringField('RelevantSkill6')
    relevant_skill7 =  StringField('RelevantSkill7')
    relevant_skill8 =  StringField('RelevantSkill8')
    relevant_skill9 =  StringField('RelevantSkill9')
    relevant_skill10 =  StringField('RelevantSkill10')
    #professional exeperince section
    company1 = StringField('Company1')
    position1 = StringField('Position1')
    position_description1 = StringField('Description1')
    start_date1 = StringField('StartDate1')
    end_date1 = StringField('EndDate1')

    company2 = StringField('Company2')
    position2 = StringField('Position2')
    position_description2 = StringField('Description2')
    start_date2 = StringField('StartDate2')
    end_date2 = StringField('EndDate2')

    company3 = StringField('Company3')
    position3 = StringField('Position3')
    position_description3 = StringField('Description3')
    start_date3 = StringField('StartDate3')
    end_date3 = StringField('EndDate3')

    company4 = StringField('Company4')
    position4 = StringField('Position4')
    position_description4 = StringField('Description4')
    start_date4 = StringField('StartDate4')
    end_date4 = StringField('EndDate4')

    company5 = StringField('Company5')
    position5 = StringField('Position5')
    position_description5 = StringField('Description5')
    start_date5 = StringField('StartDate5')
    end_date5 = StringField('EndDate5')

    #Affiliations/Interests Tab
    affiliations = StringField('Affiliations')
    certifications = StringField('Certifications')
    awards = StringField('Awards')
    interests = StringField('Interests')
    publications = StringField('Publications')
    volunteer = StringField('Volunteer')








    


