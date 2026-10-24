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
        