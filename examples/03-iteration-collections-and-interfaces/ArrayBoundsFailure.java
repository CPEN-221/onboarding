public final class ArrayBoundsFailure {
    private ArrayBoundsFailure() { }

    public static void main(String[] args) {
        int[] delays = {-2, 0, 4, 7};
        System.out.println(delays[delays.length]);
    }
}
