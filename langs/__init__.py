
import os
import importlib as imp


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
	text[lang][category][name] = text

def get_text(lang : str, category : str, name : str) -> str:
	if lang not in langs:
		return get_text(default_lang, category, name)
	if category not in texts[lang]:
		return ""
	if name not in texts[lang][category]:
		return ""
	return texts[lang][category][name]

module_names=os.listdir(os.path.dirname(os.path.abspath(__file__)))

for i in range(len(module_names)):
    if module_names[i] == "__init__.py":
        module_names.pop(i)
        break
for i in range(len(module_names)):
    if module_names[i].endswith(".py"):
        module_names[i] = module_names[i][: -3]

for i in module_names:
    imp.import_module(f".{i}", __package__)