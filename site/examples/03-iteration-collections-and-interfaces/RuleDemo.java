import java.util.List;

interface DelayRule {
    boolean matches(int delayMinutes);
}

final class AtLeastDelay implements DelayRule {
    private final int threshold;

    AtLeastDelay(int threshold) {
        this.threshold = threshold;
    }

    @Override
    public boolean matches(int delayMinutes) {
        return delayMinutes >= this.threshold;
    }
}

final class AtMostDelay implements DelayRule {
    private final int threshold;

    AtMostDelay(int threshold) {
        this.threshold = threshold;
    }

    @Override
    public boolean matches(int delayMinutes) {
        return delayMinutes <= this.threshold;
    }
}

final class BothRules implements DelayRule {
    private final DelayRule first;
    private final DelayRule second;

    BothRules(DelayRule first, DelayRule second) {
        this.first = first;
        this.second = second;
    }

    @Override
    public boolean matches(int delayMinutes) {
        return this.first.matches(delayMinutes)
            && this.second.matches(delayMinutes);
    }
}

public final class RuleDemo {
    private RuleDemo() { }

    public static void main(String[] args) {
        List<Integer> delays = List.of(-2, 0, 5, 8, 12);
        DelayRule concerning = new BothRules(
            new AtLeastDelay(5),
            new AtMostDelay(10)
        );

        int matchCount = 0;
        for (int delay : delays) {
            if (concerning.matches(delay)) {
                matchCount++;
            }
        }

        System.out.println("matching delays: " + matchCount);
    }
}
