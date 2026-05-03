# -*- coding: utf-8 -*-
"""
Characterization tests for GildedRose.

These tests document the *current* behaviour of the legacy code so that
any future refactoring that accidentally changes the externally-visible
behaviour is caught immediately.  They are NOT specification tests — they
describe what the code does, not what it ideally should do.
"""
import pytest
from gilded_rose import Item, GildedRose


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def update(item: Item) -> Item:
    """Convenience: run one update cycle and return the item."""
    GildedRose([item]).update_quality()
    return item


# ===========================================================================
# Normal Items  (5 tests)
# ===========================================================================

class TestNormalItem:
    """Quality decreases before/after sell date; never drops below 0."""

    @pytest.mark.parametrize("sell_in, quality, expected_quality, expected_sell_in", [
        (10,  20, 19,  9),   # before sell date: -1
        ( 0,  20, 18, -1),   # on sell date → expires after decrement: -2
        (-1,  10,  8, -2),   # already expired: -2
        ( 5,   0,  0,  4),   # floor before sell date
        ( 0,   1,  0, -1),   # floor after sell date
    ])
    def test_normal_item(self, sell_in, quality, expected_quality, expected_sell_in):
        item = update(Item("Normal Item", sell_in=sell_in, quality=quality))
        assert item.quality == expected_quality
        assert item.sell_in == expected_sell_in


# ===========================================================================
# Aged Brie  (5 tests)
# ===========================================================================

class TestAgedBrie:
    """Quality increases over time; capped at 50."""

    @pytest.mark.parametrize("sell_in, quality, expected_quality", [
        ( 5, 10, 11),   # before sell date: +1
        ( 1, 50, 50),   # already at cap
        ( 0, 10, 12),   # after sell date: +2
        ( 0, 49, 50),   # +2 but capped at 50
    ])
    def test_aged_brie_quality(self, sell_in, quality, expected_quality):
        item = update(Item("Aged Brie", sell_in=sell_in, quality=quality))
        assert item.quality == expected_quality

    def test_aged_brie_sell_in_decreases(self):
        item = update(Item("Aged Brie", sell_in=5, quality=10))
        assert item.sell_in == 4


# ===========================================================================
# Sulfuras, Hand of Ragnaros  (2 tests)
# ===========================================================================

class TestSulfuras:
    """Legendary item: sell_in and quality never change."""

    @pytest.mark.parametrize("sell_in, quality", [
        ( 0, 80),
        (10, 80),
    ])
    def test_sulfuras_is_immutable(self, sell_in, quality):
        item = update(Item("Sulfuras, Hand of Ragnaros",
                           sell_in=sell_in, quality=quality))
        assert item.quality == quality
        assert item.sell_in == sell_in


# ===========================================================================
# Backstage passes to a TAFKAL80ETC concert  (8 tests)
# ===========================================================================

class TestBackstagePasses:
    """Quality increases with a multiplier based on days remaining;
    drops to 0 the day after the concert."""

    @pytest.mark.parametrize("sell_in, quality, expected_quality", [
        (15, 20, 21),   # > 10 days: +1
        (10, 20, 22),   # exactly 10 days: +2
        ( 5, 20, 23),   # exactly 5 days: +3
        ( 1, 20, 23),   # 1 day left: +3
        ( 0, 20,  0),   # concert day → 0
        (-1, 20,  0),   # past concert → 0
        (10, 49, 50),   # +2 but capped at 50
    ])
    def test_backstage_pass_quality(self, sell_in, quality, expected_quality):
        item = update(Item("Backstage passes to a TAFKAL80ETC concert",
                           sell_in=sell_in, quality=quality))
        assert item.quality == expected_quality, (
            f"sell_in={sell_in}, quality={quality} → expected {expected_quality}")

    def test_backstage_pass_sell_in_decreases(self):
        item = update(Item("Backstage passes to a TAFKAL80ETC concert",
                           sell_in=10, quality=20))
        assert item.sell_in == 9


# ===========================================================================
# Conjured items  (4 tests)
# ===========================================================================

class TestConjuredItem:
    """Conjured items degrade twice as fast as normal items."""

    CONJURED = "Conjured Mana Cake"

    @pytest.mark.parametrize("sell_in, quality, expected_quality", [
        (10, 20, 18),   # before sell date: -2
        ( 0, 20, 16),   # after sell date: -4
        ( 5,  1,  0),   # floor before sell date
    ])
    def test_conjured_quality(self, sell_in, quality, expected_quality):
        item = update(Item(self.CONJURED, sell_in=sell_in, quality=quality))
        assert item.quality == expected_quality, (
            f"sell_in={sell_in}, quality={quality} → expected {expected_quality}")

    def test_conjured_sell_in_decreases(self):
        item = update(Item(self.CONJURED, sell_in=5, quality=10))
        assert item.sell_in == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
