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
    