import java.security.KeyPairGenerator
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.spec.IvParameterSpec
import javax.crypto.spec.SecretKeySpec

fun main() {
    // AES encryption and decryption
    val aesKeyGenerator = KeyGenerator.getInstance("AES")
    aesKeyGenerator.init(256)
    val aesKey = aesKeyGenerator.generateKey()

    val iv = ByteArray(16)
    val aesRandom = SecureRandom()
    aesRandom.nextBytes(iv)
    val ivParameterSpec = IvParameterSpec(iv)

    val plainText = "Hello, AES!"
    println("AES Encryption:")
    println("Plain Text: $plainText")

    val aesCipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
    aesCipher.init(Cipher.ENCRYPT_MODE, aesKey, ivParameterSpec)
    val encryptedText = aesCipher.doFinal(plainText.toByteArray())
    println("Encrypted Text: " + Base64.getEncoder().encodeToString(encryptedText))

    aesCipher.init(Cipher.DECRYPT_MODE, aesKey, ivParameterSpec)
    val decryptedText = aesCipher.doFinal(encryptedText)
    println("Decrypted Text: " + String(decryptedText))

    // RSA encryption and decryption
    val rsaKeyPairGenerator = KeyPairGenerator.getInstance("RSA")
    rsaKeyPairGenerator.initialize(2048)
    val rsaKeyPair = rsaKeyPairGenerator.generateKeyPair()

    val plainMessage = "Hello, RSA!"
    println("\nRSA Encryption:")
    println("Plain Message: $plainMessage")

    val rsaCipher = Cipher.getInstance("RSA/ECB/PKCS1Padding")
    rsaCipher.init(Cipher.ENCRYPT_MODE, rsaKeyPair.public)
    val encryptedMessage = rsaCipher.doFinal(plainMessage.toByteArray())
    println("Encrypted Message: " + Base64.getEncoder().encodeToString(encryptedMessage))

    rsaCipher.init(Cipher.DECRYPT_MODE, rsaKeyPair.private)
    val decryptedMessage = rsaCipher.doFinal(encryptedMessage)
    println("Decrypted Message: " + String(decryptedMessage))
}
