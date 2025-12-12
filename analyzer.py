import pandas as pd
import numpy as np
from scipy import stats

class MarketAnalyzer:
    """
    Pruebas estadísticas y Análisis Exploratorio de Datos (EDA).
    """
    
    def __init__(self, df):
        self.df = df

    def test_reputation_price_impact(self):
        """
        Test Mann-Whitney U para validar si la reputación afecta el precio.
        Retorna: Diccionario con resultados estadísticos.
        """
        # Filtramos datos válidos
        df_clean = self.df.dropna(subset=['price']).copy()
        
        group_gold = df_clean[df_clean['seller_reputation'] == 'green_gold']['price']
        group_others = df_clean[df_clean['seller_reputation'] != 'green_gold']['price']

        if len(group_gold) < 10 or len(group_others) < 10:
            return {"status": "insufficient_data"}

        stat, p_val = stats.mannwhitneyu(group_gold, group_others, alternative='two-sided')
        
        result = {
            "test": "Mann-Whitney U",
            "p_value": p_val,
            "significant": p_val < 0.05,
            "median_gold": group_gold.median(),
            "median_others": group_others.median()
        }
        return result

    def analyze_charm_pricing(self):
        """
        Analiza si los vendedores usan precios terminados en .99 o .90
        """
        prices = self.df['price'].dropna()
        # Obtener los decimales
        endings = (prices * 100).astype(int) % 100
        
        top_endings = endings.value_counts(normalize=True).head(3)
        return top_endings.to_dict()

    def generate_summary_report(self):
        """Orquesta los análisis y devuelve un reporte consolidado."""
        print("🔍 Ejecutando análisis estadísticos...")
        
        rep_impact = self.test_reputation_price_impact()
        charm_pricing = self.analyze_charm_pricing()
        
        return {
            "reputation_analysis": rep_impact,
            "charm_pricing_top_3": charm_pricing
        }
