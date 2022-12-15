配置文件中有用户的账号密码等信息，需要为用户保护信息。

怎么做呢？暂时没有想到很好的办法，现在设想是用户第一次使用程序时候，配置文件中明文填写账号密码等信息。启用程序连接成功后加密账号密码，输出加密字符串到配置文件中，以后使用密文进行连接。其实这也只是表面功夫，因为实际的连接需要用到明文的账号密码，必须使用对称加密还原账号密码，加密key是写在程序中的，解包后就能获取到。但是怎么说呢，世界上没有攻破不了的防御，只是这个成本问题而已，增加信息被泄漏成本，加密的本质而已。

废话不多说，开始实现：

1. 网上找到加密工具类EncryptUtil，这个加密工具类的好处是不用第三方jar包，简单方便，功能全面：
2. 

```java
//用账号密码长度判断是否已经加密，当然也可以加密后向配置文件中加入额外加密标识
if(clientConfig.getUser().length() > 30 && clientConfig.getPassword().length() > 30){
                    //尝试使用解码后的账号密码进行连接
                    user.put(JMXConnector.CREDENTIALS, new String[] {encryptUtil.AESdecode(clientConfig.getUser(), ENCRYPT_AES_KEY), encryptUtil.AESdecode(clientConfig.getPassword(), ENCRYPT_AES_KEY) });
                    jmxc = JMXConnectorFactory.connect(url,user);
                    mbsc = jmxc.getMBeanServerConnection();
                }else {
                    //尝试直接使用配置文件账号密码信息连接
                    user.put(JMXConnector.CREDENTIALS, new String[] { clientConfig.getUser(), clientConfig.getPassword() });
                    jmxc = JMXConnectorFactory.connect(url,user);
                    mbsc = jmxc.getMBeanServerConnection();

                    try {
                        // 若是能够连接成功，加密账号密码，输出到配置文件中
                        Environment environment = SpringUtil.getBean("environment");
                        String profilepath = environment.getProperty("application.file.path");
                        LinkedProperties properties = new LinkedProperties();
                        FileReader fileReader = new FileReader(profilepath);
                        properties.load(fileReader);
                        FileWriter fileWriter = new FileWriter(profilepath);

                        properties.setProperty("client.user", encryptUtil.AESencode(clientConfig.getUser(), ENCRYPT_AES_KEY));
                        properties.setProperty("client.password", encryptUtil.AESencode(clientConfig.getPassword(), ENCRYPT_AES_KEY));
                        properties.store(fileWriter, "account and password is encrypted");

                        fileReader.close();
                        fileWriter.close();
                    } catch (IOException var2) {
                        var2.printStackTrace();
                    }
```

这里我使用了自定义的 LinkedProperties ，如果使用Properties读写配置文件的话会乱序。查看Properties源码，可以看到

```java
class Properties extends Hashtable<Object,Object> {
    //...
}
```

Properties其实是一个Hashtable，所以里面的键值对会乱序。要想实现顺序也比较简单，写入我们额外使用一个LinkHashMap来保存键值对，写出时使用LinkHashMap里的数据写出即可。

```java
public class LinkedProperties extends Properties {
    private Map<String, String> linkedPropertiesMap = new LinkedHashMap<>();

    public Map<String, String> getLinkedPropertiesMap(){
        return linkedPropertiesMap;
    }
    
    @Override
    public synchronized void load(Reader reader) throws IOException {
        //...
        linkedPropertiesMap.put(key, value);
    }
    
    @Override
    public synchronized Object setProperty(String key, String value) {
        linkedPropertiesMap.put(key, value);
        return put(key, value);
    }
    
    @Override
    public void store(Writer writer, String comments) throws IOException{
      //...
      for(Map.Entry<String, String> entry : linkedPropertiesMap.entrySet()){}
      //...
    }
    
    //...
}
```

EncryptUtil工具类代码：

```java
import com.sun.org.apache.xerces.internal.impl.dv.util.Base64;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.Mac;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.security.MessageDigest;
import java.security.SecureRandom;

public class EncryptUtil {
    public static final String MD5 = "MD5";
    public static final String SHA1 = "SHA1";
    public static final String HmacMD5 = "HmacMD5";
    public static final String HmacSHA1 = "HmacSHA1";
    public static final String DES = "DES";
    public static final String AES = "AES";

    /**编码格式；默认使用uft-8*/
    public String charset = "utf-8";
    /**DES*/
    public int keysizeDES = 0;
    /**AES*/
    public int keysizeAES = 128;

    public static EncryptUtil me;

    private EncryptUtil(){
        //单例
    }
    //双重锁
    public static EncryptUtil getInstance(){
        if (me==null) {
           synchronized (EncryptUtil.class) {
               if(me == null){
                   me = new EncryptUtil();
               }
           }
        }
        return me;
    }

    /**
     * 使用MessageDigest进行单向加密（无密码）
     * @param res 被加密的文本
     * @param algorithm 加密算法名称
     * @return
     */
    private String messageDigest(String res,String algorithm){
        try {
            MessageDigest md = MessageDigest.getInstance(algorithm);
            byte[] resBytes = charset==null?res.getBytes():res.getBytes(charset);
            return base64(md.digest(resBytes));
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * 使用KeyGenerator进行单向/双向加密（可设密码）
     * @param res 被加密的原文
     * @param algorithm  加密使用的算法名称
     * @param key 加密使用的秘钥
     * @return
     */
    private String keyGeneratorMac(String res,String algorithm,String key){
        try {
            SecretKey sk = null;
            if (key==null) {
                KeyGenerator kg = KeyGenerator.getInstance(algorithm);
                sk = kg.generateKey();
            }else {
                byte[] keyBytes = charset==null?key.getBytes():key.getBytes(charset);
                sk = new SecretKeySpec(keyBytes, algorithm);
            }
            Mac mac = Mac.getInstance(algorithm);
            mac.init(sk);
            byte[] result = mac.doFinal(res.getBytes());
            return base64(result);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * 使用KeyGenerator双向加密，DES/AES，注意这里转化为字符串的时候是将2进制转为16进制格式的字符串，不是直接转，因为会出错
     * @param res 加密的原文
     * @param algorithm 加密使用的算法名称
     * @param key  加密的秘钥
     * @param keysize
     * @param isEncode
     * @return
     */
    private String keyGeneratorES(String res,String algorithm,String key,int keysize,boolean isEncode){
        try {
            KeyGenerator kg = KeyGenerator.getInstance(algorithm);
            if (keysize == 0) {
                byte[] keyBytes = charset==null?key.getBytes():key.getBytes(charset);
                kg.init(new SecureRandom(keyBytes));
            }else if (key==null) {
                kg.init(keysize);
            }else {
                byte[] keyBytes = charset==null?key.getBytes():key.getBytes(charset);
                kg.init(keysize, new SecureRandom(keyBytes));
            }
            SecretKey sk = kg.generateKey();
            SecretKeySpec sks = new SecretKeySpec(sk.getEncoded(), algorithm);
            Cipher cipher = Cipher.getInstance(algorithm);
            if (isEncode) {
                cipher.init(Cipher.ENCRYPT_MODE, sks);
                byte[] resBytes = charset==null?res.getBytes():res.getBytes(charset);
                return parseByte2HexStr(cipher.doFinal(resBytes));
            }else {
                cipher.init(Cipher.DECRYPT_MODE, sks);
                return new String(cipher.doFinal(parseHexStr2Byte(res)));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    private String base64(byte[] res){
        return Base64.encode(res);
    }

    /**将二进制转换成16进制 */
    public static String parseByte2HexStr(byte buf[]) {
        StringBuffer sb = new StringBuffer();
        for (int i = 0; i < buf.length; i++) {
            String hex = Integer.toHexString(buf[i] & 0xFF);
            if (hex.length() == 1) {
                hex = '0' + hex;
            }
            sb.append(hex.toUpperCase());
        }
        return sb.toString();
    }
    /**将16进制转换为二进制*/
    public static byte[] parseHexStr2Byte(String hexStr) {
        if (hexStr.length() < 1)
            return null;
        byte[] result = new byte[hexStr.length()/2];
        for (int i = 0;i< hexStr.length()/2; i++) {
            int high = Integer.parseInt(hexStr.substring(i*2, i*2+1), 16);
            int low = Integer.parseInt(hexStr.substring(i*2+1, i*2+2), 16);
            result[i] = (byte) (high * 16 + low);
        }
        return result;
    }

    /**
     * md5加密算法进行加密（不可逆）
     * @param res 需要加密的原文
     * @return
     */
    public String MD5(String res) {
        return messageDigest(res, MD5);
    }

    /**
     * md5加密算法进行加密（不可逆）
     * @param res  需要加密的原文
     * @param key  秘钥
     * @return
     */
    public String MD5(String res, String key) {
        return keyGeneratorMac(res, HmacMD5, key);
    }

    /**
     * 使用SHA1加密算法进行加密（不可逆）
     * @param res 需要加密的原文
     * @return
     */
    public String SHA1(String res) {
        return messageDigest(res, SHA1);
    }

    /**
     * 使用SHA1加密算法进行加密（不可逆）
     * @param res 需要加密的原文
     * @param key 秘钥
     * @return
     */
    public String SHA1(String res, String key) {
        return keyGeneratorMac(res, HmacSHA1, key);
    }

    /**
     * 使用DES加密算法进行加密（可逆）
     * @param res 需要加密的原文
     * @param key 秘钥
     * @return
     */
    public String DESencode(String res, String key) {
        return keyGeneratorES(res, DES, key, keysizeDES, true);
    }

    /**
     * 对使用DES加密算法的密文进行解密（可逆）
     * @param res 需要解密的密文
     * @param key 秘钥
     * @return
     */
    public String DESdecode(String res, String key) {
        return keyGeneratorES(res, DES, key, keysizeDES, false);
    }

    /**
     * 使用AES加密算法经行加密（可逆）
     * @param res 需要加密的密文
     * @param key 秘钥
     * @return
     */
    public String AESencode(String res, String key) {
        return keyGeneratorES(res, AES, key, keysizeAES, true);
    }

    /**
     * 对使用AES加密算法的密文进行解密
     * @param res 需要解密的密文
     * @param key 秘钥
     * @return
     */
    public String AESdecode(String res, String key) {
        return keyGeneratorES(res, AES, key, keysizeAES, false);
    }

    /**
     * 使用异或进行加密
     * @param res 需要加密的密文
     * @param key 秘钥
     * @return
     */
    public String XORencode(String res, String key) {
        byte[] bs = res.getBytes();
        for (int i = 0; i < bs.length; i++) {
            bs[i] = (byte) ((bs[i]) ^ key.hashCode());
        }
        return parseByte2HexStr(bs);
    }

    /**
     * 使用异或进行解密
     * @param res 需要解密的密文
     * @param key 秘钥
     * @return
     */
    public String XORdecode(String res, String key) {
        byte[] bs = parseHexStr2Byte(res);
        for (int i = 0; i < bs.length; i++) {
            bs[i] = (byte) ((bs[i]) ^ key.hashCode());
        }
        return new String(bs);
    }

    /**
     * 直接使用异或（第一调用加密，第二次调用解密）
     * @param res 密文
     * @param key 秘钥
     * @return
     */
    public int XOR(int res, String key) {
        return res ^ key.hashCode();
    }

    /**
     * 使用Base64进行加密
     * @param res 密文
     * @return
     */
    public String Base64Encode(String res) {
        return Base64.encode(res.getBytes());
    }

    /**
     * 使用Base64进行解密
     * @param res
     * @return
     */
    public String Base64Decode(String res) {
        return new String(Base64.decode(res));
}
```