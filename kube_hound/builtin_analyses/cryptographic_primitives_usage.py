from kube_hound.applicationobject import ApplicationObject
from kube_hound.smells import Smell
from loguru import logger
import ast
import re

class CryptographicPrimitives(StaticAnalysis):
    analysis_id = 'sourcode_cpu'
    analysis_name = 'Usage of Cryptographic Primitives Analysis'
    analysis_description = ''
    input_types = ['sourcecode']
    # Define regular expressions for cryptographic primitives
    RSA_REGEX = re.compile(r"(RSA|rsa)\.")
    AES_REGEX = re.compile(r"(AES|aes)\.")
    HMAC_REGEX = re.compile(r"(HMAC|hmac)\.")
    HASH_REGEX = re.compile(r"(Hash|hash)\.")

    def run_analysis(self, input_objects: Mapping[str, List[ApplicationObject]]) \
            -> List[AnalysisResult]:
        sourcecode_objects = input_objects.get('sourcecode')
        if sourcecode_objects is None:
            return []

        def contains_crypto(file_path):
            """
            Returns True if the source code file at the given path contains usage of cryptographic primitives, False otherwise.
            """
            with open(file_path, "r") as f:
                source_code = f.read()

            # Parse the source code using the ast module
            parsed_code = ast.parse(source_code)

            # Check for the usage of cryptographic primitives
            for node in ast.walk(parsed_code):
                if isinstance(node, ast.Attribute):
                    attribute_name = node.attr
                    if RSA_REGEX.search(attribute_name):
                        return True
                    elif AES_REGEX.search(attribute_name):
                        return True
                    elif HMAC_REGEX.search(attribute_name):
                        return True
                    elif HASH_REGEX.search(attribute_name):
                        return True

            return False

        output_results = []


        return output_results