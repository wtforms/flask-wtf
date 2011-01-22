from wtforms import TextField, IntegerField
from wtforms import DateField as _DateField
from wtforms.widgets import Input

class DateInput(Input):
    input_type = "date"


class TimeInput(Input):
    input_type = "time"


class URLInput(Input):
    input_type = "url"


class EmailInput(Input):
    input_type = "email"


class SearchInput(Input):
    input_type = "search"


class SearchField(TextField):
    widget = SearchInput()


class DateField(_DateField):
    widget = DateInput()


class URLField(TextField):
    widget = URLInput()
    

class EmailField(TextField):
    widget = EmailInput()
