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


    # ------------------------------------------------------------------
    # Conjured items — TDD: tests escritos ANTES de la implementación
    # Un ítem Conjured degrada el doble de rápido que un ítem normal.
    # ------------------------------------------------------------------

    def test_conjured_item_quality_decreases_by_2_before_sell_date(self):
        """Conjured degrada -2 por día antes del vencimiento."""
        items = [Item("Conjured Mana Cake", sell_in=5, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(18, items[0].quality)

    def test_conjured_item_quality_decreases_by_4_after_sell_date(self):
        """Conjured degrada -4 por día después del vencimiento (doble de normal)."""
        items = [Item("Conjured Mana Cake", sell_in=0, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(16, items[0].quality)

    def test_conjured_item_quality_never_goes_below_zero(self):
        """La calidad del Conjured no puede bajar de 0."""
        items = [Item("Conjured Mana Cake", sell_in=5, quality=1)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)

    def test_conjured_item_sell_in_decreases_by_1(self):
        """El sell_in del Conjured decrece 1 por día como cualquier ítem normal."""
        items = [Item("Conjured Mana Cake", sell_in=5, quality=10)]
        GildedRose(items).update_quality()
        self.assertEqual(4, items[0].sell_in)


# ------------------------------------------------------------------
# Reto adicional Senior — Inyección de dependencias
# Demuestra que GildedRose es testeable con un factory falso
# (test double) sin tocar ningún código de producción.
# ------------------------------------------------------------------

class FakeUpdater:
    """Updater espía: registra que fue llamado sin ejecutar lógica real."""
    def __init__(self, item):
        self.item = item
        self.called = False

    def update(self):
        self.called = True


class FakeFactory:
    """Factory falso que devuelve FakeUpdaters y recuerda los ítems procesados."""
    def __init__(self):
        self.updaters = []

    def for_item(self, item):
        updater = FakeUpdater(item)
        self.updaters.append(updater)
        return updater


class GildedRoseDITest(unittest.TestCase):

    def test_gilded_rose_delegates_to_injected_factory(self):
        """GildedRose llama al factory inyectado, no al UpdaterFactory por defecto."""
        items = [Item("Foo", sell_in=5, quality=10),
                 Item("Bar", sell_in=3, quality=20)]
        fake_factory = FakeFactory()

        GildedRose(items, factory=fake_factory).update_quality()

        # El factory falso recibió exactamente los 2 ítems
        self.assertEqual(2, len(fake_factory.updaters))
        # Cada updater fue invocado exactamente una vez
        self.assertTrue(all(u.called for u in fake_factory.updaters))
        # Los ítems no fueron alterados (el fake no cambia nada)
        self.assertEqual(10, items[0].quality)
        self.assertEqual(20, items[1].quality)

    def test_gilded_rose_uses_default_factory_when_none_injected(self):
        """Sin factory inyectado, GildedRose usa UpdaterFactory normalmente."""
        items = [Item("Normal Item", sell_in=5, quality=10)]
        GildedRose(items).update_quality()   # factory=None → UpdaterFactory por defecto
        self.assertEqual(9, items[0].quality)


if __name__ == '__main__':
    unittest.main()