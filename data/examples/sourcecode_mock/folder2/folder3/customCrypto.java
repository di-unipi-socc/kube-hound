import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class MyCustomHashAlgorithm extends MessageDigest {

    protected MyCustomHashAlgorithm() throws NoSuchAlgorithmException {
        super("MyCustomHashAlgorithm");
    }

    protected void engineReset() {}

    protected void engineUpdate(byte input) {}

    protected void engineUpdate(byte[] input, int offset, int len) {}


    protected byte[] engineDigest() {
        return new byte[0];
    }
}
