import math


class Avion:

    def __init__(self, indicatif, x, y, altitude, vitesse, cap, carburant):
        self.indicatif = indicatif
        self.x = x
        self.y = y
        self.altitude = altitude
        self.vitesse = vitesse
        self.cap = cap
        self.carburant = carburant
        self.est_atterri = False

    def changer_cap(self, nouveau_cap):
        self.cap = nouveau_cap % 360

    def changer_vitesse(self, nouvelle_vitesse):
        if nouvelle_vitesse > 0:
            self.vitesse = nouvelle_vitesse

    def monter(self, hauteur):
        if hauteur > 0:
            self.altitude = self.altitude + hauteur

    def descendre(self, hauteur):
        if hauteur > 0 and self.altitude - hauteur >= 0:
            self.altitude = self.altitude - hauteur

    def avancer(self, temps):
        if self.est_atterri:
            return

        angle = math.radians(self.cap)

        self.x = self.x + self.vitesse * math.cos(angle) * temps
        self.y = self.y + self.vitesse * math.sin(angle) * temps

        self.carburant = self.carburant - 0.1 * temps

        if self.carburant < 0:
            self.carburant = 0

    def atterrir(self):
        self.est_atterri = True
        self.altitude = 0
        self.vitesse = 0