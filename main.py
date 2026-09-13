import flet as ft
import sqlite3
from pathlib import Path


# ---------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "datos.db"


# ---------------------------------------------------------
# BASE DE DATOS SQLITE
# ---------------------------------------------------------

def inicializar_bd():
    conexion = sqlite3.connect(DB_FILE)

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


def obtener_notas():
    conexion = sqlite3.connect(DB_FILE)

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, texto
        FROM notas
        ORDER BY id DESC
    """)

    notas = cursor.fetchall()

    conexion.close()

    return notas


def agregar_nota(texto):
    conexion = sqlite3.connect(DB_FILE)

    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO notas (texto) VALUES (?)",
        (texto,)
    )

    conexion.commit()
    conexion.close()


def eliminar_nota(nota_id):
    conexion = sqlite3.connect(DB_FILE)

    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM notas WHERE id = ?",
        (nota_id,)
    )

    conexion.commit()
    conexion.close()

# ---------------------------------------------------------
# APLICACIÓN FLET
# ---------------------------------------------------------

def main(page: ft.Page):

    page.web_app_name = "Flet Web App"
    page.web_short_name = "FletApp"

    page.title = "Flet + Web App"
    page.padding = 20

    inicializar_bd()

    titulo = ft.Text(
        "Aplicación de prueba",
        size=24,
        weight=ft.FontWeight.BOLD
    )

    subtitulo = ft.Text(
        f"Base de datos: {DB_FILE.name}"
    )

    campo = ft.TextField(
        label="Escribe una nota",
        hint_text="Ejemplo: Comprar pan",
        expand=True
    )

    lista = ft.Column(
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    mensaje = ft.Text()


    # -----------------------------------------------------
    # MOSTRAR NOTAS
    # -----------------------------------------------------

    def cargar_notas():

        lista.controls.clear()

        notas = obtener_notas()

        if not notas:
            lista.controls.append(
                ft.Text(
                    "No hay notas guardadas.",
                    italic=True
                )
            )

        else:

            for nota_id, texto in notas:

                def eliminar(e, id_nota=nota_id):
                    
                    eliminar_nota(id_nota)

                    page.show_dialog(
                        ft.SnackBar(
                            ft.Text(f"Nota Eliminada de SQLite",
                                color=ft.Colors.WHITE,
                                weight=ft.FontWeight.BOLD
                            ),
                            bgcolor=ft.Colors.RED
                        )
                    )

                    cargar_notas()
                    page.update()

                fila = ft.Row(
                    controls=[
                        ft.Text(
                            texto,
                            expand=True
                        ),

                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Eliminar",
                            on_click=eliminar
                        )
                    ]
                )

                lista.controls.append(fila)


        page.update()


    # -----------------------------------------------------
    # AGREGAR NOTA
    # -----------------------------------------------------

    def guardar(e):

        texto = campo.value.strip()

        if not texto:
            mensaje.value = "Escribe una nota."
            mensaje.color = ft.Colors.RED
            page.update()
            return

        agregar_nota(texto)

        campo.value = ""

        # mensaje.value = "Nota guardada en SQLite."
        # mensaje.color = ft.Colors.GREEN

        page.show_dialog(
            ft.SnackBar(
                ft.Text("Nota guardada en SQLite",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD
                ),
                bgcolor=ft.Colors.GREEN
            )
        )

        cargar_notas()

    boton = ft.Button(
        "Guardar",
        icon=ft.Icons.SAVE,
        on_click=guardar
    )


    # -----------------------------------------------------
    # INTERFAZ
    # -----------------------------------------------------

    page.add(

        titulo,

        subtitulo,

        ft.Divider(),

        ft.Row(
            controls=[
                campo,
                boton
            ]
        ),

        mensaje,

        ft.Divider(),

        ft.Text(
            "Notas guardadas:",
            size=18,
            weight=ft.FontWeight.BOLD
        ),

        lista
    )


    cargar_notas()


# ---------------------------------------------------------
# EJECUCIÓN
# ---------------------------------------------------------

if __name__ == "__main__":
     ft.run(main)
