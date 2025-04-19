from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash, send_file
import datetime

class Interpreter:
    def __init__(self, valuecreate, printtext, getvalues, extension):
        self.values = {}
        self.valuecreate = valuecreate
        self.printtext = printtext
        self.getvalues = getvalues
        self.extension = extension
        
        self.results = []
        
    def createvalue(self, name, value):
        self.values[name] = value
    
    def checkgetvalue(self, commands):
        for i, command in enumerate(commands):
            if command.startswith(self.getvalues):
                valuename = commands[i+1]
                return valuename
        return None
    
    def getvalue(self, name):
        if name in self.values:
            return self.values[name]
        else:
            return None
    
    def getresults(self):
        return "\n".join([str(result) for result in self.results])

    def process_line(self, line):
        try:
            if line.startswith(self.valuecreate):
                valuename = self.checkgetvalue(line.split())
                if valuename:
                    texts = ' '.join(line.split()[1:]).replace(f"{self.getvalues} {valuename}", f"{str(self.getvalue(valuename))}") # 우흥 변수이름 값
                    while True:
                        valuename = self.checkgetvalue(texts.split())
                        if valuename:
                            texts = ' '.join(texts.split()).replace(f"{self.getvalues} {valuename}", f"{str(self.getvalue(valuename))}")
                        else:
                            break
                    self.createvalue(line.split()[1], eval(f"'{texts}'"))
                else:
                    texts = ' '.join(line.split()[2:])
                    self.createvalue(line.split()[1], eval(texts))
            elif line.startswith(self.printtext):
                valuename = self.checkgetvalue(line.split())
                if valuename:
                    if type(self.getvalue(valuename)) == str:
                        texts = ' '.join(line.split()[1:]).replace(f"{self.getvalues} {valuename}", f"\"{str(self.getvalue(valuename))}\"")
                        while True:
                            valuename = self.checkgetvalue(texts.split())
                            if valuename:
                                texts = ' '.join(texts.split()).replace(f"{self.getvalues} {valuename}", f"\"{str(self.getvalue(valuename))}\"")
                                texts = texts.replace("'", "\"")
                            else:
                                break
                    else:
                        texts = ' '.join(line.split()[1:]).replace(f"{self.getvalues} {valuename}", f"{str(self.getvalue(valuename))}") # 우흥 변수이름 값
                    self.results.append(eval(f"{texts}"))
                else:
                    texts = ' '.join(line.split()[1:])
                    texts = texts.replace("'", "\"")
                    self.results.append(eval(f"{texts}"))
            else:
                raise ValueError("Unknown command")
        except Exception as e:
            raise ValueError(f"Error processing {line} : {e}")

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

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        json_data = request.get_json()
        print(json_data)
        code = json_data.get('code', '')
        valuecreate = json_data.get('var_create_func', '변생')
        printtext = json_data.get('print_func', '출력')
        getvalue = json_data.get('var_get_func', '변가')
        extension = json_data.get('extension', '.asdf')
                
        interpreter = Interpreter(valuecreate, printtext, getvalue, extension)
        
        try:
            for line in code.split('\n'):
                interpreter.process_line(line.strip())
            result = interpreter.getresults()
            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'result': str(e)})
    else:
        # get url query string
        valuecreate = request.args.get('var-create-func', '변생')
        printtext = request.args.get('print-func', '출력')
        getvalue = request.args.get('var-get-func', '변가')
        extension = request.args.get('extension', '.asdf')
        
        return render_template('test.html', valuecreate=valuecreate, printtext=printtext, getvalue=getvalue, extension=extension)

if __name__ == '__main__':
    app.run(port=9876 ,debug=True)