public final class ReassignmentDemo {
    private ReassignmentDemo() { }

    public static void main(String[] args) {
        ArrivalBoard platformDisplay = new ArrivalBoard("Brock Hall", 610);
        ArrivalBoard mobileView = platformDisplay;

        mobileView = new ArrivalBoard("UBC Exchange", 625);
        mobileView.updatePrediction(628);

        System.out.println(platformDisplay.message(600));
        System.out.println(mobileView.message(600));
    }
}
