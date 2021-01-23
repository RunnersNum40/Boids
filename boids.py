from vectors import Vector
from screen import Screen
from random import randrange, random
import math

class Boid:
    def __init__(self, pos=(0, 0), velo=(1, 1), weights=[0.1, 0.1, 0.1], visual_range=100, species=0):
        self.pos = Vector(pos)
        self.velo = Vector(velo)
        if self.velo.magnitude == 0:
            self.velo = Vector(1, 1)

        self.weights = weights
        self.visual_range = visual_range

        self.species = species

    def update(self, flock, box):
        neighbors = [b for b in flock if abs(b.pos-self.pos) <= self.visual_range and self.species == b.species]
        if len(neighbors) > 0:
            # Because averaging angles is odd I represent each angle as a vector and find the direction of the average vector
            cohere_target = self.cohere(list(neighbors))
            cohere_direction = (cohere_target-self.pos).angle
            cohere_vector = Vector.from_dir(cohere_direction, self.weights[0])

            seperation_direction = self.seperation(list(neighbors))
            seperation_vector = Vector.from_dir(seperation_direction, self.weights[1])

            alignment_direction = self.alignment(list(neighbors))
            alignment_vector = Vector.from_dir(alignment_direction, self.weights[2])

            current = Vector.from_dir(self.velo.angle, 1)

            avg = (cohere_vector+seperation_vector+alignment_vector+current)/(sum(self.weights)+1)

            self.new_velo = Vector.from_dir(avg.angle, self.velo.magnitude)

            self.new_velo.vec[0] -= self.pos.vec[0]/(box[0]//2)/30
            self.new_velo.vec[1] -= self.pos.vec[1]/(box[1]//2)/30

    def cohere(self, neighbors):
        """Return the average position of all neighbors"""
        neighbors = [p.pos for p in neighbors]
        center = sum(neighbors, Vector(0, 0))/len(neighbors)
        return center

    def seperation(self, neighbors):
        """Return the angle away from the closest neighbor"""
        closest = min(neighbors, key=lambda n: abs(n.pos-self.pos))
        away = (self.pos-closest.pos).angle
        return away

    def alignment(self, neighbors):
        """Return the average angle of all neighbors"""
        angle_vectors = [Vector.from_dir(b.velo.angle, 1) for b in neighbors]
        alignment_direction = (sum(angle_vectors, Vector(0, 0))/len(angle_vectors)).angle
        return alignment_direction

    def move(self, move_factor, box):
        self.velo = getattr(self, "new_velo", self.velo)
        self.velo.magnitude = (self.velo.magnitude-1)/2+1
        self.pos += self.velo*move_factor

        # Clamp the position inside the screen
        self.pos.vec[0] = min(max(self.pos.vec[0], -box[0]//2+1), box[0]//2-1)
        self.pos.vec[1] = min(max(self.pos.vec[1], -box[1]//2+1), box[1]//2-1)


class Flock:
    def __init__(self, instances, screen=None):
        self.boids = [Boid((randrange(-300, 301), randrange(-300, 301)), (random()*2-1, random()*2-1), [0.2, 0.25, 0.2]) for _ in range(instances)]
        if screen == None:
            self.screen = Screen(1380, 800, 120)

    def tick(self):
        for n, boid in enumerate(self.boids):
            boid.update(self.boids[:n]+self.boids[n+1:], (self.screen.width, self.screen.height))

        for boid in self.boids:
            boid.move(1, (self.screen.width, self.screen.height))

        self.screen.draw(self.boids)

    def main_loop(self, max_ticks=-1):
        nticks = 0
        while max_ticks < 0 or nticks < max_ticks:
            self.tick()
            nticks += 1

if __name__ == '__main__':
    boids = Flock(30)
    boids.main_loop(max_ticks=7200)