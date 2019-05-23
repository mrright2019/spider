
var com = {};
com.str = {
    _KEY: "",
    _IV: "abcd134556abcedf",
    Encrypt: function (str) {
        var key = CryptoJS.enc.Utf8.parse(this._KEY);
        var iv = CryptoJS.enc.Utf8.parse(this._IV);

        var encrypted = '';

        var srcs = CryptoJS.enc.Utf8.parse(str);
        encrypted = CryptoJS.AES.encrypt(srcs, key, {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });

        return encrypted.ciphertext.toString();
    },
    Decrypt: function (str) {
		var result =  com.str.DecryptInner(str);
		 try {
            var newstr =  com.str.DecryptInner(result);
			if(newstr!=""){
				result = newstr;
			}
          } catch (ex) {
			var msg = ex;
        }
        return result;
    },
	 DecryptInner: function (str) {
        var key = CryptoJS.enc.Utf8.parse(this._KEY);
        var iv = CryptoJS.enc.Utf8.parse(this._IV);
        var encryptedHexStr = CryptoJS.enc.Hex.parse(str);
        var srcs = CryptoJS.enc.Base64.stringify(encryptedHexStr);
        var decrypt = CryptoJS.AES.decrypt(srcs, key, {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
        var decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
        // return decryptedStr;
		var result =  decryptedStr.toString();
		 try {
            result =  Decrypt(result);
          } catch (ex) {
			var msg = ex;
        }
        return result;
    }
}


  function iemap(myarray ,callback, thisArg) {
 
        var T, A, k;
 
        if (myarray == null) {
            throw new TypeError(" this is null or not defined");
        }
        var O = Object(myarray);
 
        var len = O.length >>> 0; 
        if (typeof callback !== "function") {
            throw new TypeError(callback + " is not a function");
        }
        if (thisArg) {
            T = thisArg;
        }
      
        A = new Array(len);
        k = 0;
        while(k < len) {
            var kValue, mappedValue;
            if (k in O) {               
                kValue = O[ k ]; 
                mappedValue = callback.call(T, kValue, k, O);
 
                A[ k ] = mappedValue;
            }
            k++;
        }
        return A;
    };


function setkey(key){
    com.str._KEY = key;
}


function Navi(unzipid) {
    var realid = com.str.Decrypt(unzipid)
    return realid;
}

function getid(unzipid){
    var key = CryptoJS.enc.Utf8.parse(com.str._KEY);
    var iv = CryptoJS.enc.Utf8.parse(com.str._IV);
    var encryptedHexStr = CryptoJS.enc.Hex.parse(unzipid);
    var srcs = CryptoJS.enc.Base64.stringify(encryptedHexStr);
    var decrypt = CryptoJS.AES.decrypt(srcs, key, {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
    var decryptedStr = decrypt.toString();
    var result =  decryptedStr.toString();
    return encryptedHexStr;
    // return result;
    return decryptedStr;
}