from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QBrush, QPen, QColor
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpinBox,
    QGroupBox
)


class Radar(QWidget):

    def __init__(
        self,
        simulation,
        interface
    ):

        super().__init__()

        self.simulation = simulation

        self.interface = interface

        self.setMinimumSize(
            800,
            600
        )

    def actualiser(self):

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        # Fond
        painter.fillRect(
            self.rect(),
            QBrush(
                QColor("#07111f")
            )
        )

        largeur = self.width()

        hauteur = self.height()

        # Grille
        painter.setPen(
            QPen(
                QColor("#24405c")
            )
        )

        for x in range(
            0,
            largeur,
            50
        ):

            painter.drawLine(
                x,
                0,
                x,
                hauteur
            )

        for y in range(
            0,
            hauteur,
            50
        ):

            painter.drawLine(
                0,
                y,
                largeur,
                y
            )

        # Zone d'atterrissage
        zone_x = (
            self.simulation.zone_atterrissage_x
        )

        zone_y = (
            self.simulation.zone_atterrissage_y
        )

        taille_zone = (
            self.simulation.taille_zone_atterrissage
        )

        zone_x = int(
            zone_x / 1000 * largeur
        )

        zone_y = int(
            zone_y / 1000 * hauteur
        )

        painter.setPen(
            QPen(
                QColor("#00ff88"),
                2
            )
        )

        painter.setBrush(
            QBrush(
                QColor("#123d2b")
            )
        )

        painter.drawEllipse(
            zone_x - taille_zone,
            zone_y - taille_zone,
            taille_zone * 2,
            taille_zone * 2
        )

        # Collisions
        collisions = (
            self.simulation.detecter_collisions()
        )

        avions_en_collision = []

        for avion1, avion2 in collisions:

            if avion1 not in avions_en_collision:

                avions_en_collision.append(
                    avion1
                )

            if avion2 not in avions_en_collision:

                avions_en_collision.append(
                    avion2
                )

        # Avions
        for avion in self.simulation.avions:

            if avion.est_atterri:

                continue

            avion_x = int(
                avion.x / 1000 * largeur
            )

            avion_y = int(
                avion.y / 1000 * hauteur
            )

            # Avion en collision
            if avion in avions_en_collision:

                painter.setPen(
                    QPen(
                        QColor("#ff3333"),
                        3
                    )
                )

                painter.setBrush(
                    QBrush(
                        QColor("#ff3333")
                    )
                )

            # Avion sélectionné
            elif (
                avion
                == self.interface.avion_selectionne
            ):

                painter.setPen(
                    QPen(
                        QColor("#ffff00"),
                        3
                    )
                )

                painter.setBrush(
                    QBrush(
                        QColor("#ffff00")
                    )
                )

            # Avion normal
            else:

                painter.setPen(
                    QPen(
                        QColor("#ffffff")
                    )
                )

                painter.setBrush(
                    QBrush(
                        QColor("#ffffff")
                    )
                )

            painter.drawEllipse(
                avion_x - 7,
                avion_y - 7,
                14,
                14
            )

            painter.setPen(
                QPen(
                    QColor("#ffffff")
                )
            )

            painter.drawText(
                avion_x + 10,
                avion_y,
                avion.indicatif
            )

    def mousePressEvent(
        self,
        event
    ):

        position_souris_x = (
            event.position().x()
        )

        position_souris_y = (
            event.position().y()
        )

        largeur = self.width()

        hauteur = self.height()

        avion_trouve = None

        for avion in self.simulation.avions:

            if avion.est_atterri:

                continue

            avion_x = (
                avion.x
                / 1000
                * largeur
            )

            avion_y = (
                avion.y
                / 1000
                * hauteur
            )

            distance = (
                (
                    position_souris_x
                    - avion_x
                ) ** 2
                +
                (
                    position_souris_y
                    - avion_y
                ) ** 2
            ) ** 0.5

            if distance < 20:

                avion_trouve = avion

                break

        if avion_trouve is not None:

            self.interface.selectionner_avion(
                avion_trouve
            )


class Interface(QWidget):

    def __init__(
        self,
        simulation
    ):

        super().__init__()

        self.simulation = simulation

        self.avion_selectionne = None

        self.setWindowTitle(
            "Simulateur de tour de contrôle"
        )

        self.resize(
            1200,
            750
        )

        # Titre
        titre = QLabel(
            "SIMULATEUR DE TOUR DE CONTRÔLE"
        )

        titre.setStyleSheet(
            "font-size: 20px;"
            "font-weight: bold;"
            "padding: 10px;"
        )

        # Radar
        self.radar = Radar(
            simulation,
            self
        )

        # Informations
        groupe_infos = QGroupBox(
            "Avion sélectionné"
        )

        self.infos = QLabel(
            "Cliquez sur un avion"
        )

        self.infos.setStyleSheet(
            "font-size: 14px;"
            "padding: 10px;"
        )

        infos_layout = QVBoxLayout()

        infos_layout.addWidget(
            self.infos
        )

        groupe_infos.setLayout(
            infos_layout
        )

        # Cap
        self.cap = QSpinBox()

        self.cap.setRange(
            0,
            359
        )

        self.cap.setSuffix(
            " °"
        )

        bouton_cap = QPushButton(
            "Changer le cap"
        )

        bouton_cap.clicked.connect(
            self.changer_cap
        )

        # Vitesse
        self.vitesse = QSpinBox()

        self.vitesse.setRange(
            1,
            1000
        )

        self.vitesse.setSuffix(
            " km/h"
        )

        bouton_vitesse = QPushButton(
            "Changer la vitesse"
        )

        bouton_vitesse.clicked.connect(
            self.changer_vitesse
        )

        # Altitude
        self.altitude = QSpinBox()

        self.altitude.setRange(
            0,
            12000
        )

        self.altitude.setSuffix(
            " m"
        )

        bouton_montee = QPushButton(
            "Monter +500 m"
        )

        bouton_montee.clicked.connect(
            self.monter
        )

        bouton_descente = QPushButton(
            "Descendre -500 m"
        )

        bouton_descente.clicked.connect(
            self.descendre
        )

        # Atterrissage
        bouton_atterrir = QPushButton(
            "Atterrir"
        )

        bouton_atterrir.clicked.connect(
            self.atterrir
        )

        # Alerte
        self.alerte = QLabel(
            "Aucune collision"
        )

        self.alerte.setStyleSheet(
            "font-size: 16px;"
            "font-weight: bold;"
            "padding: 10px;"
            "color: #00ff88;"
        )

        # Difficulté
        self.difficulte = QLabel(
            "Difficulté : 1"
        )

        self.difficulte.setStyleSheet(
            "font-size: 16px;"
            "font-weight: bold;"
            "padding: 10px;"
        )

        # Événement
        self.evenement = QLabel(
            "Événement : Aucun événement"
        )

        self.evenement.setWordWrap(
            True
        )

        self.evenement.setStyleSheet(
            "font-size: 14px;"
            "padding: 10px;"
        )

        # Commandes
        commandes = QVBoxLayout()

        commandes.addWidget(
            groupe_infos
        )

        commandes.addWidget(
            QLabel("Cap :")
        )

        commandes.addWidget(
            self.cap
        )

        commandes.addWidget(
            bouton_cap
        )

        commandes.addWidget(
            QLabel("Vitesse :")
        )

        commandes.addWidget(
            self.vitesse
        )

        commandes.addWidget(
            bouton_vitesse
        )

        commandes.addWidget(
            QLabel("Altitude :")
        )

        commandes.addWidget(
            self.altitude
        )

        commandes.addWidget(
            bouton_montee
        )

        commandes.addWidget(
            bouton_descente
        )

        commandes.addWidget(
            bouton_atterrir
        )

        commandes.addWidget(
            self.alerte
        )

        commandes.addWidget(
            self.difficulte
        )

        commandes.addWidget(
            self.evenement
        )

        # Score
        self.score = QLabel(
            "Score : 0"
        )

        self.score.setStyleSheet(
            "font-size: 16px;"
            "font-weight: bold;"
            "padding: 10px;"
        )

        commandes.addWidget(
            self.score
        )

        commandes.addStretch()

        # Organisation
        partie_principale = QHBoxLayout()

        partie_principale.addWidget(
            self.radar
        )

        partie_principale.addLayout(
            commandes
        )

        layout = QVBoxLayout()

        layout.addWidget(
            titre
        )

        layout.addLayout(
            partie_principale
        )

        self.setLayout(
            layout
        )

        # Timer
        self.timer = QTimer()

        self.timer.timeout.connect(
            self.actualiser
        )

        self.timer.start(
            100
        )

    def actualiser(self):

        self.simulation.mettre_a_jour(
            0.1
        )

        self.radar.actualiser()

        # Score
        self.score.setText(
            "Score : "
            + str(
                self.simulation.score
            )
        )

        # Difficulté
        self.difficulte.setText(
            "Difficulté : "
            + str(
                self.simulation.difficulte
            )
        )

        # Événement
        self.evenement.setText(
            "Événement : "
            + self.simulation.dernier_evenement
        )

        # Collisions
        collisions = (
            self.simulation.detecter_collisions()
        )

        if len(collisions) > 0:

            texte = (
                "⚠ COLLISION DÉTECTÉE !\n"
            )

            for avion1, avion2 in collisions:

                texte = (
                    texte
                    + avion1.indicatif
                    + " / "
                    + avion2.indicatif
                    + "\n"
                )

            self.alerte.setText(
                texte
            )

            self.alerte.setStyleSheet(
                "font-size: 16px;"
                "font-weight: bold;"
                "padding: 10px;"
                "color: #ff3333;"
            )

        else:

            self.alerte.setText(
                "Aucune collision"
            )

            self.alerte.setStyleSheet(
                "font-size: 16px;"
                "font-weight: bold;"
                "padding: 10px;"
                "color: #00ff88;"
            )

        # Informations
        if (
            self.avion_selectionne
            is not None
        ):

            self.afficher_infos()

    def selectionner_avion(
        self,
        avion
    ):

        self.avion_selectionne = avion

        self.cap.setValue(
            int(avion.cap)
        )

        self.vitesse.setValue(
            int(avion.vitesse)
        )

        self.altitude.setValue(
            int(avion.altitude)
        )

        self.afficher_infos()

        self.radar.update()

    def afficher_infos(self):

        if (
            self.avion_selectionne
            is None
        ):

            return

        avion = (
            self.avion_selectionne
        )

        texte = (
            "Indicatif : "
            + avion.indicatif
            + "\n\nPosition : ("
            + str(round(avion.x, 1))
            + " ; "
            + str(round(avion.y, 1))
            + ")"
            + "\n\nAltitude : "
            + str(avion.altitude)
            + " m"
            + "\n\nVitesse : "
            + str(avion.vitesse)
            + " km/h"
            + "\n\nCap : "
            + str(avion.cap)
            + " °"
            + "\n\nCarburant : "
            + str(round(
                avion.carburant,
                1
            ))
        )

        self.infos.setText(
            texte
        )

    def changer_cap(self):

        if (
            self.avion_selectionne
            is None
        ):

            return

        self.avion_selectionne.changer_cap(
            self.cap.value()
        )

        self.radar.update()

    def changer_vitesse(self):

        if (
            self.avion_selectionne
            is None
        ):

            return

        self.avion_selectionne.changer_vitesse(
            self.vitesse.value()
        )

    def monter(self):

        if (
            self.avion_selectionne
            is None
        ):

            return

        self.avion_selectionne.monter(
            500
        )

        self.altitude.setValue(
            self.avion_selectionne.altitude
        )

        self.afficher_infos()

    def descendre(self):

        if (
            self.avion_selectionne
            is None
        ):

            return

        self.avion_selectionne.descendre(
            500
        )

        self.altitude.setValue(
            self.avion_selectionne.altitude
        )

        self.afficher_infos()

    def atterrir(self):

        if (
            self.avion_selectionne
            is None
        ):

            return

        reussi = (
            self.simulation.atterrir_avion(
                self.avion_selectionne
            )
        )

        if reussi:

            self.infos.setText(
                "Avion atterri !"
            )

        else:

            self.infos.setText(
                "Impossible d'atterrir ici."
            )

        self.radar.update()