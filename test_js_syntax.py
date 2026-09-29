import pyjsparser

with open('static_script.js', 'r', encoding='utf-8') as f:
    js = f.read()

parser = pyjsparser.PyJsParser()
try:
    tree = parser.parse(js)
    print("JS syntax is 100% VALID according to pyjsparser!")
except Exception as e:
    print("PYJSPARSER SYNTAX ERROR:")
    print(e)
