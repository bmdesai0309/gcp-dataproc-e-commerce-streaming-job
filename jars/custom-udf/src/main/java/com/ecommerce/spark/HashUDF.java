package com.ecommerce.spark;

import org.apache.spark.sql.api.java.UDF1;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * A Spark Java UDF to perform SHA-256 hashing for PII masking.
 * Implements UDF1<InputType, ReturnType>.
 */
public class HashUDF implements UDF1<String, String> {

    @Override
    public String call(String input) throws Exception {
        if (input == null) {
            return null;
        }
        return sha256Hash(input);
    }

    private String sha256Hash(String base) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(base.getBytes("UTF-8"));
            StringBuilder hexString = new StringBuilder();

            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException | java.io.UnsupportedEncodingException ex) {
            throw new RuntimeException("Could not generate SHA-256 hash", ex);
        }
    }
}