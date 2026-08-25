public final class ArrivalBoardDemo {
    private ArrivalBoardDemo() { }

    public static void main(String[] args) {
        ArrivalBoard platformDisplay = new ArrivalBoard("Brock Hall", 610);
        ArrivalBoard mobileView = platformDisplay;

        System.out.println(platformDisplay.message(600));
        mobileView.updatePrediction(614);
        System.out.println(platformDisplay.message(600));
    }
}
