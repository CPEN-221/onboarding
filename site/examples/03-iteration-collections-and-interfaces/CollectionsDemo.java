import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public final class CollectionsDemo {
    private CollectionsDemo() { }

    public static void main(String[] args) {
        List<String> observedRoutes = new ArrayList<>();
        observedRoutes.add("44");
        observedRoutes.add("84");
        observedRoutes.add("44");

        Set<String> distinctRoutes = new HashSet<>(observedRoutes);

        Map<String, Integer> latestDelayByRoute = new HashMap<>();
        latestDelayByRoute.put("44", 4);
        latestDelayByRoute.put("84", -1);
        latestDelayByRoute.put("44", 7);

        System.out.println("observations: " + observedRoutes.size());
        System.out.println("distinct routes: " + distinctRoutes.size());
        System.out.println("contains 44: " + distinctRoutes.contains("44"));
        System.out.println("latest delay for 44: " + latestDelayByRoute.get("44"));
    }
}
