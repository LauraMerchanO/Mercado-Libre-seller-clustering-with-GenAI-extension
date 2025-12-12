import pandas as pd
import numpy as np

class DataLoader:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"Datos cargados exitosamente: {self.df.shape[0]} registros.")
            return self.df
        except FileNotFoundError:
            raise Exception(f"No se encontró el archivo en: {self.file_path}")

    def clean_data(self):
        if self.df is None:
            raise Exception("Primero debes cargar los datos con load_data()")

        # 1. Fechas
        if 'tim_day' in self.df.columns:
            self.df['tim_day'] = pd.to_datetime(self.df['tim_day'])

        # 2. Manejo de Nulos en Precios
        # Si regular_price es NaN, asumimos que es igual al precio actual (no hay descuento)
        self.df['regular_price_clean'] = self.df['regular_price'].fillna(self.df['price'])
        
        # 3. Cálculo de Descuento (%)
        self.df['discount_pct'] = (1 - (self.df['price'] / self.df['regular_price_clean'])) * 100
        self.df['discount_pct'] = self.df['discount_pct'].apply(lambda x: max(0, x)) # Evitar negativos por errores de data

        # 4. Normalización de Reputación
        self.df['seller_reputation'] = self.df['seller_reputation'].fillna('Sin Reputación')

        # 5. Feature: Longitud del título (útil para análisis)
        self.df['title_len'] = self.df['titulo'].astype(str).apply(len)

        print("Limpieza básica y Feature Engineering completados.")
        return self.df
