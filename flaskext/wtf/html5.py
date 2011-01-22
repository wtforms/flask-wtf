from wtforms import TextField, IntegerField
from wtforms import DateField as _DateField
from wtforms.widgets import Input

class DateInput(Input):
    """
    Creates <input type=date> widget
    """
    input_type = "date"


class URLInput(Input):
    """
    Creates <input type=url> widget
    """
    input_type = "url"


class EmailInput(Input):
    """
    Creates <input type=email> widget
    """

    input_type = "email"


class SearchInput(Input):
    """
    Creates <input type=search> widget
    """

    input_type = "search"


class SearchField(TextField):
    """
    TextField using SearchInput by default
    """
    widget = SearchInput()


class DateField(_DateField):
    """
    DateField using DateInput by default
    """
 
    widget = DateInput()


class URLField(TextField):
    """
    TextField using URLInput by default
    """
 
    widget = URLInput()
    

class EmailField(TextField):
    """
    TextField using EmailInput by default
    """
 
    widget = EmailInput()

