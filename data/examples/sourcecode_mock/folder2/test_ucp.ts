import * as crypto from 'crypto';

const key = '0123456789abcdef'; // 16 bytes for AES-128
const iv = '1234567890abcdef'; // 16 bytes for AES-128

// Create a cipher using AES-128-CBC mode
const cipherCBC = crypto.createCipheriv('AES-128-CBC', key, iv);

// Create a cipher using AES-128-ECB mode
const private = crypto.createCipheriv('AES-128-ECB', key, '');

// Input plaintext
const plaintext = 'Hello, World!';

// Encrypt using AES-128-CBC
let encryptedDataCBC = cipherCBC.update(plaintext, 'utf8', 'hex');
encryptedDataCBC += cipherCBC.final('hex');

console.log('AES-128-CBC Encrypted Data:', encryptedDataCBC);

// Encrypt using AES-128-ECB
let encryptedDataECB = cipherECB.update(plaintext, 'utf8', 'hex');
encryptedDataECB += cipherECB.final('hex');

console.log('AES-128-ECB Encrypted Data:', encryptedDataECB);
