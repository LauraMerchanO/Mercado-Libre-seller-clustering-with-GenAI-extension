import pandas as pd
from data_loader import DataLoader
from analyzer import MarketAnalyzer
from segmentation import SellerSegmenter
from genai_advisor import GenAIAdvisor

FILE_PATH = 'df_challenge_meli - df_challenge_meli.csv' 
API_KEY = None 

def main():
    # 1. Carga y Limpieza
    loader = DataLoader(FILE_PATH)
    try:
        df = loader.load_data()
        df = loader.clean_data()
    except Exception as e:
        print(e)
        return

    # 2. Análisis Estadístico (EDA)
    analyzer = MarketAnalyzer(df)
    report = analyzer.generate_summary_report()
    
    print("--- Principales hallazgos ---")
    if report['reputation_analysis']['significant']:
        print(f"-> Hallazgo: La reputación SÍ influye en el precio (p-value < 0.05).")
    print(f"-> Terminaciones de precio más comunes: {report['charm_pricing_top_3']}")

    # 3. Segmentación (ML)
    segmenter = SellerSegmenter(df)
    seller_profiles = segmenter.create_segments()
    
    sample_seller_id = seller_profiles.index[0]
    sample_seller_data = seller_profiles.loc[sample_seller_id]
    
    print(f"\n🧪 --- Demo GenAI para Vendedor: {sample_seller_id} ---")
    print(f"Cluster asignado: {sample_seller_data['cluster_label']}")
    
    advisor = GenAIAdvisor()
    
    # Ejemplo con el Cluster 3 (High Ticket) 
    sample_seller = seller_profiles[seller_profiles['cluster_id'] == 3].iloc[0]
    
    resultado = advisor.get_recommendation(
        row=sample_seller, 
        cluster_id=3
    )
    
    print(f"Cluster: {resultado['profile_detected']}")
    print(f">> Prompt Generado (Interno):\n{resultado['prompt_used'][:150]}...\n")
    print("-" * 40)
    print(f">> RESPUESTA IA:\n{resultado['strategy']}")

if __name__ == "__main__":
    main()
