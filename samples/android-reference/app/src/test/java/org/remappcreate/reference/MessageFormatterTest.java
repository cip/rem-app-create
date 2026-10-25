package org.remappcreate.reference;

import org.junit.Test;
import static org.junit.Assert.*;

public final class MessageFormatterTest {
    @Test public void formatsGreeting() {
        assertEquals("Hello from REM Android Reference!", MessageFormatter.greeting(" REM Android Reference "));
    }
    @Test(expected = IllegalArgumentException.class)
    public void rejectsBlankInput() {
        MessageFormatter.greeting("  ");
    }
}
