import pandas as pd
import getpass  # Librería para inputs seguros (tipo contraseña)
import os
from data_loader import DataLoader
from analyzer import MarketAnalyzer
from segmentation import SellerSegmenter
from genai_advisor import GenAIAdvisor

FILE_PATH = 'df_challenge_meli - df_challenge_meli.csv' 

def print_separator(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def main():

    # --- SOLICITUD DE LLAVE ---
    print("\n CONFIGURACIÓN DE IA:")
    print("Si tienes una API Key de Gemini/Google, ingrésala ahora.")
    print("Si no, presiona ENTER para usar el modo 'Simulación' (Mock).")
    
    api_key_input = getpass.getpass("API Key: ").strip()
    
    if api_key_input:
        print(" API Key detectada. Usando modo: CONECTADO.")
    else:
        print("  Sin API Key. Usando modo: SIMULACIÓN (Ideal para demos).")
        api_key_input = None # Aseguramos que sea None para el Advisor

    # 1. CARGA DE DATOS
    loader = DataLoader(FILE_PATH)
    try:
        df = loader.load_data()
        df = loader.clean_data()
    except Exception as e:
        print(f"Error crítico cargando datos: {e}")
        return

    # 2. ANÁLISIS EXPLORATORIO (EDA)
    print_separator("📊 FASE 1: EDA & HIPÓTESIS")
    analyzer = MarketAnalyzer(df)
    insights = analyzer.get_full_report()
    
    # Mostrar resumen rápido (mismo lógica anterior)
    charm = insights.get('charm_pricing', {})
    print(f"\n-> Patrones detectados: {'Charm Pricing' if charm.get('uses_psychology') else 'Ninguno destacado'}")

    # 3. SEGMENTACIÓN
    print_separator("FASE 2: SEGMENTACIÓN DE VENDEDORES (K-MEANS)")
    segmenter = SellerSegmenter(df)
    seller_profiles = segmenter.create_segments()
    
    # 4. GEN-AI ADVISOR
    print_separator("🤖 FASE 3: ASESORÍA CON GEN-AI")
    
    # Seleccionamos vendedor ejemplo (High Ticket Cluster 3)
    try:
        sample_seller = seller_profiles[seller_profiles['cluster_id'] == 3].iloc[0]
    except:
        sample_seller = seller_profiles.iloc[0]

    print(f"Consultando estrategia para: {sample_seller.name}")
    print(f"Perfil de Cluster: {sample_seller['cluster_label']}")
    # ... (Dentro de main.py, en la FASE 3) ...

    print_separator("🤖 FASE 3: ASESORÍA 100% GEN-AI (DYNAMIC)")

    # 1. Obtenemos las estadísticas promedio del cluster al que pertenece el vendedor
    # Esto es crucial para el "Paso 1" de la IA
    target_cluster_id = 3 # Ejemplo: High Ticket
    
    # Filtramos los vendedores de ese cluster
    cluster_sellers = seller_profiles[seller_profiles['cluster_id'] == target_cluster_id]
    
    # Calculamos el "Centroide" (el vendedor promedio de este grupo)
    cluster_stats = {
        'price': cluster_sellers['price'].median(),
        'stock': cluster_sellers['stock'].mean(),
        'discount_pct': cluster_sellers['discount_pct'].mean(),
        'seller_reputation': 4.5 # Asumimos o calculamos si es numérico
    }

    # Seleccionamos un vendedor específico para aconsejar
    sample_seller = cluster_sellers.iloc[0]

    print(f"Consultando para: {sample_seller.name}")
    
    # Instanciamos OBLIGATORIAMENTE con Key
    if not api_key_input:
        print(" DETENIDO: Este modo requiere API Key real.")
        return

    advisor = GenAIAdvisor(api_key=api_key_input)
    
    # Llamamos al nuevo método dinámico
    resultado = advisor.get_recommendation_dynamic(
        seller_row=sample_seller, 
        cluster_stats_row=cluster_stats
    )
    
    print("\n" + "-"*40)
    print(f" PERFIL DETECTADO POR IA: {resultado['perfil_ia'].upper()}")
    print(f" ESTRATEGIA MACRO: {resultado['estrategia_macro']}")
    print("-" * 40)
    print(f" CONSEJOS PERSONALIZADOS:\n{resultado['recomendacion_final']}")
    print("-" * 40)

if __name__ == "__main__":
    main()
