from pathlib import Path
import ast
import re
from typing import Dict, List, Mapping, Optional
from time import sleep
from kube_hound.analysis import AnalysisResult, StaticAnalysis
from loguru import logger
import docker
import os
import requests
import esprima
import javalang

from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell


class SuspiciousCryptographicNames(StaticAnalysis):
    analysis_id = 'sourcecode_scn'
    analysis_name = 'Suspicious Cryptographic Names'
    analysis_description = 'detect instances of suspicious cryptographic names inside the microservices sourcecode'
    input_types = ['sourcecode']


    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:

        AES = "AES"
        IV = "IV"
        RSA = "RSA"
        #skip_file = [".md", ".txt", ".ini", ".conf", ".cfg", ".json", ".html", ".xml", ".pdf", ".log", ".csv", ".sh", ".bat", ".css", ".svg", ".dat", ".msg", ".sql", ".po", ".pot", ".proto", ".in"]
        no_skip_file = [".py", ".java", ".go", ".javascript", ".go", ".cs"]
        output_results = []

        assert 'sourcecode' in input_objects
        sourcecode_objects = input_objects['sourcecode']



        # Array containing the directories to be analyzed
        directories = [str(sourcecode.path) for sourcecode in sourcecode_objects]
        for directory in directories:
            for type_file in Path(directory).rglob('*'):
                if type_file.is_file() and type_file.suffix in no_skip_file:
                    if type_file.is_file() and type_file.suffix==".py":
                        # for python files analysis is working well
                        self.python_analysis(type_file, AES, IV, RSA, output_results)
                    elif type_file.is_file():
                        self.base_analysis(type_file, AES, IV, RSA, output_results)
                    else:
                        try:
                            if type_file.is_file():
                                self.remaining_types_analysis(type_file, AES, IV, RSA, output_results)
                        except Exception as e:
                            print(f"Error parsing {type_file}: {e}")
        logger.debug(directories)

        return output_results

    def base_analysis(self, type_file, AES, IV, RSA, output_results):
        #split file in words
        with open(type_file, 'r') as file:
            file_content = file.read()
            suspicious_names = []
            warning_lines = {}
            tokens = re.findall(r'\w+|[\w_]+', file_content)
            tokens = [token.strip() for token in tokens if token.strip()]

            #check if words have suspicious keywords
            for word in tokens:
                if AES.lower() in word.lower():
                    if word not in suspicious_names:
                        suspicious_names.append(word)
                if IV.lower() in word.lower():
                    if word not in suspicious_names:
                        suspicious_names.append(word)
                if RSA.lower() in word.lower():
                    if word not in suspicious_names:
                        suspicious_names.append(word)
        #find line and build warning_lines dict
        with open(type_file, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                for name in suspicious_names:
                    if name in line:
                        if warning_lines.get(name) is not None:
                            warning_lines[name].append(line_number)
                        else:
                            warning_lines[name] = [line_number]
        logger.info(warning_lines)

        for key in warning_lines:
            message = f"Suspicious name \"{key}\" found in the file, may indicate implementation of custom crypto code.\n" + \
                      "Check for custom code implementation."
            description = f"Potential usage of custom crypto code in {type_file.name}.\n" + \
                          f"lines: {warning_lines[key]}.\n" + \
                          f"reason: {message}"
            output_results.append(AnalysisResult(description, {Smell.SCN}))


    def python_analysis(self, type_file, AES, IV, RSA, output_results):
        with open(type_file, 'r') as file:
            # Read the content of the file
            file_content = file.read()
            fun_var_names = []
            warning_lines = {}
            message = ""
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
                if AES.lower() not in name.lower() and IV.lower() not in name.lower() and RSA.lower() not in name.lower() and name in warning_lines:
                    warning_lines.pop(name)
            for key in warning_lines:
                message = f"Suspicious name \"{key}\" found in the file, may indicate implementation of custom crypto code.\n" + \
                          "Check for custom code implementation."
                description = f"Potential usage of custom crypto code in {type_file.name}.\n" + \
                              f"lines: {warning_lines[key]}.\n" + \
                              f"reason: {message}"
                output_results.append(AnalysisResult(description, {Smell.SCN}))

    def js_analysis(self, type_file, AES, IV, RSA):
        with (open(type_file, 'r') as file):
            # Read the content of the file
            fun_var_names = []
            warning_lines = {}
            file_content = file.read()
            logger.info("Analyzing " + type_file.name)
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

                    #elif node.type in ('ExpressionStatement') and node.expression.type == 'CallExpression':
                    #    logger.info("found function call statement")
                    #    fun_var_names.append(node.expression.callee.property.name)
                    #    if warning_lines.get(node.expression.callee.property.name) is not None:
                    #        warning_lines[node.expression.callee.property.name].append(node.expression.callee.property.loc.start.line)
                    #    else:
                    #        warning_lines[node.expression.callee.property.name] = [node.expression.callee.property.loc.start.line]

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
                        if AES.lower() not in name.lower() and IV.lower() not in name.lower() and RSA.lower() not in name.lower() and name in warning_lines:
                            warning_lines.pop(name)

            return warning_lines
