const SECRET_KEY = "743677397A24432646294A404E635166";

function myEncrypt(data) {
  return doEncrypt(data, SECRET_KEY);
}

let result = myEncrypt("TEMP");
console.log("Encrypt result: " + result);