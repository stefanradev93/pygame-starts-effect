import pygame
import math
import sys
import random

# Global settings with a short name
_s = {
    'fps': 60,
    'clock': None,
    'screen': None,
    'running': True,
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'screensize': (1280, 640),
    'caption': 'Stars',
    'nbgstars': 200,
    'stars': []
}


def processEvents():
    """The event loop in a separate function."""

    for event in pygame.event.get():
        # Close window event
        if event.type == pygame.QUIT:
            _s['running'] = False
            pygame.quit()
            sys.exit(0)
        # Keyboard events
        if event.type == pygame.KEYDOWN:
            # If space pressed, generate star
            if event.key == pygame.K_SPACE:
                # Generate star and append it to stars list
                _s['stars'].append(createStar())
                # Play some music?


def initPyGame():
    """Initializer for pygame."""

    pygame.init()
    _s['screen'] = pygame.display.set_mode(_s['screensize'])
    pygame.display.set_caption(_s['caption'])
    _s['clock'] = pygame.time.Clock()


def drawBackground():
    """Fills screen."""

    _s['screen'].fill(_s['black'])


def createBackgroundStars(n):
    """Create stars at random positions."""

    return [
    [random.randint(0, _s['screensize'][0]), random.randint(0, _s['screensize'][1])]
    for _ in range(n)
    ]


def drawBackgroundStars(stars):
    """Creates and displays stars."""

    # Draw all background stars
    for star in stars:
        # A line with same start and end coords is a point
        pygame.draw.line(_s['screen'], _s['white'], (star[0], star[1]), (star[0], star[1]))
        # Update position of each star
        star[1] = star[1] - 1
        # If horizontal position of star reached zero, remove and place and bottom
        if star[1] < 0:
            star[0] = random.randint(0, _s['screensize'][0])
            star[1] = _s['screensize'][1]


def createStar():
    """Creates a star of with n jags of length length."""

    # Generate random coordinates for center of star
    cx = random.randint(0, _s['screensize'][0])
    cy = random.randint(0, _s['screensize'][1])

    # Generate random color for star
    color = [random.randint(0, 255) for _ in range(3)]

    # Generate random rotation, length and number of jots
    n = random.randint(5, 12)
    rotation = random.randint(0, 360)
    length = random.randint(50, 150)

    # Represent star as a dictionary and return it
    return {'cx': cx, 'cy': cy, 'color': color,
            'n': n, 'length': length, 'rotation': rotation}


def drawSingleStar(star):
    """Draws a single star with parameters specified by the star dict"""

    # Define an empty points list and create points
    points = []
    for i in range(star['n'] * 2):

        # Get length of star, note, that we loop
        # twice the number n, since each star needs
        # 2 * n points (one lower, one upper)
        r = star['length']
        if i % 2 == 0:
            # If we are here, this is the lower point of the star
            r = r // 3
        # Compute angle and add the rotation degree
        angle = (i * math.pi / star['n']) + (star['rotation'] * math.pi / 360)
        # Calculate coordinates of rotated point and add to list
        x = star['cx'] + int(math.cos(angle) * r)
        y = star['cy'] + int(math.sin(angle) * r)
        points.append([x, y])

    # Draw the star
    pygame.draw.polygon(_s['screen'], star['color'], points)


def drawStars():
    """Draws all foreground stars, if any, and channge parameters."""

    # Keep track of disappeared stars
    starsToRemove = []

    # Draw all stars
    for i, star in enumerate(_s['stars']):
        drawSingleStar(star)
        # Change rotation and length
        star['rotation'] += 1
        star['length'] -= 1
        # Mark stars that have disappeared for removal
        if star['length'] <= 0:
            starsToRemove.append(i)

    # Remove disappared stars
    _s['stars'] = [star for i, star in enumerate(_s['stars']) if i not in starsToRemove]


def update():
    """Flips screen and controls framerate."""

    pygame.display.flip()
    _s['clock'].tick(_s['fps'])


if __name__ == "__main__":

    initPyGame()
    stars = createBackgroundStars(_s['nbgstars'])
    while _s['running']:
        processEvents()
        drawBackground()
        drawBackgroundStars(stars)
        drawStars()
        update()
