from pdb import run
import pygame
import random


class SortVisualizer:
    def __init__(self, num_of_bars=100, max_bar_height=500, bar_width=4, bar_margin=1, sort_speed=5):
        pygame.init()
        self.window_width = num_of_bars * (bar_width + bar_margin)
        self.window_height = max_bar_height + 50
        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height))
        pygame.display.set_caption("Sort Visualizer")
        self.num_of_bars = num_of_bars
        self.max_bar_height = max_bar_height
        self.bar_width = bar_width
        self.bar_margin = bar_margin
        self.sort_speed = sort_speed
        self.bars = [random.randint(1, max_bar_height)
                     for _ in range(num_of_bars)]

    def _draw_bars(self):
        self.window.fill((255, 255, 255))
        for i, bar_height in enumerate(self.bars):
            x = i * (self.bar_width + self.bar_margin) + self.bar_margin
            y = self.max_bar_height - bar_height + 10
            bar_rect = pygame.Rect(x, y, self.bar_width, bar_height)
            pygame.draw.rect(self.window, (0, 0, 255), bar_rect)
        pygame.display.update()
        pygame.time.wait(self.sort_speed)

    # Simple bubble sort algorithm. Time = O(n^2) --- Memory = O(1)
    def bubble_sort(self):
        for i in range(len(self.bars)):
            for j in range(len(self.bars) - 1 - i):
                if self.bars[j] > self.bars[j + 1]:
                    self.bars[j], self.bars[j +
                                            1] = self.bars[j + 1], self.bars[j]
                    self._draw_bars()

    # Simple instertion sort algorithm. Time = O(n^2) --- Memory = O(1)
    def insertion_sort(self):
        for i in range(1, len(self.bars)):
            key = self.bars[i]
            j = i-1
            while j >= 0 and key < self.bars[j]:
                self.bars[j+1] = self.bars[j]
                j -= 1
                self._draw_bars()
            self.bars[j+1] = key

    # Simple Merge sort algo. Time = O(n logn) --- Memory = O(n)
    def merge_sort(self):
        self._merge()

    # Auxiliary method (only for internal use). Merge two subarrays and update self.bars
    def _merge(self, start_idx=None, end_idx=None, mid_idx=None):
        if start_idx == None and end_idx == None:
            start_idx, end_idx = 0, len(self.bars)-1
        if end_idx-start_idx > 0:
            if not mid_idx:
                mid_idx = (end_idx+start_idx)//2
            self._merge(start_idx, mid_idx)
            self._merge(mid_idx+1, end_idx)
            tmp = [None]*(end_idx-start_idx+1)
            i = start_idx
            j = mid_idx+1
            k = 0
            while i <= mid_idx and j <= end_idx:
                if self.bars[i] <= self.bars[j]:
                    tmp[k] = self.bars[i]
                    i += 1
                else:
                    tmp[k] = self.bars[j]
                    j += 1
                k += 1
            while i <= mid_idx:
                tmp[k] = self.bars[i]
                i += 1
                k += 1
            while j <= end_idx:
                tmp[k] = self.bars[j]
                j += 1
                k += 1
            self.bars[start_idx:end_idx+1] = tmp
            self._draw_bars()

    # Quick sort algorigthm. Time = O(n^2) (avg nlogn) --- Memory = log(n) (Not stable (doesn't keep order))
    def quick_sort(self, low=None, high=None):
        if low == None and high == None:
            low, high = 0, len(self.bars) - 1
        if low < high:
            # pivot index such that elements lower then pivot are located on the left, and grater on the right
            pi = self._partition(low, high)
            self.quick_sort(low, pi-1)
            self.quick_sort(pi+1, high)

    def _partition(self, low, high) -> int:

        pivot = self.bars[high]
        # pivot index
        i = low - 1

        for j in range(low, high):
            if self.bars[j] <= pivot:
                i += 1
                (self.bars[i], self.bars[j]) = (self.bars[j], self.bars[i])
                self._draw_bars()

        self.bars[high], self.bars[i+1] = self.bars[i+1], self.bars[high]
        self._draw_bars()
        return i + 1

    # Tim Sort algorithm. Time = O(n logn) --- Memory = O(n)
    def tim_sort(self, MIN_MERGE=64):
        """Main function for Tim Sort

        Args:
            MIN_MERGE (int, optional): max run size -> so min possible merge. Defaults to 64.
        """
        run_size = self.calc_run_size(MIN_MERGE)
        for start in range(0, len(self.bars), run_size):
            end = min(start+run_size, len(self.bars))
            # sorting each run using insertion sort
            for i in range(start+1, end):
                j = i
                while j > start and self.bars[j] < self.bars[j-1]:
                    self.bars[j-1], self.bars[j] = self.bars[j], self.bars[j-1]
                    j -= 1

        # merging each run
        while run_size < len(self.bars):
            for left in range(0, len(self.bars), 2*run_size):
                mid = left + run_size
                right = min(mid+run_size, len(self.bars)-1)
                self._merge(left, right, mid)

    def calc_run_size(self, MIN_MERGE) -> int:
        r = 0
        n = len(self.bars)
        while n >= MIN_MERGE:
            r |= n & 1
            n >>= 1
        return n+r


if __name__ == "__main__":
    SortVisualizer(num_of_bars=200, bar_width=3, sort_speed=2).tim_sort()
