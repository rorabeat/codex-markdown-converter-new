import re
import markdown


def convert_math_markdown_to_html(text: str) -> str:
    """
    Convert Markdown with LaTeX-style math into HTML.

    - Inline math: $...$
    - Block math: $$...$$

    Uses MathJax in the HTML output so formulas render in browsers.
    """
    # Normalize block math to MathJax script tags before markdown conversion
    def block_repl(match):
        expr = match.group(1).strip()
        return f"\n<script type=\"math/tex; mode=display\">{expr}</script>\n"

    text = re.sub(r"\$\$(.+?)\$\$", block_repl, text, flags=re.DOTALL)

    # Normalize inline math
    def inline_repl(match):
        expr = match.group(1).strip()
        return f"<script type=\"math/tex\">{expr}</script>"

    text = re.sub(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", inline_repl, text)

    body = markdown.markdown(text, extensions=["extra"])

    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Markdown + Math</title>
    <script>
      window.MathJax = {{
        tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']] }},
        svg: {{ fontCache: 'global' }}
      }};
    </script>
    <script defer src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js\"></script>
  </head>
  <body>
    {body}
  </body>
</html>"""


if __name__ == "__main__":
    sample = """
# 수식 예제

오일러 공식: $e^{i\\pi} + 1 = 0$

$$
\\int_0^1 x^2 dx = \\frac{1}{3}
$$
"""
    html = convert_math_markdown_to_html(sample)
    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("output.html 생성 완료")
