# -*- coding: utf-8 -*-
"""
AHL · Milvus Lite 向量匹配 POC
================================
目的：验证 Milvus（嵌入式 Lite 版）作为 AHL「最优匹配」引擎的底座，
     在 Python 3.14 上跑通「语义检索 + 元数据过滤」完整闭环。

场景：酒店最优匹配 —— 用自然语言描述需求，返回语义最匹配的酒店。
      对应 SOUL 群论视角的「匹配问题」+ IDENTITY 的「版本追求=最优匹配」方法论。

依赖：pymilvus 3.0.1 + milvus-lite 3.2.1 + model2vec(potion-base-8M, 256维)
运行：python toolbox/ahl_milvus_poc.py
"""
import sys
import time
import numpy as np
from pymilvus import MilvusClient
from model2vec import StaticModel

# Windows GBK 控制台 → UTF-8，避免 emoji/中文报 UnicodeEncodeError
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# 同时把结果落盘为干净 UTF-8 文件（绕过 PowerShell 管道乱码）
class _Tee:
    def __init__(self, path):
        self._f = open(path, "w", encoding="utf-8")
        self._stdout = sys.stdout
    def write(self, s):
        self._stdout.write(s)
        self._f.write(s)
    def flush(self):
        self._stdout.flush()
        self._f.flush()
    def close(self):
        self._f.close()

_TEE = _Tee("toolbox/ahl_milvus_poc_result.txt")
sys.stdout = _TEE

# ---------------------------------------------------------------------------
# 0. 配置
# ---------------------------------------------------------------------------
DB_FILE = "ahl_hotels.db"          # Milvus Lite 本地持久化文件
COLLECTION = "ahl_hotels"          # 集合名
DIM = 256                          # potion-base-8M 维度
EMBED_MODEL = "minishlab/potion-base-8M"

# ---------------------------------------------------------------------------
# 1. 加载 embedding 模型（与 Eric 现有 local_semantic_search 同源）
# ---------------------------------------------------------------------------
print("⏳ 加载 embedding 模型", EMBED_MODEL, "...")
t0 = time.time()
model = StaticModel.from_pretrained(EMBED_MODEL)
print(f"   ✅ 模型就绪 ({time.time()-t0:.1f}s), 维度={DIM}")

def embed(texts):
    """文本 -> L2 归一化向量"""
    v = model.encode(texts)
    v = np.asarray(v, dtype=np.float32)
    v = v / np.linalg.norm(v, axis=1, keepdims=True)  # 归一化，配合 COSINE/IP
    return v.tolist()

# ---------------------------------------------------------------------------
# 2. 样例酒店库（AHL 场景，含元数据字段）
# ---------------------------------------------------------------------------
HOTELS = [
    {"name": "都江堰国堰宾馆",   "city": "都江堰", "tier": "高端", "tag": "水文化·文创·历史",
     "desc": "临都江堰水利工程，水文化主题，单一IP贯穿空间，预留第三方文创运营区"},
    {"name": "成都花园宾馆",     "city": "成都",   "tier": "高端", "tag": "文化主题·花园·国潮",
     "desc": "市中心花园式酒店，文化主题改造样板，国潮与在地文化结合"},
    {"name": "岷山饭店",         "city": "成都",   "tier": "中高端", "tag": "商务·政务·老字号",
     "desc": "成都老牌商务酒店，政务接待与商务会议为主，配套完善"},
    {"name": "西昌岷山饭店",     "city": "西昌",   "tier": "高端", "tag": "度假·商务·标杆",
     "desc": "西昌度假商务标杆，12000方自有资产改造，经营奇迹样本"},
    {"name": "重庆丽苑维景国际", "city": "重庆",   "tier": "高端", "tag": "商务·国际·收益管理",
     "desc": "国际品牌商务酒店，收益管理能力行业标杆，RGI长期领先"},
    {"name": "襄阳共享维景",     "city": "襄阳",   "tier": "中端", "tag": "商旅·共享·性价比",
     "desc": "商旅共享型酒店，性价比导向，适合差旅与中转客群"},
    {"name": "青城山医养度假酒店", "city": "青城山", "tier": "中高端", "tag": "医养·康养·疗愈",
     "desc": "医养结合轻资产模式，康养疗愈，配套健康管理与慢病调理"},
    {"name": "三亚亲子度假酒店", "city": "三亚",   "tier": "中高端", "tag": "亲子·家庭·度假",
     "desc": "亲子家庭度假酒店，儿童俱乐部，泳池沙滩，一价全包"},
    {"name": "古尔沟温泉度假酒店", "city": "古尔沟", "tier": "中高端", "tag": "温泉·康养·藏羌",
     "desc": "天然温泉度假，藏羌文化，冬季温泉疗养圣地"},
    {"name": "上海设计精品酒店", "city": "上海",   "tier": "中端", "tag": "设计·潮玩·年轻",
     "desc": "设计感精品酒店，年轻潮玩客群，社交型公共空间"},
    {"name": "成都快捷商务酒店", "city": "成都",   "tier": "经济", "tag": "快捷·商务·性价比",
     "desc": "经济型快捷商务酒店，标准化客房，高性价比差旅选择"},
    {"name": "川西野奢营地",     "city": "川西",   "tier": "高端", "tag": "体旅·野奢·自然",
     "desc": "高原野奢帐篷营地，体旅融合，星空与雪山景观，户外体验"},
]

# ---------------------------------------------------------------------------
# 3. 建集合 + 灌数据
# ---------------------------------------------------------------------------
def build_index():
    client = MilvusClient(DB_FILE)
    if client.has_collection(COLLECTION):
        client.drop_collection(COLLECTION)

    client.create_collection(
        collection_name=COLLECTION,
        dimension=DIM,
        metric_type="COSINE",          # 余弦相似度
        # 标量字段在 pymilvus 3.x 通过 schema 或 auto 推断；这里用显式 schema 保证过滤字段存在
    )

    rows = []
    for i, h in enumerate(HOTELS):
        vec = embed([f"{h['name']} {h['tag']} {h['desc']}"])[0]
        rows.append({
            "id": i,                     # 主键，Milvus 必须显式提供（除非 auto_id）
            "name": h["name"],
            "city": h["city"],
            "tier": h["tier"],
            "tag": h["tag"],
            "desc": h["desc"],
            "vector": vec,
        })

    client.insert(collection_name=COLLECTION, data=rows)
    print(f"   ✅ 已写入 {len(rows)} 家酒店向量")
    return client

# ---------------------------------------------------------------------------
# 4. 查询：语义检索 + 元数据过滤
# ---------------------------------------------------------------------------
def search(client, query, top_k=3, filter_expr=None, note=""):
    print(f"\n🔍 查询：{query}" + (f"  [过滤: {filter_expr}]" if filter_expr else ""))
    qv = embed([query])[0]
    res = client.search(
        collection_name=COLLECTION,
        data=[qv],
        limit=top_k,
        output_fields=["name", "city", "tier", "tag"],
        filter=filter_expr,
    )
    hits = res[0]
    for i, h in enumerate(hits, 1):
        ent = h["entity"]
        score = h["distance"]          # COSINE 距离，越接近 1 越相似
        print(f"   {i}. {ent['name']:<14} | {ent['city']:<4} {ent['tier']:<3} | {ent['tag']:<14} | 相似度={score:.3f}")
    return hits

# ---------------------------------------------------------------------------
# 5. 主流程
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    t_start = time.time()
    client = build_index()

    print("\n" + "=" * 72)
    print("场景 A · 纯语义匹配（无过滤）—— 自然语言找酒店")
    print("=" * 72)
    search(client, "有文化底蕴、适合带家人安静度假的中高端酒店", top_k=3)

    print("\n" + "=" * 72)
    print("场景 B · 混合检索（向量 + 元数据过滤）—— 成都的高端酒店")
    print("=" * 72)
    search(client, "高端商务政务酒店", top_k=3, filter_expr='city == "成都" and tier == "高端"')

    print("\n" + "=" * 72)
    print("场景 C · 康养/温泉需求")
    print("=" * 72)
    search(client, "带温泉、能疗愈放松的康养度假", top_k=3)

    print("\n" + "=" * 72)
    print(f"✅ POC 完成，总耗时 {time.time()-t_start:.2f}s")
    print(f"   数据持久化于：{DB_FILE}")
    print("=" * 72)
