# Emitter object keeps track of the generated code and outputs it.
class Emitter:
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.header = ""
        self.code = ""
        self.codeEnd = ""

    def emit(self, code):
        self.code += code

    def emitLine(self, code):
        self.code += code + '\n'

    def emitLineEnd(self, code):
        self.codeEnd += code + '\n'

    def headerLine(self, code):
        self.header += code + '\n'

    def writeFile(self):
        #with open(self.fullPath, 'w') as outputFile:
        #    outputFile.write(self.header + self.code)
        print(self.header + self.code + self.codeEnd)
