# Test Usage of Cryptographic Primitives

- `config.yaml` contains the deployment configurations for the example. the sourcecode key specifies the directory to analyse.
- `folder1`,  `folder2`, `net` various files written in different languages, inserted at different depths inside the directory to simulate how the tool would work in a realistic enviroment.
- Inside these folders are some source code files containing custom crypto code.


## Tool output
Kubehound will detect Usage of Cryptographic Primitives in sourcecode files written in the following languages:
python and java.

C# and vbnet analysis still need to be implemented.

### Command to run

```
./data/examples/sourcecode_mock/run.sh
```

### Detected smells
```
Analysis results:
Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in customCryptoJava.java
	line: 4
	reason: Make sure using a non-standard cryptographic algorithm is safe here.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in customCrypto.java
	line: 4
	reason: Make sure using a non-standard cryptographic algorithm is safe here.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in customCrypto.py
	line: 3
	reason: Make sure using a non-standard cryptographic algorithm is safe here.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in customCryptoPython.py
	line: 3
	reason: Make sure using a non-standard cryptographic algorithm is safe here.


```