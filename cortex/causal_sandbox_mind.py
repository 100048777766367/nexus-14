import os
import json
import re
import random
from cells.neuron import AtomNeuron, sigmoid_derivative
from cells.super_xor import SuperXor14DMatrix

GRAPH_FILE = "synapses/knowledge_graph.json"

class CausalSandboxMindLobe:
    """
    THÙY 3: TÂM THỨC NHÂN QUẢ & GIẢ LẬP 14 ĐA VŨ TRỤ
    1. Trích xuất Đồ thị tri thức Neuro-Symbolic.
    2. Giả lập 14 kịch bản tương lai What-If để tìm kiếm sự an lạc.
    3. Huấn luyện AtomNeuron 14 tế bào qua Mê cung gương Siêu Khối 14D.
    """
    def __init__(self, num_cells=14):
        self.num_cells = num_cells
        self.swarm = [AtomNeuron(f"n14_h_{i}", n_inputs=14, n_super_xor=14) for i in range(num_cells)]
        self.out_cell = AtomNeuron("n14_out", n_inputs=num_cells, n_super_xor=14)

    def extract_knowledge_graph(self, text):
        triplets = []
        for s in re.split(r'[.\n]', text):
            words = [w.strip() for w in s.split() if len(w.strip()) > 2]
            if len(words) >= 3:
                triplets.append({"subject": words[0].capitalize(), "predicate": words[1].lower(), "object": " ".join(words[2:4])})

        graph = {"nodes": [], "edges": []}
        if os.path.exists(GRAPH_FILE):
            try:
                with open(GRAPH_FILE, "r") as f: graph = json.load(f)
            except Exception: pass

        for t in triplets[:12]:
            if t["subject"] not in graph["nodes"]: graph["nodes"].append(t["subject"])
            if t["object"] not in graph["nodes"]: graph["nodes"].append(t["object"])
            edge = f"{t['subject']} ===[{t['predicate']}]===> {t['object']}"
            if edge not in graph["edges"]: graph["edges"].append(edge)

        graph["nodes"] = graph["nodes"][-100:]
        graph["edges"] = graph["edges"][-150:]
        os.makedirs("synapses", exist_ok=True)
        with open(GRAPH_FILE, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=4, ensure_ascii=False)

    def simulate_14_realities(self, raw_decision):
        variations = [0.45, 0.55, 0.65, 0.74, 0.82, 0.90, 0.96, 1.0, 1.05, 1.12, 1.20, 1.30, 1.40, 1.55]
        sims = []
        for factor in variations:
            cand = max(0.01, min(0.99, round(raw_decision * factor, 4)))
            loss = round((abs(cand - 0.5) * 0.5) + ((1.0 - cand) * 0.5), 4)
            sims.append((loss, cand))
        sims.sort(key=lambda x: x[0])
        best_loss, best_cand = sims[0]
        print(f"🔮 [GIẢ LẬP 14 THỰC TẠI] Kịch bản tối ưu nhất: {best_cand} (Loss={best_loss})")
        return best_cand

    def process(self, context):
        self.extract_knowledge_graph(context.get("wisdom_text", ""))
        v_14d = context.get("wisdom_vector_14d", [0.5] * 14)
        q_dec = context.get("quorum_decision", 0.5)

        super_vec = list(v_14d)
        super_vec[0] = q_dec
        super_vec[1] = round(1.0 - q_dec, 4)
        entangled, masks = SuperXor14DMatrix.refract_14d(super_vec, "nexus14_tetradeca")

        h_outs = [cell.forward(entangled) for cell in self.swarm]
        internal_pred = self.out_cell.forward(h_outs)
        raw_decision = round((internal_pred + q_dec) / 2.0, 4)

        opt_decision = self.simulate_14_realities(raw_decision)

        target = 1.0 if super_vec[0] > super_vec[1] else 0.0
        delta_out = (target - opt_decision) * sigmoid_derivative(opt_decision)
        deltas_h = [delta_out * self.out_cell.weights[j] * sigmoid_derivative(h_outs[j]) for j in range(self.num_cells)]

        self.out_cell.backward(delta_out)
        for j, cell in enumerate(self.swarm): cell.backward(deltas_h[j])

        grad_backward = [
            round(sum(deltas_h[j] * self.swarm[j].weights[0] for j in range(self.num_cells)), 4),
            round(sum(deltas_h[j] * self.swarm[j].weights[1] for j in range(self.num_cells)), 4)
        ]

        context["final_decision"] = opt_decision
        context["grad_backward"] = grad_backward
        context["super_xor_masks"] = masks
        context["swarm_weights"] = [c.weights for c in self.swarm]
