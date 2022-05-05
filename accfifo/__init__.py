# Copyright (c) 2013-2015, Vehbi Sinan Tunalioglu <vst@vsthost.com>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# (See http://opensource.org/licenses/BSD-2-Clause)
"""
Computes the FIFO accounting valuation and stock inventory.
"""

import datetime
from collections import deque


class Entry(object):
    """
    Defines an accounting entry.
    """

    def __init__(self, quantity, price, factor=1, **kwargs):
        """
        Initializes an entry object with quantity, price and arbitrary
        data associated with the entry to be used post-fifo-accounting
        analysis purposes.

        Note the factor parameter. This prameter is applied to the
        price.
        """
        ## Save data slots:
        self.quantity = quantity
        self.price = price
        self.factor = factor
        self.data = kwargs

    def __repr__(self):
        return "%s @%s" % (self.quantity, self.price)

    @property
    def size(self):
        return abs(self.quantity)

    @property
    def buy(self):
        return self.quantity > 0

    @property
    def sell(self):
        return not self.buy

    @property
    def zero(self):
        return self.quantity == 0

    @property
    def value(self):
        return self.quantity * self.price * self.factor

    def copy(self, quantity=None):
        return Entry(quantity or self.quantity, self.price, self.factor, **self.data.copy())


class FIFO(object):
    """
    Implements a FIFO accounting rule by (1) calculating the cost of
    the inventory in hand, (2) calculating the historical PnL trace.
    """

    def __init__(self, entries=None):
        """
        Initializes and computes the FIFO accounting.

        Note that entries are supposed to be sorted.
        """
        ## Mark the start timestamp:
        self._started_at = datetime.datetime.now()
        self._finished_at = None

        ## Save data slots:
        self._entries = entries or []

        ## Declare and initialize private fields to be used during computing:
        self._balance = 0
        self.inventory = deque()
        self.trace = []

        ## Start computing:
        self._compute()

    @property
    def is_empty(self):
        """
        Indicates if the inventory is empty.
        """
        return len(self.inventory) == 0

    @property
    def stock(self):
        """
        Returns the available stock.
        """
        return self._balance

    @property
    def valuation(self):
        """
        Returns the inventory valuation.
        """
        return sum([s.quantity * s.price for s in self.inventory])

    @property
    def valuation_factored(self):
        """
        Returns the inventory valuation which is factored.
        """
        return sum([s.quantity * s.price * s.factor for s in self.inventory])

    @property
    def avgcost(self):
        """
        Returns the average cost of the inventory.
        """
        ## If we don't have any stock, simply return None, else average:
        return None if self._balance == 0 else (self.valuation / self._balance)

    @property
    def avgcost_factored(self):
        """
        Returns the average cost of the inventory which is factored.
        """
        ## If we don't have any stock, simply return None, else average:
        return None if self._balance == 0 else (self.valuation_factored / self._balance)

    @property
    def runtime(self):
        """
        Returns the total runtime.
        """
        if self._started_at is not None and self._finished_at is not None:
            return self._finished_at - self._started_at
        return None

    def _push(self, entry):
        """
        Pushes the entry to the inventory as new stock movement.
        """
        self.inventory.append(entry)
        self._balance += entry.quantity

    def _fill(self, entry):
        """
        Fills existing stock entries by calculating new stocks if required.
        """
        ## OK, we know that this is a contra-entry for our existing
        ## stock entries, ie. if our balance is positive, this is
        ## negative, or vice-versa. Keep in mind that it may even be
        ## bigger in quantity compared to out balance which will
        ## eventually reverse the sign of our balance, like selling
        ## 100 items when we have stock only for 50. This function
        ## will deal with these situations and calculate new stock
        ## entries.
        ##
        ## OK, let's start with this munch-fill-reverse cycle by
        ## creating a copy of the entry:
        entry = entry.copy()

        ## We will continue as long as the entry has quantity:
        while not entry.zero:
            ## Let's consume the earliest entry from the
            ## inventory. But, if the inventory is empty, we can then
            ## safely push the entry to the inventory:
            if self.is_empty:
                ## Yes, the inventory is empty. Push:
                self._push(entry)

                ## We are done here now! Return:
                return

            ## We have entries in the inventory. Get the earliest:
            earliest = self.inventory.popleft()

            ## There are 3 possible cases:
            ##
            ## 1. entry.size < earliest.size  : Munch from earliest, put earliest back and return
            ## 2. entry.size == earliest.size : Remove the earliest entirely and return
            ## 3. entry.size > earliest.size  : Remove the earliest, adjust entry and continue cycle
            ##
            ## Note that in any of these cases we will update the
            ## trace, too. Let's start:
            if entry.size <= earliest.size:
                ## We will now munch from the earliest:
                munched = earliest.copy(-entry.quantity)

                ## Update the earliest:
                earliest.quantity += entry.quantity

                ## Put earliest back to the inventory if still have quantity:
                if earliest.quantity != 0:
                    self.inventory.appendleft(earliest)

                ## Update the trace:
                self.trace.append([munched, entry])

                ## Update the balance:
                self._balance += entry.quantity

                ## Done, return:
                return
            else:
                ## Munch from the entry:
                munched = entry.copy(-earliest.quantity)

                ## Update the entry:
                entry.quantity += earliest.quantity

                ## Update the trace:
                self.trace.append([earliest, munched])

                ## Update the balance and continue:
                self._balance += munched.quantity

    def _compute(self):
        """
        Computes the FIFO accounting for the given entries and produces
        the (1) cost of the inventory in hand, (2) historical PnL trace.
        """
        ## We will iterate over the entries and operate on the
        ## inventory. Let's start:
        for entry in self._entries:
            ## We will add new stock to the inventory or remove
            ## existing stock from the inventory. It looks pretty
            ## straight-forward. But is it?
            ##
            ## There is a special case which is called "short-selling"
            ## in the financial jargon. This is similar to backorders
            ## in the convential trading of goods which means selling
            ## goods which you don't have in your inventory yet.
            ##
            ## This means that we have the following possible
            ## situations:
            ##
            ## | Stock    | Entry |
            ## |----------|-------|
            ## | positive | buy   |
            ## | positive | sell  |
            ## | negative | buy   |
            ## | negative | sell  |
            ##
            ## As you see, there are two cases which are pretty easy
            ## to handle:
            ##
            ## | Stock    | Entry | Action        |
            ## |----------|-------|---------------|
            ## | positive | buy   | Keep adding   |
            ## | negative | sell  | Keep removing |
            ##
            ## Let's do this:
            if (self._balance >= 0 and entry.buy) or (self._balance <= 0 and entry.sell):
                ## Yes, we will push the entry to the inventory as is:
                self._push(entry)
            ## Good, we will now proceed with the more complicated
            ## operation: Closing previously opened stock
            ## positions. This applies to the following cases with the
            ## required actions to be taken respectively.
            ##
            ## | Stock    | Entry | Action                                     |
            ## |----------|-------|--------------------------------------------|
            ## | positive | sell  | Munch from stock (and reverse if required) |
            ## | negative | buy   | Fill backorders (and reverse if required)  |
            ##
            ## Note that we must make sure that we skip "0"-quantity entries.
            elif not entry.zero:
                ## OK, the entry is not zero. We will proceeding
                ## filling positions:
                self._fill(entry)

            ## We are done with the entry. Let's move to the next one.

        ## This marks the end of the the FIFO computation:
        self._finished_at = datetime.datetime.now()


if __name__ == "__main__":
    ## NOTE: Not for production purposes.
    ##
    ## Consume a CSV file of entries and calculate FIFO
    ## accounting. First import libraries:
    import sys
    import csv

    ## Run a CSV file of entries and see the results if argument provided:
    if len(sys.argv) > 1:
        ## Read entries:
        entries = [Entry(float(line[0]), float(line[1]), float(line[2]) if len(line) > 2 else 1) for line in csv.reader(open(sys.argv[1]))]

        ## Run fifo:
        fifo = FIFO(entries)

        ## Print output:
        print("Available Stock          : ", fifo.stock)
        print("Stock Valuation          : ", fifo.valuation)
        print("Factored Average Cost    : ", fifo.avgcost)
        print("Factored Stock Valuation : ", fifo.valuation_factored)
        print("Average Cost             : ", fifo.avgcost_factored)
        print("Trace Length             : ", len(fifo.trace))
        print("Total Runtime            : ", fifo.runtime)

        ## Print trace:
        if not (len(sys.argv) > 2 and sys.argv[2] == "-q"):
            for element in fifo.trace:
                print("    ", ",".join(["(%s)" % (i,) for i in element]))
