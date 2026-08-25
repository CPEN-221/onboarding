package ca.ubc.ece.cpen221.prep;

/** Creates a short summary of a transit prediction. */
public final class TransitSummary {
    private TransitSummary() { }

    /**
     * Classifies an arrival prediction relative to its schedule.
     *
     * @param route a route number
     * @param scheduledMinute the scheduled minute on the service-day timeline
     * @param predictedMinute the predicted minute on the same timeline
     * @return a route label followed by EARLY, ON TIME, or LATE
     */
    public static String describe(int route, int scheduledMinute, int predictedMinute) {
        String status;
        if (predictedMinute < scheduledMinute) {
            status = "EARLY";
        } else if (predictedMinute > scheduledMinute) {
            status = "LATE";
        } else {
            status = "ON TIME";
        }
        return "Route " + route + ": " + status;
    }

    /** Runs the example used by the preparation guide. */
    public static void main(String[] args) {
        System.out.println(describe(44, 600, 600));
    }
}
