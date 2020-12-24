from flask import Flask, request, redirect, flash, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import Email, Length, InputRequired
from flask_wtf.csrf import CSRFProtect
from scaleoapi import API
from loguru import logger
import os


SECRET = os.getenv('SECRET')


logger.add('app.log', format='{time} {level} {message}', level='DEBUG', rotation='1 week', compression='zip')
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET
csrf = CSRFProtect(app)


class LoginForm(FlaskForm):
    email = StringField(
        'email', validators=[
            InputRequired(message="Обязательное поле для заполнения"),
            Email(message='E-mail введен неверно.'),
            Length(max=50, message="Поле E-mail может содержать не более 50 символов.")
        ])
    password = PasswordField(
        'password', validators=[
            InputRequired('Это поле обязательно для заполнения'),
            Length(min=8, max=20, message="Пароль должен содержать от 8 до 20 символов"),
        ])
    telegram = StringField(
        'telegram', validators=[
            Length(max=35, message="Поле telegram может содержать не более 35 символов."),
        ])


@logger.catch
def find_kirillic(string: str) -> bool:
    kirill = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    r = [x for x in kirill if x in string.lower()]
    if len(r) >= 1:
        return True
    else:
        return False


@logger.catch
@app.route('/', methods=['GET', 'POST'])
def main():
    form = LoginForm()
    errors = None
    msg = None

    if request.method == 'POST':
        print()
        if 'recover-mail' in request.values:
            api = API(email=request.values['recover-mail'])
            api.send_data()
            if api.status_code == 200:
                msg = "Проверьте свою электронную почту для получения дальнейших инструкций."
            else:
                errors = ["Пользователь не найден"]
            logger.debug(api.content)
            return render_template(
                'index.html',
                form=form,
                errors=errors,
                msg=msg
            )
        if form.validate_on_submit():
            txt_err = []
            check_email = find_kirillic(request.form['email'])
            check_pass = find_kirillic(request.form['password'])
            if check_email or check_pass:
                if check_email:
                    txt_err.append('E-mail введен неверно.')
                if check_pass:
                    txt_err.append('В пароле допустимы только символы латиницы.')
                errors=txt_err
                logger.debug(errors)
                return render_template(
                    'index.html',
                    form=form,
                    errors=errors,
                    msg=msg
                )
            if 'repassword' in request.form:
                """register"""

                if not request.form['telegram']:
                    errors = ['Заполните поле Телеграм/Skype.']
                    logger.debug(errors)
                    return render_template(
                        'index.html',
                        form=form,
                        errors=errors,
                        msg=msg
                    )

                api = API(
                    email=request.form['email'],
                    password=request.form['password'],
                    repassword=request.form['repassword'],
                    telegram=request.form['telegram'],
                )
                api.send_data()
                if api.status_code == 201:
                    return redirect(api.content['info']['one_time_login_link'])
                elif api.status_code == 422:
                    errs = api.content['info']['errors']
                    logger.debug(api.content)
                    if errs:
                        for error in errs:
                            if error == 'password_hash':
                                pass
                            elif error == 'password_repeat':
                                txt_err.append("Пароли не совпадают")
                            elif error == 'password':
                                txt_err.append('Пароль должен содержать не менее 8 символов')
                            elif error == 'email':
                                txt_err.append("Партнёр уже зарегистрирован")
                            else:
                                txt_err.append(errors[error][0])
                        logger.debug(errors)
                    else:
                        txt_err.append("что-то пошло не так.\n администрация уже решает проблему")
                        logger.error(api.content)
                    errors = txt_err
                else:
                    errors = ['Неизвестная ошибка.\n Администрация уже разбирается']
                    logger.error(api.content)

                return render_template(
                    'index.html',
                    form=form,
                    errors=errors,
                    msg=msg
                )
            else:
                """login"""
                api = API(
                    email=request.form['email'],
                    password=request.form['password']
                )
                api.send_data()
                if api.status_code == 200:
                    return redirect(api.content['info']['one_time_login_link'])
                elif api.status_code == 422:
                    errors = ["Не верный email или пароль"]
                else:
                    txt_err.append("что-то пошло не так.\n администрация уже решает проблему")
                    errors = txt_err
                logger.debug(errors)
                return render_template(
                    'index.html',
                    form=form,
                    errors=errors,
                    msg=msg
                )

    return render_template(
        'index.html',
        form=form,
        errors=errors,
        msg=msg
    )


if __name__ == '__main__':
    app.run()
