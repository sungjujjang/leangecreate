from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash, send_file
import datetime

app = Flask(__name__)

@app.route('/')
def make():
    return render_template('make.html')

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

@app.route('/download', methods=['POST'])
def dwn():
    result = None
    request_ip = request.remote_addr
    if request.method == 'POST':
        print_func = request.form.get('print-func')
        var_create_func = request.form.get('var-create-func')
        var_get_func = request.form.get('var-get-func')
        extension = request.form.get('extension')
        print(f"print_func: {print_func}, var_create_func: {var_create_func}, var_get_func: {var_get_func}, extension: {extension}")
        if extension.startswith('.'):
            pass
        else:
            extension = '.' + extension
        with open('interpreter.py', 'r', encoding='utf-8') as f:
            original_code = f.read()

        new_code = update_interpreter_code(
            original_code,
            valuecreate=var_create_func,
            printtext=print_func,
            getvalue=var_get_func,
            extension=extension
        )
        
        nowtimetext = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"interpreter-{request_ip}-{nowtimetext}.py"
        
        with open(f'./static/{filename}.py', 'w', encoding='utf-8') as f:
            f.write(new_code)
            f.close()
        
        return send_file(f'./static/{filename}.py', as_attachment=True, download_name='interpreter.py')
    else:
        return jsonify({'error': 'Invalid request method'}), 400

if __name__ == '__main__':
    app.run(debug=True)