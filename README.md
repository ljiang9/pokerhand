# pokerhand

终端扑克牌型评估器:输入 5 张牌,输出牌型与牌力;也支持两手牌对决。

```bash
python -m pokerhand "As Ks Qs Js Ts"          # 皇家同花顺 Royal Flush
python -m pokerhand --compare "Ah Kh Qh Jh 9h" "Ad Kd Qd Jd 9d"
```

牌面记法:`2-9 T J Q K A` + 花色 `s/h/d/c`(黑桃/红桃/方块/梅花)。

## 设计取舍

- 只做 5 张牌评估,不做 7 选 5(德州扑克式)——"小巧"的定位。
- 牌力表示为 `(类别分, tiebreaker 元组)`,Python 元组比较天然实现"先比牌型再比踢脚"。
- 轮子顺 `A-2-3-4-5` 按顶张 5 处理,同花+轮子顺是最小的同花顺。

## 已知局限

- 只支持 5 张牌,不做 7 张选 5 的最优组合评估。
- 花色无大小之分,同牌力判平局(符合德州规则,分池)。
- 教学玩具,不做胜率/赔率计算。

## 许可证

MIT,Copyright (c) 2026 ljiang9
