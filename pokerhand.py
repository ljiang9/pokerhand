#!/usr/bin/env python3
"""扑克牌型评估器: 5 张牌的牌力判定与对决。

用法:
    pokerhand "As Ks Qs Js Ts"
    pokerhand --compare "Ah Kh Qh Jh 9h" "Ad Kd Qd Jd 9d"

牌面记法: 2-9 T J Q K A + 花色 s(黑桃) h(红桃) d(方块) c(梅花)
"""

import argparse
import sys
from collections import Counter

RANKS = "23456789TJQKA"
SUITS = "shdc"
RANK_VALUE = {r: i for i, r in enumerate(RANKS, start=2)}

CATEGORIES = {
    10: "皇家同花顺 Royal Flush",
    9: "同花顺 Straight Flush",
    8: "四条 Four of a Kind",
    7: "葫芦 Full House",
    6: "同花 Flush",
    5: "顺子 Straight",
    4: "三条 Three of a Kind",
    3: "两对 Two Pair",
    2: "一对 Pair",
    1: "高牌 High Card",
}


def parse_hand(text):
    """解析 5 张牌, 返回 [(rank_value, suit)] 列表。"""
    parts = text.split()
    if len(parts) != 5:
        raise ValueError(f"需要 5 张牌, 得到 {len(parts)} 张: {text!r}")
    cards = []
    for p in parts:
        p = p.strip()
        if len(p) != 2 or p[0].upper() not in RANK_VALUE or p[1].lower() not in SUITS:
            raise ValueError(f"非法牌面: {p!r} (格式如 As, 需 2-9TJQKA + shdc)")
        cards.append((RANK_VALUE[p[0].upper()], p[1].lower()))
    if len(set(cards)) != 5:
        raise ValueError(f"牌不能重复: {text!r}")
    return cards


def _straight_high(ranks):
    """返回顺子的顶张点数, 不是顺子返回 None。轮子顺 A-2-3-4-5 顶张为 5。"""
    uniq = sorted(set(ranks))
    if len(uniq) != 5:
        return None
    if uniq[-1] - uniq[0] == 4:
        return uniq[-1]
    if uniq == [2, 3, 4, 5, 14]:  # A-2-3-4-5
        return 5
    return None


def evaluate(cards):
    """评估牌力, 返回 (类别分, tiebreaker元组)。越大越强。"""
    ranks = sorted((r for r, _ in cards), reverse=True)
    suits = [s for _, s in cards]
    flush = len(set(suits)) == 1
    s_high = _straight_high(ranks)
    counts = Counter(ranks)
    # 按 (数量, 点数) 降序排: [四条点, 踢脚...] / [三条点, 对子点] / ...
    groups = sorted(counts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    if flush and s_high == 14:
        return (10, (14,))
    if flush and s_high:
        return (9, (s_high,))
    if groups[0][1] == 4:
        quad, kicker = groups[0][0], groups[1][0]
        return (8, (quad, kicker))
    if groups[0][1] == 3 and groups[1][1] == 2:
        return (7, (groups[0][0], groups[1][0]))
    if flush:
        return (6, tuple(ranks))
    if s_high:
        return (5, (s_high,))
    if groups[0][1] == 3:
        trips = groups[0][0]
        kickers = sorted((r for r, c in groups[1:] for _ in range(c)), reverse=True)
        return (4, (trips, *kickers))
    if groups[0][1] == 2 and groups[1][1] == 2:
        pairs = sorted((groups[0][0], groups[1][0]), reverse=True)
        kicker = groups[2][0]
        return (3, (*pairs, kicker))
    if groups[0][1] == 2:
        pair = groups[0][0]
        kickers = sorted((r for r, c in groups[1:] for _ in range(c)), reverse=True)
        return (2, (pair, *kickers))
    return (1, tuple(ranks))


def describe(score):
    cat, tb = score
    name = CATEGORIES[cat]
    tb_str = " ".join(RANKS[v - 2] for v in tb)
    return f"{name} (tiebreak: {tb_str})"


def cmd_show(args):
    cards = parse_hand(args.hand)
    print(describe(evaluate(cards)))


def cmd_compare(args):
    c1, c2 = parse_hand(args.compare[0]), parse_hand(args.compare[1])
    s1, s2 = evaluate(c1), evaluate(c2)
    print(f"手牌一: {describe(s1)}")
    print(f"手牌二: {describe(s2)}")
    if s1 > s2:
        print("结果: 手牌一获胜")
    elif s2 > s1:
        print("结果: 手牌二获胜")
    else:
        print("结果: 平局")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pokerhand", description="扑克牌型评估器 (5 张牌)")
    ap.add_argument("hand", nargs="?", help='5 张牌, 如 "As Ks Qs Js Ts"')
    ap.add_argument("--compare", nargs=2, metavar=("HAND1", "HAND2"), help="对决两手牌")
    args = ap.parse_args(argv)
    try:
        if args.compare:
            cmd_compare(args)
        elif args.hand:
            cmd_show(args)
        else:
            ap.print_help()
            return 2
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
