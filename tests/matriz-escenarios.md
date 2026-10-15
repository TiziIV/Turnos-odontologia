# Correspondencia escenario → test

| Requisito / escenario | Regla | Test |
|---|---|---|
| Camino feliz | RN-01, RN-07 | `test_camino_feliz_201_utc`, `test_alta_valida_pendiente_online_y_fin_calculado` |
| Referencias o inactivos | RN-10, RN-11 | `test_referencias_o_inactivos_422`, `test_referencia_inexistente_no_guarda` |
| Solapamiento profesional o sillón | RN-01, RN-03 | `test_solapamiento_profesional_o_sillon_409`, `test_rn01_rn03_rechaza_interseccion_por_profesional_o_sillon` |
| Borde inicio = fin anterior | RN-03 | `test_borde_inicio_igual_al_fin_anterior_201`, `test_rn03_borde_inicio_igual_al_fin_anterior_es_valido` |
| Un minuto y contención | RN-03 | `test_rn03_un_minuto_y_contencion_se_rechazan` |
| Recursos distintos y estados finales | RN-09 | `test_rn01_recursos_distintos_no_conflictuan`, `test_rn09_estados_finales_no_ocupan_recursos` |
| Duración de catálogo | RN-02 | `test_rn02_fin_deriva_de_duracion_de_prestacion`, `test_rn02_duraciones_de_catalogo` |
| Duración inválida / campos extra | RN-02, RN-13 | `test_rn02_duracion_no_positiva_se_rechaza`, `test_entrada_invalida_422` |
| Offsets equivalentes | tiempo UTC | `test_offsets_equivalentes_409`, `test_tiempo_offsets_equivalentes_son_el_mismo_instante` |
| Datos sintéticos | RN-06 | `test_rn06_emails_y_documentos_sinteticos` |
| Dominio sin framework | arquitectura | `test_dominio_no_importa_frameworks` |
