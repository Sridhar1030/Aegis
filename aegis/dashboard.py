import streamlit as st
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

from agents.graph import graph

st.set_page_config(page_title="AEGIS", page_icon="🛡️", layout="wide")

st.title("🛡️ AEGIS — AI-Enhanced Guardian for Intelligent Systems")
st.markdown("---")

col_input, col_spacer = st.columns([2, 3])
with col_input:
    pr_id = st.text_input("PR ID", value="PR-456")
    run = st.button("Run Pipeline", type="primary", use_container_width=True)

if run:
    with st.spinner("Running pipeline: replay → memory → risk → guard..."):
        result = graph.invoke({"pr_id": pr_id})

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    latency = result.get("replay_latency_delta", 0)
    risk = result.get("risk_score", 0)
    anomaly = result.get("anomaly_detected", False)

    with col1:
        st.metric("Replay Latency", f"{latency:.3f}s")
    with col2:
        st.metric("Risk Score", f"{risk:.2f}")
    with col3:
        failures = result.get("similar_failures") or []
        st.metric("Similar Failures", len(failures))
    with col4:
        if anomaly:
            st.metric("Guard Status", "ROLLBACK")
        else:
            st.metric("Guard Status", "APPROVED")

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.subheader("Risk Reasoning")
        st.info(result.get("risk_reasoning", "N/A"))

        st.subheader("Similar Past Failures")
        if failures:
            for i, f in enumerate(failures, 1):
                st.warning(f"{i}. {f}")
        else:
            st.write("No similar failures found.")

    with right:
        st.subheader("Guard Decision")
        if anomaly:
            st.error("🚨 ANOMALY DETECTED — Deployment blocked. Rollback triggered.")
        else:
            st.success("✅ All clear — Safe to deploy.")

        st.subheader("Full Pipeline State")
        st.json(result)
