# Getting Started with CPEN 221 | Segment 2: Objects, State, and References

The platform display and a mobile view both show the prediction for Brock Hall. A
new update reaches the mobile view first. The platform display changes too, even
though the update method was not called through the variable named
`platformDisplay`.

Both variables refer to the same arrival-board object. Updating that object through
either reference changes the one shared state. To predict this behaviour, we need
to distinguish variables, references, and objects rather than describing all three
as “the data”.

By the end, you should be able to:

- distinguish a class declaration, an object, a reference, and a variable;
- construct an object and invoke an instance method;
- explain how constructors establish the initial values of private fields;
- distinguish local variables, parameters, instance fields, and static fields;
- trace aliases using abstract diagram labels rather than invented memory addresses;
- predict the difference between mutating an object and reassigning a variable; and
- explain what `null` means and why dereferencing it fails.

## 1. Construct an Arrival Board

An arrival board has a stop name and a current prediction. The prediction may
change while the stop name remains fixed. This class represents that decision:

```java
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
```

A **class declaration** describes the fields, constructors, and methods available
for objects of that class. The declaration is source code. It is not itself an
arrival board at Brock Hall.

This expression constructs an object:

```java
new ArrivalBoard("Brock Hall", 610)
```

`new` allocates an `ArrivalBoard` object and invokes the constructor whose parameter
types match the arguments. If construction completes normally, the expression
evaluates to a **reference** to that object. Java references identify objects and
arrays within a running program. Java does not expose a source-level numeric address
that we should copy into a diagram.

The Java Virtual Machine Specification describes runtime data areas, but a
source-level reference does not reveal where an object is physically stored. An
implementation may move an object or eliminate an allocation when doing so
preserves the required program behaviour. Our diagrams therefore describe
Java-level reachability and state, not an implementation's memory map.

Most programs retain the reference in a variable:

```java
ArrivalBoard platformDisplay = new ArrivalBoard("Brock Hall", 610);
```

The declaration introduces a variable named `platformDisplay`. Its type permits it
to hold a reference to an `ArrivalBoard` object or the special value `null`. The
object has its own fields. The variable is not another name for either field.

## 2. Use a Constructor to Establish State

A **constructor** initializes a newly allocated object. Its name matches the class
and it has no return type. This constructor receives values through two parameters:

```java
public ArrivalBoard(String stopName, int predictedMinute) {
    if (stopName == null || stopName.isBlank()) {
        throw new IllegalArgumentException("stopName must contain text");
    }
    checkMinute(predictedMinute);
    this.stopName = stopName;
    this.predictedMinute = predictedMinute;
}
```

The parameter and field may have the same spelling. Within
`this.predictedMinute = predictedMinute`, `this.predictedMinute` selects the field
of the new object and the unqualified `predictedMinute` selects the parameter. The
assignment copies the parameter's integer value into the field.

The constructor checks its arguments before storing them. It rejects a missing or
blank stop name and a minute outside the chosen service-day range. These checks keep
an `ArrivalBoard` from completing construction with values that its methods are not
prepared to interpret.

The two fields make different change promises:

- `final String stopName` must be assigned during construction and cannot later be
  reassigned for that object;
- `int predictedMinute` may be assigned again by an instance method.

`final` constrains assignment to the field. It does not make every object reachable
through a final reference deeply immutable. A later reading develops that
distinction; here the referenced `String` is itself immutable.

The constant `MAX_SERVICE_MINUTE` has both `static` and `final`. An **instance
field** such as `predictedMinute` belongs to each constructed `ArrivalBoard` object.
A **static field** belongs to the class rather than to one arrival board. Every
method uses the same named constant, and no method can assign it again after its
initialization.

<form class="quick-check" data-quick-check data-answer="field">
<fieldset>
<legend>In <code>this.predictedMinute = predictedMinute</code>, what does the expression on the left select?</legend>
<label><input type="radio" name="this-selection" value="parameter"> The constructor parameter</label>
<label><input type="radio" name="this-selection" value="field"> The field of the object being initialized</label>
<label><input type="radio" name="this-selection" value="static"> The static constant</label>
<label><input type="radio" name="this-selection" value="local"> A new local variable</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p><code>this</code> refers to the receiver object for the constructor call. The qualified name selects that object's field; the unqualified name on the right selects the parameter.</p>
</details>
</form>

## 3. Call an Instance Method through a Reference

The expression below invokes an instance method:

```java
platformDisplay.message(600)
```

Java first evaluates `platformDisplay` to obtain a reference. The referenced object
becomes the **receiver** of the call. Within `message`, `this` refers to that
receiver, so `this.stopName` and `this.predictedMinute` read its fields.

The argument `600` initializes the parameter `currentMinute`. The method then
declares the local variable `waitMinutes`. These names have different scopes:

- the parameter is in scope throughout the method body;
- the local variable is in scope from its declaration to the end of its block; and
- the instance fields exist as part of the receiver and are selected through
  `this` or another suitable reference.

The call returns a `String`; it does not mutate the board. By contrast,
`updatePrediction` assigns a new value to the receiver's `predictedMinute` field:

```java
public void updatePrediction(int predictedMinute) {
    checkMinute(predictedMinute);
    this.predictedMinute = predictedMinute;
}
```

Its return type is `void`, so a completed call does not produce a result value for
the caller. The relevant observable effect is the changed field.

## 4. Trace Two Aliases

The following program introduces two variables:

```java
ArrivalBoard platformDisplay = new ArrivalBoard("Brock Hall", 610);
ArrivalBoard mobileView = platformDisplay;
```

The first declaration constructs one object and stores its reference. The second
declaration evaluates `platformDisplay` and copies that reference into `mobileView`.
It does not run `new`, invoke a constructor, or copy the object. The variables are
**aliases** because they refer to the same object.

We can record the state with an abstract object label:

```text
platformDisplay ──→ object A
mobileView ───────→ object A

object A: ArrivalBoard
    stopName       = "Brock Hall"
    predictedMinute = 610
```

The label `A` belongs to our diagram. Java did not print it, store it in either
variable, or promise that this object occupies a particular address. The diagram
records only the identity relationships needed for this trace.

Now execute:

```java
System.out.println(platformDisplay.message(600));
mobileView.updatePrediction(614);
System.out.println(platformDisplay.message(600));
```

The observed output was:

```text
Brock Hall: 10 minutes
Brock Hall: 14 minutes
```

The update call uses `mobileView`, but its receiver is object A. The later message
call uses `platformDisplay`, whose reference also reaches object A. Both calls
therefore observe the same `predictedMinute` field.

> **Design principle: trace identity before reasoning about mutable state.**

Names alone do not reveal whether two operations reach one object or two. Draw the
references first, then apply each field update to the selected receiver.

<form class="quick-check" data-quick-check data-answer="fourteen">
<fieldset>
<legend>After <code>mobileView.updatePrediction(614)</code>, what wait does <code>platformDisplay.message(600)</code> report?</legend>
<label><input type="radio" name="alias-result" value="ten"> 10 minutes</label>
<label><input type="radio" name="alias-result" value="fourteen"> 14 minutes</label>
<label><input type="radio" name="alias-result" value="none"> No result because only <code>mobileView</code> changed</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>Both variables refer to object A. The update changes object A's field to 614, so the later call computes <code>614 - 600</code>.</p>
</details>
</form>

## 5. Reassignment Changes a Variable, Not an Object

Aliasing can end when one variable receives a different reference:

```java
ArrivalBoard platformDisplay = new ArrivalBoard("Brock Hall", 610);
ArrivalBoard mobileView = platformDisplay;

mobileView = new ArrivalBoard("UBC Exchange", 625);
mobileView.updatePrediction(628);
```

The second `new` expression constructs object B. The assignment changes
`mobileView` so that it refers to B. It does not modify object A or redirect
`platformDisplay`:

```text
platformDisplay ──→ object A { "Brock Hall", 610 }
mobileView ───────→ object B { "UBC Exchange", 628 }
```

Running the complete reassignment example produced:

```text
Brock Hall: 10 minutes
UBC Exchange: 28 minutes
```

Assignment has the same basic rule for primitive and reference variables: Java
evaluates the right side and copies its value into the variable on the left. For a
reference variable, the copied value is a reference. The assignment does not imply
an object copy.

## 6. Compare Reference Identity Deliberately

The operator `==` compares two reference values for identity. It reports whether
both references select the same object or are both `null`:

```java
ArrivalBoard first = new ArrivalBoard("Brock Hall", 610);
ArrivalBoard alias = first;
ArrivalBoard separate = new ArrivalBoard("Brock Hall", 610);

System.out.println(first == alias);    // true
System.out.println(first == separate); // false
```

`first` and `alias` hold copies of one reference. `separate` holds the reference
produced by a second `new` expression, so it selects a different object even though
the two objects begin with equal-looking field values.

Reference identity answers an object-reachability question; it does not define when
two arrival boards should count as the same abstract value. Java classes can define
a separate value-equality operation through `equals`. Designing that operation
requires a decision about which observable properties matter and how equality
interacts with hashing. The main course readings develop that contract. In this
segment, use `==` only when object identity or `null` is the intended question.

Access control provides another boundary around the object. The fields are
`private`, so ordinary client code cannot assign `board.predictedMinute` directly.
Clients use the public constructor and methods, which apply the range checks before
changing state. Java access control follows classes, packages, modules, and declared
member access; it is not determined by which filesystem directory happens to be
open in an editor.

## 7. Treat `null` as the Absence of an Object Reference

A variable whose type is a class may hold `null`:

```java
ArrivalBoard unavailableBoard = null;
```

`null` is not a hidden arrival board with zero-valued fields. It is the null
reference value and does not refer to an object. Assignment and comparison can use
it, but an instance method call requires a receiver object.

This statement compiles because the variable's declared type has a `message`
method:

```java
unavailableBoard.message(600)
```

When the call ran, Java tried to use the null reference as a receiver and threw
`NullPointerException`. This is a runtime failure. The compiler knows the variable's
declared type; it does not generally prove that every reference expression is
non-null at every possible execution point.

<form class="quick-check" data-quick-check data-answer="runtime">
<fieldset>
<legend>How should we classify a call to <code>unavailableBoard.message(600)</code> when the variable holds <code>null</code>?</legend>
<label><input type="radio" name="null-category" value="compilation"> Compilation failure</label>
<label><input type="radio" name="null-category" value="runtime"> Runtime failure</label>
<label><input type="radio" name="null-category" value="zero"> A successful call that uses zero-valued fields</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>The source type-checks, but no receiver object exists when the call executes. Java throws <code>NullPointerException</code>.</p>
</details>
</form>

## 8. A Common Misconception: Each Variable Has Its Own Object

A class-typed variable does not automatically contain a complete independent object.
It contains a reference value or `null`. `new` constructs an object; a later plain
assignment copies the resulting reference.

This is why counting variables does not count objects. The alias example has two
variables and one `ArrivalBoard` object. The reassignment example has two variables
and two `ArrivalBoard` objects after the second construction. String literals and
other library objects may also exist, so a statement about the total number of
objects should name the class or objects being counted.

## 9. Practice by Updating the Diagram

### 1. Trace construction

After `new ArrivalBoard("Wesbrook Mall", 645)` completes, list the constructor
parameters and the two instance-field values. Which variable or field uses the
class-wide constant?

<details class="practice-explanation">
<summary>Compare with the trace</summary>
<p>The parameters initially hold <code>"Wesbrook Mall"</code> and <code>645</code>. The constructor stores those values in <code>stopName</code> and <code>predictedMinute</code>. <code>MAX_SERVICE_MINUTE</code> is a static field read by <code>checkMinute</code>; it is not copied into each board.</p>
</details>

### 2. Predict an alias update

Variables `first`, `second`, and `third` all receive the same reference. The program
calls `third.updatePrediction(700)`. Which prediction does a call through `first`
observe? Explain without referring to the variable names as separate boards.

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p>All three references select the same receiver object. The update assigns <code>700</code> to that object's field, so a later call through <code>first</code> observes 700.</p>
</details>

### 3. Separate mutation from reassignment

Explain the different effects of these statements:

```java
second.updatePrediction(700);
second = new ArrivalBoard("Waterfront", 720);
```

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p>The method call mutates the object currently selected by <code>second</code>. The assignment constructs another object and changes only which reference <code>second</code> holds. Other aliases continue to refer to the earlier object.</p>
</details>

### 4. Find the scopes

In `message`, identify the parameter, local variable, instance fields, and static
field. State where the parameter and local variable become available.

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p><code>currentMinute</code> is a parameter in scope throughout the method body. <code>waitMinutes</code> is a local variable in scope from its declaration to the end of the block. <code>stopName</code> and <code>predictedMinute</code> are instance fields selected from the receiver. <code>MAX_SERVICE_MINUTE</code> is static and belongs to the class.</p>
</details>

### 5. Diagnose invalid construction

Predict what happens when client code evaluates
`new ArrivalBoard("", 610)`. At which stage does the failure occur, and does the
caller receive a reference to a completed `ArrivalBoard` object?

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p>The source compiles. During construction, the blank-name check throws <code>IllegalArgumentException</code>. Construction does not complete normally, so the expression does not return a reference to a completed board.</p>
</details>

## Summary

A class declaration describes a type of object. `new` allocates an object, invokes
a constructor, and—when construction completes—produces a reference. A variable of
a class type holds such a reference or `null`; it does not automatically contain an
independent object.

Constructors establish initial field values. Instance fields belong to each object,
while static fields belong to the class. Instance methods use a receiver, available
as `this`, and can read or update that receiver's fields.

Assignment copies a value. Copying a reference creates an alias, so mutations
through either alias reach the same object. Reassigning one variable changes that
variable's reference without redirecting other aliases. A diagram should use
abstract object identities and should not claim to reveal physical addresses or an
implementation's allocation strategy.

The next segment uses these object and reference rules while iterating through
arrays and collections and selecting behaviour through interfaces.

## References

- [The Java Language Specification, Java SE 25, Chapter 4: Types, Values, and Variables](https://docs.oracle.com/javase/specs/jls/se25/html/jls-4.html)
- [The Java Language Specification, Java SE 25, Section 8.3: Field Declarations](https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html#jls-8.3)
- [The Java Language Specification, Java SE 25, Section 15.9: Class Instance Creation Expressions](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.9)
- [The Java Virtual Machine Specification, Java SE 25, Section 2.7: Representation of Objects](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-2.html#jvms-2.7)
