package ca.ubc.ece.cpen221.prep;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class TransitSummaryTest {
    @Test
    void describesEarlyArrival() {
        assertEquals("Route 44: EARLY", TransitSummary.describe(44, 600, 593));
    }

    @Test
    void describesOnTimeArrival() {
        assertEquals("Route 44: ON TIME", TransitSummary.describe(44, 600, 600));
    }

    @Test
    void describesLateArrival() {
        assertEquals("Route 44: LATE", TransitSummary.describe(44, 600, 602));
    }
}
