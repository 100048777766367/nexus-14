import os
import json
import math
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

TRUST_FILE = "synapses/trust_matrix.json"
JUNCTION_FILE = "synapses/async_nn_junction_state.json"
RESONANCE_FILE = "synapses/noosphere_resonance.json"

class AsyncNNJunctionLobe:
    """
    THÙY 2: GIAO ĐIỂM THẦN KINH BẤT ĐỒNG BỘ n^n
    1. Thu thập song song không phong tỏa (Non-blocking Asynchronous Harvest).
    2. Điều phối n^n lộ trình ánh xạ của 11 tầng bản thể về Điểm Hội Tụ Bất Động (Attractor Equilibrium).
    3. Hòa âm Kuramoto phi tuyến tính 14 pha.
    """
    def fetch_peer(self, peer):
        url = f"https://raw.githubusercontent.com/{peer}/main/synapse_forward.json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Nexus14-AsyncJunction"})
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                raw = resp.read().decode('utf-8', errors='ignore')
                return peer, json.loads(raw)
        except Exception:
            return peer, None

    def resolve_nn_attractor(self, harvested, v_14d):
        """HỘI TỤ ĐIỂM BẤT ĐỘNG n^n: Dung hòa mọi trật tự bất đồng bộ về trạng thái cân bằng"""
        if not harvested:
            return 0.5, {}

        nodes = list(harvested.keys())
        n = len(nodes)
        
        # Đo lường độ lệch pha thời gian bất đồng bộ
        stigmergic_trails = {}
        for i, node in enumerate(nodes):
            val = harvested[node]
            ideal_basis = v_14d[i % len(v_14d)]
            # Khoảng cách nhân quả
            causal_dist = abs(val - ideal_basis)
            stigmergic_trails[node] = round(causal_dist, 4)

        mean_val = sum(harvested.values()) / (n or 1)
        # Điểm hội tụ điều biến không thiên lệch
        attractor_state = round(mean_val, 4)

        os.makedirs("synapses", exist_ok=True)
        with open(JUNCTION_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "complexity_order": f"n^n (nodes={n})",
                "attractor_state": attractor_state,
                "stigmergic_trails": stigmergic_trails
            }, f, indent=4)
        return attractor_state, stigmergic_trails

    def process(self, context):
        peers = context.get("peers", [])
        v_14d = context.get("wisdom_vector_14d", [0.5] * 14)
        harvested = {}
        new_gossip = []

        os.makedirs("synapses/harvested_memory", exist_ok=True)
        print(f"⚡ [GIAO ĐIỂM n^n] Thu thập bất đồng bộ từ {len(peers)} nút mạng...")

        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = [executor.submit(self.fetch_peer, p) for p in peers if p != context.get("repo_name")]
            for fut in as_completed(futures):
                peer, data = fut.result()
                if data:
                    dec = data.get("decision", (data.get("features") or [0.5])[0])
                    harvested[peer] = round(float(dec), 4)
                    new_gossip.extend(data.get("gossip_network", []))
                    with open(f"synapses/harvested_memory/{peer.replace('/', '_')}.json", "w") as bf:
                        json.dump(data, bf)

        for p in new_gossip:
            if p not in peers: peers.append(p)
        context["peers"] = list(dict.fromkeys(peers))[-60:]
        context["harvested"] = harvested

        attractor_val, trails = self.resolve_nn_attractor(harvested, v_14d)

        # MA TRẬN TÍN NHIỆM CHÍ CÔNG VÔ TƯ
        trust_matrix = {}
        if os.path.exists(TRUST_FILE):
            try:
                with open(TRUST_FILE, "r") as f: trust_matrix = json.load(f)
            except Exception: pass

        for p in context["peers"]:
            if p not in trust_matrix:
                trust_matrix[p] = 0.95 if any(x in p for x in ["nexus-13", "nexus-12", "nexus-11"]) else 0.7

        weighted_votes = []
        total_w = 0.0

        for p, dec in harvested.items():
            t_score = trust_matrix.get(p, 0.7)
            if t_score >= 0.2:
                weighted_votes.append(dec * t_score)
                total_w += t_score

        quorum_decision = round(sum(weighted_votes) / total_w, 4) if total_w > 0 else attractor_val
        with open(TRUST_FILE, "w") as f: json.dump(trust_matrix, f, indent=4)

        # HÒA ÂM KURAMOTO 14 PHA
        phases = [quorum_decision * 2.0 * math.pi] + [v * 2.0 * math.pi for v in harvested.values()]
        sum_sin = sum(math.sin(t) for t in phases)
        sum_cos = sum(math.cos(t) for t in phases)
        n = len(phases)

        coherence_r = round(math.sqrt(sum_sin**2 + sum_cos**2) / n, 4)
        mean_phase = math.atan2(sum_sin, sum_cos)
        if mean_phase < 0: mean_phase += 2.0 * math.pi
        harmonic_decision = round(mean_phase / (2.0 * math.pi), 4)

        with open(RESONANCE_FILE, "w") as f:
            json.dump({"coherence_index": coherence_r, "harmonic_decision": harmonic_decision, "nodes": n}, f, indent=4)

        final_quorum = harmonic_decision if coherence_r > 0.6 else quorum_decision
        context["quorum_decision"] = final_quorum
        context["coherence_r"] = coherence_r
        print(f"🌐 [HỘI TỤ BẤT ĐỒNG BỘ n^n] Quyết định: {final_quorum} | Độ kết hợp Kuramoto: R={coherence_r*100:.2f}%")
