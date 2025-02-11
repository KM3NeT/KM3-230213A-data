from math import acos, pi, sqrt, tan, sin

# reference values at 460 nm
water_index           = 1.3499
dndl                  = 0.0298
c_light               = 299792458*1e-9
v_light               = c_light/(water_index + dndl)
cos_cherenkov_angle   = 1.0 / water_index
cherenkov_angle       = acos( cos_cherenkov_angle )

class Cherenkov  :

    "Cherenkov photon properties for a trk and a position"

    def __init__ ( self, trk, pos ) :

        v = pos - trk.pos 
        l = v.dot( trk.dir )
        k2 = v.dot(v) - l*l

        # distances and arrival time, assuming photon was emitted under theta_c
        self.d_closest = sqrt( k2 ) if k2>0 else 0
        self.d_photon  = self.d_closest/ sin(cherenkov_angle )
        self.d_trk   = l - self.d_closest / tan( cherenkov_angle )
        self.time      = trk.t + self.d_trk / c_light + self.d_photon /v_light



def emission_points( trk, hit , both = False ) :
    """
     Returns the emission point(s) of a trk for a given hit. 
    
     Here, it is not assumed the light is emitted under the cherenkov angle
     from the track. We simply compute where the photon must have been emitted 
     to reach the hit at the given time.

     In general, there are two solutions, but the later one is found to
     be almost always the correct one.
     """

    q = hit.pos - trk.pos
    T = hit.t - trk.t

    # solve the quadratic equation
    A = v_light**2 / c_light**2 -1  # note A<0
    B = 2 * q.dot( trk.dir ) - 2 * T * v_light**2 / c_light 
    C = T**2 * v_light**2 - q.dot(q)

    D = B**2 - 4 * A * C

    if D < 0 : return []
    
    t1 = ( -B + D**0.5 ) / (2* A) # earlier: it seems this is always the ghost
    t2 = ( -B - D**0.5 ) / (2* A) # later

    if both :
        return [t1, t2]
    return [t2]