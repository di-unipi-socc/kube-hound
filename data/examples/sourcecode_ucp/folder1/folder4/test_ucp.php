<?php

// AES encryption
function encryptAES($plaintext, $key) {
    $cipher = "AES-128-ECB"; // AES-128 with ECB mode
    $ciphertext = openssl_encrypt($plaintext, $cipher, $key, OPENSSL_RAW_DATA);
    return $ciphertext;
}

function decryptAES($ciphertext, $key) {
    $cipher = "AES-128-ECB"; // AES-128 with ECB mode
    $plaintext = openssl_decrypt($ciphertext, $cipher, $key, OPENSSL_RAW_DATA);
    return $plaintext;
}

// RSA encryption
function generateRSAKeyPair() {
    $config = array(
        "private_key_bits" => 2048,
        "private_key_type" => OPENSSL_KEYTYPE_RSA
    );
    $res = openssl_pkey_new($config);
    openssl_pkey_export($res, $privateKey);
    $publicKey = openssl_pkey_get_details($res)["key"];
    return array($privateKey, $publicKey);
}

function encryptRSA($plaintext, $publicKey) {
    openssl_public_encrypt($plaintext, $ciphertext, $publicKey);
    return $ciphertext;
}

function decryptRSA($ciphertext, $privateKey) {
    openssl_private_decrypt($ciphertext, $plaintext, $privateKey);
    return $plaintext;
}

// Usage example
$plaintext = "Hello, World!";

// AES encryption and decryption
$aesKey = random_bytes(16); // 16 bytes key for AES-128
$ciphertextAES = encryptAES($plaintext, $aesKey);
$decryptedTextAES = decryptAES($ciphertextAES, $aesKey);

// RSA encryption and decryption
list($privateKey, $publicKey) = generateRSAKeyPair();
$ciphertextRSA = encryptRSA($plaintext, $publicKey);
$decryptedTextRSA = decryptRSA($ciphertextRSA, $privateKey);

echo "Plaintext: $plaintext\n";
echo "AES Ciphertext: " . base64_encode($ciphertextAES) . "\n";
echo "Decrypted AES Text: $decryptedTextAES\n";
echo "RSA Ciphertext: " . base64_encode($ciphertextRSA) . "\n";
echo "Decrypted RSA Text: $decryptedTextRSA\n";

