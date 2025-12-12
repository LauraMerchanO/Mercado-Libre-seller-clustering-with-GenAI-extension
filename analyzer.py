import pandas as pd
import numpy as np
from scipy import stats

class MarketAnalyzer:
    """
    Realiza Análisis Exploratorio de Datos (EDA) profundo y pruebas de hipótesis estadísticas.
    """
    
    def __init__(self, df):
        self.df = df
        self.results = {}

    def _remove_outliers(self, data):
        """Método auxiliar interno para limpiar outliers extremos (IQR)."""
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        return data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR)))]

    def analyze_price_distribution(self):
        """
        Analiza la distribución de precios y realiza test de normalidad.
        """
        prices = self.df['price'].dropna()
        # Test D'Agostino's K^2
        stat, p_val = stats.normaltest(prices)
        
        self.results['normality_test'] = {
            "is_normal": p_val >= 0.05,
            "p_value": p_val,
            "message": "Distribución Normal" if p_val >= 0.05 else "Distribución No Normal (Posiblemente Log-Normal)"
        }
        return self.results['normality_test']

    def test_reputation_impact(self):
        """
        Test: ¿Tienen precios diferentes los vendedores Green_Gold vs Sin Reputación?
        Usa Mann-Whitney U (No paramétrico).
        """
        df_clean = self.df.dropna(subset=['price']).copy()
        df_clean['rep_filled'] = df_clean['seller_reputation'].fillna('Sin Reputación')
        
        group_gold = df_clean[df_clean['rep_filled'] == 'green_gold']['price']
        group_none = df_clean[df_clean['rep_filled'] == 'Sin Reputación']['price']
        
        if len(group_gold) < 5 or len(group_none) < 5:
            return {"error": "Datos insuficientes para el test."}

        stat, p_val = stats.mannwhitneyu(group_gold, group_none, alternative='two-sided')
        
        diff_median_pct = ((group_gold.median() - group_none.median()) / group_none.median()) * 100
        
        self.results['reputation_impact'] = {
            "p_value": p_val,
            "significant": p_val < 0.05,
            "median_gold": group_gold.median(),
            "median_none": group_none.median(),
            "diff_pct": diff_median_pct,
            "interpretation": "Impacto Significativo" if p_val < 0.05 else "Sin evidencia de impacto"
        }
        return self.results['reputation_impact']

    def test_logistics_dependency(self):
        """
        Test Chi-Cuadrada: ¿Depende el tipo de logística de la reputación?
        """
        # Tabla de contingencia
        contingency = pd.crosstab(
            self.df['seller_reputation'].fillna('NoRep'), 
            self.df['logistic_type']
        )
        
        chi2, p, dof, expected = stats.chi2_contingency(contingency)
        
        self.results['logistics_test'] = {
            "p_value": p,
            "significant": p < 0.05,
            "interpretation": "Existe dependencia fuerte (Logística varía según Reputación)" if p < 0.05 else "Variables independientes"
        }
        return self.results['logistics_test']

    def analyze_charm_pricing(self):
        """Detecta patrones de precios psicológicos (.99, .90)."""
        valid_prices = self.df['price'].dropna()
        # Obtener los últimos dos dígitos
        endings = (valid_prices * 100).astype(int) % 100
        
        top_3 = endings.value_counts(normalize=True).head(3)
        
        is_psychological = (99 in top_3.index) or (90 in top_3.index)
        
        self.results['charm_pricing'] = {
            "top_endings": top_3.to_dict(),
            "uses_psychology": is_psychological
        }
        return self.results['charm_pricing']

    def analyze_title_quality(self):
        """Analiza 'Gritos' (All Caps) vs Precio."""
        df_titles = self.df[['titulo', 'price']].dropna()
        df_titles['is_caps'] = df_titles['titulo'].astype(str).apply(lambda x: x.isupper())
        
        caps_price = df_titles[df_titles['is_caps'] == True]['price'].median()
        normal_price = df_titles[df_titles['is_caps'] == False]['price'].median()
        
        self.results['title_analysis'] = {
            "median_price_caps": caps_price,
            "median_price_normal": normal_price,
            "bad_practice_detected": caps_price < normal_price # Asumimos que caps = barato/urgente
        }
        return self.results['title_analysis']

    def get_full_report(self):
        """Ejecuta todos los análisis en orden."""
        print("🔍 Ejecutando batería de tests estadísticos...")
        self.analyze_price_distribution()
        self.test_reputation_impact()
        self.test_logistics_dependency()
        self.analyze_charm_pricing()
        self.analyze_title_quality()
        return self.results
        
