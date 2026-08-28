# Battle System

A text-based, turn-based combat simulator built in Python, created as a hands-on
project while learning object-oriented programming.

## What it does

Two fighters — an `Archer` and a `Warrior` — take turns attacking each other
until one is defeated. The `Warrior` has armor that reduces incoming damage;
the `Archer` deals more raw damage but has no defense. Every battle is logged
to a file, including a timestamp and graceful handling of any errors.

## Concepts demonstrated

- **Abstract base classes** — `Player` uses `ABC` and `@abstractmethod` to force
  every subclass to implement its own `attack()` method
- **Inheritance & polymorphism** — `Archer` and `Warrior` both inherit from
  `Player` but attack in completely different ways
- **Shared helper methods** — `check_defeated()` lives once on `Player` and is
  reused by every subclass
- **Conditional behavior** — `hasattr(target, "block")` lets `Archer.attack()`
  work correctly whether or not the target can block, without knowing its
  exact class
- **Custom dunder methods** — `__str__`, `__eq__`, and `__lt__` let `Player`
  objects be printed, compared, and sorted naturally
- **Context managers** — `BattleSession` uses `__enter__`/`__exit__` to log
  every battle to a file and gracefully handle errors without crashing
- **File I/O & datetime** — battle logs are timestamped and saved to
  `battle_log.txt`

## Sample output

```
[##########] 50/50
[#####-----] 25/50
[#---------] 5/50

--- Round 1 ---
Gandalf swings a sword at Merlin for 20 damage!
Merlin shoots Gandalf for 10 damage!

--- Round 2 ---
Gandalf swings a sword at Merlin for 20 damage!
Merlin shoots Gandalf for 10 damage!

--- Round 3 ---
Gandalf swings a sword at Merlin for 20 damage!
Merlin has been defeated!

Battle over!
Gandalf wins!

p1 == p2: True
p1 == p3: False
p3 < p1: True

Battle log starting at 05:12:33
Battle log saved! (session lasted 0:00:00.001234)
```

## Running it

```
python battle_system.py
```

No dependencies beyond the Python standard library.

## About

Built while working through Python OOP fundamentals — inheritance, abstract
classes, dunder methods, and context managers — as a small project to tie the
concepts together into something real rather than isolated examples.
