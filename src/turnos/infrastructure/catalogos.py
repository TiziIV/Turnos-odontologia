from turnos.domain.model.entidades import Paciente, Prestacion, Profesional, Sillon


def catalogos_sinteticos() -> tuple[
    dict[int, Paciente],
    dict[int, Profesional],
    dict[int, Sillon],
    dict[int, Prestacion],
]:
    pacientes = {
        1: Paciente(
            1, "Carla", "Pérez", "00000001", "+5490000000001", "paciente1@example.test"
        ),
        2: Paciente(
            2, "Diego", "Ruiz", "00000002", "+5490000000002", "paciente2@example.test"
        ),
    }
    profesionales = {
        1: Profesional(1, "Ana", "Gómez", "MP-00001", "Odontología general", True),
        2: Profesional(2, "Bruno", "Díaz", "MP-00002", "Endodoncia", True),
        3: Profesional(3, "Eva", "Sosa", "MP-00003", "Ortodoncia", False),
    }
    sillones = {
        1: Sillon(1, "BOX-1", "Sillón 1 — general", True),
        2: Sillon(2, "BOX-2", "Sillón 2 — general", True),
        3: Sillon(3, "BOX-X", "Sillón fuera de servicio", False),
    }
    prestaciones = {
        1: Prestacion(1, "LIMPIEZA", "Limpieza dental", 30, True),
        2: Prestacion(2, "CONSULTA", "Consulta general", 20, True),
        3: Prestacion(3, "EXTRACCION", "Extracción simple", 40, True),
        4: Prestacion(4, "ENDO", "Endodoncia", 60, True),
        5: Prestacion(5, "INACTIVA", "Prestación retirada", 30, False),
    }
    return pacientes, profesionales, sillones, prestaciones
