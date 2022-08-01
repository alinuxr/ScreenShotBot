'''
For data translation make a dict

Files for translator:
work dir ./languages
files languages:
- eng.py
- rus.py

possible to easy add new language

'''
from types import SimpleNamespace
import sys
sys.path.insert(1, r'./languages')
from rus import rus
from eng import eng

class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)
class Translate():
    def __init__(self, lang):
        self.text = {}
        self.text.update({"rus": NestedNamespace(rus)})
        self.text.update({"eng": NestedNamespace(eng)})
        self.data = lang
    def message_answer(self, message: str):
        return getattr(self.text[self.data], message)
