# Test Usage of Cryptographic Primitives

- `config.yaml` contains the deployment configurations for the example. the sourcecode key specifies the directory to analyse.
- `folder1`,  `folder2`, `net` various files written in different languages, containing instances of the usage of cryptographic primitives smell, inserted at different depths inside the directory to show the full abilities of the analysis.


## Tool output
Kuberhound will detect Usage of Cryptographic Primitives in sourcecode files written in the following languages:
java, php, python, javascript, kotlin and typescript.

C# and vbnet analysis still need to be implemented.

### Command to run

```
./data/examples/sourcecode_ucp/run.sh
```

### Detected smells
```
Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.java
	line: 51
	reason: Use a secure padding scheme.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.java
	line: 57
	reason: Use a secure padding scheme.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.java
	line: 64
	reason: Use a secure padding scheme.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.java
	line: 70
	reason: Use a secure padding scheme.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.php
	line: 6
	reason: Use secure mode and padding scheme.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.php
	line: 29
	reason: Use secure mode and padding scheme.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.py
	line: 7
	reason: Use secure mode and padding scheme.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.py
	line: 12
	reason: Use secure mode and padding scheme.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.js
	line: 11
	reason: Use a secure mode and padding scheme.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.kt
	line: 22
	reason: Use another cipher mode or disable padding.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.kt
	line: 40
	reason: Use a secure padding scheme.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.ts
	line: 7
	reason: Use a secure mode and padding scheme.

Usage of Cryptographic Primitives Analysis - detected smells {UCP}
	Sonarqube found potential problems in test_ucp.ts
	line: 10
	reason: Use a secure mode and padding scheme.

```