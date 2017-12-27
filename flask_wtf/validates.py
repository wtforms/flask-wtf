from functools import wraps

from flask import _app_ctx_stack as stack
from werkzeug.local import LocalProxy

from .form import FlaskForm


def validates(form_cls=None, **fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ctx = stack.top
            if ctx is not None:
                ctx.current_form = _make_form(form_cls, **fields)
                ctx.current_form.validate_on_submit()
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def _make_form(form_cls, **fields):
    if form_cls is not None:
        cls = type("_DynamicForm_%s" % form_cls.__name__, (form_cls,), fields)
    else:
        cls = type("_DynamicForm", (FlaskForm,), fields)
    return cls()


def _current_form():
    ctx = stack.top
    if not hasattr(ctx, "current_form"):
        return None
    else:
        return ctx.current_form


current_form = LocalProxy(_current_form)
