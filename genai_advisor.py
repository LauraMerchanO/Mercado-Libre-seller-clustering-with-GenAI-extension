import google.generativeai as genai
import json
import re

class GenAIAdvisor:
    """
    Módulo 100% conectado a Gemini API.
    Implementa un patrón de 'Chain of Thought' (Cadena de Pensamiento):
    1. La IA analiza los datos duros para perfilar al cluster.
    2. La IA usa ese perfil para aconsejar al vendedor individual.
    """
    
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("❌ ERROR CRÍTICO: Se requiere una API Key de Google Gemini para operar este módulo.")
            
        # Configuración del cliente real
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        print("✅ Cliente GenAI conectado exitosamente.")

    def _clean_json_response(self, text):
        """Limpia la respuesta del LLM para asegurar que sea un JSON válido."""
        # Elimina bloques de código markdown si la IA los pone (```json ... ```)
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```', '', text)
        return text.strip()

    def _generate_dynamic_profile(self, cluster_stats):
        """
        PASO 1: Llamada a la API para definir el perfil del segmento.
        """
        prompt_analysis = f"""
        ACTÚA COMO: Chief Data Officer de Mercado Libre.
        
        TAREA: Analiza las estadísticas promedio de este segmento de vendedores.
        
        DATOS DEL SEGMENTO:
        - Precio Promedio: ${cluster_stats.get('price', 0):.2f}
        - Stock Promedio: {cluster_stats.get('stock', 0):.0f} unidades
        - Descuento Promedio: {cluster_stats.get('discount_pct', 0):.1f}%
        - Reputación Promedio: {cluster_stats.get('seller_reputation', 0):.1f}/5
        
        SALIDA OBLIGATORIA:
        Responde ÚNICAMENTE con un objeto JSON válido con este formato exacto:
        {{
            "perfil": "Nombre corto y creativo del perfil",
            "estrategia": "Resumen de 1 linea sobre qué deben hacer para crecer"
        }}
        No añadas texto extra fuera del JSON.
        """
        
        try:
            # Llamada REAL a Gemini
            response = self.model.generate_content(prompt_analysis)
            clean_text = self._clean_json_response(response.text)
            return json.loads(clean_text)
            
        except Exception as e:
            # Fallback de seguridad por si la IA devuelve un JSON roto, pero sigue siendo un error técnico
            print(f"⚠️ Error parseando perfil dinámico: {e}")
            return {
                "perfil": "Perfil No Identificado (Error IA)",
                "estrategia": "Revisar métricas manualmente"
            }

    def get_recommendation_dynamic(self, seller_row, cluster_stats_row):
        """
        Flujo Maestro:
        1. Pide a la IA que cree el perfil (basado en el cluster).
        2. Pide a la IA que aconseje al vendedor (basado en el perfil generado en 1).
        """
        
        # --- PASO 1: AI PROFILING (Llamada API #1) ---
        print("   🧠 Analizando ADN del cluster con Gemini...")
        dynamic_context = self._generate_dynamic_profile(cluster_stats_row)
        
        print(f"   -> Perfil detectado por IA: {dynamic_context['perfil']}")
        
        # --- PASO 2: AI ADVISING (Llamada API #2) ---
        print("   💡 Generando estrategia personalizada...")
        
        # Construimos un prompt usando la inteligencia generada en el paso anterior
        prompt = f"""
        [ROL]
        Eres un Consultor Senior de E-commerce.
        
        [CONTEXTO ESTRATÉGICO]
        Has identificado que este vendedor pertenece al perfil: "{dynamic_context['perfil']}".
        La estrategia maestra para este grupo es: "{dynamic_context['estrategia']}".
        
        [DATOS DEL VENDEDOR]
        - Nickname: {seller_row.get('seller_nickname', 'Vendedor')}
        - Precio: ${seller_row.get('price', 0):.2f}
        - Stock: {seller_row.get('stock', 0)}
        
        [TAREA]
        Genera 3 recomendaciones tácticas, directas y accionables para este vendedor.
        Las recomendaciones deben alinear sus datos individuales con la estrategia maestra.
        """
        
        try:
            # Llamada REAL a Gemini (Segunda llamada)
            response = self.model.generate_content(prompt)
            
            return {
                "perfil_ia": dynamic_context['perfil'],
                "estrategia_macro": dynamic_context['estrategia'],
                "recomendacion_final": response.text
            }
        except Exception as e:
            return {
                "error": f"Error conectando con Gemini: {e}"
            }
