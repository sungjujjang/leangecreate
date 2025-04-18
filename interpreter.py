import sys

valuecreate = "변생"
printtext = "출력"
getvalue = "변가"
extension = ".nomu"

class Interpreter:
    def __init__(self):
        self.values = {}
        
    def createvalue(self, name, value):
        self.values[name] = value
    
    def checkgetvalue(self, commands):
        for i, command in enumerate(commands):
            if command.startswith(getvalue):
                valuename = commands[i+1]
                return valuename
        return None
    
    def getvalue(self, name):
        if name in self.values:
            return self.values[name]
        else:
            return None
    
    def process_line(self, line):
        try:
            if line.startswith(valuecreate):
                valuename = self.checkgetvalue(line.split())
                if valuename:
                    texts = ' '.join(line.split()[1:]).replace(f"{getvalue} {valuename}", f"{str(self.getvalue(valuename))}") # 우흥 변수이름 값
                    while True:
                        valuename = self.checkgetvalue(texts.split())
                        if valuename:
                            texts = ' '.join(texts.split()).replace(f"{getvalue} {valuename}", f"{str(self.getvalue(valuename))}")
                        else:
                            break
                    self.createvalue(line.split()[1], eval(f"'{texts}'"))
                else:
                    texts = ' '.join(line.split()[2:])
                    self.createvalue(line.split()[1], eval(texts))
            elif line.startswith(printtext):
                valuename = self.checkgetvalue(line.split())
                if valuename:
                    if type(self.getvalue(valuename)) == str:
                        texts = ' '.join(line.split()[1:]).replace(f"{getvalue} {valuename}", f"\"{str(self.getvalue(valuename))}\"")
                        while True:
                            valuename = self.checkgetvalue(texts.split())
                            if valuename:
                                texts = ' '.join(texts.split()).replace(f"{getvalue} {valuename}", f"\"{str(self.getvalue(valuename))}\"")
                                texts = texts.replace("'", "\"")
                            else:
                                break
                    else:
                        texts = ' '.join(line.split()[1:]).replace(f"{getvalue} {valuename}", f"{str(self.getvalue(valuename))}") # 우흥 변수이름 값
                    print(eval(f"{texts}"))
                else:
                    texts = ' '.join(line.split()[1:])
                    texts = texts.replace("'", "\"")
                    print(eval(f"'{texts}'"))
            else:
                raise ValueError("Unknown command")
        except Exception as e:
            raise ValueError(f"Error processing {line} : {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith(extension):
        print(f"Error: File must have the '{extension}' extension.")
        sys.exit(1)

    interpreter = Interpreter()

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    interpreter.process_line(line)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error: {e}")