# -*- coding: utf-8 -*-
from django import template
import re
import pygments
from pygments.lexers import LEXERS, guess_lexer, get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.special import TextLexer
from pygments.lexers.c_cpp import CppLexer

register = template.Library()
regex = re.compile(r'<code>(.*?)</code>', re.DOTALL)

# http://www.blacksailor.com/en/blog/code-highlighting-in-django-templates-using-pygments-2/
#  {% load highlighting %}
# {{ code|highlight|safe }}
# <code>{code1}</code>  <code>{code2}</code> can be highlighted


@register.filter(name='highlight')
def highlight(value, single=''):
    if single == 'tag':
        try:
            last_end = 0
            to_return = ''
            found = 0
            for match_obj in regex.finditer(value):
                code_string = match_obj.group(1)
                try:
                    lexer = guess_lexer(code_string)
                except ValueError:
                    lexer = TextLexer
                py_string = pygments.highlight(code_string, lexer, HtmlFormatter())
                to_return = to_return + value[last_end:match_obj.start(1)] + py_string
                last_end = match_obj.end(1)
                found += 1
            to_return = to_return + value[last_end:]
            return to_return
        except:
            return value
    else:
        try:
            try:
                lexer = guess_lexer(value)
            except ValueError:
                lexer = TextLexer
            py_string = pygments.highlight(value, lexer, HtmlFormatter())
            return py_string
        except Exception as e:
            return value


# c++ c python python3 java
@register.filter(name='code')
def code(value, lang_name):
    try:
        try:
            lexer = get_lexer_by_name(lang_name)
        except (ValueError, pygments.util.ClassNotFound):
            lexer = TextLexer
        py_string = pygments.highlight(value, lexer, HtmlFormatter())
        return py_string
    except:
        return value
