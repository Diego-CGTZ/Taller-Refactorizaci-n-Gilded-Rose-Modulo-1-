# -*- coding: utf-8 -*-

AGED_BRIE      = "Aged Brie"
SULFURAS       = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if self._is_sulfuras(item):
                continue
            if item.name == AGED_BRIE:
                self._update_aged_brie(item)
            elif item.name == BACKSTAGE_PASS:
                self._update_backstage_pass(item)
            else:
                self._update_normal_item(item)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _is_sulfuras(self, item):
        return item.name == SULFURAS

    def _update_normal_item(self, item):
        if item.quality > 0:
            item.quality = item.quality - 1
        item.sell_in = item.sell_in - 1
        if item.sell_in < 0:
            if item.quality > 0:
                item.quality = item.quality - 1

    def _update_aged_brie(self, item):
        if item.quality < 50:
            item.quality = item.quality + 1
        item.sell_in = item.sell_in - 1
        if item.sell_in < 0:
            if item.quality < 50:
                item.quality = item.quality + 1

    def _update_backstage_pass(self, item):
        if item.quality < 50:
            item.quality = item.quality + 1
            if item.sell_in < 11:
                if item.quality < 50:
                    item.quality = item.quality + 1
            if item.sell_in < 6:
                if item.quality < 50:
                    item.quality = item.quality + 1
        item.sell_in = item.sell_in - 1
        if item.sell_in < 0:
            item.quality = item.quality - item.quality


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)