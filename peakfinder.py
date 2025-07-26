
class PeakFinder:
    initial_wrist_point = (0, 0)
    first_point_x = 0
    first_point_y = 100000000
    second_point_x = 0
    second_point_y = 0
    third_point_x = 0
    third_point_y = 0

    max_head_y = -1000000000
    min_head_y = 1000000000

    found = False
    done_backswing = False
    def __init__(self, threshold):
        self.threshold = threshold
        self.count = 0

    def find_peak(self, p1x, p1y, p2x, p2y, p3x, p3y, init_x, init_y):

        if p1y <= self.first_point_y and self.found == False:
            # Update coordinates for the most recent frame
            self.initial_wrist_point = init_x, init_y
            self.first_point_y = p1y
            self.first_point_x = p1x
            self.second_point_y = p2y
            self.second_point_x = p2x
            self.third_point_y = p3y
            self.third_point_x = p3x
            self.count = 0  # Reset count if the condition is met
        elif p1y >= self.first_point_y and self.found == False:
            # If the condition is not met, increase count
            self.count += 1

            # Check if count has reached the threshold

            if self.count >= self.threshold and self.initial_wrist_point[1] - self.first_point_y >= 200:
                self.found = True
                print(self.found)
            if self.count >= self.threshold and self.initial_wrist_point[1] - self.first_point_y <= 200:
                self.count = 0

    def find_range(self, new_head_y, wrist_y, hip_y):
        if wrist_y < hip_y and self.found == True:
            self.done_backswing = True
        if self.done_backswing == False:
            if new_head_y <= self.min_head_y:
                self.min_head_y = new_head_y
            if new_head_y >= self.max_head_y:
                self.max_head_y = new_head_y


