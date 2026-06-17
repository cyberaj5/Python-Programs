from googletrans import Translator
translator = Translator()
result = translator.translate("Bonjour", src="fr", dest="en")
print(result.text)
