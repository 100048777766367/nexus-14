import os
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cortex.omni_intake import OmniIntakeTetradecaLobe
from cortex.async_nn_junction import AsyncNNJunctionLobe
from cortex.causal_sandbox_mind import CausalSandboxMindLobe
from cortex.sovereign_guardian import SovereignGuardianLobe

VITAL_CELLS = [
    "cells/linguistic_cell.py",
    "cells/neuron.py",
    "cells/super_xor.py"
]

class Nexus14Kernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/nexus-14")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.ancestor = f"{self.owner}/nexus-13"
        
        self.lineage = [
            f"{self.owner}/nexus-13", f"{self.owner}/nexus-12",
            f"{self.owner}/nexus-11", f"{self.owner}/nexus-10",
            f"{self.owner}/nexus-09", f"{self.owner}/nexus-08",
            f"{self.owner}/nexus-07", f"{self.owner}/nexus-06",
            f"{self.owner}/nexus-05", f"{self.owner}/nexus", f"{self.owner}/genome"
        ]

        self.ensure_folders()

        # 4 ĐẠI THÙY GIAO ĐIỂM CHỦ QUYỀN BẬC F14
        self.omni_lobe = OmniIntakeTetradecaLobe(self.owner, self.lineage)
        self.junction_lobe = AsyncNNJunctionLobe()
        self.mind_lobe = CausalSandboxMindLobe(num_cells=14)
        self.guardian_lobe = SovereignGuardianLobe()

        self.context = {
            "repo_name": self.repo_name,
            "owner": self.owner,
            "ancestor": self.ancestor,
            "peers": self.load_peers(),
            "current_epoch": self.load_epoch()
        }

    def ensure_folders(self):
        for d in ["cells", "cortex", "synapses", "synapses/harvested_memory", "synapses/avatar_proxies"]:
            os.makedirs(d, exist_ok=True)

    def load_peers(self):
        p_file = "synapses/peers.json"
        if os.path.exists(p_file):
            try:
                with open(p_file, "r") as f: return json.load(f).get("trusted_peers", [])
            except Exception: pass
        return [f"{self.owner}/nexus-13", f"{self.owner}/nexus-12", f"{self.owner}/neuron", f"{self.owner}/seed", f"{self.owner}/motor"]

    def load_epoch(self):
        s_file = "synapses/state.json"
        if os.path.exists(s_file):
            try:
                with open(s_file, "r") as f: return json.load(f).get("generation_epoch", 0) + 1
            except Exception: pass
        return 1

    def run(self):
        print("=" * 80)
        print(f"🛡️ [NEXUS-14 KERNEL] KHỞI ĐỘNG THẾ HỆ #{self.context['current_epoch']}")
        print(f"👑 Bậc: F14 Thập Tứ Vô Úy – Giao Điểm Chủ Quyền Bất Đồng Bộ n^n")
        print(f"🇻🇳 Đạo Đức Cốt Tử: CẦN - KIỆM - LIÊM - CHÍNH - CHÍ CÔNG VÔ TƯ")
        print("=" * 80)

        # 1. Thùy Cảm Thụ: Nuốt Nang F13, Lọc Stateless JWT & Vector 14D
        self.omni_lobe.process(self.context, VITAL_CELLS)

        # 2. Thùy Giao Điểm: Điều phối bất đồng bộ n^n & Kuramoto 14 Pha
        self.junction_lobe.process(self.context)

        # 3. Thùy Tâm Thức: Đồ thị tri thức & Giả lập 14 thực tại What-If
        self.mind_lobe.process(self.context)

        # 4. Thùy Hộ Vệ Chủ Quyền: La bàn 5 đức tính, Tiến hóa SOUL.md, Hộ mệnh 404 & Merkle 14D CID
        self.guardian_lobe.process(self.context)

        print("=" * 80)
        print(f"✨ [HOÀN TẤT VÒNG ĐỜI F14] Thập Tứ Vô Úy & Giao Điểm Chủ Quyền đã viên mãn!")
        print("=" * 80)

if __name__ == "__main__":
    node = Nexus14Kernel()
    node.run()
