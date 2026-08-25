# Getting Started with CPEN 221 | Segment 3: Iteration, Collections, and Interfaces

A prediction service receives several observations for each route. The program must
count late predictions, preserve the order in which observations arrived, identify
distinct routes, and retain the latest delay for each route. One container cannot
provide all four meanings by accident; the program must choose the data structure
whose contract matches each requirement.

We will begin with a fixed array and two loop forms. We will then use `List`, `Set`,
and `Map` for three different relationships and finish by selecting delay rules
through an interface.

By the end, you should be able to:

- trace indexed and enhanced `for` loops;
- explain array length, valid indices, and an out-of-bounds failure;
- read and construct a generic type such as `List<Integer>`;
- choose among `List`, `Set`, and `Map` from their behavioural contracts;
- distinguish an unspecified iteration order from a random order;
- use an interface as a shared type for several implementations; and
- combine behaviour through object composition.

## 1. Traverse a Fixed Array by Index

An **array** stores a fixed number of components of one declared type. This
declaration constructs an array with four `int` components and initializes them:

```java
int[] delays = {-2, 0, 4, 7};
```

The variable `delays` holds a reference to the array object. The components have
indices `0`, `1`, `2`, and `3`. The array's `length` is `4`; `length` is a count,
not the final valid index.

This loop counts the positive delays:

```java
int lateCount = 0;

for (int index = 0; index < delays.length; index++) {
    if (delays[index] > 0) {
        lateCount++;
    }
}
```

A basic `for` loop has four execution parts:

1. `int index = 0` runs once before the first condition check.
2. `index < delays.length` runs before every possible iteration.
3. The body runs when the condition is true.
4. `index++` runs after the body and before the next condition check.

The trace is:

| `index` at body entry | `delays[index]` | Is it positive? | `lateCount` after body |
|---:|---:|---|---:|
| 0 | −2 | no | 0 |
| 1 | 0 | no | 0 |
| 2 | 4 | yes | 1 |
| 3 | 7 | yes | 2 |

After the fourth iteration, `index++` changes the local variable to `4`. The
condition `4 < 4` is false, so the loop stops before evaluating `delays[4]`.

Running the complete example produced:

```text
late predictions: 2
```

<form class="quick-check" data-quick-check data-answer="less-than">
<fieldset>
<legend>Which condition visits every component of this array exactly once without an out-of-bounds access?</legend>
<label><input type="radio" name="array-condition" value="less-than"> <code>index &lt; delays.length</code></label>
<label><input type="radio" name="array-condition" value="less-equal"> <code>index &lt;= delays.length</code></label>
<label><input type="radio" name="array-condition" value="minus-one"> <code>index &lt; delays.length - 1</code></label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>The valid indices range from zero through <code>length - 1</code>. The strict comparison admits exactly those values.</p>
</details>
</form>

Java checks an array index when the access executes. The expression
`delays[delays.length]` compiles because both the index and components have suitable
types. At runtime, index `4` is outside this four-component array, so Java throws
`ArrayIndexOutOfBoundsException`.

This guarantee concerns the observable array access. We can reason about valid
indices without claiming that the array occupies a particular physical heap
location; allocation strategy is not a Java language-level property of the source.

## 2. Use an Enhanced Loop When the Index Does Not Matter

The counting operation needs each delay value but does not otherwise use its index.
An enhanced `for` loop states that relationship directly:

```java
int lateCount = 0;

for (int delay : delays) {
    if (delay > 0) {
        lateCount++;
    }
}
```

On each iteration, Java assigns the next array component's value to the local
variable `delay`. The body sees `-2`, `0`, `4`, and `7` in array order.

Assigning another integer to `delay` would change only the loop variable for that
iteration. It would not assign a component of the array. Use an indexed loop when
the algorithm must know a position or replace a component; use the enhanced form
when it consumes each value without needing the index.

> **Design principle: make the loop express the relationship the algorithm needs.**

An unnecessary index creates another value whose bounds and updates must be proved
correct. An enhanced loop removes that obligation when position does not matter.

## 3. Use a List for an Ordered Sequence

Arrays have fixed length. A prediction service usually does not know in advance how
many observations it will receive. A `List` represents an ordered sequence whose
size can be queried and whose common implementations can grow:

```java
import java.util.ArrayList;
import java.util.List;

List<String> observedRoutes = new ArrayList<>();
observedRoutes.add("44");
observedRoutes.add("84");
observedRoutes.add("44");
```

The declared type is the interface `List<String>`. The constructed object has class
`ArrayList<String>`, one implementation of that interface. Declaring the variable
with the interface type makes the required operations—ordered list operations—the
visible dependency.

The angle brackets supply a **generic type argument**. `List<String>` permits string
elements and lets the compiler reject an attempt to add an unrelated type. The
empty diamond in `new ArrayList<>()` asks the compiler to infer `String` from the
surrounding declaration.

`add` appends an element and returns a `boolean`. For `ArrayList`, the one-argument
form returns `true` after adding; this program does not need that result. The list
now has size three, retains insertion order, and contains `"44"` twice. A list does
not imply uniqueness.

Primitive types cannot appear directly as generic type arguments. Java uses the
reference type `Integer` for integer elements:

```java
List<Integer> delays = List.of(-2, 0, 4, 7);
```

Java's boxing conversion produces `Integer` values for these `int` literals, and
unboxing supplies `int` values when an enhanced loop declares `int delay`. There is
no need to invoke the deprecated `new Integer(...)` constructor.

## 4. Use a Set for Unique Elements

The observation sequence contains three entries but only two route identifiers. A
`Set` represents a collection that contains no duplicate elements:

```java
import java.util.HashSet;
import java.util.Set;

Set<String> distinctRoutes = new HashSet<>(observedRoutes);
```

The constructor visits the list elements and adds them to the set. Adding the
second `"44"` does not create a second equal set element. The resulting size is two,
and `distinctRoutes.contains("44")` is true.

`HashSet` does not guarantee its iteration order. It is inaccurate to call the
order random: an observed order may remain stable for many executions, yet clients
still have no contract that permits them to depend on it. If a requirement needs
insertion order, select an implementation whose specification promises it, such as
`LinkedHashSet`, or retain a separate list.

<form class="quick-check" data-quick-check data-answer="two-unspecified">
<fieldset>
<legend>After adding <code>"44"</code>, <code>"84"</code>, and <code>"44"</code> to a <code>HashSet</code>, which statement is supported by its contract?</legend>
<label><input type="radio" name="set-contract" value="three-random"> Its size is three and iteration is random.</label>
<label><input type="radio" name="set-contract" value="two-insertion"> Its size is two and iteration follows insertion order.</label>
<label><input type="radio" name="set-contract" value="two-unspecified"> Its size is two and its iteration order is unspecified.</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>A set retains one element from each equality class. <code>HashSet</code> makes no iteration-order guarantee.</p>
</details>
</form>

## 5. Use a Map for Key-to-Value Associations

The service also needs the latest observed delay for each route. A `Map` associates
each key with at most one value:

```java
import java.util.HashMap;
import java.util.Map;

Map<String, Integer> latestDelayByRoute = new HashMap<>();
latestDelayByRoute.put("44", 4);
latestDelayByRoute.put("84", -1);
latestDelayByRoute.put("44", 7);
```

The third `put` associates key `"44"` with `7`, replacing its previous association
with `4`. It does not append another entry for the same key. The expression
`latestDelayByRoute.get("44")` therefore produces `7`.

The first generic argument is the key type; the second is the value type. A map is
not a list whose indices happen to be strings. Its operations express lookup by
keys, key uniqueness, and replacement of an existing association.

Like `HashSet`, `HashMap` provides no iteration-order guarantee. The example prints
the result of a lookup by a specified key rather than printing the whole map and
claiming one observed order.

Running the collections example produced:

```text
observations: 3
distinct routes: 2
contains 44: true
latest delay for 44: 7
```

## 6. Choose the Contract Before the Implementation

The four containers answer different questions:

| Requirement | Suitable abstraction | Relevant guarantee |
|---|---|---|
| Retain four fixed delay values by position | `int[]` | fixed length; indexed components |
| Preserve an observation sequence, including repeats | `List<String>` | ordered sequence; duplicates permitted |
| Track which route identifiers occur | `Set<String>` | no duplicate elements |
| Look up the latest delay by route | `Map<String, Integer>` | at most one value per key |

The choice begins with the required relationship. `ArrayList`, `HashSet`, and
`HashMap` are implementation choices made after the program identifies the list,
set, or map contract it needs.

An implementation also has performance properties, but performance does not repair
a mismatched meaning. A fast set cannot preserve duplicate observations, and a fast
list does not by itself state that route identifiers must be unique.

## 7. Use an Interface to Share an Operation

The service sometimes selects delays by a rule. One rule accepts delays of at least
five minutes; another accepts delays of at most ten. Both can implement one
interface:

```java
interface DelayRule {
    boolean matches(int delayMinutes);
}
```

An **interface** declares operations that implementing classes promise to provide.
It does not select one implementation or create an object.

The first implementation stores a threshold:

```java
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
```

`AtMostDelay` has the same method header but uses `<=`. A variable of type
`DelayRule` may refer to an object of either implementing class:

```java
DelayRule lowerBound = new AtLeastDelay(5);
DelayRule upperBound = new AtMostDelay(10);
```

A call such as `lowerBound.matches(8)` uses the implementation belonging to the
receiver object's class. The interface type states which operation the caller may
request; the object determines how that operation behaves.

## 8. Combine Rules through Composition

A delay is concerning for this example only if it is at least five and at most ten
minutes. A third implementation can hold two rule objects and delegate to both:

```java
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
```

The fields use the interface type, so `BothRules` can combine any two conforming
implementations. It does not need a separate field declaration for every pair of
concrete rule classes.

```java
DelayRule concerning = new BothRules(
    new AtLeastDelay(5),
    new AtMostDelay(10)
);
```

This is **composition**: an object provides its behaviour by holding and using other
objects. No implementation inheritance is needed. Each rule retains one focused
responsibility, while `BothRules` supplies the combination policy.

The complete example applies the composed rule to `List.of(-2, 0, 5, 8, 12)` using
an enhanced loop. It produced:

```text
matching delays: 2
```

<form class="quick-check" data-quick-check data-answer="five-eight">
<fieldset>
<legend>Which values match a rule composed from “at least 5” and “at most 10”?</legend>
<label><input type="radio" name="rule-result" value="five-eight"> <code>5</code> and <code>8</code></label>
<label><input type="radio" name="rule-result" value="eight-twelve"> <code>8</code> and <code>12</code></label>
<label><input type="radio" name="rule-result" value="all-positive"> Every positive value</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>Both component calls must return true. Five and eight lie in the inclusive range; twelve fails the upper-bound rule.</p>
</details>
</form>

## 9. A Common Misconception: One Collection Type Is Enough

All collections hold multiple values, but that common description is too weak to
guide a design. Order, duplication, lookup, replacement, and fixed size are
observable parts of a container's contract.

Using one familiar implementation for every requirement forces clients to recover
missing meaning through conventions. For example, a `List<String>` used as a set
requires every mutating client to remember to check for duplicates. A `Set<String>`
used as an event log silently discards repeated events and may not preserve their
order. Select the abstraction that states the intended relationship.

## 10. Practice by Tracing Containers and Calls

### 1. Repair an array loop

A loop uses `index <= delays.length`. State the first invalid index and the runtime
failure it produces. Give the repaired condition.

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p>The first invalid index is <code>delays.length</code>. Evaluating that access throws <code>ArrayIndexOutOfBoundsException</code>. Use <code>index &lt; delays.length</code>.</p>
</details>

### 2. Trace boxing and iteration

For `List<Integer> values = List.of(2, 4)`, explain the type stored by the list and
the value received by `int value` in an enhanced loop.

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p>The generic list contains references to <code>Integer</code> objects. Boxing converts the literals for storage, and unboxing supplies the primitive values <code>2</code> and <code>4</code> to the loop variable.</p>
</details>

### 3. Choose a collection

Choose a list, set, or map for each requirement: retain every prediction in arrival
order; record which stop identifiers occurred; retrieve the latest prediction for a
given stop identifier. State the contract property that supports each answer.

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p>Use a list for the ordered sequence including repeats, a set for unique identifiers, and a map for lookup from each identifier to its latest prediction.</p>
</details>

### 4. Update a map

A map associates `"44"` with `4`, then with `7`. How many keys does it contain if no
other entries exist, and what does `get("44")` produce?

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p>It contains one key. The second <code>put</code> replaces the value associated with that key, so lookup produces <code>7</code>.</p>
</details>

### 5. Trace interface dispatch

A variable declared as `DelayRule` refers to an `AtMostDelay(10)` object. Which
implementation handles `matches(12)`, and what does it return?

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p>The receiver object has class <code>AtMostDelay</code>, so its implementation handles the call and evaluates <code>12 &lt;= 10</code> as false.</p>
</details>

### 6. Extend by composition

Describe a `NotRule` that accepts one `DelayRule` and reverses its result. Which
field and method would it need? Why does it not need to know the component's concrete
class?

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p><code>NotRule</code> needs one <code>DelayRule</code> field and a <code>matches</code> method that returns <code>!component.matches(delayMinutes)</code>. The interface promises the needed operation for every implementation, so the wrapper depends on that contract rather than a concrete class.</p>
</details>

## Summary

An array stores a fixed number of typed components with indices from zero through
`length - 1`. Indexed loops expose positions; enhanced loops express traversal when
the algorithm needs values but not indices. Java checks array bounds when an access
executes.

Generic collection types state additional relationships. A `List` is an ordered
sequence that permits duplicates, a `Set` contains no duplicate elements, and a
`Map` associates each key with at most one value. `HashSet` and `HashMap` do not
promise an iteration order; unspecified order is not the same claim as random
order.

An interface states an operation shared by several implementations. A call through
the interface uses the implementation of the receiver object's class. Composition
builds behaviour by storing and invoking other interface-typed objects, as
`BothRules` combines two independent delay rules.

Together, the three segments supply the Java mechanisms assumed at the
start of the CPEN 221 core readings: entry points, expressions, methods, control
flow, objects, references, arrays, collections, iteration, and interfaces.

## References

- [The Java Language Specification, Java SE 25, Chapter 10: Arrays](https://docs.oracle.com/javase/specs/jls/se25/html/jls-10.html)
- [Java SE 25 API: `List`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/List.html)
- [Java SE 25 API: `Set`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Set.html)
- [Java SE 25 API: `Map`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Map.html)
- [Java SE 25 API: `HashSet`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/HashSet.html)
- [The Java Language Specification, Java SE 25, Chapter 9: Interfaces](https://docs.oracle.com/javase/specs/jls/se25/html/jls-9.html)
