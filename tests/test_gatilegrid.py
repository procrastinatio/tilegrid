# -*- coding: utf-8 -*-

import unittest
from gatilegrid import GeoadminTileGrid


class TestGeoadminTileGrid(unittest.TestCase):

    def testTileGridWrongExtent(self):
        try:
            GeoadminTileGrid(extent=[10.0, 10.0, 20.0, 20.0])
        except Exception as e:
            self.assertIsInstance(e, AssertionError)
        else:
            raise Exception('GeoadminTileGrid instance: extent assertion error \
                too small not raised')

        try:
            GeoadminTileGrid(extent=[430000.0, 40000.0, 420000.0, 340000.0])
        except Exception as e:
            self.assertIsInstance(e, AssertionError)
        else:
            raise Exception('GeoadminTileGrid instance: extent assertion error \
                inconsistent not raised')

    def testTileSize(self):
        gagrid = GeoadminTileGrid()
        ts = gagrid.tileSize(20)
        self.assertEqual(ts, 2560.0)
        try:
            gagrid.tileSize(40)
        except Exception as e:
            self.assertIsInstance(e, AssertionError)
        else:
            raise Exception('tileSize: assertion error not raised')

        self.assertEqual(gagrid.tileAddressTemplate,
                         '{zoom}/{tileCol}/{tileRow}')

    def testTileBoundsAndAddress(self):
        gagrid = GeoadminTileGrid()
        tbe = [548000.0, 196400.0, 573600.0, 222000.0]
        tb = gagrid.tileBounds(17, 5, 5)
        self.assertEqual(tb[0], tbe[0])
        self.assertEqual(tb[1], tbe[1])
        self.assertEqual(tb[2], tbe[2])
        self.assertEqual(tb[3], tbe[3])
        try:
            gagrid.tileBounds(77, 5, 5)
        except Exception as e:
            self.assertIsInstance(e, AssertionError)
        else:
            raise Exception('tileBounds: assertion error not raised')

        ta = gagrid.tileAddress(0, [gagrid.MINX, gagrid.MAXY])
        self.assertEqual(ta[0], 0)
        self.assertEqual(ta[1], 0)
        ta = gagrid.tileAddress(17, [tb[0], tb[3]])
        self.assertEqual(ta[0], 5)
        self.assertEqual(ta[1], 5)

    def testIterGrid(self):
        gagrid = GeoadminTileGrid()
        gen = gagrid.iterGrid(0, 0)
        self.assertTrue(hasattr(gen, '__iter__'))
        tileSpec = [t for t in gen]
        self.assertEqual(len(tileSpec), 1)
        self.assertEqual(len(tileSpec[0]), 4)
        self.assertEqual(tileSpec[0][1], 0)
        self.assertEqual(tileSpec[0][2], 0)
        self.assertEqual(tileSpec[0][3], 0)
        self.assertEqual(str(tileSpec[0][0]), str(gagrid.tileBounds(0, 0, 0)))

        gen = gagrid.iterGrid(13, 14)
        tilesSpec = [i for i in gen]
        self.assertEqual(len(tilesSpec), 12)
        self.assertEqual(tilesSpec[0][1], 13)
        self.assertEqual(tilesSpec[6][1], 14)
        bounds = tilesSpec[2][0]
        z = tilesSpec[2][1]
        col = tilesSpec[2][2]
        row = tilesSpec[2][3]
        self.assertEqual(bounds, gagrid.tileBounds(z, col, row))

        try:
            for i in gagrid.iterGrid(13, 33):
                print(i)
        except Exception as e:
            self.assertIsInstance(e, AssertionError)
        else:
            raise Exception('iterGrid: assertion error maxZoom \
                            too big not raised')

        try:
            for i in gagrid.iterGrid(-1, 11):
                print(i)
        except Exception as e:
            self.assertIsInstance(e, AssertionError)
        else:
            raise Exception('iterGrid: assertion error minZoom \
                            too small not raised')

        try:
            for i in gagrid.iterGrid(13, 11):
                print(i)
        except Exception as e:
            self.assertIsInstance(e, AssertionError)
        else:
            raise Exception('iterGrid: assertion error maxZoom \
                            bigger than minZoom not raised')

    def testGetScale(self):
        gagrid = GeoadminTileGrid()
        s14 = gagrid.getScale(14)
        s28 = gagrid.getScale(28)
        self.assertGreater(s14, s28)
        self.assertEqual(round(s14), 2456688.0)
        self.assertEqual(round(s28), 378.0)

    def testIterGridWithExtent(self):
        offset = 20000.0
        gagridDefault = GeoadminTileGrid()
        extent = [gagridDefault.MINX + offset, gagridDefault.MINY + offset,
                  gagridDefault.MAXX - offset, gagridDefault.MAXY - offset]
        gagridExtent = GeoadminTileGrid(extent=extent)

        self.assertGreater(gagridDefault.xSpan, gagridExtent.xSpan)
        self.assertGreater(gagridDefault.ySpan, gagridExtent.ySpan)

        tilesSpecDefault = [t for t in gagridDefault.iterGrid(20, 21)]
        tilesSpecExtent = [t for t in gagridExtent.iterGrid(20, 21)]

        self.assertGreater(len(tilesSpecDefault), len(tilesSpecExtent))
        self.assertEqual(tilesSpecExtent[0][1], 20)
        self.assertEqual(tilesSpecExtent[len(tilesSpecExtent) - 1][1], 21)

        nbTiles = gagridExtent.numberOfTilesAtZoom(20) + \
            gagridExtent.numberOfTilesAtZoom(21)
        self.assertEqual(len(tilesSpecExtent), nbTiles)

    def testNumberOfTiles(self):
        zoom = 20
        gagrid = GeoadminTileGrid()
        [minRow, minCol, maxRow, maxCol] = gagrid.getExtentAddress(zoom)
        nb = gagrid.numberOfTilesAtZoom(zoom)
        nbx = gagrid.numberOfXTilesAtZoom(zoom)
        nby = gagrid.numberOfYTilesAtZoom(zoom)
        self.assertGreater(maxCol, maxRow)
        self.assertEqual(len([t for t in gagrid.iterGrid(zoom, zoom)]), nb)
        self.assertEqual(nb, 23500)
        self.assertEqual(nb, nbx * nby)
        self.assertGreater(nbx, nby)

        zoom = 22
        [minRow, minCol, maxRow, maxCol] = gagrid.getExtentAddress(zoom)
        nb = gagrid.numberOfTilesAtZoom(zoom)
        nbx = gagrid.numberOfXTilesAtZoom(zoom)
        nby = gagrid.numberOfYTilesAtZoom(zoom)
        self.assertGreater(maxCol, maxRow)
        self.assertEqual(len([t for t in gagrid.iterGrid(zoom, zoom)]), nb)
        self.assertEqual(nb, 375000)
        self.assertEqual(nb, nbx * nby)
        self.assertGreater(nbx, nby)
