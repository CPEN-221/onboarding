public final class ArrivalDisplayExpanded {
    private ArrivalDisplayExpanded() { }

    public static void main(String[] args) {
        int scheduledMinute = 600;
        int predictedMinute = 597;
        String message = arrivalMessage(scheduledMinute, predictedMinute);

        System.out.println(message);
    }

    static String arrivalMessage(int scheduledMinute, int predictedMinute) {
        // Both arguments are service-day minute values from 0 through 1800.
        int difference = predictedMinute - scheduledMinute;
        if (difference < 0) {
            return "EARLY by " + -difference + " minutes";
        }
        if (difference > 0) {
            return "LATE by " + difference + " minutes";
        }
        return "ON TIME";
    }
}
