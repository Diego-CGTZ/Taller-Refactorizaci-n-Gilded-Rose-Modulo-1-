# -*- coding: utf-8 -*-

AGED_BRIE      = "Aged Brie"
SULFURAS       = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"


# ===========================================================================
# Template Method — clase base
# ===========================================================================

class ItemUpdater:
    """Comportamiento por defecto: ítem normal."""

    def update(self, item):
        self._update_sell_in(item)
        self._update_quality(item)

    def _update_sell_in(self, item):
        item.sell_in -= 1

    def _update_quality(self, item):
        if item.quality > 0:
            item.quality -= 1
        if item.sell_in < 0 and item.quality > 0:   # doble degradación post-vencimiento
            item.quality -= 1


# ===========================================================================
# Subclases — sobreescriben solo lo necesario
# ===========================================================================

class SulfurasUpdater(ItemUpdater):
    def update(self, item):
        pass  # ítem legendario: nunca cambia


class AgedBrieUpdater(ItemUpdater):
    def _update_quality(self, item):
        if item.quality < 50:
            item.quality += 1
        if item.sell_in < 0 and item.quality < 50:  # doble mejora post-vencimiento
            item.quality += 1


class BackstagePassUpdater(ItemUpdater):
    def _update_quality(self, item):
        if item.sell_in < 0:                         # concierto pasó → calidad = 0
            item.quality = 0
            return
        if item.quality < 50:
            item.quality += 1                        # +1 base
        if item.sell_in < 10 and item.quality < 50:  # bono: ≤10 días restantes
            item.quality += 1
        if item.sell_in < 5 and item.quality < 50:   # bono: ≤5 días restantes
            item.quality += 1


# ===========================================================================
# GildedRose — delega en el updater correcto
# ===========================================================================

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            self._get_updater(item).update(item)

    def _get_updater(self, item):
        if item.name == SULFURAS:
            return SulfurasUpdater()
        if item.name == AGED_BRIE:
            return AgedBrieUpdater()
        if item.name == BACKSTAGE_PASS:
            return BackstagePassUpdater()
        return ItemUpdater()


# ===========================================================================
# Item — sin cambios (regla del kata)
# ===========================================================================

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)