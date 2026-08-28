"""
Battle System - A text-based turn-based combat simulator

Demonstrates core Python OOP concepts:
- Abstract base classes (ABC)
- Inheritance and polymorphism
- Method overriding
- Shared helper methods
- Custom dunder methods (__eq__, __lt__, __str__)
- Conditional behavior with hasattr()
- Context managers (__enter__/__exit__)
- File I/O for logging
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Player(ABC):
    """Abstract base class for all fighters. Cannot be instantiated directly."""

    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def __str__(self):
        return f"{self.name} - {self.hp} HP"

    def __eq__(self, other):
        return self.name == other.name and self.hp == other.hp

    def __lt__(self, other):
        return self.hp < other.hp

    def check_defeated(self, target):
        if target.hp <= 0:
            print(f"{target.name} has been defeated!")

    @abstractmethod
    def attack(self, target, damage=10):
        """Every subclass must implement its own attack behavior."""
        pass


class Archer(Player):
    """Deals ranged damage. Damage is reduced if the target can block."""

    def attack(self, target, damage=15):
        if hasattr(target, "block"):
            damage = target.block(damage)
        target.hp -= damage
        print(f"{self.name} shoots {target.name} for {damage} damage!")
        self.check_defeated(target)


class Warrior(Player):
    """Melee fighter with armor that reduces incoming damage."""

    def __init__(self, name, hp, armor):
        super().__init__(name, hp)
        self.armor = armor

    def block(self, damage):
        reduced_damage = damage - self.armor
        if reduced_damage < 0:
            reduced_damage = 0
        return reduced_damage

    def attack(self, target, damage=20):
        target.hp -= damage
        print(f"{self.name} swings a sword at {target.name} for {damage} damage!")
        self.check_defeated(target)


def hp_bar(current_hp, max_hp, length=20):
    """Builds a text-based visual HP bar, e.g. [██████░░░░] 30/50"""
    filled = int((current_hp / max_hp) * length)
    empty = length - filled
    bar = "#" * filled + "-" * empty
    return f"[{bar}] {current_hp}/{max_hp}"


def battle(player1, player2):
    """Runs a full turn-based battle between two Player objects until one is defeated."""
    round_num = 1
    while player1.hp > 0 and player2.hp > 0:
        print(f"\n--- Round {round_num} ---")
        player1.attack(player2)
        if player2.hp <= 0:
            break
        player2.attack(player1)
        round_num += 1

    print("\nBattle over!")
    if player1.hp <= 0:
        print(f"{player2.name} wins!")
    else:
        print(f"{player1.name} wins!")


class BattleSession:
    """Context manager that logs a battle session to a text file,
    with a timestamp and graceful handling of any errors during the battle."""

    def __enter__(self):
        self.log = []
        self.start_time = datetime.now()
        print(f"Battle log starting at {self.start_time.strftime('%H:%M:%S')}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is not None:
            self.log.append(f"Something went wrong: {exc_value}")

        with open("battle_log.txt", "w") as f:
            for line in self.log:
                f.write(line + "\n")

        duration = datetime.now() - self.start_time
        print(f"Battle log saved! (session lasted {duration})")
        return True  # suppress any exception so the program keeps running


if __name__ == "__main__":
    # --- Demo 1: HP bars ---
    print(hp_bar(50, 50))
    print(hp_bar(25, 50))
    print(hp_bar(5, 50))

    # --- Demo 2: Full battle ---
    gandalf = Warrior("Gandalf", 50, 5)
    merlin = Archer("Merlin", 60)
    battle(gandalf, merlin)

    # --- Demo 3: Custom comparisons ---
    p1 = Archer("Merlin", 60)
    p2 = Archer("Merlin", 60)
    p3 = Archer("Thorin", 40)
    print(f"\np1 == p2: {p1 == p2}")   # True, same name and hp
    print(f"p1 == p3: {p1 == p3}")     # False
    print(f"p3 < p1: {p3 < p1}")       # True, 40 < 60

    # --- Demo 4: Logged battle session with a simulated error ---
    with BattleSession() as session:
        session.log.append("Merlin attacks Gandalf for 15 damage")
        session.log.append("Gandalf attacks Merlin for 20 damage")
        raise Exception("Gandalf's hp went unexpectedly negative")
