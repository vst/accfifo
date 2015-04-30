from accfifo import Entry
from accfifo import FIFO
from decimal import Decimal
import unittest


class TestFIFO(unittest.TestCase):
    """
    Tests FIFO accounting.
    """

    def test_no_entries(self):
        """
        Tests the case that there are no entries.
        """
        ## Create the FIFO accounting:
        fifo = FIFO()

        ## Inventory is empty:
        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)

        ## There is no trace:
        self.assertTrue(len(fifo.trace) == 0)

        ## There is no stock in the inventory:
        self.assertEqual(fifo.stock, 0)

        ## No average cost could be calculated:
        self.assertIsNone(fifo.avgcost)

    def test_single_buy(self):
        ## Create the entry:
        entries = [Entry(100, 10)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is not empty:
        self.assertTrue(len(fifo.inventory) == 1)
        self.assertFalse(fifo.is_empty)

        ## There is no trace as there are no closing entries:
        self.assertTrue(len(fifo.trace) == 0)

        ## There is stock in the inventory:
        self.assertTrue(fifo.stock, 100)

        ## The average cost was calculated:
        self.assertIsNotNone(fifo.avgcost)
        self.assertEqual(fifo.avgcost, 10)

    def test_two_buys(self):
        ## Create the entry:
        entries = [Entry(100, 10), Entry(100, 20)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is not empty:
        self.assertTrue(len(fifo.inventory) == 2)
        self.assertFalse(fifo.is_empty)

        ## There is no trace as there are no closing entries:
        self.assertTrue(len(fifo.trace) == 0)

        ## There is stock in the inventory:
        self.assertTrue(fifo.stock, 200)

        ## The average cost was calculated:
        self.assertIsNotNone(fifo.avgcost)
        self.assertEqual(fifo.avgcost, 15)

    def test_single_sell(self):
        ## Create the entry:
        entries = [Entry(-100, 10)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is not empty:
        self.assertTrue(len(fifo.inventory) == 1)
        self.assertFalse(fifo.is_empty)

        ## There is no trace as there are no closing entries:
        self.assertTrue(len(fifo.trace) == 0)

        ## There is stock in the inventory:
        self.assertTrue(fifo.stock, -100)

        ## The average cost was calculated:
        self.assertIsNotNone(fifo.avgcost)
        self.assertEqual(fifo.avgcost, 10)

    def test_two_buys(self):
        ## Create the entry:
        entries = [Entry(-100, 10), Entry(-100, 20)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is not empty:
        self.assertTrue(len(fifo.inventory) == 2)
        self.assertFalse(fifo.is_empty)

        ## There is no trace as there are no closing entries:
        self.assertTrue(len(fifo.trace) == 0)

        ## There is stock in the inventory:
        self.assertTrue(fifo.stock, -200)

        ## The average cost was calculated:
        self.assertIsNotNone(fifo.avgcost)
        self.assertEqual(fifo.avgcost, 15)

    def test_quick_square(self):
        ## Create the entry:
        entries = [Entry(100, 10), Entry(-100, 10)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is empty:
        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)

        ## There is a trace as all the stock is sold out:
        self.assertTrue(len(fifo.trace) == 1)

        ## There is no stock in the inventory:
        self.assertEqual(fifo.stock, 0)

        ## No average cost could be calculated:
        self.assertIsNone(fifo.avgcost)

    def test_quick_alternate_square(self):
        ## Create the entry:
        entries = [Entry(100, 10), Entry(-100, 10)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is empty:
        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)

        ## There is a trace as all the stock is sold out:
        self.assertTrue(len(fifo.trace) == 1)

        ## There is no stock in the inventory:
        self.assertEqual(fifo.stock, 0)

        ## No average cost could be calculated:
        self.assertIsNone(fifo.avgcost)

    def test_double_square(self):
        ## Create the entry:
        entries = [Entry(100, 10), Entry(-100, 10), Entry(100, 10), Entry(-100, 10)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is empty:
        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)

        ## There is a trace as all the stock is sold out:
        self.assertTrue(len(fifo.trace) == 2)

        ## There is no stock in the inventory:
        self.assertEqual(fifo.stock, 0)

        ## No average cost could be calculated:
        self.assertIsNone(fifo.avgcost)

    def test_double_alternate_square(self):
        ## Create the entry:
        entries = [Entry(100, 10), Entry(-100, 10), Entry(-100, 10), Entry(100, 10)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is empty:
        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)

        ## There is a trace as all the stock is sold out:
        self.assertTrue(len(fifo.trace) == 2)

        ## There is no stock in the inventory:
        self.assertEqual(fifo.stock, 0)

        ## No average cost could be calculated:
        self.assertIsNone(fifo.avgcost)

    def test_alternate_buy_sell(self):
        ## Create the entry:
        entries = [Entry(100, 10), Entry(-200, 10)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is not empty:
        self.assertTrue(len(fifo.inventory) == 1)
        self.assertFalse(fifo.is_empty)

        ## There is a trace as some stock entries are closed:
        self.assertTrue(len(fifo.trace) == 1)

        ## There is some stock in the inventory:
        self.assertEqual(fifo.stock, -100)

        ## Average cost is calculated:
        self.assertIsNotNone(fifo.avgcost)
        self.assertEqual(fifo.avgcost, 10)

    def test_alternate_sell_buy(self):
        ## Create the entry:
        entries = [Entry(-100, 10), Entry(200, 10)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is not empty:
        self.assertTrue(len(fifo.inventory) == 1)
        self.assertFalse(fifo.is_empty)

        ## There is a trace as some stock entries are closed:
        self.assertTrue(len(fifo.trace) == 1)

        ## There is some stock in the inventory:
        self.assertEqual(fifo.stock, 100)

        ## Average cost is calculated:
        self.assertIsNotNone(fifo.avgcost)
        self.assertEqual(fifo.avgcost, 10)

    def test_multiple_entry_stock_out(self):
        ## Create the entry:
        entries = [Entry(100, 10), Entry(-50, 10), Entry(-50, 15)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is empty:
        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)

        ## There is a trace as some stock entries are closed:
        self.assertTrue(len(fifo.trace) == 2)

        ## There is some stock in the inventory:
        self.assertEqual(fifo.stock, 0)

        ## No average cost is calculated:
        self.assertIsNone(fifo.avgcost)

    def test_multiple_entry_stock_out_alt(self):
        ## Create the entry:
        entries = [Entry(-100, 10), Entry(50, 10), Entry(50, 15)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is empty:
        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)

        ## There is a trace as some stock entries are closed:
        self.assertTrue(len(fifo.trace) == 2)

        ## There is some stock in the inventory:
        self.assertEqual(fifo.stock, 0)

        ## No average cost is calculated:
        self.assertIsNone(fifo.avgcost)

    def test_double_multiple_entry_stock_out(self):
        ## Create the entry:
        entries = [Entry(50, 10), Entry(50, 12), Entry(-50, 10), Entry(-50, 15)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is empty:
        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)

        ## There is a trace as some stock entries are closed:
        self.assertTrue(len(fifo.trace) == 2)

        ## There is some stock in the inventory:
        self.assertEqual(fifo.stock, 0)

        ## No average cost is calculated:
        self.assertIsNone(fifo.avgcost)

    def test_double_multiple_entry_stock_out_alt(self):
        ## Create the entry:
        entries = [Entry(40, 10), Entry(60, 12), Entry(-50, 10), Entry(-50, 15)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is empty:
        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)

        ## There is a trace as some stock entries are closed:
        self.assertTrue(len(fifo.trace) == 3)

        ## There is some stock in the inventory:
        self.assertEqual(fifo.stock, 0)

        ## No average cost is calculated:
        self.assertIsNone(fifo.avgcost)

    def test_double_multiple_entry_stock_out_alt2(self):
        ## Create the entry:
        entries = [Entry(60, 10), Entry(40, 12), Entry(-50, 10), Entry(-50, 15)]

        ## Create the FIFO accounting:
        fifo = FIFO(entries)

        ## Inventory is empty:
        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)

        ## There is a trace as some stock entries are closed:
        self.assertTrue(len(fifo.trace) == 3)

        ## There is some stock in the inventory:
        self.assertEqual(fifo.stock, 0)

        ## No average cost is calculated:
        self.assertIsNone(fifo.avgcost)

    def test_complex_trades(self):
        ## Create the FIFO accounting, check the stock and the average cost:
        fifo = FIFO([Entry(60, 10), Entry(10, 12), Entry(-50, 10)])
        self.assertEqual(fifo.stock, 20)
        self.assertEqual(fifo.avgcost, 11)

        ## Create the FIFO accounting, check the stock and the average cost:
        fifo = FIFO([Entry(60, 10), Entry(10, 12), Entry(-80, 10)])
        self.assertEqual(fifo.stock, -10)
        self.assertEqual(fifo.avgcost, 10)

        ## Create the FIFO accounting, check the stock and the average cost:
        fifo = FIFO([Entry(60, 10), Entry(-10, 12), Entry(-20, 10), Entry(50, 12), Entry(-60, 14), Entry(10, 21)])
        self.assertEqual(fifo.stock, 30)
        self.assertEqual(fifo.avgcost, 15)

        ## Let's do a handful one:
        fifo = FIFO([Entry(20, 10), Entry(32, 7), Entry(97, 6), Entry(17, 2), Entry(14, 0),
                     Entry(-50, 9), Entry(-59, 6), Entry(-50, 8), Entry(63, 10), Entry(-31, 6),
                     Entry(-21, 1), Entry(-36, 10), Entry(-18, 2), Entry(91, 2), Entry(85, 4),
                     Entry(-81, 1), Entry(33, 2), Entry(45, 4), Entry(-18, 4), Entry(-33, 7),
                     Entry(-47, 3), Entry(-49, 7), Entry(73, 3), Entry(79, 10), Entry(3, 5),
                     Entry(50, 7), Entry(-82, 10), Entry(47, 9), Entry(72, 10), Entry(40, 1)])
        self.assertEqual(fifo.stock, 286)
        self.assertEqual(fifo.avgcost, 8)

        # Close the handful one:
        fifo = FIFO([Entry(20, 10), Entry(32, 7), Entry(97, 6), Entry(17, 2), Entry(14, 0),
                     Entry(-50, 9), Entry(-59, 6), Entry(-50, 8), Entry(63, 10), Entry(-31, 6),
                     Entry(-21, 1), Entry(-36, 10), Entry(-18, 2), Entry(91, 2), Entry(85, 4),
                     Entry(-81, 1), Entry(33, 2), Entry(45, 4), Entry(-18, 4), Entry(-33, 7),
                     Entry(-47, 3), Entry(-49, 7), Entry(73, 3), Entry(79, 10), Entry(3, 5),
                     Entry(50, 7), Entry(-82, 10), Entry(47, 9), Entry(72, 10), Entry(40, 1),
                     Entry(-286, 8)])
        self.assertEqual(fifo.stock, 0)
        self.assertIsNone(fifo.avgcost)


if __name__ == "__main__":
    ## Test the above:
    unittest.main()
