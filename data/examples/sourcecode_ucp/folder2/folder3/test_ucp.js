const crypto = require('crypto');

// AES encryption and decryption
const aesKey = crypto.randomBytes(32); // 256-bit AES key
const iv = crypto.randomBytes(16); // AES initialization vector

const plainText = 'Hello, AES!';
console.log('AES Encryption:');
console.log('Plain Text: ' + plainText);

const cipher = crypto.createCipheriv('aes-256-cbc', aesKey, iv);
let encryptedText = cipher.update(plainText, 'utf8', 'hex');
encryptedText += cipher.final('hex');
console.log('Encrypted Text: ' + encryptedText);

const decipher = crypto.createDecipheriv('aes-256-cbc', aesKey, iv);
let decryptedText = decipher.update(encryptedText, 'hex', 'utf8');
decryptedText += decipher.final('utf8');
console.log('Decrypted Text: ' + decryptedText);

// RSA encryption and decryption
const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
  modulusLength: 2048,
  publicKeyEncoding: {
    type: 'pkcs1',
    format: 'pem',
  },
  privateKeyEncoding: {
    type: 'pkcs1',
    format: 'pem',
  },
});

const plainMessage = 'Hello, RSA!';
console.log('\nRSA Encryption:');
console.log('Plain Message: ' + plainMessage);

const encryptedMessage = crypto.publicEncrypt(publicKey, Buffer.from(plainMessage));
console.log('Encrypted Message: ' + encryptedMessage.toString('base64'));

const decryptedMessage = crypto.privateDecrypt(privateKey, encryptedMessage);
console.log('Decrypted Message: ' + decryptedMessage.toString('utf8'));
