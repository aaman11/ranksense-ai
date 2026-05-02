"""RankSense AI — AEO Diagnostic Engine (Gemini Edition)."""
import streamlit as st
import pandas as pd

from gemini_client import run_all_personas
from analyzer import analyze

st.set_page_config(
    page_title="RankSense AI — Gemini Edition",
    page_icon="🧠",
    layout="wide",
)

# --- Header ---
st.markdown("### 🧠 RankSense AI")
st.title("AEO Diagnostic Engine — Gemini Edition")
st.caption(
    "See how Gemini recommends brands across three buyer personas — "
    "Budget, Premium & Expert. Compare rankings and uncover your AI Visibility Score."
)

# --- Input ---
EXAMPLES = [
    "best magnesium supplement for seniors",
    "best running shoes for marathons",
    "best CRM for small business",
    "best electric SUV under $50k",
]

col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input(
        "Product query",
        placeholder="e.g. best magnesium supplement for seniors",
        label_visibility="collapsed",
    )
with col2:
    run = st.button("✨ Analyze", type="primary", use_container_width=True)

st.write("**Try:** " + " · ".join(f"`{e}`" for e in EXAMPLES))

# --- Run ---
if run:
    if not query or len(query.strip()) < 3:
        st.error("Enter a query (3+ characters).")
        st.stop()

    with st.spinner("Querying Gemini across 3 personas…"):
        results = run_all_personas(query.strip())
        analysis = analyze(results)

    # --- Visibility Leaderboard ---
    st.subheader("🏆 AI Visibility Leaderboard")
    st.caption("Rank 1 = 5 pts · Rank 5 = 1 pt · Score normalized to 0–100")
    if analysis["frequency"]:
        df = pd.DataFrame([
            {
                "Brand": b["brand"],
                "Visibility": b["visibility"],
                "Mentions": f"{b['count']}/{len([r for r in results if r['rankings']])}",
                "Best Rank": b["best_rank"],
                "Personas": ", ".join(b["personas"]),
            }
            for b in analysis["frequency"][:10]
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No rankings returned. Try again.")

    # --- Insights & Suggestions ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📈 Insights")
        for s in analysis["insights"]:
            st.markdown(f"- {s}")
    with c2:
        st.subheader("💡 Suggestions")
        for s in analysis["suggestions"]:
            st.markdown(f"- {s}")

    # --- Per-Persona Rankings ---
    st.subheader("👥 Rankings by Persona")
    cols = st.columns(len(results))
    for col, r in zip(cols, results):
        with col:
            st.markdown(f"**{r['label']}**")
            if r.get("error"):
                st.error(r["error"])
            elif not r["rankings"]:
                st.warning("No rankings parsed.")
            else:
                for item in r["rankings"]:
                    st.markdown(
                        f"**{item['rank']}. {item['brand']}**  \n"
                        f"<span style='color:#888;font-size:0.85em'>{item['reason']}</span>",
                        unsafe_allow_html=True,
                    )

st.divider()
st.caption("Powered by Google Gemini 2.5 Pro · One model, three perspectives.")
