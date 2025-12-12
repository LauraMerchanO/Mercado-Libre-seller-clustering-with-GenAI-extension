import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

class SellerSegmenter:
    """
    Segmenta a los vendedores en clusters basados en su comportamiento.
    """
    
    def __init__(self, df):
        self.df = df
        self.model = None
        self.scaler = StandardScaler()

    def create_segments(self, n_clusters=3):
        """
        Aplica K-Means Clustering.
        Features usadas: Precio promedio, Stock total, Diversidad de categorías.
        """
        print(f"Iniciando segmentación en {n_clusters} clusters...")
        
        # 1. Agrupar por vendedor para tener perfil único
        seller_profile = self.df.groupby('seller_nickname').agg({
            'price': 'median',       # Mediana de precios
            'stock': 'sum',          # Stock total
            'discount_pct': 'mean',  # Agresividad en descuentos
            'title_len': 'mean'      # Calidad promedio de título
        }).dropna()

        # 2. Escalar datos (Crucial para K-Means)
        X = self.scaler.fit_transform(seller_profile)

        # 3. Entrenar Modelo
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = self.model.fit_predict(X)

        # 4. Asignar etiquetas al dataframe agrupado
        seller_profile['cluster_id'] = clusters
        
        # Asignar nombres descriptivos simples basados en precio y stock (Lógica simplificada)
        # En producción, esto requiere análisis de centroides
        cluster_map = self._label_clusters(seller_profile)
        seller_profile['cluster_label'] = seller_profile['cluster_id'].map(cluster_map)

        print("Segmentación completada.")
        return seller_profile

    def _label_clusters(self, df_grouped):
        """Etiqueta dinámica basada en la mediana de precio del cluster."""
        means = df_grouped.groupby('cluster_id')['price'].mean().sort_values()
        
        # Asignamos etiquetas según el precio promedio del cluster (Bajo, Medio, Alto)
        labels = ['Liquidación/Low-Cost', 'Estándar', 'High-Ticket/Premium']
        mapping = {}
        
        for i, cluster_id in enumerate(means.index):
            if i < len(labels):
                mapping[cluster_id] = labels[i]
            else:
                mapping[cluster_id] = f'Cluster {cluster_id}'
                
        return mapping
