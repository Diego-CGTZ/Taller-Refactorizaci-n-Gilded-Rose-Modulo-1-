# -*- coding: utf-8 -*-

AGED_BRIE      = "Aged Brie"
SULFURAS       = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"


# ===========================================================================
# Jerarquía Strategy — una clase por comportamiento
# ===========================================================================

class ItemUpdater:
    """Clase base: define la interfaz del updater."""

    def __init__(self, item):
        self.item = item

    def update(self):
        raise NotImplementedError


class NormalItemUpdater(ItemUpdater):
    def update(self):
        self.item.sell_in -= 1
        degradation = 2 if self.item.sell_in < 0 else 1
        self.item.quality = max(0, self.item.quality - degradation)


class AgedBrieUpdater(ItemUpdater):
    def update(self):
        self.item.sell_in -= 1
        improvement = 2 if self.item.sell_in < 0 else 1
        self.item.quality = min(50, self.item.quality + improvement)


class SulfurasUpdater(ItemUpdater):
    def update(self):
        pass  # ítem legendario: nunca cambia


class BackstagePassUpdater(ItemUpdater):
    def update(self):
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self.item.quality = 0
        elif self.item.sell_in < 5:
            self.item.quality = min(50, self.item.quality + 3)
        elif self.item.sell_in < 10:
            self.item.quality = min(50, self.item.quality + 2)
        else:
            self.item.quality = min(50, self.item.quality + 1)


# ===========================================================================
# Factory — selecciona el updater correcto según el nombre del ítem
# ===========================================================================

class UpdaterFactory:
    _registry = {
        AGED_BRIE:      AgedBrieUpdater,
        SULFURAS:       SulfurasUpdater,
        BACKSTAGE_PASS: BackstagePassUpdater,
    }

    @classmethod
    def for_item(cls, item):
        updater_class = cls._registry.get(item.name, NormalItemUpdater)
        return updater_class(item)


# ===========================================================================
# GildedRose — simplificado al máximo
# ===========================================================================

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            UpdaterFactory.for_item(item).update()


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