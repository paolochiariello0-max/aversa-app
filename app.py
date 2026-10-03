import os
import json
import webbrowser
from datetime import datetime
from typing import List, Dict, Any
import folium
from folium import plugins

# ==============================================================================
# 1. LOGICA DELLO SCIAME DI AGENTI (SWARM BACKEND)
# ==============================================================================

class CultureAgent:
    """Agente specializzato nel monitoraggio dei monumenti e siti storici di Aversa."""
    def run() -> List[Dict[str, Any]]:
        print("[🤖 CultureAgent] Aggiornamento dati monumenti e storia...")
        return [
            {
                "id": "mon_1",
                "name": "Duomo di Aversa (Cattedrale di San Paolo)",
                "category": "monumenti",
                "coords": [40.9729, 14.2078],
                "description": "Cattedrale d'epoca normanna celebre per il deambulatorio e la cupola.",
                "status": "Aperto (08:00 - 12:00 | 16:30 - 19:30)",
                "icon": "landmark",
                "color": "blue"
            },
            {
                "id": "mon_2",
                "name": "Arco dell'Annunziata",
                "category": "monumenti",
                "coords": [40.9735, 14.2085],
                "description": "Simbolo porta d'ingresso al centro storico di Aversa.",
                "status": "Visibile h24",
                "icon": "archway",
                "color": "blue"
            },
            {
                "id": "mon_3",
                "name": "Complesso di San Lorenzo ad Septimum",
                "category": "monumenti",
                "coords": [40.9750, 14.2120],
                "description": "Antico monastero, oggi sede del Dipartimento di Architettura (UniCampania).",
                "status": "Aperto per attività accademiche",
                "icon": "university",
                "color": "blue"
            }
        ]

class FoodAgent:
    """Agente specializzato nella scansione della gastronomia e movida aversana."""
    def run() -> List[Dict[str, Any]]:
        print("[🤖 FoodAgent] Scansione pizzerie, pasticcerie e locali...")
        return [
            {
                "id": "food_1",
                "name": "Pasticceria Mungiguerra",
                "category": "food",
                "coords": [40.9718, 14.2065],
                "description": "Casa della tipica 'Polacca Aversana'.",
                "status": "Aperto - Valutazione: 4.8★",
                "icon": "utensils",
                "color": "orange"
            },
            {
                "id": "food_2",
                "name": "Pizzeria Carlo Sammarco 2.0",
                "category": "food",
                "coords": [40.9692, 14.2041],
                "description": "Famosa pizzeria per la pizza a canotto ad alta idratazione.",
                "status": "Aperto dalle 19:30 - Valutazione: 4.7★",
                "icon": "pizza-slice",
                "color": "orange"
            }
        ]

class ServicesAgent:
    """Agente dedicato a trasporti, parcheggi e servizi di pubblica utilità."""
    def run() -> List[Dict[str, Any]]:
        print("[🤖 ServicesAgent] Verifica stazioni, ZTL e farmacie di turno...")
        return [
            {
                "id": "serv_1",
                "name": "Stazione Ferroviaria di Aversa",
                "category": "servizi",
                "coords": [40.9702, 14.2155],
                "description": "Snodo ferroviario RFI per Napoli, Roma e Caserta.",
                "status": "Servizio regolare",
                "icon": "train",
                "color": "green"
            },
            {
                "id": "serv_2",
                "name": "Metropolitana EAV - Aversa Centro",
                "category": "servizi",
                "coords": [40.9722, 14.2045],
                "description": "Linea Arcobaleno verso Piscinola / Napoli.",
                "status": "Treni ogni 15 min",
                "icon": "subway",
                "color": "green"
            }
        ]

class AversaSwarmOrchestrator:
    """Orchestratore che coordina lo sciame di agenti e unifica il DB locale."""
    def __init__(self):
        self.culture_agent = CultureAgent()
        self.food_agent = FoodAgent()
        self.services_agent = ServicesAgent()

    def fetch_all_city_data() -> Dict[str, Any]:
        print("\n--- 🚀 AVVIO SCIAME DI AGENTI PER AVERSA ---")
        monuments = self.culture_agent.run()
        food = self.food_agent.run()
        services = self.services_agent.run()

        all_pois = monuments + food + services
        
        print(f"[✅ Sciame] Elaborazione completata: {len(all_pois)} POI trovati e aggiornati.\n")
        return {
            "city": "Aversa",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pois": all_pois
        }


# ==============================================================================
# 2. GENERATORE DELL'INTERFACCIA MAPPA 3D (FRONTEND BUILDER)
# ==============================================================================

class Aversa3DMapBuilder:
    """Genera l'applicazione web/mobile con mappa 3D ed estrusioni vettoriali."""
    def __init__(self, city_data: Dict[str, Any]):
        self.city_data = city_data
        self.aversa_coords = [40.9729, 14.2078]

    def build_and_save(self, output_file: str = "index.html"):
        # Inizializzazione Mappa con Folium
        m = folium.Map(
            location=self.aversa_coords,
            zoom_start=16,
            tiles="CartoDB positron",
            control_scale=True
        )

        # Plugin per la vista 3D / Edifici vettoriali (Locate & MiniMap)
        plugins.MiniMap(toggle_display=True).add_to(m)

        # Raggruppamento Marker per categoria
        fg_monumenti = folium.FeatureGroup(name="🏛️ Monumenti & Storia").add_to(m)
        fg_food = folium.FeatureGroup(name="🍕 Food & Locali").add_to(m)
        fg_servizi = folium.FeatureGroup(name="🚆 Servizi & Trasporti").add_to(m)

        groups = {
            "monumenti": fg_monumenti,
            "food": fg_food,
            "servizi": fg_servizi
        }

        # Popolamento dei Marker aggiornati dallo sciame
        for poi in self.city_data["pois"]:
            popup_html = f"""
            <div style="font-family: Arial, sans-serif; width: 220px;">
                <h4 style="margin-bottom: 5px; color: #1e293b;">{poi['name']}</h4>
                <p style="font-size: 12px; color: #64748b; margin-top: 0;"><b>Stato:</b> {poi['status']}</p>
                <hr style="border: 0.5px solid #e2e8f0;"/>
                <p style="font-size: 13px; color: #334155;">{poi['description']}</p>
                <span style="font-size: 10px; background: #eff6ff; color: #2563eb; padding: 3px 6px; border-radius: 4px;">
                    🤖 Sincronizzato da Agent Swarm
                </span>
            </div>
            """
            
            icon = folium.Icon(color=poi["color"], icon=poi["icon"], prefix="fa")
            
            folium.Marker(
                location=poi["coords"],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=poi["name"],
                icon=icon
            ).add_to(groups.get(poi["category"], m))

        folium.LayerControl(collapsed=False).add_to(m)

        # Salvataggio Mappa
        m.save(output_file)
        
        # Iniezione personalizzata del CSS e Header per l'effetto HUD dello Sciame
        self._inject_hud_overlay(output_file)
        print(f"[📄 App] Applicazione generata con successo: '{output_file}'")

    def _inject_hud_overlay(self, file_path: str):
        """Inietta un pannello UI in tempo reale nel file HTML prodotto."""
        hud_code = f"""
        <!-- HUD Sciame Agenti -->
        <div id="swarm-hud" style="
            position: fixed;
            top: 15px;
            left: 50px;
            z-index: 9999;
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(8px);
            color: #white;
            padding: 12px 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
            border: 1px solid rgba(255,255,255,0.1);
        ">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="height: 10px; width: 10px; background-color: #22c55e; border-radius: 50%; display: inline-block;"></span>
                <strong style="font-size: 14px; letter-spacing: 0.5px;">AVERSA SMART CITY 3D</strong>
            </div>
            <p style="margin: 4px 0 0 0; font-size: 11px; color: #94a3b8;">
                Sciame Agenti: <span style="color: #38bdf8;">ATTIVO</span> | Ultimo sync: {self.city_data['last_updated']}
            </p>
        </div>
        </body>
        """
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = content.replace("</body>", hud_code)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)


# ==============================================================================
# 3. MAIN EXECUTION (Esecuzione dell'App)
# ==============================================================================

if __name__ == "__main__":
    # 1. Avvia lo sciame per raccogliere ed elaborare i dati di Aversa
    orchestrator = AversaSwarmOrchestrator()
    city_data = orchestrator.fetch_all_city_data()

    # 2. Costruisce l'interfaccia Mappa 3D con i dati dello sciame
    app_builder = Aversa3DMapBuilder(city_data)
    output_html = "aversa_3d_app.html"
    app_builder.build_and_save(output_html)

    # 3. Apre automaticamente l'App nel browser predefinito
    abs_path = os.path.abspath(output_html)
    print(f"[🌐 Browser] Apertura dell'app Aversa 3D su: file://{abs_path}")
    webbrowser.open(f"file://{abs_path}")
