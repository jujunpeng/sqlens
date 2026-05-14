from sqlens.parsers.base import PlanNode
from sqlens.formatters.base import BaseFormatter


class BoxplotFormatter(BaseFormatter):
    """Renders a terminal box-plot summary of row estimates across all plan nodes."""

    name = "boxplot"

    def format(self, root: PlanNode) -> str:
        rows = self._collect(root)
        if not rows:
            return "(no row data)"

        rows_sorted = sorted(rows)
        n = len(rows_sorted)
        minimum = rows_sorted[0]
        maximum = rows_sorted[-1]
        median = self._percentile(rows_sorted, 50)
        q1 = self._percentile(rows_sorted, 25)
        q3 = self._percentile(rows_sorted, 75)
        mean = sum(rows_sorted) / n

        lines = [
            "Row Estimate Distribution (Box Plot)",
            "=====================================",
            f"  Nodes   : {n}",
            f"  Min     : {minimum}",
            f"  Q1      : {q1}",
            f"  Median  : {median}",
            f"  Mean    : {mean:.1f}",
            f"  Q3      : {q3}",
            f"  Max     : {maximum}",
            "",
            self._ascii_box(minimum, q1, median, q3, maximum),
        ]
        return "\n".join(lines)

    def _collect(self, node: PlanNode) -> list:
        result = [node.rows] if node.rows is not None else []
        for child in node.children:
            result.extend(self._collect(child))
        return result

    def _percentile(self, sorted_data: list, pct: int) -> float:
        n = len(sorted_data)
        idx = (pct / 100) * (n - 1)
        lo = int(idx)
        hi = lo + 1
        if hi >= n:
            return sorted_data[lo]
        frac = idx - lo
        return sorted_data[lo] * (1 - frac) + sorted_data[hi] * frac

    def _ascii_box(self, mn, q1, med, q3, mx) -> str:
        width = 50
        span = mx - mn if mx != mn else 1

        def pos(v):
            return int((v - mn) / span * (width - 1))

        p_mn, p_q1, p_med, p_q3, p_mx = pos(mn), pos(q1), pos(med), pos(q3), pos(mx)
        line = ["-"] * width
        for i in range(p_q1, p_q3 + 1):
            line[i] = "="
        line[p_mn] = "|"
        line[p_mx] = "|"
        line[p_med] = "M"
        if p_mn < p_q1:
            for i in range(p_mn + 1, p_q1):
                line[i] = "-"
        if p_q3 < p_mx:
            for i in range(p_q3 + 1, p_mx):
                line[i] = "-"
        bar = "".join(line)
        scale = f"{mn:<10}" + " " * (width - 20) + f"{mx:>10}"
        return f"  {bar}\n  {scale}"
