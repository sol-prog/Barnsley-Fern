"""Barnsley Fern fractal generation"""
import random
import array
from PIL import Image

class Barnsley:
    """Generate Barnsley like fractals using affine transforms"""
    def __init__(self, nr_points, coefficients="fern"):
        self.nr_points = nr_points

        #Initial (starting point)
        self.x = 0.0
        self.y = 0.0

        # Store the fractal points
        self.point_x = []
        self.point_y = []

        # Select the set of coefficients to use
        if coefficients == "fern":
            self.probability_factors = [0.01, 0.85, 0.07, 0.07]
            self.a = [0, 0.85, 0.20, -0.15]
            self.b = [0, 0.04, -0.26, 0.28]
            self.c = [0, -0.04, 0.23, 0.26]
            self.d = [0.16, 0.85, 0.22, 0.24]
            self.e = [0, 0, 0, 0]
            self.f = [0, 1.6, 1.6, 0.44]            
        elif coefficients == "tree":
            self.probability_factors = [0.05, 0.4, 0.4, 0.15]        
            self.a = [0.0, 0.42, 0.42, 0.1]
            self.b = [0.0, -0.42, 0.42, 0.0]
            self.c = [0.0, 0.42, -0.42, 0.0]
            self.d = [0.5, 0.42, 0.42, 0.1]
            self.e = [0.0, 0.0, 0.0, 0.0]
            self.f = [0.0, 0.2, 0.2, 0.2]
        elif coefficients == "sierpinsky":
            self.probability_factors = [0.33, 0.33, 0.34]        
            self.a = [0.5, 0.5, 0.5]
            self.b = [0.0, 0.0, 0.0]
            self.c = [0.0, 0.0, 0.0]
            self.d = [0.5, 0.5, 0.5]
            self.e = [1.0, 1.0, 50.0]
            self.f = [1.0, 50.0, 50.0]
        elif coefficients == "custom":
            self.probability_factors = [0.04, 0.8, 0.08, 0.08]
            self.a = [0, 0.7, 0.20, -0.2]
            self.b = [0, 0.035, -0.29, 0.28]
            self.c = [0, -0.04, 0.23, 0.26]
            self.d = [0.16, 0.8, 0.22, 0.25]
            self.e = [0, 0, 0, 0]
            self.f = [0, 1.6, 1.6, 0.44]


        self.nr_transforms = len(self.probability_factors)

        # Cumulative sum of the probabilty factors,
        # this defines the intervals corresponding to each transform
        self.cumulative_probabilities = [0] * (self.nr_transforms + 1)
        for i in range(1, len(self.cumulative_probabilities)):
            self.cumulative_probabilities[i] = self.cumulative_probabilities[i - 1] + \
                                               self.probability_factors[i - 1]

    def select_transform(self):
        """Randomly select an affine transform"""
        rnd = random.random()
        for i in range(self.nr_transforms):
            if self.cumulative_probabilities[i] <= rnd <= self.cumulative_probabilities[i + 1]:
                self.current_transform = i
                break

    def next_point(self):
        """Get the next point of the fractal"""
        self.select_transform()
        x_new = self.a[self.current_transform] * self.x + self.b[self.current_transform] * self.y + self.e[self.current_transform]
        y_new = self.c[self.current_transform] * self.x + self.d[self.current_transform] * self.y + self.f[self.current_transform]
        self.x = x_new
        self.y = y_new
        self.point_x.append(x_new)
        self.point_y.append(y_new)

    def generate_points(self):
        """Generate all the fractal points"""
        for _ in range(self.nr_points):
            self.next_point()

        # Bounding box for the fractal
        self.x_min = min(self.point_x)
        self.x_max = max(self.point_x)
        self.y_min = min(self.point_y)
        self.y_max = max(self.point_y)


def main():
    """Generate and the save as a PNG image a Barnsley Fern"""

    # Initialize the fractal data
    nr_points = 100000
    fern = Barnsley(nr_points)
    fern.generate_points()

    # Define the image size and scale factor for the fractal data
    width, height = 500, 500
    scale = min([height/(fern.y_max - fern.y_min), width/(fern.x_max - fern.x_min)]) * 0.9

    # Initialize an array that will store the image pixel data
    image_data = array.array('B', [255, 255, 255] * width * height)

    # For every point of the fractal data, transform the point in the image space
    # and fill the pixel color
    for i in range(nr_points):
        x = int((fern.point_x[i] - fern.x_min) * scale) + int((width - (fern.x_max - fern.x_min) * scale)/2)
        y = -int((fern.point_y[i] - fern.y_min) * scale) - int((height - (fern.y_max - fern.y_min) * scale)/2)

        index = 3 * (y * width + x)
        image_data[index] = 0
        image_data[index + 1] = 255
        image_data[index + 2] = 0

    # Show and save the image
    img = Image.frombytes("RGB", (width, height), image_data.tobytes())
    img.show("Barnsley's Fern")
    img.save("barnsley_fern.png")

if __name__ == "__main__":
    # execute only if run as a script
    main()
