from pathlib import Path
import ast
import re
from typing import Dict, List, Mapping, Optional
from kube_hound.analysis import AnalysisResult, StaticAnalysis
from loguru import logger
import esprima
import javalang

from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell



class SuspiciousCryptographicNames(StaticAnalysis):
    analysis_id = 'sourcecode_scn'
    analysis_name = 'Suspicious Cryptographic Names'
    analysis_description = 'detect instances of suspicious cryptographic names inside the microservices sourcecode'
    input_types = ['sourcecode']

    AES = "aes"
    IV = "iv"
    RSA = "rsa"

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        AES = "aes"
        IV = "iv"
        RSA = "rsa"


        # Non suspicious names [user could add words in future]
        not_suspicious = ["private", "positive", "negative"]

        # User could specify what types of files to analyze/not analyze in future
        skip_file = [".md", ".txt", ".ini", ".conf", ".cfg", ".json", ".html", ".xml", ".pdf", ".log", ".csv", ".sh", ".bat", ".css", ".svg", ".dat", ".msg", ".sql", ".po", ".pot", ".proto", ".in", ".sum"]
        #no_skip_file = [".py", ".java", ".go", ".js", ".cs"]
        output_results = []
        analyzed_files = []

        assert 'sourcecode' in input_objects
        sourcecode_objects = input_objects['sourcecode']



        # Array containing the directories to be analyzed
        directories = [str(sourcecode.path) for sourcecode in sourcecode_objects]
        for directory in directories:
            for type_file in Path(directory).rglob('*'):
                if type_file not in analyzed_files:
                    analyzed_files.append(type_file)
                    if type_file.is_file() and type_file.suffix not in skip_file:
                        if type_file.is_file() and type_file.suffix==".py":
                            # for python files analysis is working well
                            self.python_analysis(type_file, AES, IV, RSA, not_suspicious, output_results)
                        if type_file.is_file() and type_file.suffix==".java":
                            # for python files analysis is working well
                            self.java_analysis(type_file, AES, IV, RSA, not_suspicious, output_results)
                        if type_file.is_file() and type_file.suffix==".js":
                            # for python files analysis is working well
                            self.js_analysis(type_file, AES, IV, RSA, not_suspicious, output_results)
                        else:
                            try:
                                if type_file.is_file():
                                    self.base_analysis(type_file, AES, IV, RSA, not_suspicious, output_results)
                            except Exception as e:
                                print(f"Error parsing {type_file}: {e}")
        logger.debug(directories)

        return output_results

    def base_analysis(self, type_file, AES, IV, RSA, not_suspicious, output_results):
        #split file in words
        with open(type_file, 'r') as file:
            file_content = file.read()
            suspicious_names = []
            warning_lines = {}
            tokens = re.findall(r'\w+|[\w_]+', file_content)
            tokens = [token.strip() for token in tokens if token.strip()]

            # check if tokens contains any suspicious keywords
            for word in tokens:
                if AES in word.lower():
                    if word not in suspicious_names:
                        suspicious_names.append(word)
                if IV in word.lower():
                    if word not in suspicious_names:
                        suspicious_names.append(word)
                if RSA in word.lower():
                    if word not in suspicious_names:
                        suspicious_names.append(word)

        self.find_issue(type_file, suspicious_names, not_suspicious, warning_lines, output_results)

    def python_analysis(self, type_file, AES, IV, RSA, not_suspicious, output_results):
        # ANALYSIS BASED ON ABSTRACT TREE CREATION OF THE PYTHON FILE
        with open(type_file, 'r') as file:
            # Read the content of the file
            file_content = file.read()
            fun_var_names = []
            warning_lines = {}
            tree = ast.parse(file_content)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef) or isinstance(node, ast.ClassDef):
                    fun_var_names.append(node.name)
                    if warning_lines.get(node.name) is not None:
                        warning_lines[node.name].append(node.lineno)
                    else:
                        warning_lines[node.name] = [node.lineno]
                elif isinstance(node, ast.Name):
                    fun_var_names.append(node.id)
                    if warning_lines.get(node.id) is not None:
                        warning_lines[node.id].append(node.lineno)
                    else:
                        warning_lines[node.id] = [node.lineno]

            # find suspicious names
            for name in fun_var_names:
                if ((AES not in name.lower() and IV not in name.lower() and RSA not in name.lower()) or (name.lower() in not_suspicious)) and (name in warning_lines):
                    warning_lines.pop(name)
            body = ""
            if warning_lines:
                description = f"Potential usage of custom crypto code in {type_file.name}"
                for key in warning_lines:
                    line_numbers = self.array_to_string(warning_lines[key])
                    body =  body + f"-   \"{key}\" at lines: {line_numbers}.\n"
                message = f"{description}\n" + \
                          f"{body}" +\
                          f"reason: Suspicious name found in the file, may indicate implementation of custom crypto code.\n" + \
                        "Check for custom code implementation."
                output_results.append(AnalysisResult(message, {Smell.OCC}))

    def java_analysis(self, type_file, AES, IV, RSA, not_suspicious, output_results):
        # ANALYSIS BASED ON ABSTRACT TREE CREATION OF THE JAVA FILE
        with open(type_file, 'r') as file:

            # Read the content of the file
            file_content = file.read()
            tokens = []
            suspicious_names = []
            warning_lines = {}
            # Create java ast tree and filter save node names only for function declarations and varaiable decations
            tree = javalang.parse.parse(file_content)
            for path, node in tree.filter(javalang.tree.MethodDeclaration):
                if node.name not in tokens :
                    tokens.append(node.name)

            for path, node in tree.filter(javalang.tree.VariableDeclarator):
                if node.name not in tokens:
                    tokens.append(node.name)

            # check if tokens contains any suspicious keywords
            for word in tokens:
                if AES in word.lower():
                    if word not in suspicious_names:
                        suspicious_names.append(word)
                if IV in word.lower():
                    if word not in suspicious_names:
                        suspicious_names.append(word)
                if RSA in word.lower():
                    if word not in suspicious_names:
                        suspicious_names.append(word)

        self.find_issue(type_file, suspicious_names, not_suspicious, warning_lines, output_results)

    def js_analysis(self, type_file, AES, IV, RSA, not_suspicious, output_results):
        # ANALYSIS BASED ON ABSTRACT TREE CREATION OF JAVASCRIPT FILE
        with (open(type_file, 'r') as file):
            # Read the content of the file
            fun_var_names = []
            warning_lines = {}
            file_content = file.read()

            try:
                parsed_code = esprima.parseScript(file_content, loc=True)
            except Exception as e:
                print(f"Error parsing JavaScript: {e}")
                parsed_code = None

            # Traverse the syntax tree to extract function names and variable names
            if parsed_code is not None:
                for node in parsed_code.body:
                    if node.type in ('FunctionDeclaration'):
                        # Extract function names from FunctionDeclaration nodes
                        fun_var_names.append(node.id.name)
                        if warning_lines.get(node.id.name) is not None:
                            warning_lines[node.id.name].append(node.id.loc.start.line)
                        else:
                            warning_lines[node.id.name] = [node.id.loc.start.line]

                    elif node.type in ('VariableDeclaration', 'VariableDeclarationStatement'):
                        # Extract variable names from VariableDeclaration nodes
                        for declaration in node.declarations:
                            if declaration.id.type == 'Identifier':
                                fun_var_names.append(declaration.id.name)

                                if warning_lines.get(declaration.id.name) is not None:
                                    warning_lines[declaration.id.name].append(declaration.id.loc.start.line)
                                else:
                                    warning_lines[declaration.id.name] = [declaration.id.loc.start.line]

            # find suspicious names
            for name in fun_var_names:
                if ((AES not in name.lower() and IV not in name.lower() and RSA not in name.lower()) or (name.lower() in not_suspicious)) and (name in warning_lines):
                    warning_lines.pop(name)

            body = ""
            if warning_lines:
                description = f"Potential usage of custom crypto code in {type_file.name}"
                for key in warning_lines:
                    line_numbers = self.array_to_string(warning_lines[key])
                    body = body + f"-   \"{key}\" at lines: {line_numbers}.\n"
                message = f"{description}\n" + \
                          f"{body}" + \
                          f"reason: Suspicious name found in the file, may indicate implementation of custom crypto code.\n" + \
                          "Check for custom code implementation."
                output_results.append(AnalysisResult(message, {Smell.OCC}))

    def find_issue(self, type_file, suspicious_names, not_suspicious, warning_lines, output_results):
        # find line and build warning_lines dict
        with open(type_file, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                for name in suspicious_names:
                    if name in line and name.lower() not in not_suspicious:
                        if warning_lines.get(name) is not None:
                            warning_lines[name].append(line_number)
                        else:
                            warning_lines[name] = [line_number]

        body = ""
        if warning_lines:
            description = f"Potential usage of custom crypto code in {type_file.name}"
            for key in warning_lines:
                line_numbers = self.array_to_string(warning_lines[key])
                body = body + f"-   \"{key}\" at lines: {line_numbers}.\n"
            message = f"{description}\n" + \
                      f"{body}" + \
                      f"reason: Suspicious name found in the file, may indicate implementation of custom crypto code.\n" + \
                      "Check for custom code implementation."
            output_results.append(AnalysisResult(message, {Smell.OCC}))

    def array_to_string(self, words):
        string = ', '.join(map(str, words))
        return string
