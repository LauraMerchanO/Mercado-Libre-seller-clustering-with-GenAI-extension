class GenAIAdvisor:
    def __init__(self):
        # Ya no usamos un diccionario hardcodeado. 
        # La IA va a descubrir esto.
        pass

    def _generate_dynamic_profile(self, cluster_stats):
        """
        Paso 1: La IA analiza los CENTROIDES (promedios) del cluster 
        para decidir qué tipo de vendedores son.
        """
        prompt_analysis = f"""
        ACTÚA COMO: Chief Data Officer de Mercado Libre.
        
        TAREA: Analiza las estadísticas promedio de este segmento de vendedores y define su perfil.
        
        DATOS DEL SEGMENTO:
        - Precio Promedio: ${cluster_stats['price']:.2f}
        - Stock Promedio: {cluster_stats['stock']:.0f}
        - Descuento Promedio: {cluster_stats['discount_pct']:.1f}%
        - Reputación Promedio: {cluster_stats['seller_reputation']:.1f}/5
        
        SALIDA:
        Devuelve SOLO un breve resumen en formato:
        PERFIL: [Nombre creativo del perfil]
        ESTRATEGIA: [Qué deberían hacer para crecer]
        """
        
        # --- SIMULACIÓN DE LLM INTERPRETANDO DATOS ---
        # Aquí la IA "piensa" basada en los números que ve
        if cluster_stats['price'] > 5000 and cluster_stats['stock'] < 50:
            return {
                "perfil": "Boutique de Lujo / Nicho",
                "estrategia": "Enfocarse en exclusividad, financiación y experiencia de unboxing."
            }
        elif cluster_stats['price'] < 500 and cluster_stats['stock'] > 1000:
            return {
                "perfil": "Mayorista de Rotación Rápida",
                "estrategia": "Optimizar logística masiva y márgenes por volumen."
            }
        else:
            return {
                "perfil": "Vendedor Estándar en Crecimiento",
                "estrategia": "Profesionalizar catálogo y mejorar reputación."
            }

    def get_recommendation_dynamic(self, seller_row, cluster_stats_row):
        """
        Flujo de 2 Pasos:
        1. Generar Insight del Cluster (Dynamic Profiling).
        2. Generar Recomendación para el Vendedor (Personalization).
        """
        
        # PASO 1: Que la IA decida qué significa este cluster
        dynamic_context = self._generate_dynamic_profile(cluster_stats_row)
        
        # PASO 2: Usar ese insight generado para aconsejar al vendedor específico
        prompt = f"""
        [ROL]
        Consultor de IA.
        
        [CONTEXTO MACRO]
        Este vendedor pertenece al segmento identificado como "{dynamic_context['perfil']}".
        La estrategia general para este grupo es: "{dynamic_context['estrategia']}".
        
        [DATOS DEL VENDEDOR INDIVIDUAL]
        - Nickname: {seller_row['seller_nickname']}
        - Precio: ${seller_row['price']:.2f}
        
        [TAREA]
        Basado en la estrategia del segmento, da 3 consejos tácticos para este vendedor.
        """
        
        # Respuesta simulada usando el contexto dinámico
        return f"""
        Basado en que tu perfil fue detectado automáticamente como '{dynamic_context['perfil']}':
        1. {dynamic_context['estrategia']} (Aplicado a tu precio de ${seller_row['price']})
        2. Revisa tus competidores directos en este nicho.
        3. Ajusta tu logística para este volumen de stock.
        """
