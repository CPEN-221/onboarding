public final class ArrivalBoard {
    private static final int MAX_SERVICE_MINUTE = 1800;

    private final String stopName;
    private int predictedMinute;

    public ArrivalBoard(String stopName, int predictedMinute) {
        if (stopName == null || stopName.isBlank()) {
            throw new IllegalArgumentException("stopName must contain text");
        }
        checkMinute(predictedMinute);
        this.stopName = stopName;
        this.predictedMinute = predictedMinute;
    }

    public void updatePrediction(int predictedMinute) {
        checkMinute(predictedMinute);
        this.predictedMinute = predictedMinute;
    }

    public String message(int currentMinute) {
        checkMinute(currentMinute);
        int waitMinutes = this.predictedMinute - currentMinute;
        return this.stopName + ": " + waitMinutes + " minutes";
    }

    private static void checkMinute(int minute) {
        if (minute < 0 || minute > MAX_SERVICE_MINUTE) {
            throw new IllegalArgumentException("minute outside service day");
        }
    }
}
