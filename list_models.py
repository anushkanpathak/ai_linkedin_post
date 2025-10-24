import google.generativeai as genai


GOOGLE_API_KEY = "AIzaSyDUKlh_-UD0zoGFiiXGpPnNomlqd9ZYKI4"
genai.configure(api_key=GOOGLE_API_KEY)


models = genai.list_models()
print("Available Models:")
for m in models:
    print(f"- {m.name}")
