# Getting Started with CPEN 221 | Segment 1: Running Java Programs

The arrival display says that the next bus will arrive in −3 minutes.

The program subtracted the scheduled minute from the predicted minute and printed
the result. Its arithmetic answered one question: the prediction is three minutes
before the schedule. The display treated that result as a waiting time, so correct
arithmetic produced the wrong message.

We will repair this display while learning how a small Java program starts, how it
evaluates expressions, how values move into methods, and how control flow selects a
result. The same mechanisms appear in the larger Gradle project in Chapter 1.

By the end, you should be able to:

- run a Java 25 compact source file and identify where its execution begins;
- trace expressions, local variables, assignments, and method calls;
- use `int`, `boolean`, and `String` values without treating their types as
  interchangeable;
- predict the branch selected by an `if` statement;
- distinguish a compilation failure, a runtime failure, and an unwanted result; and
- translate a compact source example into the explicit class-and-`static` form used
  in course projects.

## 1. Begin with an Observable Program

This complete file records a scheduled arrival at minute 600 and a prediction at
minute 597. These values could denote 10:00 and 9:57 on one service day.

```java
void main() {
    int scheduledMinute = 600;
    int predictedMinute = 597;
    int difference = predictedMinute - scheduledMinute;

    System.out.println("Arrival in " + difference + " minutes");
}
```

Save the file as `RawDifference.java`. With Java 25 installed, run it from the
directory containing the file:

```bash
java RawDifference.java
```

The observed output was:

```text
Arrival in -3 minutes
```

`RawDifference.java` is a **source file**: text that follows Java's grammatical and
typing rules. The `java` launcher compiles this source and starts the program. In
this compact source file, execution begins with the first statement inside
`void main()`. The three declarations above `System.out.println` run in order.

Java 25 permits this compact form so that a small program does not need an explicit
class declaration. The form is part of the Java language, not a special operation
performed by the readings website. We will use it briefly while the program fits in
one file, then show the explicit form used in course projects.

The output also gives us a concrete failure to repair. The value `-3` is meaningful
inside the calculation, but the phrase `Arrival in -3 minutes` does not communicate
that the vehicle is early. We need the program to interpret the sign before it
prints a message.

## 2. Trace Values Before Changing the Program

Consider the first declaration:

```java
int scheduledMinute = 600;
```

The declaration introduces a local variable named `scheduledMinute`. Its declared
type is `int`, Java's 32-bit signed integer type, and its initial value is `600`.
A **local variable** is a name available within the method or block that declares
it. The declaration does not create a field on an object.

The third declaration contains more work:

```java
int difference = predictedMinute - scheduledMinute;
```

Java evaluates the expression on the right of `=` first. It reads `597` through
`predictedMinute`, reads `600` through `scheduledMinute`, and applies integer
subtraction. The expression evaluates to `-3`. Java then assigns that value to the
new variable `difference`.

A trace records the state after each declaration:

| Statement just completed | `scheduledMinute` | `predictedMinute` | `difference` |
|---|---:|---:|---:|
| `int scheduledMinute = 600;` | 600 | not declared | not declared |
| `int predictedMinute = 597;` | 600 | 597 | not declared |
| `int difference = predictedMinute - scheduledMinute;` | 600 | 597 | −3 |

“Not declared” differs from zero. Before a local variable's declaration, that name
does not denote a variable in this method. Java does not execute the whole file and
fill every future variable with a convenient default.

The print statement combines a `String` with an `int`:

```java
System.out.println("Arrival in " + difference + " minutes");
```

A `String` represents a sequence of UTF-16 code units used as text. When either
operand of `+` is a `String`, Java performs string concatenation for that operation.
It produces the text `"Arrival in -3"`, then concatenates `" minutes"`. This rule
does not make `String` and `int` interchangeable. For example, Java rejects this
declaration:

```java
int predictedMinute = "597"; // deliberately invalid: String is not int
```

The characters `5`, `9`, and `7` can appear in a string, but the string is not an
integer value. A later program may parse input text into an integer; that conversion
is an operation that can fail, not an automatic change of type.

<form class="quick-check" data-quick-check data-answer="minus-three">
<fieldset>
<legend>After the three declarations in <code>RawDifference.java</code>, which value does <code>difference</code> hold?</legend>
<label><input type="radio" name="difference-value" value="three"> <code>3</code></label>
<label><input type="radio" name="difference-value" value="minus-three"> <code>-3</code></label>
<label><input type="radio" name="difference-value" value="string"> <code>"-3"</code></label>
<label><input type="radio" name="difference-value" value="undeclared"> It has not been declared.</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>Java evaluates <code>597 - 600</code> using integer subtraction and assigns the integer value <code>-3</code> to <code>difference</code>. Concatenation converts that value to text only when the print expression is evaluated.</p>
</details>
</form>

## 3. Give the Interpretation a Method

The original program mixes two responsibilities. It calculates a difference and
decides how that difference should be described. We will move the interpretation
into a method named `arrivalMessage`:

```java
String arrivalMessage(int scheduledMinute, int predictedMinute) {
    int difference = predictedMinute - scheduledMinute;
    if (difference < 0) {
        return "EARLY by " + -difference + " minutes";
    }
    if (difference > 0) {
        return "LATE by " + difference + " minutes";
    }
    return "ON TIME";
}
```

The first line is the method's **header**. It states four facts:

- the method's name is `arrivalMessage`;
- a caller must supply two arguments;
- each corresponding parameter has type `int`; and
- a completed call produces a `String` value.

The variables `scheduledMinute` and `predictedMinute` in the header are
**parameters**. When a caller evaluates
`arrivalMessage(600, 597)`, Java assigns the argument values `600` and `597` to
those parameters for that call. The method then calculates its own local
`difference`.

For this example, both arguments must be service-day minute values from 0 through
1800. That assumption keeps the values meaningful and ensures that the subtraction
and negation fit in an `int`. The Java type `int` alone does not express this range;
we will learn to state such requirements more systematically in Chapter 2.

Each `return` finishes the current call and supplies its expression's value to the
caller. A call with arguments `600` and `597` returns the string
`"EARLY by 3 minutes"`. The method does not print that string. Its caller decides
whether to print, store, test, or otherwise use the returned value.

## 4. Select One Result with Control Flow

The expression `difference < 0` evaluates to a `boolean`: either `true` or `false`.
An `if` statement executes its body only when its condition evaluates to `true`.

Trace the call `arrivalMessage(600, 597)`:

1. The subtraction assigns `-3` to `difference`.
2. `difference < 0` evaluates to `true`.
3. The first body evaluates `-difference` as `3` and constructs the early message.
4. `return` finishes the call. Java does not evaluate the second `if` or the final
   `return` during this call.

Now trace `arrivalMessage(600, 607)`:

1. `difference` receives `7`.
2. `difference < 0` is `false`, so Java skips the first body.
3. `difference > 0` is `true`, so the method returns `"LATE by 7 minutes"`.

When both arguments are `600`, both comparisons are false. Execution reaches the
remaining return and produces `"ON TIME"`. The zero case is a boundary: changing
either comparison to include equality would assign it to a different category.

<form class="quick-check" data-quick-check data-answer="on-time">
<fieldset>
<legend>What does <code>arrivalMessage(600, 600)</code> return?</legend>
<label><input type="radio" name="boundary-result" value="early"> <code>"EARLY by 0 minutes"</code></label>
<label><input type="radio" name="boundary-result" value="on-time"> <code>"ON TIME"</code></label>
<label><input type="radio" name="boundary-result" value="late"> <code>"LATE by 0 minutes"</code></label>
<label><input type="radio" name="boundary-result" value="nothing"> No value; neither <code>if</code> body runs.</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>Both strict comparisons are false when <code>difference</code> is zero. Execution continues to the final <code>return</code>, which produces <code>"ON TIME"</code>.</p>
</details>
</form>

The complete compact program now calls the method and prints its result:

```java
void main() {
    int scheduledMinute = 600;
    int predictedMinute = 597;
    String message = arrivalMessage(scheduledMinute, predictedMinute);

    System.out.println(message);
}

String arrivalMessage(int scheduledMinute, int predictedMinute) {
    // Both arguments are service-day minute values from 0 through 1800.
    int difference = predictedMinute - scheduledMinute;
    if (difference < 0) {
        return "EARLY by " + -difference + " minutes";
    }
    if (difference > 0) {
        return "LATE by " + difference + " minutes";
    }
    return "ON TIME";
}
```

Running `java ArrivalDisplay.java` produced:

```text
EARLY by 3 minutes
```

> **Design principle: separate a calculation from the decision about how its result
> should be interpreted.**

The method name gives the interpretation a place in the program. The caller no
longer needs to reconstruct the sign convention or duplicate its branches.

## 5. Classify Failures Before Repairing Them

Java programs can fail at different stages. The stage determines what evidence is
available and what to inspect next.

A **compilation failure** occurs when the source violates a grammatical or static
typing rule. Assigning `"597"` to an `int` variable belongs in this category. The
program does not begin running.

A **runtime failure** occurs after compilation and launch. This statement compiles
because `Integer.parseInt` accepts a `String` and has return type `int`:

```java
int predictedMinute = Integer.parseInt("soon");
```

When it ran, `Integer.parseInt` could not interpret `"soon"` as an integer and
threw `NumberFormatException`. The exception type is more important here than the
exact wording and line formatting of one `java` implementation's diagnostic.

An **unwanted result** occurs when the program runs to completion but does not meet
its requirement. `RawDifference.java` belongs in this category. The output follows
Java's rules; the message is unsuitable for the arrival display.

<form class="quick-check" data-quick-check data-answer="compilation">
<fieldset>
<legend>How should we first classify <code>int predictedMinute = "597";</code>?</legend>
<label><input type="radio" name="failure-category" value="compilation"> Compilation failure</label>
<label><input type="radio" name="failure-category" value="runtime"> Runtime failure</label>
<label><input type="radio" name="failure-category" value="unwanted"> Unwanted result after successful execution</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>The declared variable requires an <code>int</code>, while the expression has type <code>String</code>. The compiler rejects the assignment before the program starts.</p>
</details>
</form>

This classification is more durable than memorising an exact compiler message.
Diagnostic wording can change across JDK releases. The relevant Java rule is that a
`String` value cannot be assigned to an `int` variable without an explicit
conversion that produces an integer.

## 6. Move from a Small File to a Course Project

Compact source files reduce ceremony while we learn the first mechanisms. Ordinary
course projects use named classes, packages, and a build tool. Here is the same
program in an explicit class:

```java
public final class ArrivalDisplayExpanded {
    private ArrivalDisplayExpanded() { }

    public static void main(String[] args) {
        int scheduledMinute = 600;
        int predictedMinute = 597;
        String message = arrivalMessage(scheduledMinute, predictedMinute);

        System.out.println(message);
    }

    static String arrivalMessage(int scheduledMinute, int predictedMinute) {
        // Both arguments are service-day minute values from 0 through 1800.
        int difference = predictedMinute - scheduledMinute;
        if (difference < 0) {
            return "EARLY by " + -difference + " minutes";
        }
        if (difference > 0) {
            return "LATE by " + difference + " minutes";
        }
        return "ON TIME";
    }
}
```

The explicit version adds structure around the same control flow:

- `ArrivalDisplayExpanded` names the class that groups the two methods. A public
  class and its source file use the same name.
- `static` states that a method belongs to the class and does not require a receiver
  object. The next segment distinguishes static methods from instance methods.
- `String[] args` receives command-line arguments. This program does not use them.
- `final` prevents another class from extending this utility class.
- The private constructor prevents ordinary client code from constructing an
  `ArrivalDisplayExpanded` object when the class contains only static operations.

Java 25 does not require every program to use this particular `main` header. It
accepts the compact `void main()` shown earlier and other candidate main methods.
CPEN 221 projects use the explicit `public static void main(String[] args)` form
when they need a command-line entry point because it states the class and arguments
explicitly and works naturally with the project build.

Compiling with `javac -Xlint:all ArrivalDisplayExpanded.java` and then running
`java ArrivalDisplayExpanded` produced the same line as the compact program:

```text
EARLY by 3 minutes
```

## 7. A Common Misconception: Execution Starts at the Top

A Java source file is not executed from its first character to its last. Class and
method declarations describe program structure. The launcher selects a candidate
`main` method and begins with that method's body. Other method bodies run only when
a call reaches them.

In `ArrivalDisplay.java`, Java does not execute `arrivalMessage` merely because its
declaration appears in the file. `main` calls it with two argument values. The call
transfers control into the method, and `return` transfers a value and control back
to the caller.

This distinction becomes important as programs acquire more files and classes. Text
position helps a reader navigate source; calls and control-flow statements determine
the execution order.

## 8. Practice by Predicting and Explaining

Answer each question before running or editing the program.

### 1. Complete a trace

For `arrivalMessage(720, 725)`, record the values of both parameters and
`difference`. State which comparisons Java evaluates and which `return` finishes
the call.

<details class="practice-explanation">
<summary>Compare with the trace</summary>
<p>The parameters receive <code>720</code> and <code>725</code>. The subtraction assigns <code>5</code> to <code>difference</code>. The first comparison is false; the second is true. The second body returns <code>"LATE by 5 minutes"</code>.</p>
</details>

### 2. Repair a boundary

A revision changes the first condition to `difference <= 0`. Predict the result of
`arrivalMessage(600, 600)`. Identify the smallest repair and explain why a test only
using early and late predictions would not expose this error.

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p>The revised method returns <code>"EARLY by 0 minutes"</code>. Restore the strict comparison <code>difference &lt; 0</code>. Tests using only negative and positive differences do not exercise the zero boundary, so both can pass while the on-time case remains wrong.</p>
</details>

### 3. Separate type from text

Explain why `"597" + 3` produces `"5973"` while `597 + 3` produces `600`. Name the
type of each result.

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p>The first left operand is a <code>String</code>, so <code>+</code> performs concatenation and produces another <code>String</code>. Both operands in the second expression are <code>int</code> values, so Java performs integer addition and produces an <code>int</code>.</p>
</details>

### 4. Classify three observations

Classify each as a compilation failure, runtime failure, or unwanted result:

- the source omits the closing brace of `main`;
- `Integer.parseInt("soon")` throws `NumberFormatException`; and
- the display prints `Arrival in -3 minutes` and exits normally.

For each classification, state what happened rather than copying a diagnostic.

<details class="practice-explanation">
<summary>Compare with the classifications</summary>
<p>The missing brace is a compilation failure because the source does not satisfy Java's grammar. The exception is a runtime failure because parsing begins after successful compilation. The negative message is an unwanted result because execution finishes but the output does not meet the display requirement.</p>
</details>

### 5. Explain the two program forms

Name one feature shared by the compact and explicit arrival-display programs and
one structural difference. Does the explicit form make the classification logic
more correct?

<details class="practice-explanation">
<summary>Compare with the explanation</summary>
<p>Both programs begin in a candidate <code>main</code>, call <code>arrivalMessage</code>, and use the same branches. The explicit form declares a named class and static methods; the compact form uses an implicitly declared class and instance methods. The wrapper does not change the classification logic or make it more correct.</p>
</details>

## Summary

A Java program begins at a selected `main` method, not at the first line of its
source file. Statements in the method evaluate expressions, introduce local
variables, assign values, call other methods, and select branches.

Types constrain those operations. An `int` value and a `String` containing digits
are not interchangeable. A method header states the types of its parameters and
returned value, while `return` finishes one call with a result.

Compilation failures, runtime failures, and unwanted results provide different
evidence. Classify the stage before choosing a repair. The arrival display ran
successfully but interpreted a signed difference incorrectly; the repaired method
maps negative, zero, and positive differences to messages explicitly.

Compact source files give small Java 25 programs a direct entry point. The explicit
class-and-`static` form adds the structure used by larger projects without changing
the underlying expressions and control flow. The next segment introduces objects,
instance methods, state, and references.

## References

- [Java SE 25: Compact Source Files and Instance `main` Methods](https://docs.oracle.com/en/java/javase/25/language/compact-source-files-instance-main-methods.html)
- [The Java Language Specification, Java SE 25, Chapter 4: Types, Values, and Variables](https://docs.oracle.com/javase/specs/jls/se25/html/jls-4.html)
- [The Java Language Specification, Java SE 25, Chapter 14: Blocks, Statements, and Patterns](https://docs.oracle.com/javase/specs/jls/se25/html/jls-14.html)
