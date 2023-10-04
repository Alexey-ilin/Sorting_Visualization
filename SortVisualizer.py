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

    def bubble_sort(self):
        for i in range(len(self.bars)):
            for j in range(len(self.bars) - 1 - i):
                if self.bars[j] > self.bars[j + 1]:
                    self.bars[j], self.bars[j +
                                            1] = self.bars[j + 1], self.bars[j]
                    self._draw_bars()
                    pygame.time.wait(self.sort_speed)

    """Simple instertion sort algorithm"""

    def insertion_sort(self):
        for i in range(1, len(self.bars)):
            key = self.bars[i]
            j = i-1
            while j >= 0 and key < self.bars[j]:
                self.bars[j+1] = self.bars[j]
                j -= 1
                self._draw_bars()
                pygame.time.wait(self.sort_speed)
            self.bars[j+1] = key

    def merge_sort(self):
        self._merge_sort_helper()

    def _merge_sort_helper(self, start_idx=None, end_idx=None):
        if start_idx == None:
            start_idx, end_idx = 0, len(self.bars)-1
        if end_idx-start_idx > 0:
            mid_idx = (end_idx+start_idx)//2
            self._merge_sort_helper(start_idx, mid_idx)
            self._merge_sort_helper(mid_idx+1, end_idx)
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
            pygame.time.wait(self.sort_speed)


if __name__ == "__main__":
    SortVisualizer(num_of_bars=200, bar_width=3, sort_speed=10).merge_sort()
