Imports System
Imports System.Security.Cryptography
Imports System.Text

Module Program
    Sub Main()
        ' AES Encryption and Decryption
        Dim aesKey As Byte() = Encoding.UTF8.GetBytes("0123456789abcdef") ' 16-byte key
        Dim aesIV As Byte() = Encoding.UTF8.GetBytes("1234567890abcdef") ' 16-byte IV

        Dim plaintext As String = "Hello, World!"
        Console.WriteLine("Plaintext: " & plaintext)

        Dim encryptedBytes As Byte() = EncryptAES(plaintext, aesKey, aesIV)
        Dim encryptedText As String = Convert.ToBase64String(encryptedBytes)
        Console.WriteLine("Encrypted Text: " & encryptedText)

        Dim decryptedText As String = DecryptAES(encryptedBytes, aesKey, aesIV)
        Console.WriteLine("Decrypted Text: " & decryptedText)

        ' RSA Encryption and Decryption
        Dim rsa As New RSACryptoServiceProvider()

        Dim publicKey As String = rsa.ToXmlString(False) ' Export the public key
        Dim privateKey As String = rsa.ToXmlString(True) ' Export the private key

        Dim plaintext2 As String = "Hello, RSA!"
        Console.WriteLine("Plaintext: " & plaintext2)

        Dim encryptedBytes2 As Byte() = EncryptRSA(plaintext2, publicKey)
        Dim encryptedText2 As String = Convert.ToBase64String(encryptedBytes2)
        Console.WriteLine("Encrypted Text: " & encryptedText2)

        Dim decryptedText2 As String = DecryptRSA(encryptedBytes2, privateKey)
        Console.WriteLine("Decrypted Text: " & decryptedText2)
    End Sub

    Function EncryptAES(plaintext As String, key As Byte(), iv As Byte()) As Byte()
        Dim aes As New AesCryptoServiceProvider()
        aes.Key = key
        aes.IV = iv

        Dim encryptor As ICryptoTransform = aes.CreateEncryptor()
        Dim plaintextBytes As Byte() = Encoding.UTF8.GetBytes(plaintext)

        Dim encryptedBytes As Byte() = encryptor.TransformFinalBlock(plaintextBytes, 0, plaintextBytes.Length)
        Return encryptedBytes
    End Function

    Function DecryptAES(encryptedBytes As Byte(), key As Byte(), iv As Byte()) As String
        Dim aes As New AesCryptoServiceProvider()
        aes.Key = key
        aes.IV = iv

        Dim decryptor As ICryptoTransform = aes.CreateDecryptor()

        Dim decryptedBytes As Byte() = decryptor.TransformFinalBlock(encryptedBytes, 0, encryptedBytes.Length)
        Dim decryptedText As String = Encoding.UTF8.GetString(decryptedBytes)
        Return decryptedText
    End Function

    Function EncryptRSA(plaintext As String, publicKey As String) As Byte()
        Dim rsa As New RSACryptoServiceProvider()
        rsa.FromXmlString(publicKey)

        Dim plaintextBytes As Byte() = Encoding.UTF8.GetBytes(plaintext)
        Dim encryptedBytes As Byte() = rsa.Encrypt(plaintextBytes, False)
        Return encryptedBytes
    End Function

    Function DecryptRSA(encryptedBytes As Byte(), privateKey As String) As String
        Dim rsa As New RSACryptoServiceProvider()
        rsa.FromXmlString(privateKey)

        Dim decryptedBytes As Byte() = rsa.Decrypt(encryptedBytes, False)
        Dim decryptedText As String = Encoding.UTF8.GetString(decryptedBytes)
        Return decryptedText
    End Function
End Module
