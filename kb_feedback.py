# -*- coding: utf-8 -*-
"""
B166ER 路由反馈CLI
用法:
  python kb_feedback.py "用户问题" "路由到的KB" "实际应该用" 1或0
示例:
  python kb_feedback.py "酒店收益如何提升" "hotel-industry" "hotel-revenue-management" 0
  python kb_feedback.py "YC申请截止日期" "startup-fundraising" "startup-fundraising" 1
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from evolve_kb import B166EREvolution

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python kb_feedback.py <query> <routed_kb> <actual_kb> [correct:0|1]")
        print("示例: python kb_feedback.py '酒店收益' 'hotel-industry' 'hotel-revenue' 0")
        sys.exit(1)
    
    query = sys.argv[1]
    routed = sys.argv[2]
    actual = sys.argv[3] if len(sys.argv) > 3 else ""
    correct = sys.argv[4] == "1" if len(sys.argv) > 4 else None
    
    evo = B166EREvolution()
    evo.log_feedback(query, routed, actual, correct)
    
    if correct is None:
        print(f"已记录: {query[:30]}... -> {routed}")
    else:
        print(f"反馈已记录 (正确性: {'✓' if correct else '✗'})")
