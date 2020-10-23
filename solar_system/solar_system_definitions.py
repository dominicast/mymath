
# Bodies

NAME = 'name'
MASS = 'mass'  # [kg]
RADIUS = 'radius'  # [m]
COLOR = 'color'
MEAN_DISTANCE = 'mean-distance'  # [AU]
ORDER_NR = 'order-nr'

SUN = {
    NAME: 'Sun',
    MASS: 1.9885 * pow(10, 30),
    RADIUS: 6.957 * pow(10, 8),
    COLOR: (1., 0.847, 0.035),
    MEAN_DISTANCE: 0,
    ORDER_NR: 0
}

MERCURY = {
    NAME: 'Mercury',
    MASS: 3.302 * pow(10, 23),
    RADIUS: 2.44 * pow(10, 6),
    COLOR: (0.675, 0.592, 0.416),
    MEAN_DISTANCE: 0.387,
    ORDER_NR: 1
}

VENUS = {
    NAME: 'Venus',
    MASS: 4.8685*pow(10, 24),
    RADIUS: 6.05184 * pow(10, 6),
    COLOR: (0.894, 0.773, 0.651),
    MEAN_DISTANCE: 0.723,
    ORDER_NR: 2
}

EARTH = {
    NAME: 'Earth',
    MASS: 5.97219 * pow(10, 24),
    RADIUS: 6.37101 * pow(10, 6),
    COLOR: (0.259, 0.424, 0.996),
    MEAN_DISTANCE: 1,
    ORDER_NR: 3
}

MOON = {
    NAME: 'Moon',
    MASS: 7.349 * pow(10, 22) ,
    RADIUS: 1.73753 * pow(10, 6),
    COLOR: (0.588, 0.58, 0.584),
    MEAN_DISTANCE: 1,
    ORDER_NR: 3
}

MARS = {
    NAME: 'Mars',
    MASS: 6.4171 * pow(10, 23),
    RADIUS: 3.38992 * pow(10, 6),
    COLOR: (0.941, 0.294, 0.114),
    MEAN_DISTANCE: 1.524,
    ORDER_NR: 4
}

JUPITER = {
    NAME: 'Jupiter',
    MASS: 1.89813 * pow(10, 27),
    RADIUS: 6.9911 * pow(10, 7),
    COLOR: (0.792, 0.51, 0.416),
    MEAN_DISTANCE: 5.203,
    ORDER_NR: 5
}

SATURN = {
    NAME: 'Saturn',
    MASS: 5.6834 * pow(10, 26),
    RADIUS: 5.8232 * pow(10, 7),
    COLOR: (0.706, 0.655, 0.388),
    MEAN_DISTANCE: 9.582,
    ORDER_NR: 6
}

URANUS = {
    NAME: 'Uranus',
    MASS: 8.6813 * pow(10, 25),
    RADIUS: 2.5362 * pow(10, 7),
    COLOR: (0.749, 0.902, 0.918),
    MEAN_DISTANCE: 19.20,
    ORDER_NR: 7
}

NEPTUNE = {
    NAME: 'Neptune',
    MASS: 1.024 * pow(10, 26),
    RADIUS: 2.4624 * pow(10, 7),
    COLOR: (0.239, 0.267, 0.62),
    MEAN_DISTANCE: 30.05,
    ORDER_NR: 8
}


# Initial conditions 17.10.2013 16:00

X = 'x'; Y = 'y'; Z = 'z';
VX = 'vx'; VY = 'vy'; VZ = 'vz';

SUN_IC = {
    X: 0,
    Y: 0,
    Z: 0,
    VX: 0,
    VY: 0,
    VZ: 0
}

MERCURY_IC = {
    X: 2.699256202625721 * pow(10, -1),
    Y: -2.945510912763388 * pow(10, -1),
    Z: -3.696675812633399 * pow(10, -4),
    VX: 1.561896404958095 * pow(10, -2),
    VY: 2.169157526816811 * pow(10, -2),
    VZ: 1.551833430476102 * pow(10, -3)
}

VENUS_IC = {
    X: 5.464852488455190 * pow(10, -1),
    Y: -4.783861666843854 * pow(10, -1),
    Z: 4.798888564017594 * pow(10, -2),
    VX: 1.318627597778329 * pow(10, -2),
    VY: 1.516700055825804 * pow(10, -2),
    VZ: 2.662965477224826 * pow(10, -4)
}

EARTH_IC = {
    X: 9.770505872741465 * pow(10, -1),
    Y: 1.690040669781609 * pow(10, -1),
    Z: 9.843601704544269 * pow(10, -2),
    VX: -3.077197091901566 * pow(10, -3),
    VY: 1.692320172129821 * pow(10, -2),
    VZ: -1.383397601779740 * pow(10, -3)
}

MOON_IC = {
    X: 9.795481265482870 * pow(10, -1),
    Y: 1.687280949525631 * pow(10, -1),
    Z: 9.884749180681386 * pow(10, -2),
    VX: -2.977622074551740 * pow(10, -3),
    VY: 1.750905810358991 * pow(10, -2),
    VZ: -1.455473815404281 * pow(10, -3)
}

MARS_IC = {
    X: -4.839729488908665 * pow(10, -1),
    Y: 1.560630802450471 * pow(10, 0),
    Z: -9.913374596063972 * pow(10, -2),
    VX: -1.249711683427429 * pow(10, -2),
    VY: -3.172037129830012 * pow(10, -3),
    VZ: -1.047799161775436 * pow(10, -3)
}

JUPITER_IC = {
    X: 5.653696041446783 * pow(10, -1),
    Y: 5.126945373315730 * pow(10, 0),
    Z: -2.563779438429464 * pow(10, -1),
    VX: -7.477161414122874 * pow(10, -3),
    VY: 1.157735522887552 * pow(10, -3),
    VZ: -7.304406745079823 * pow(10, -4)
}

SATURN_IC = {
    X: -8.646714279106760 * pow(10, 0),
    Y: -4.738275608763417 * pow(10, 0),
    Z: -2.658804447914820 * pow(10, -1),
    VX: 2.359453009042619 * pow(10, -3),
    VY: -4.813470722521699 * pow(10, -3),
    VZ: 4.882764918036705 * pow(10, -4)
}

URANUS_IC = {
    X: 1.988385163968572 * pow(10, 1),
    Y: -1.405926882792088 * pow(10, 0),
    Z: 2.057920386344378 * pow(10, 0),
    VX: 2.155405725825843 * pow(10, -4),
    VY: 3.747819746273274 * pow(10, -3),
    VZ: -1.826727345802505 * pow(10, -4)
}

NEPTUNE_IC = {
    X: 2.259965604627899 * pow(10, 1),
    Y: -1.941340140795343 * pow(10, 1),
    Z: 3.357236604763358 * pow(10, 0),
    VX: 2.026226391500671 * pow(10, -3),
    VY: 2.404346714025546 * pow(10, -3),
    VZ: -1.197451013633338 * pow(10, -5)
}
