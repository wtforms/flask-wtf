from flask import Flask, render_template, request
from flask.ext.wtf import Form
from flask.ext.wtf.yandex_captcha import YandexCaptchaField


YANDEX_CLEANWEB_API_PUBLIC_KEY = 'cw.1.1.20110707T172051Z.faf547ce44f3d10b.d7e3028845ea04f56c38f7eef90999f765dd0d1f'
YANDEX_CLEANWEB_API_KEY = YANDEX_CLEANWEB_API_PUBLIC_KEY
SECRET_KEY = 'SECRET KEY'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


class YandexCaptchaForm(Form):
    yandex_captcha = YandexCaptchaField()


@app.route("/", methods=("GET", "POST"))
def index():
    form = YandexCaptchaForm()
    if request.method == 'GET':
        form = YandexCaptchaForm()
    elif request.method == 'POST':
        form = YandexCaptchaForm(request.form)
        if form.validate():
            return 'Ok'
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()
