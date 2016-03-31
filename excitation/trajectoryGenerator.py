import numpy as np

class TrajectoryGenerator(object):
    '''
        pulsating trajectory generator for one joint using fourier series from Swers, Gansemann (1997)
        gives values for one time instant at the current time
    '''
    def __init__(self, dofs):
        self.dofs = dofs
        self.oscillators = list()

        #TODO: these are just some values, get them from optimzation or outside
        self.w_f_global = 2.0
        a = [[-0.2], [0.5], [-0.8], [0.5], [1], [-0.7], [-0.8]]
        b = [[0.9], [0.9], [1.5], [0.8], [1], [1.3], [0.8]]
        q = [10, 50, -80, -25, 50, 0, -15]
        nf = [1,1,1,1,1,1,1]

        for i in range(0, dofs):
            self.oscillators.append(OscillationGenerator(w_f = self.w_f_global, a = np.array(a[i]),
                                                         b = np.array(b[i]), q0 = q[i], nf = nf[i], use_deg = True
                                                        )
                                   )

    def getAngle(self, dof):
        return self.oscillators[dof].getAngle(self.time)

    def getVelocity(self, dof):
        return self.oscillators[dof].getVelocity(self.time)

    def getAcceleration(self, dof):
        return self.oscillators[dof].getAcceleration(self.time)

    def getPeriodLength(self):
        '''return period length of oscillation in seconds'''
        return 2*np.pi/self.w_f_global

    def setTime(self, time):
        '''set current time in seconds'''
        self.time = time

class OscillationGenerator(object):
    def __init__(self, w_f, a, b, q0, nf, use_deg):
        '''
        generate periodic oscillation from fourier series

        - w_f is the global pulsation (frequency is w_f / 2pi)
        - a and b are (arrays of) amplitudes of the sine/cosine
          functions for each joint
        - q0 is the joint angle offset (center of pulsation)
        - nf is the desired amount of coefficients for this fourier series
        '''
        self.w_f = float(w_f)
        self.a = a
        self.b = b
        self.q0 = float(q0)
        self.nf = nf
        self.use_deg = use_deg

    def getAngle(self, t):
        #- t is the current time
        q = 0
        for l in range(1, self.nf+1):
            q = (self.a[l-1]/(self.w_f*l))*np.sin(self.w_f*l*t) - \
                 (self.b[l-1]/(self.w_f*l))*np.cos(self.w_f*l*t)
        if self.use_deg:
            q = np.rad2deg(q)
        q += self.nf*self.q0
        return q

    def getVelocity(self, t):
        dq = 0
        for l in range(1, self.nf+1):
            dq += self.a[l-1]*np.cos(self.w_f*l*t) + \
                  self.b[l-1]*np.sin(self.w_f*l*t)
        if self.use_deg:
            dq = np.rad2deg(dq)
        return dq

    def getAcceleration(self, t):
        ddq = 0
        for l in range(1, self.nf+1):
            ddq += -self.a[l-1]*self.w_f*l*np.sin(self.w_f*l*t) + \
                  self.b[l-1]*self.w_f*l*np.cos(self.w_f*l*t)
        if self.use_deg:
            ddq = np.rad2deg(ddq)
        return ddq

