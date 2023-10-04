from functools import wraps
import sys
import time
import pygame
import random
import BinaryTree

sys.setrecursionlimit(10000)


class SortVisualizer:
    def __init__(self, num_of_bars=100, max_bar_height=500, bar_width=4, bar_margin=1, sort_speed=5, visualize=True):
        pygame.init()
        self.num_of_bars = num_of_bars
        self.max_bar_height = max_bar_height
        self.bar_width = bar_width
        self.bar_margin = bar_margin
        self.bars = [random.randint(1, self.max_bar_height)
                     for _ in range(self.num_of_bars)]
        self.visualize = visualize
        if self.visualize:
            self.window_width = num_of_bars * (bar_width + bar_margin)
            self.window_height = max_bar_height + 50
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height))
            pygame.display.set_caption("Sort Visualizer")
            self.sort_speed = sort_speed

    def _draw_bars(self):
        if self.visualize:
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

    # Selection sort. Time = O(n^2) --- Memory = O(1)

    def selection_sort(self):
        for i in range(len(self.bars)-1):
            cur_min = i
            for j in range(i+1, len(self.bars)):
                if self.bars[cur_min] > self.bars[j]:
                    cur_min = j
            self.bars[i], self.bars[cur_min] = self.bars[cur_min], self.bars[i]
            self._draw_bars()

    # Shell sort. Time = O(n^3/2) --- Memory = O(1)
    def shell_sort(self):
        gap = len(self.bars) // 2
        while gap > 0:
            j = gap
            # Check the array in from left to right
            # Till the last possible index of j
            while j < len(self.bars):
                i = j-gap  # This will keep help in maintain gap value

                while i >= 0:
                    # If value on right side is already greater than left side value
                    # We don't do swap else we swap
                    if self.bars[i+gap] > self.bars[i]:

                        break
                    else:
                        self.bars[i+gap], self.bars[i] = self.bars[i], self.bars[i+gap]
                    self._draw_bars()
                    i = i-gap  # To check left side also
                    # If the element present is greater than current element
                j += 1
            gap = gap//2

    # Tree sort algo. Time = O(n logn) --- Memory = O(n)
    def tree_sort(self):
        self._draw_bars()
        root = None
        for value in self.bars:
            root = self._insert_recursive(root, value)
        self.bars = self._lefttoright_traverse(root)
        self._draw_bars()
        pygame.time.wait(1000)

    # recursevly populate binary tree
    def _insert_recursive(self, root: BinaryTree.Node, value: int):
        if not root:
            root = BinaryTree.Node(value)
            return root

        if value < root.value:
            root.left = self._insert_recursive(root.left, value)
        elif value >= root.value:
            root.right = self._insert_recursive(root.right, value)

        return root

    # traverse binary tree
    @classmethod
    def _lefttoright_traverse(cls, root: BinaryTree.Node, tmp: list = list()):
        if root:
            cls._lefttoright_traverse(root.left, tmp)
            tmp.append(root.value)
            cls._lefttoright_traverse(root.right, tmp)
            return tmp


def test_time_exec():

    vis = SortVisualizer(num_of_bars=5000, bar_width=0,
                         sort_speed=0, max_bar_height=5000, visualize=False)
    start = time.perf_counter()
    sorted(vis.bars)
    end = time.perf_counter()
    print(f"Built-in sorted function excecutes in {end-start:.4f} sec")
    start = time.perf_counter()
    vis.bubble_sort()
    end = time.perf_counter()
    print(f"Bubble sort algo excecutes in {end-start:.4f} sec")
    start = time.perf_counter()
    vis.merge_sort()
    end = time.perf_counter()
    print(f"Merge sort algo excecutes in {end-start:.4f} sec")
    start = time.perf_counter()
    vis.quick_sort()
    end = time.perf_counter()
    print(f"Quick sort algo excecutes in {end-start:.4f} sec")
    # start = time.perf_counter()
    # vis.tim_sort()
    # end = time.perf_counter()
    # print(f"Tim sort algo excecutes in {end-start:.4f} sec")
    start = time.perf_counter()
    vis.tree_sort()
    end = time.perf_counter()
    print(f"Tree sort algo excecutes in {end-start:.4f} sec")
    start = time.perf_counter()
    vis.insertion_sort()
    end = time.perf_counter()
    print(f"Insertion sort algo excecutes in {end-start:.4f} sec")
    start = time.perf_counter()
    vis.selection_sort()
    end = time.perf_counter()
    print(f"Selection sort algo excecutes in {end-start:.4f} sec")
    start = time.perf_counter()
    vis.shell_sort()
    end = time.perf_counter()
    print(f"Shell sort algo excecutes in {end-start:.4f} sec")


if __name__ == "__main__":
    # SortVisualizer(num_of_bars=1000, bar_width=0,
    #    sort_speed=0, max_bar_height=1000, visualize=False).quick_sort()
    test_time_exec()
