# -*- coding: utf-8 -*-
"""
Gilded Rose — refactored to SOLID principles.

Design:
  ItemUpdater (ABC)            ← abstraction (DIP)
  ├── NormalItemUpdater        ← SRP: only knows normal-item rules
  ├── AgedBrieUpdater          ← SRP
  ├── SulfurasUpdater          ← SRP
  └── BackstagePassUpdater     ← SRP

  GildedRose                  ← depends on ItemUpdater, not on concretions (DIP)
      _registry: dict[str, ItemUpdater]
      update_quality() delegates to the right updater (OCP: add new type → add new class)

Adding a new item type never requires modifying existing classes (Open/Closed Principle).
"""
from abc import ABC, abstractmethod

# ---------------------------------------------------------------------------
# Item name constants
# ---------------------------------------------------------------------------
AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"
CONJURED       = "Conjured Mana Cake"

_MIN_QUALITY = 0
_MAX_QUALITY = 50


def _clamp(value: int) -> int:
    """Keep quality within [0, 50]."""
    return max(_MIN_QUALITY, min(_MAX_QUALITY, value))


# ---------------------------------------------------------------------------
# Item — unchanged per kata rules
# ---------------------------------------------------------------------------
class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


# ---------------------------------------------------------------------------
# Abstraction (Dependency Inversion Principle)
# ---------------------------------------------------------------------------
class ItemUpdater(ABC):
    """Strategy interface: one implementation per item behaviour."""

    @abstractmethod
    def update(self, item: Item) -> None:
        """Mutate *item* for one day."""

    # Shared helpers available to all concrete updaters
    @staticmethod
    def _decrease_sell_in(item: Item) -> None:
        item.sell_in -= 1

    @staticmethod
    def _raise_quality(item: Item, amount: int = 1) -> None:
        item.quality = _clamp(item.quality + amount)

    @staticmethod
    def _lower_quality(item: Item, amount: int = 1) -> None:
        item.quality = _clamp(item.quality - amount)

    def _is_expired(self, item: Item) -> bool:
        return item.sell_in < 0


# ---------------------------------------------------------------------------
# Concrete updaters (Single Responsibility Principle)
# ---------------------------------------------------------------------------
class NormalItemUpdater(ItemUpdater):
    """
    Normal items:
      - quality -1 each day, -2 after sell date.
      - quality never below 0.
    """

    def update(self, item: Item) -> None:
        self._decrease_sell_in(item)
        degradation = 2 if self._is_expired(item) else 1
        self._lower_quality(item, degradation)


class AgedBrieUpdater(ItemUpdater):
    """
    Aged Brie:
      - quality +1 each day, +2 after sell date.
      - quality never above 50.
    """

    def update(self, item: Item) -> None:
        self._decrease_sell_in(item)
        appreciation = 2 if self._is_expired(item) else 1
        self._raise_quality(item, appreciation)


class SulfurasUpdater(ItemUpdater):
    """
    Sulfuras, Hand of Ragnaros:
      - legendary item; never sold, never changes.
    """

    def update(self, item: Item) -> None:
        pass  # immutable — intentionally empty


class BackstagePassUpdater(ItemUpdater):
    """
    Backstage passes to a TAFKAL80ETC concert:
      - quality +1 when sell_in > 10
      - quality +2 when sell_in in [6, 10]
      - quality +3 when sell_in in [1, 5]
      - quality drops to 0 after the concert (sell_in <= 0 before decrement)
    """

    def update(self, item: Item) -> None:
        self._decrease_sell_in(item)
        if self._is_expired(item):
            item.quality = 0
            return
        if item.sell_in < 5:
            self._raise_quality(item, 3)
        elif item.sell_in < 10:
            self._raise_quality(item, 2)
        else:
            self._raise_quality(item, 1)


class ConjuredItemUpdater(ItemUpdater):
    """
    Conjured items:
      - quality -2 each day, -4 after sell date.
      - quality never below 0.
    """

    def update(self, item: Item) -> None:
        self._decrease_sell_in(item)
        degradation = 4 if self._is_expired(item) else 2
        self._lower_quality(item, degradation)


# ---------------------------------------------------------------------------
# GildedRose — depends on abstractions, not concretions (DIP + OCP)
# ---------------------------------------------------------------------------
class GildedRose:
    """
    Orchestrator.  Delegates all update logic to the appropriate ItemUpdater.
    To support a new item type: create a new ItemUpdater subclass and add it
    to the registry — zero changes to existing classes.
    """

    _registry: dict[str, ItemUpdater] = {
        AGED_BRIE:       AgedBrieUpdater(),
        SULFURAS:        SulfurasUpdater(),
        BACKSTAGE_PASS:  BackstagePassUpdater(),
        CONJURED:        ConjuredItemUpdater(),
    }
    _default_updater: ItemUpdater = NormalItemUpdater()

    def __init__(self, items):
        self.items = items

    def update_quality(self) -> None:
        for item in self.items:
            updater = self._registry.get(item.name, self._default_updater)
            updater.update(item)
