public final class ArraySummary {
    private ArraySummary() { }

    public static void main(String[] args) {
        int[] delays = {-2, 0, 4, 7};
        int lateCount = 0;

        for (int index = 0; index < delays.length; index++) {
            if (delays[index] > 0) {
                lateCount++;
            }
        }

        System.out.println("late predictions: " + lateCount);
    }
}
