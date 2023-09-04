# Test Usage of Cryptographic Primitives

- `config.yaml` contains the deployment configurations for the example. the sourcecode key specifies the directory to analyse.
- `folder1`,  `folder2`, `net` various files written in different languages, inserted at different depths inside the directory to simulate how the tool would work in a realistic enviroment.
- Inside these folders are some source code files containing custom crypto code.


## Tool output
Kubehound will detect Usage of Cryptographic Primitives in sourcecode files written in the following languages:
python and java.

C# and vbnet UCP analysis still need to be implemented.

Kubehound will detect Suspiciou Cryptographic Names in sourcecode files.

### Command to run

```
./data/examples/sourcecode_mock/run.sh
```

### Detected smells
```
Analysis results:
Usage of Cryptographic Primitives Analysis - detected smells {OCC}
	Sonarqube found potential problems in customCryptoJava.java at line 4
	>   public class MyCryptographicAlgorithm extends MessageDigest {
	reason: Make sure using a non-standard cryptographic algorithm is safe here.

Usage of Cryptographic Primitives Analysis - detected smells {OCC}
	Sonarqube found potential problems in customCrypto.java at line 4
	>   public class MyCustomHashAlgorithm extends MessageDigest {
	reason: Make sure using a non-standard cryptographic algorithm is safe here.

Usage of Cryptographic Primitives Analysis - detected smells {OCC}
	Sonarqube found potential problems in customCrypto.py at line 3
	>   class CustomPasswordHasher(BasePasswordHasher):
	reason: Make sure using a non-standard cryptographic algorithm is safe here.

Usage of Cryptographic Primitives Analysis - detected smells {OCC}
	Sonarqube found potential problems in customCryptoPython.py at line 3
	>   class CustomPasswordHasher(BasePasswordHasher):
	reason: Make sure using a non-standard cryptographic algorithm is safe here.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:6, 38.
	>   encrypt_aes
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:11, 39.
	>   decrypt_aes
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:23, 43.
	>   encrypt_rsa
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:28, 44.
	>   decrypt_rsa
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:37, 38, 39.
	>   aes_key
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:38, 39, 47.
	>   ciphertext_aes
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:39, 48.
	>   decrypted_text_aes
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:43, 44, 49.
	>   ciphertext_rsa
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:44, 50.
	>   decrypted_text_rsa
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:19, 42, 44, 21, 29.
	>   private_key
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:7, 7, 12, 12.
	>   AES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:18, 24, 29.
	>   RSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:1, 5, 7, 12, 36, 37, 47, 48.
	>   AES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:2, 16, 18, 24, 29, 41, 49, 50.
	>   RSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:6, 38.
	>   encrypt_aes
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:11, 39.
	>   decrypt_aes
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:19, 21, 28, 29, 42, 44.
	>   private_key
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:23, 43.
	>   encrypt_rsa
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:28, 44.
	>   decrypt_rsa
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:37, 38, 39.
	>   aes_key
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:38, 39, 47.
	>   ciphertext_aes
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:39, 48.
	>   decrypted_text_aes
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:43, 44, 49.
	>   ciphertext_rsa
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.py at lines:44, 50.
	>   decrypted_text_rsa
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:12, 38.
	>   generateAESKey
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:12, 19, 20, 50, 52, 56, 58.
	>   aesKey
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:15, 44.
	>   generateRSAKeyPair
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:15, 29, 30.
	>   rsaKeyPair
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:19, 50.
	>   encryptWithAES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:20, 56.
	>   decryptWithAES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:29, 63.
	>   encryptWithRSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:30, 69.
	>   decryptWithRSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:6, 69.
	>   PrivateKey
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:11, 12, 17, 18, 19, 20, 22, 38, 39, 50, 51, 56, 57.
	>   AES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:12, 19, 20, 50, 52, 56, 58.
	>   aesKey
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:12, 38.
	>   generateAESKey
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:14, 15, 27, 28, 29, 30, 32, 44, 45, 63, 64, 69, 70.
	>   RSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:15, 29, 30.
	>   rsaKeyPair
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:15, 44.
	>   generateRSAKeyPair
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:19, 50.
	>   encryptWithAES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:20, 56.
	>   decryptWithAES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:29, 63.
	>   encryptWithRSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:30, 69.
	>   decryptWithRSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:30.
	>   getPrivate
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:32.
	>   nRSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.java at lines:69, 71.
	>   privateKey
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:3, 4, 5, 10, 11, 41, 42, 43, 44, 52, 53.
	>   AES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:4, 43.
	>   encryptAES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:10, 44.
	>   decryptAES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:16, 17, 20, 28, 33, 46, 47, 48, 49, 54, 55.
	>   RSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:17, 47.
	>   generateRSAKeyPair
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:19.
	>   private_key_bits
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:20.
	>   private_key_type
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:20.
	>   OPENSSL_KEYTYPE_RSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:23, 25, 33, 34, 47, 49.
	>   privateKey
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:28, 48.
	>   encryptRSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:33, 49.
	>   decryptRSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:34.
	>   openssl_private_decrypt
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:42, 43, 44.
	>   aesKey
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:43, 44, 52.
	>   ciphertextAES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:44, 53.
	>   decryptedTextAES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:48, 49, 54.
	>   ciphertextRSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.php at lines:49, 55.
	>   decryptedTextRSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.ts at lines:3, 4, 6, 7, 9, 10, 15, 19, 21, 25.
	>   AES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.ts at lines:4, 7, 10.
	>   iv
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.ts at lines:7, 10.
	>   createCipheriv
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.js at lines:4.
	>   aesKey
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.js at lines:5.
	>   iv
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:4, 16.
	>   IvParameterSpec
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:8, 9, 18, 19, 22.
	>   AES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:9, 10, 11.
	>   aesKeyGenerator
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:9, 10, 11, 23, 27.
	>   aesKey
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:13, 15, 16, 23, 27, 45.
	>   iv
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:14, 15.
	>   aesRandom
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:16, 23, 27.
	>   ivParameterSpec
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:22, 23, 24, 27, 28.
	>   aesCipher
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:31, 32, 36, 37, 40.
	>   RSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:32, 33, 34.
	>   rsaKeyPairGenerator
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:32, 33, 34, 41, 45.
	>   rsaKeyPair
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:37.
	>   nRSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.kt at lines:40, 41, 42, 45, 46.
	>   rsaCipher
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:7, 14, 18, 38, 50.
	>   AES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:8, 14, 18.
	>   aesKey
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:8, 9, 14, 18, 39, 40, 41, 43, 51, 52, 53, 55.
	>   aes
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:9, 14, 18.
	>   aesIV
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:9, 14, 18, 41, 53.
	>   IV
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:14, 38.
	>   EncryptAES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:18, 50.
	>   DecryptAES
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:21, 22, 27, 30, 34, 62, 63, 71, 72.
	>   RSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:22, 24, 25, 63, 64, 67, 72, 73, 75.
	>   rsa
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:22, 63, 72.
	>   RSACryptoServiceProvider
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:25, 34, 71, 73.
	>   privateKey
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:25, 34, 38, 41, 50, 53, 71, 73.
	>   iv
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:30, 62.
	>   EncryptRSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:34, 71.
	>   DecryptRSA
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.

Suspicious Cryptographic Names - detected smells {OCC}
	Potential usage of custom crypto code in test_ucp.vb at lines:39, 51.
	>   AesCryptoServiceProvider
	reason: Suspicious name found in the file, may indicate implementation of custom crypto code.
	Check for custom code implementation.



```