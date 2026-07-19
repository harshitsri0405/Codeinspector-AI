import os

class ReportService:
    @staticmethod
    def compile_markdown_report(project_name, code_content, pylint_res, bandit_res, radon_res, ai_res, perf_res):
        """
        [Day 13 Feature] Compiles all hybrid engine analysis results into a structured 
        and clean Markdown text layout ready for distribution.
        """
        static_score = pylint_res.get('score', 8.0) * 10.0
        ai_score = ai_res.get('score', 80) if isinstance(ai_res, dict) else 80
        blended_score = round((static_score + ai_score) / 2, 2)
        
        ai_summary = ai_res.get('summary', 'Clean baseline architecture execution.') if isinstance(ai_res, dict) else 'Execution complete.'
        
        report_md = f"""# 🚀 AUTOMATED AI CODE REVIEW REPORT

### 📋 Project Identity Profile
* **Project Profile Name:** {project_name}
* **Scanner Combined Score:** {blended_score} / 100
* **Cyclomatic Complexity Level:** {radon_res.get('cyclomatic_complexity', '1.0')}
* **Maintainability Performance Index:** {radon_res.get('maintainability_index', '85.0')}/100

---

## 💡 Executive AI Code Review Summary
{ai_summary}

---

## 📊 Core Quality & Structure Diagnostics

### 🔒 Security & Vulnerabilities (Bandit Scanner Log)
"""
        if not bandit_res:
            report_md += "* 🎉 No critical execution vulnerabilities or security flaws identified by the scanner.\n"
        else:
            for flaw in bandit_res:
                report_md += f"* **[{flaw.get('severity', 'Medium')}] {flaw.get('issue', 'Alert')}**\n  * *Context Explanation:* {flaw.get('explanation')}\n"

        report_md += "\n### ✨ Style Standards & Layout Formats (Pylint Engine)\n"
        pylint_findings = pylint_res.get('findings', [])
        if not pylint_findings:
            report_md += "* 🎉 Script variables align completely with modular clean coding design formatting limits.\n"
        else:
            for note in pylint_findings:
                report_md += f"* ⚠️ {note}\n"

        report_md += "\n### 🤖 Expert Optimization Guidelines (AI Assistant Insights)\n"
        ai_findings = ai_res.get('findings', []) if isinstance(ai_res, dict) else []
        if not ai_findings:
            report_md += "* Code parameters conform fully with robust standard enterprise execution patterns.\n"
        else:
            for note in ai_findings:
                report_md += f"* **[{note.get('severity', 'Medium')}] {note.get('issue', 'Optimization')}**\n  * *Reasoning:* {note.get('explanation')}\n  * *Action Item:* {note.get('suggestion')}\n"

        report_md += f"""
---

## ⚡ Performance Optimization Metrics
* **Calculated Algorithmic Time Complexity:** {perf_res.get('estimated_time_complexity', 'O(N)')}
* **Calculated Algorithmic Space Bounds:** {perf_res.get('estimated_space_complexity', 'O(1)')}
* **I/O Latency Bottleneck Traps:** {perf_res.get('io_overhead_risk', 'Low')}

### Identified Code Performance Blocks:
"""
        bottlenecks = perf_res.get('bottlenecks', [])
        if not bottlenecks:
            report_md += "* Loop controls evaluate within optimal efficiency speed limits.\n"
        else:
            for bottleneck in bottlenecks:
                report_md += f"* 💡 {bottleneck}\n"

        report_md += f"""
---
*Report auto-compiled natively by AI Code Review Assistant Infrastructure Engine.*
"""
        return report_md