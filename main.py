import sys

from PySide6.QtWidgets import QApplication

from avion import Avion
from simulation import Simulation
from interface import Interface


def main():

    app = QApplication(sys.argv)

    simulation = Simulation()

    avion1 = Avion(
        "AF1234",
        200,
        200,
        3000,
        400,
        0,
        80
    )

    avion2 = Avion(
        "BA9012",
        700,
        300,
        4000,
        300,
        180,
        70
    )

    avion3 = Avion(
        "LH4567",
        300,
        800,
        5000,
        350,
        90,
        90
    )

    simulation.ajouter_avion(
        avion1
    )

    simulation.ajouter_avion(
        avion2
    )

    simulation.ajouter_avion(
        avion3
    )

    interface = Interface(
        simulation
    )

    interface.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()