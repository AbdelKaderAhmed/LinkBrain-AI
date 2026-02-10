import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

class LinkBrainMonitor:
    """
    LinkBrain AI | Engine Room (Developer Dashboard)
    Optimized for Groq Cloud performance tracking and Llama 3 token estimation.
    """
    def __init__(self, db_path='linkbrain_admin.db'):
        self.db_path = db_path
        self.setup_page()

    def setup_page(self):
        st.set_page_config(
            page_title="LinkBrain AI | Engine Room",
            page_icon="⚡",
            layout="wide"
        )
        # Custom Professional Dark Theme (GitHub-inspired palette)
        st.markdown("""
            <style>
            .main { background-color: #0d1117; }
            .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
            [data-testid="stMetricValue"] { color: #58a6ff; font-family: 'JetBrains Mono', monospace; }
            .stTabs [data-baseweb="tab"] { color: #8b949e; font-weight: 600; }
            .stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom-color: #58a6ff !important; }
            </style>
        """, unsafe_allow_html=True)

    def fetch_logs(self):
        """Connects to SQLite and processes performance data for analysis."""
        try:
            conn = sqlite3.connect(self.db_path)
            query = "SELECT * FROM perf_logs ORDER BY timestamp DESC"
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                # Llama 3 estimation: ~0.75 tokens per word (more efficient than GPT-4)
                # Using 1.3 as a balanced multiplier for diverse languages
                df['est_tokens'] = (df['content_length'] / 4) * 1.3 
            return df
        except Exception as e:
            st.error(f"Database Connection Error: {e}")
            return pd.DataFrame()

    def render_header(self):
        st.markdown("<h1 style='color: #f0f6fc;'>⚡ LinkBrain AI <span style='color: #58a6ff; font-weight: 200;'>Engine Room</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8b949e;'>Real-time Performance Monitoring for Groq LPU™ Infrastructure</p>", unsafe_allow_html=True)

    def render_kpi_layer(self, df):
        """Displays key system performance indicators."""
        m1, m2, m3, m4, m5 = st.columns(5)
        
        # Core Analytics Logic
        avg_lat = df['latency'].mean()
        # Ensure we count any non-error status as success
        success_rate = (len(df[~df['status'].str.contains('Error', na=False)]) / len(df)) * 100
        total_tokens = df['est_tokens'].sum()
        today_data = df[df['timestamp'].dt.date == datetime.now().date()]

        m1.metric("Avg Latency", f"{avg_lat:.2f}s")
        m2.metric("Success Rate", f"{success_rate:.1f}%")
        m3.metric("Total Executions", f"{len(df):,}")
        m4.metric("Total Tokens (Est)", f"{int(total_tokens):,}")
        m5.metric("Tokens Today (Est)", f"{int(today_data['est_tokens'].sum()):,}")

    def render_charts(self, df):
        """Visualizes performance distribution and consumption patterns."""
        tab_perf, tab_usage, tab_raw = st.tabs(["📈 Performance Analysis", "📊 Distribution", "📂 System Logs"])

        with tab_perf:
            col1, col2 = st.columns(2)
            with col1:
                # Analyzing latency spread - crucial for monitoring Groq speed
                fig_box = px.box(df, x='tool_name', y='latency', color='tool_name',
                                title="Latency Spread by Feature", template="plotly_dark",
                                color_discrete_sequence=px.colors.qualitative.Safe)
                st.plotly_chart(fig_box, use_container_width=True)
            
            with col2:
                # Request volume timeline (Hourly)
                df_time = df.set_index('timestamp').resample('H').size().reset_index(name='counts')
                fig_line = px.line(df_time, x='timestamp', y='counts', title="Request Volume Timeline",
                                  template="plotly_dark", line_shape="spline")
                fig_line.update_traces(line_color='#58a6ff', fill='tozeroy')
                st.plotly_chart(fig_line, use_container_width=True)

        with tab_usage:
            col3, col4 = st.columns(2)
            with col3:
                # Share of requests across different tools
                fig_pie = px.pie(df, names='tool_name', hole=0.6, title="Feature Usage Share",
                                template="plotly_dark", color_discrete_sequence=px.colors.sequential.Blues_r)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col4:
                # Token burn rate visualization
                token_df = df.groupby('tool_name')['est_tokens'].sum().reset_index()
                fig_bar = px.bar(token_df, x='tool_name', y='est_tokens', color='tool_name',
                                title="Token Consumption per Feature", template="plotly_dark")
                st.plotly_chart(fig_bar, use_container_width=True)

        with tab_raw:
            st.subheader("Raw System Execution Logs")
            # Filtering for scannability
            st.dataframe(df[['timestamp', 'tool_name', 'latency', 'status', 'est_tokens']], 
                         use_container_width=True, hide_index=True)

# Main Execution Flow
if __name__ == "__main__":
    monitor = LinkBrainMonitor()
    monitor.render_header()
    
    data = monitor.fetch_logs()
    
    if not data.empty:
        monitor.render_kpi_layer(data)
        st.divider()
        monitor.render_charts(data)
    else:
        st.warning("System database initialized but no operational logs found yet. Execute AI tools to see analytics.")