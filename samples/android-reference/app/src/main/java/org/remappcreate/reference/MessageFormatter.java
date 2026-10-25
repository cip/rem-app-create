package org.remappcreate.reference;

/** Pure JVM logic: test without Android framework or emulator. */
public final class MessageFormatter {
    private MessageFormatter() {}
    public static String greeting(String appName) {
        if (appName == null || appName.trim().isEmpty()) {
            throw new IllegalArgumentException("appName must not be empty");
        }
        return "Hello from " + appName.trim() + "!";
    }
}
