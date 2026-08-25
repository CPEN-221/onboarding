public final class NullReferenceFailure {
    private NullReferenceFailure() { }

    public static void main(String[] args) {
        ArrivalBoard unavailableBoard = null;
        System.out.println(unavailableBoard.message(600));
    }
}
