
# File name: Simulation.py

from ursina import *

class Sky(Entity):
    def __init__(self):
        super().__init__(
            model = 'sphere',
            texture = 'models/StarsMap_2500x1250.jpg',
            parent = scene,
            scale = 10000,
            double_sided = True
        )

app = Ursina()

window.title = 'Planet Simulation'                # The window title


def update():
   
    for planet, planet_ in zip(planets, planets_):
        planet_.x,planet_.y = planet.update_position(planets)
        points = planet.draw()
        if  points is not None and len(points)>2:
            orbits = Entity(model=Mesh(vertices=points, mode='line'))
    
# Our Planet class -- for making planets.
class Planet():
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day

    def __init__(self, name, x, y, mass):
        self.name = name 
        self.x = x
        self.y = y
        self.mass = mass
        self.sun = False
        self.orbit = []
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def load(self):
        x = self.x * self.SCALE 
        y = self.y * self.SCALE

        if self.sun:
            return Entity(model='sphere', texture='models/Sun.jpg',scale=90)
        elif self.name =='Mercury':
            return Entity(model='models/'+self.name+'.glb',position=(x,y),scale =0.033/2 )
        elif self.name =='Venus':
            return Entity(model='models/'+self.name+'.glb',position=(x,y),scale =0.09/2 )
        elif self.name =='Earth':
            return Entity(model='models/'+self.name+'.glb',position=(x,y),scale =0.1/2 )
        elif self.name =='Mars':
            return Entity(model='models/'+self.name+'.glb',position=(x,y),scale =0.05/2 )
    
    def draw(self):
        x = self.x * self.SCALE 
        y = self.y * self.SCALE 

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
	            x, y = point
	            x = x * self.SCALE
	            y = y * self.SCALE
	            updated_points.append([x, y, 0])
            return updated_points
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
	        self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
	        if self == planet:
		        continue
			 
	        fx, fy = self.attraction(planet)
	        total_fx += fx
	        total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
        return self.x * self.SCALE , self.y * self.SCALE


sky = Sky()

sun = Planet('Sun',0,0, 1.98892 * 10**30)
sun.sun = True
sun_ = sun.load()

mercury = Planet('Mercury',0.387 * Planet.AU,10, 3.30 * 10**23)
mercury_ = mercury.load()
mercury.y_vel = -47.4 * 1000

venus = Planet('Venus',0.723 * Planet.AU,0,  4.8685 * 10**24)
venus_  = venus.load()
venus.y_vel = -35.02 * 1000

earth = Planet('Earth',-1 * Planet.AU,0, 5.9742 * 10**24 )
earth_ = earth.load()
earth.y_vel = 29.783 * 1000 

mars = Planet('Mars',-1.524 * Planet.AU,0, 6.39 * 10**23)
mars_ = mars.load()
mars.y_vel = 24.077 * 1000

planets = [sun, mercury, venus, earth, mars]
planets_ = [sun_, mercury_, venus_, earth_, mars_]

EditorCamera()



app.run()
