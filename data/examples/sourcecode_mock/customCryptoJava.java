import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class MyCryptographicAlgorithm extends MessageDigest {

    protected MyCryptographicAlgorithm() throws NoSuchAlgorithmException {
        super("MyCryptographicAlgorithm");
    }
    @Override
    protected void engineUpdate(byte input) {
    }

    @Override
    protected void engineUpdate(byte[] input, int offset, int len) {
    }

    @Override
    protected byte[] engineDigest() {
        return new byte[0];
    }

    @Override
    protected void engineReset() {
    }
}
