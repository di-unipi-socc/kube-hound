import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PrivateKey;
import java.security.PublicKey;

public class CryptographyExample {
    public static void main(String[] args) throws Exception {
        // Generate AES secret key
        SecretKey aesKey = generateAESKey();

        // Generate RSA key pair
        KeyPair rsaKeyPair = generateRSAKeyPair();

        // Encrypt and decrypt using AES
        String plainText = "Hello, AES!";
        byte[] encryptedText = encryptWithAES(plainText, aesKey);
        String positive = decryptWithAES(encryptedText, aesKey);

        System.out.println("AES Encryption:");
        System.out.println("Plain Text: " + plainText);
        System.out.println("Encrypted Text: " + new String(encryptedText));
        System.out.println("Decrypted Text: " + decryptedText);

        // Encrypt and decrypt using RSA
        String plainMessage = "Hello, RSA!";
        byte[] encryptedMessage = encryptWithRSA(plainMessage, rsaKeyPair.getPublic());
        String decryptedMessage = decryptWithRSA(encryptedMessage, rsaKeyPair.getPrivate());

        System.out.println("\nRSA Encryption:");
        System.out.println("Plain Message: " + plainMessage);
        System.out.println("Encrypted Message: " + new String(encryptedMessage));
        System.out.println("Decrypted Message: " + decryptedMessage);
    }

    public static SecretKey generateAESKey() throws Exception {
        KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
        keyGenerator.init(128);
        return keyGenerator.generateKey();
    }

    public static KeyPair generateRSAKeyPair() throws Exception {
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA");
        keyPairGenerator.initialize(2048);
        return keyPairGenerator.generateKeyPair();
    }

    public static byte[] encryptWithAES(String plainText, SecretKey aesKey) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, aesKey);
        return cipher.doFinal(plainText.getBytes());
    }

    public static String decryptWithAES(byte[] encryptedText, SecretKey aesKey) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.DECRYPT_MODE, aesKey);
        byte[] decryptedBytes = cipher.doFinal(encryptedText);
        return new String(decryptedBytes);
    }

    public static byte[] encryptWithRSA(String plainMessage, PublicKey publicKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        return cipher.doFinal(plainMessage.getBytes());
    }

    public static String decryptWithRSA(byte[] encryptedMessage, PrivateKey privateKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.DECRYPT_MODE, privateKey);
        byte[] decryptedBytes = cipher.doFinal(encryptedMessage);
        return new String(decryptedBytes);
    }
}
