from avion import Avion
import math
import random


class Simulation:

    def __init__(self):
        self.avions = []
        self.score = 0
        self.temps = 0
        self.difficulte = 1

        self.compteur_generation = 0
        self.compteur_evenement = 0

        self.dernier_evenement = "Aucun événement"
        self.partie_terminee = False
        self.victoire = False
        self.message_fin = ""

        self.zone_atterrissage_x = 500
        self.zone_atterrissage_y = 500
        self.taille_zone_atterrissage = 50

    def ajouter_avion(self, avion):
        self.avions.append(avion)

    def mettre_a_jour(self, temps):
        if self.partie_terminee:
            return

        self.temps = self.temps + temps
        self.compteur_generation = self.compteur_generation + temps
        self.compteur_evenement = self.compteur_evenement + temps

        for avion in self.avions:
            avion.avancer(temps / 3600)

            # Un avion qui sort du radar provoque une défaite
            if (
                avion.x < 0
                or avion.x > 1000
                or avion.y < 0
                or avion.y > 1000
            ):
                self.partie_terminee = True
                self.victoire = False
                self.message_fin = (
                    avion.indicatif + " est sorti du radar !"
                )

        # Vérification des collisions
        if len(self.detecter_collisions()) > 0:
            self.partie_terminee = True
            self.victoire = False
            self.message_fin = "Collision entre deux avions !"

        # Difficulté progressive
        if self.temps >= self.difficulte * 30:
            self.difficulte = self.difficulte + 1

        # Apparition de nouveaux avions
        temps_apparition = max(8, 20 - self.difficulte * 2)

        if self.compteur_generation >= temps_apparition:
            self.generer_avion()
            self.compteur_generation = 0

        # Événement aléatoire
        if self.compteur_evenement >= 25:
            self.evenement_aleatoire()
            self.compteur_evenement = 0

        # Vérification du carburant
        for avion in self.avions:
            if avion.carburant <= 0 and not avion.est_atterri:
                self.partie_terminee = True
                self.victoire = False
                self.message_fin = (
                    avion.indicatif + " n'a plus de carburant !"
                )

    def generer_avion(self):
        indicatif = "AF" + str(random.randint(1000, 9999))

        cote = random.randint(0, 3)
        altitude = random.randint(2000, 8000)
        vitesse = random.randint(250, 500)
        carburant = random.randint(50, 100)

        if cote == 0:
            x = 50
            y = random.randint(100, 900)
            cap = 0

        elif cote == 1:
            x = 950
            y = random.randint(100, 900)
            cap = 180

        elif cote == 2:
            x = random.randint(100, 900)
            y = 50
            cap = 90

        else:
            x = random.randint(100, 900)
            y = 950
            cap = 270

        nouvel_avion = Avion(
            indicatif,
            x,
            y,
            altitude,
            vitesse,
            cap,
            carburant
        )

        self.ajouter_avion(nouvel_avion)

    def evenement_aleatoire(self):
        if len(self.avions) == 0:
            self.dernier_evenement = "Aucun avion disponible"
            return

        avion = random.choice(self.avions)

        if avion.est_atterri:
            self.dernier_evenement = "Aucun événement"
            return

        evenement = random.randint(1, 3)

        if evenement == 1:
            avion.changer_vitesse(
                max(150, avion.vitesse - 100)
            )
            self.dernier_evenement = (
                avion.indicatif + " : vitesse réduite"
            )

        elif evenement == 2:
            avion.descendre(500)
            self.dernier_evenement = (
                avion.indicatif + " : perte d'altitude"
            )

        else:
            nouveau_cap = avion.cap + random.choice([-30, 30])
            avion.changer_cap(nouveau_cap)
            self.dernier_evenement = (
                avion.indicatif + " : changement de cap"
            )

    def detecter_collisions(self):
        collisions = []

        for i in range(len(self.avions)):
            for j in range(i + 1, len(self.avions)):

                avion1 = self.avions[i]
                avion2 = self.avions[j]

                if avion1.est_atterri or avion2.est_atterri:
                    continue

                distance = math.sqrt(
                    (avion1.x - avion2.x) ** 2
                    + (avion1.y - avion2.y) ** 2
                )

                difference_altitude = abs(
                    avion1.altitude - avion2.altitude
                )

                if distance < 50 and difference_altitude < 300:
                    collisions.append((avion1, avion2))

        return collisions

    def avion_dans_zone_atterrissage(self, avion):
        distance = math.sqrt(
            (avion.x - self.zone_atterrissage_x) ** 2
            + (avion.y - self.zone_atterrissage_y) ** 2
        )

        return distance <= self.taille_zone_atterrissage

    def atterrir_avion(self, avion):
        if self.partie_terminee:
            return False

        if self.avion_dans_zone_atterrissage(avion):

            if avion.altitude <= 100:

                avion.atterrir()

                self.score = self.score + 100

                # Si tous les avions sont posés,
                # on peut considérer la partie gagnée.
                avions_actifs = [
                    a for a in self.avions
                    if not a.est_atterri
                ]

                if len(avions_actifs) == 0:
                    self.partie_terminee = True
                    self.victoire = True
                    self.message_fin = "Tous les avions sont atterris !"

                return True

        return False

    def afficher_avions(self):
        for avion in self.avions:
            print(
                avion.indicatif,
                "- Position :",
                round(avion.x, 2),
                round(avion.y, 2),
                "- Altitude :",
                avion.altitude,
                "m",
                "- Vitesse :",
                avion.vitesse,
                "km/h"
            )