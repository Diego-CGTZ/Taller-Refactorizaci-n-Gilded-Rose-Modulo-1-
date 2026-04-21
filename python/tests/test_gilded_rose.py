# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class TestGildedRose(unittest.TestCase):

    # ──────────────────────────────────────────────
    # Normal Items
    # ──────────────────────────────────────────────

    def test_normal_item_quality_decreases_by_1_before_sell_date(self):
        items = [Item("Normal Item", sell_in=10, quality=20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(19, items[0].quality)
        self.assertEqual(9, items[0].sell_in)

    def test_normal_item_sell_in_decreases_by_1(self):
        items = [Item("Normal Item", sell_in=5, quality=10)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(4, items[0].sell_in)

    def test_normal_item_quality_decreases_by_2_after_sell_date(self):
        """Once sell_in passes 0, quality degrades twice as fast."""
        items = [Item("Normal Item", sell_in=0, quality=20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(18, items[0].quality)

    def test_normal_item_quality_decreases_by_2_when_sell_in_negative(self):
        items = [Item("Normal Item", sell_in=-1, quality=10)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(8, items[0].quality)

    def test_quality_never_goes_below_zero(self):
        items = [Item("Normal Item", sell_in=5, quality=0)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(0, items[0].quality)

    def test_quality_never_goes_below_zero_after_sell_date(self):
        items = [Item("Normal Item", sell_in=0, quality=1)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(0, items[0].quality)

    # ──────────────────────────────────────────────
    # Aged Brie
    # ──────────────────────────────────────────────

    def test_aged_brie_increases_quality_before_sell_date(self):
        items = [Item("Aged Brie", sell_in=5, quality=10)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(11, items[0].quality)

    def test_aged_brie_increases_quality_after_sell_date(self):
        """After sell_in passes, Aged Brie quality increases by 2."""
        items = [Item("Aged Brie", sell_in=0, quality=10)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(12, items[0].quality)

    def test_aged_brie_quality_never_exceeds_50(self):
        items = [Item("Aged Brie", sell_in=5, quality=50)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(50, items[0].quality)

    def test_aged_brie_quality_capped_at_50_near_limit(self):
        items = [Item("Aged Brie", sell_in=0, quality=49)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(50, items[0].quality)

    # ──────────────────────────────────────────────
    # Sulfuras, Hand of Ragnaros
    # ──────────────────────────────────────────────

    def test_sulfuras_quality_never_changes(self):
        items = [Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(80, items[0].quality)

    def test_sulfuras_sell_in_never_changes(self):
        items = [Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(0, items[0].sell_in)

    def test_sulfuras_quality_never_changes_positive_sell_in(self):
        items = [Item("Sulfuras, Hand of Ragnaros", sell_in=10, quality=80)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(80, items[0].quality)
        self.assertEqual(10, items[0].sell_in)

    # ──────────────────────────────────────────────
    # Backstage passes
    # ──────────────────────────────────────────────

    def test_backstage_pass_quality_increases_by_1_more_than_10_days(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(21, items[0].quality)

    def test_backstage_pass_quality_increases_by_2_when_10_days_or_less(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(22, items[0].quality)

    def test_backstage_pass_quality_increases_by_2_when_between_6_and_10_days(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=7, quality=20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(22, items[0].quality)

    def test_backstage_pass_quality_increases_by_3_when_5_days_or_less(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(23, items[0].quality)

    def test_backstage_pass_quality_increases_by_3_when_1_day_left(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=1, quality=20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(23, items[0].quality)

    def test_backstage_pass_quality_drops_to_zero_after_concert(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=20)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(0, items[0].quality)

    def test_backstage_pass_quality_never_exceeds_50(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual(50, items[0].quality)


if __name__ == "__main__":
    unittest.main()
