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
# Normal Items
# ===========================================================================

class TestNormalItem:
    """Quality decreases before/after sell date; never drops below 0."""

    @pytest.mark.parametrize("sell_in, quality, expected_quality, expected_sell_in", [
        # Before sell date: quality -1
        (10, 20, 19, 9),
        (1,  10,  9, 0),
        (5,   5,  4, 4),
        # On / after sell date: quality -2
        (0,  20, 18, -1),
        (-1, 10,  8, -2),
        # Floor: quality never below 0
        (5,   0,  0,  4),
        (0,   1,  0, -1),
        (0,   0,  0, -1),
    ])
    def test_normal_item_quality_and_sell_in(
            self, sell_in, quality, expected_quality, expected_sell_in):
        """Normal item: quality decreases 1 before expiry, 2 after; floor at 0."""
        item = update(Item("Normal Item", sell_in=sell_in, quality=quality))
        assert item.quality == expected_quality, (
            f"sell_in={sell_in}, quality={quality} → expected quality {expected_quality}")
        assert item.sell_in == expected_sell_in


# ===========================================================================
# Aged Brie
# ===========================================================================

class TestAgedBrie:
    """Quality increases over time; capped at 50."""

    @pytest.mark.parametrize("sell_in, quality, expected_quality", [
        # Before sell date: +1
        (5,  10, 11),
        (1,  49, 50),   # cap edge
        (1,  50, 50),   # already at cap
        # After sell date: +2  (once sell_in passes 0)
        (0,  10, 12),
        (-1, 10, 12),
        (0,  49, 50),   # cap edge after sell date
        (0,  50, 50),   # cap after sell date
    ])
    def test_aged_brie_quality(self, sell_in, quality, expected_quality):
        """Aged Brie increases in quality; never exceeds 50."""
        item = update(Item("Aged Brie", sell_in=sell_in, quality=quality))
        assert item.quality == expected_quality

    def test_aged_brie_sell_in_decreases(self):
        item = update(Item("Aged Brie", sell_in=5, quality=10))
        assert item.sell_in == 4


# ===========================================================================
# Sulfuras, Hand of Ragnaros
# ===========================================================================

class TestSulfuras:
    """Legendary item: sell_in and quality never change."""

    @pytest.mark.parametrize("sell_in, quality", [
        (0,  80),
        (10, 80),
        (-1, 80),
    ])
    def test_sulfuras_is_immutable(self, sell_in, quality):
        """Sulfuras never changes quality or sell_in, regardless of date."""
        item = update(Item("Sulfuras, Hand of Ragnaros",
                           sell_in=sell_in, quality=quality))
        assert item.quality == quality
        assert item.sell_in == sell_in


# ===========================================================================
# Backstage passes to a TAFKAL80ETC concert
# ===========================================================================

class TestBackstagePasses:
    """Quality increases with a multiplier that depends on days remaining;
    drops to 0 the day after the concert."""

    @pytest.mark.parametrize("sell_in, quality, expected_quality", [
        # > 10 days: +1
        (15, 20, 21),
        (11, 20, 21),
        # 10 days or fewer: +2
        (10, 20, 22),
        (8,  20, 22),
        (6,  20, 22),
        # 5 days or fewer: +3
        (5,  20, 23),
        (3,  20, 23),
        (1,  20, 23),
        # After concert: drops to 0
        (0,  20,  0),
        (-1, 20,  0),
        # Quality cap at 50
        (5,  49, 50),   # +3 but capped at 50
        (10, 49, 50),   # +2 but capped at 50
        (15, 49, 50),   # +1 but capped at 50
        (5,  50, 50),   # already at cap
    ])
    def test_backstage_pass_quality(self, sell_in, quality, expected_quality):
        """Backstage pass quality increases based on days remaining; 0 after concert."""
        item = update(Item("Backstage passes to a TAFKAL80ETC concert",
                           sell_in=sell_in, quality=quality))
        assert item.quality == expected_quality, (
            f"sell_in={sell_in}, quality={quality} → expected {expected_quality}")

    def test_backstage_pass_sell_in_decreases(self):
        item = update(Item("Backstage passes to a TAFKAL80ETC concert",
                           sell_in=10, quality=20))
        assert item.sell_in == 9


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
