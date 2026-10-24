import os
import json
import hashlib
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from fpdf import FPDF

RECORD_SIZE = 100
FILE_DAT = "contactos.dat"
FILE_INDEX = "indice.json"
FILE_HASH = "contactos.sha256"
FILE_EXPORT_JSON = "contactos_exportados.json"
FILE_EXPORT_PDF = "reporte_contactos.pdf"

class GestorArchivos:
    def __init__(self):
        self.indice = {}
        self.cargar_indice()

    def cargar_indice(self):
        if not os.path.exists(FILE_INDEX):
            self.indice = {}
            return
        try:
            with open(FILE_INDEX, "r", encoding="utf-8") as f:
                self.indice = json.load(f)
        except PermissionError:
            messagebox.showerror("Error de permisos", f"No hay permisos de lectura para {FILE_INDEX}")
            self.indice = {}
        except json.JSONDecodeError:
            messagebox.showerror("Archivo corrupto", f"El indice {FILE_INDEX} esta corrupto")
            self.indice = {}
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el indice {e}")
            self.indice = {}

    def guardar_indice(self):
        try:
            with open(FILE_INDEX, "w", encoding="utf-8")as f:
                json.dump(self.indice, f, indent=4, ensure_ascii=False)
        except PermissionError:
            raise PermissionError(f"Sin permisos de escritura en {FILE_INDEX}")

    def calcular_hash(self):
        if not os.path.exists(FILE_DAT):
            return ""
        sha256 = hashlib-sha256()
        with open(FILE_DAT, "rb") as f:
            sha256.update(f.read())
        return sha256.hexdigest()

    def actualizar_hash(self):
        with open(FILE_HASH, "w", encoding="utf-8") as f:
            f.write(self.calcular_hash())

    def verificar_integridad(self):
        if not os.path.exists(FILE_DAT) or not os.path.exists(FILE_HASH):
            return True, "Archivos de datos o hash aun no generados"
        try:
            with open(FILE_HASH, "r", encoding="utf-8")as f:
                hash_guardado = f.read().strip()
            hash_actual = self.calcular_hash()
            if hash_guardado == hash_actual:
                return True, f"Integridad verificado correctamente. \nSHA-256: {hash_actual[:24]}..."
            else:
                return False, "El archivo 'contactos.dat' fue modificado fuera de la aplicacion"
        except Exception as e:
            return False, f"No se pudo verificar la integridad {e}"

    def ajustar_campo_utf8(self, texto, largo_bytes):
        b_texto = str(texto).strip().encode("utf-8")[:largo_bytes]
        texto_seguro = b_texto.decode("utf-8", errors="ignore")
        faltantes = largo_bytes - len(texto_seguro.encode("utf-8"))
        return texto_seguro + (" " * faltantes)

    def formatear_registro(self, id_c, nombre, tel, correo, ciudad):
        c_id = self.ajustar_campo_utf8(id_c, 10)
        c_nom = self.ajustar_campo_utf8(nombre, 30)
        c_tel = self.ajustar_campo_utf8(tel, 15)
        c_cor = self.ajustar_campo_utf8(correo, 25)
        c_ciu = self.ajustar_campo_utf8(ciudad, 20)
        return c_id + c_nom + c_tel + c_cor + c_ciu

    # Informacion del contacto

    def agregar_contacto(self, id_c, nombre, tel, correo, ciudad):
        str_id = str(id_c)
        if str_id in self.indice:
            raise ValueError(f"El ID {id_c} ya está registrado")
        registro = self.formatear_registro(id_c, nombre, tel, correo, ciudad)

        if not os.path.exists(FILE_DAT):
            open(FILE_DAT, "w", encoding="utf-8").close()

        with open(FILE_DAT, "r+", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END)
            pos_inicial = f.tell()
            num_registro = pos_inicial // RECORD_SIZE
            f.write(registro)
            pos_final = f.tell()

        self.indice[str_id] = num_registro
        self.guardar_indice()
        self.actualizar_hash()
        return num_registro, pos_inicial, pos_final

    def buscar_contacto(self, id_c):
        str_id = str(id_c)
        if str_id not in self.indice:
            return None, None

        if not os.path.exists(FILE_DAT):
            raise FileNotFoundError("El archivo 'contactos.dat' no existe")

        num_registro = self.indice[str_id]
        desplazamiento = num_registro * RECORD_SIZE

        with open(FILE_DAT, "r", encoding="utf-8")as f:
            f.seek(desplazamiento)
            pos_actual = f.tell()
            raw_bytes = f.read(RECORD_SIZE).encode("utf-8")
        if len(raw_bytes) < RECORD_SIZE:
            raise IOError("El registro está imcompleto o el está corrupto")

        contacto = {
            "id": int(raw_bytes[0:10].decode("utf-8", errors="ignore").strip()),
            "nombre": raw_bytes[10:40].decode("utf-8", errors="ignore").strip(),
            "telefono": raw_bytes[40:55].decode("utf-8", errors="ignore").strip(),
            "correo": raw_bytes[55:80].decode("utf-8", errors="ignore").strip(),
            "ciudad": raw_bytes[80:100].decode("utf-8", errors="ignore").strip(),
        }
        return contacto, pos_actual

    def mod_contacto(self, id_c, nombre, tel, correo, ciudad):
        str_id = str(id_c)
        if str_id not in self.indice:
            raise KeyError(f"El contado con ID {id_c} no existe")
        if not os.path.exists(FILE_DAT):
            raise FileNotFoundError("El archivo 'contactos.dat' no existe")

        num_registros = self.indice[str_id]
        registro_nuevo = self.formatear_registro(id_c, nombre, tel, correo, ciudad)

        with open(FILE_DAT, "r+", encoding="utf-8")as f:
            f.seek(num_registros * RECORD_SIZE)
            pos_escritura = f.tell()
            f.write(registro_nuevo)

        self.actualizar_hash()
        return num_registros, pos_escritura

    