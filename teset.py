def update_interpreter_code(original_code, valuecreate, printtext, getvalue, extension):
    replacements = {
        'valuecreate = "변생"': f'valuecreate = "{valuecreate}"',
        'printtext = "출력"': f'printtext = "{printtext}"',
        'getvalue = "변가"': f'getvalue = "{getvalue}"',
        'extension = ".nomu"': f'extension = "{extension}"',
    }
    
    new_code = original_code
    for old, new in replacements.items():
        new_code = new_code.replace(old, new)
    
    return new_code

with open('testint.py', 'r', encoding='utf-8') as f:
    original_code = f.read()

new_code = update_interpreter_code(
    original_code,
    valuecreate="변수생성",
    printtext="출력하기",
    getvalue="값가져오기",
    extension=".newlang"
)

print(new_code)

with open('testint.py', 'w', encoding='utf-8') as f:
    f.write(new_code)
