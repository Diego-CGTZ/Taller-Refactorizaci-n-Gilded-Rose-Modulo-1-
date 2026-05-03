# -*- coding: utf-8 -*-
"""
Characterization tests for GildedRose (legacy code).

These tests document the *current* behaviour of the code —
not the ideal behaviour. They act as a safety net before any refactoring.
"""
import unittest
from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):

    # ------------------------------------------------------------------
    # Normal Item (4 tests)
    # ------------------------------------------------------------------

    def test_normal_item_quality_decreases_by_1_before_sell_date(self):
        items = [Item("Normal Item", sell_in=10, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(19, items[0].quality)
        self.assertEqual(9, items[0].sell_in)

    def test_normal_item_quality_decreases_by_2_on_sell_date(self):
        """sell_in starts at 0 → after update sell_in=-1, quality loses 2."""
        items = [Item("Normal Item", sell_in=0, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(18, items[0].quality)

    def test_normal_item_quality_decreases_by_2_after_sell_date(self):
        items = [Item("Normal Item", sell_in=-1, quality=10)]
        GildedRose(items).update_quality()
        self.assertEqual(8, items[0].quality)

    def test_normal_item_quality_never_goes_below_zero(self):
        items = [Item("Normal Item", sell_in=5, quality=0)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)

    # ------------------------------------------------------------------
    # Aged Brie (3 tests)
    # ------------------------------------------------------------------

    def test_aged_brie_quality_increases_before_sell_date(self):
        items = [Item("Aged Brie", sell_in=5, quality=10)]
        GildedRose(items).update_quality()
        self.assertEqual(11, items[0].quality)
        self.assertEqual(4, items[0].sell_in)

    def test_aged_brie_quality_increases_twice_after_sell_date(self):
        """sell_in=0 → after update sell_in=-1, quality gains 2."""
        items = [Item("Aged Brie", sell_in=0, quality=10)]
        GildedRose(items).update_quality()
        self.assertEqual(12, items[0].quality)

    def test_aged_brie_quality_never_exceeds_50(self):
        items = [Item("Aged Brie", sell_in=5, quality=50)]
        GildedRose(items).update_quality()
        self.assertEqual(50, items[0].quality)

    # ------------------------------------------------------------------
    # Sulfuras (2 tests)
    # ------------------------------------------------------------------

    def test_sulfuras_quality_never_changes(self):
        items = [Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)]
        GildedRose(items).update_quality()
        self.assertEqual(80, items[0].quality)

    def test_sulfuras_sell_in_never_changes(self):
        items = [Item("Sulfuras, Hand of Ragnaros", sell_in=5, quality=80)]
        GildedRose(items).update_quality()
        self.assertEqual(5, items[0].sell_in)

    # ------------------------------------------------------------------
    # Backstage passes (4 tests)
    # ------------------------------------------------------------------

    def test_backstage_pass_quality_increases_by_1_when_more_than_10_days(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert",
                      sell_in=15, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(21, items[0].quality)

    def test_backstage_pass_quality_increases_by_2_when_10_days_or_fewer(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert",
                      sell_in=10, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(22, items[0].quality)

    def test_backstage_pass_quality_increases_by_3_when_5_days_or_fewer(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert",
                      sell_in=5, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(23, items[0].quality)

    def test_backstage_pass_quality_drops_to_zero_after_concert(self):
        """sell_in=0 means the concert is today; after update quality = 0."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert",
                      sell_in=0, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)

    # ------------------------------------------------------------------
    # sell_in tracking (1 test)
    # ------------------------------------------------------------------

    def test_sell_in_decreases_by_1_each_day(self):
        """Applies to any non-Sulfuras item."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert",
                      sell_in=10, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(9, items[0].sell_in)


if __name__ == '__main__':
    unittest.main()