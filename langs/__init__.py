
import os
import importlib as imp
import json


langs = [
	"en"
]

default_lang = langs[0]

texts : dict[str, dict[str, dict[str, str]]] = {i : {} for i in langs}

def register_lang(lang :str):
	if lang not in langs:
		langs.append(lang)
		texts[lang] = {}

def register_text(lang : str, category : str, name : str, text : str):
	if lang not in langs:
		register_lang(lang)
	if category not in texts[lang]:
		texts[lang][category] = {}
	texts[lang][category][name] = text

def get_text(lang : str, category : str, name : str) -> str:
	if lang not in langs:
		return get_text(default_lang, category, name)
	if category not in texts[lang]:
		return ""
	if name not in texts[lang][category]:
		return ""
	return texts[lang][category][name]


def register_builtin():
	fold = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	fold = os.path.join(fold, "assets", "lang")
	for lang in os.listdir(fold):
		register_lang(lang)
		lang_path = os.path.join(fold, lang)
		for category in os.listdir(os.path.join(lang_path)):
			category_path = os.path.join(lang_path, category)
			for file in os.listdir(category_path):
				with open(os.path.join(category_path, file), encoding='utf-8') as f:
					d = json.load(f)
					for i in d.keys():
						register_text(lang, category, i, d[i])

register_builtin()
print(texts)