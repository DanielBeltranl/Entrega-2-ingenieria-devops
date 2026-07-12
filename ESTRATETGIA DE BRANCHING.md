# Guía de Convenciones y Flujo de Trabajo

Este documento define los estándares de nomenclatura, mensajería de commits y el flujo de integración para garantizar la calidad y trazabilidad del código en el proyecto.

## 1. Nomenclatura de Ramas (Branching Strategy)

Se utiliza un sistema de prefijos basado en el objetivo de la tarea. Todas las ramas deben escribirse en minúsculas.

| Prefijo | Descripción | Ejemplo               |
| :--- | :--- |:----------------------|
| `feat/` | Desarrollo de nuevas funcionalidades o características. | `feat/list-all`       |
| `hotfix/` | Reparaciones críticas y rápidas en producción. | `hotfix/list-all`     |
| `doc/` | Creación o actualización de documentación técnica. | `doc/README.md`       |
| `pipeline/` | Cambios en archivos de configuración de GitHub Actions (`.yml`). | `pipeline/validación` |

---

## 2. Convenciones de Commits

Para mantener un historial de Git legible, cada commit debe comenzar con el prefijo correspondiente al tipo de cambio, seguido de una descripción breve y clara en imperativo o presente.

**Formato:** `<prefijo>: <descripción>`

* **Ejemplo:** `feat: cambio DTO funcion list all`

---

## 3. Flujo de Trabajo 

Seguimos el flujo de gitflow para asegurar el aislamiento de cada nueva función, arreglo, etc. y generar un historial de cambios mas ordenado y descriptivo

1.  **Sincronización:** Toda nueva rama debe partir de un `git pull` actualizado de la rama `develop`.
2.  **Consolidación (Merge Flow):**
    * `Feature Branch` ➔ `develop`: Una vez terminada la tarea, se abre un Pull Request (PR).
    * `develop` ➔ `main`: Los cambios validados en develop se mueven a main para releases oficiales.
3.  **Regla de Oro:** Nunca se realiza un merge directo a `develop` o `main` sin pasar por el proceso de revisión.

---

## 4. Revisión de Código (Code Review)

La calidad del código es responsabilidad del equipo. El proceso de revisión se define bajo los siguientes puntos:

* **Asignación:** Cada PR tenia como revisor al otro miembro de la pareja.
* **Metodología:** Las revisiones se realizan mediante videollamada.
* **Aprobación:** Una vez resueltas las observaciones en la llamada, se hacia el merge correspondiente.