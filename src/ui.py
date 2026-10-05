import streamlit as st


def load_css():
    css_file = "assets/style.css"

    with open(css_file, "r", encoding="utf-8") as file:
        css = file.read()

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def page_header(title, description):
    st.title(title)
    st.write(description)
    st.divider()


def sidebar_branding():
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; padding:10px 0 20px 0;">
                <h1 style="font-size:28px; margin-bottom:5px;">
                    SegmentIQ AI
                </h1>
                <p style="font-size:14px; color:#94a3b8;">
                    Customer Segmentation<br>
                    & Business Intelligence
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.markdown(
            """
            **Project Type**  
            Unsupervised Machine Learning

            **Algorithm**  
            K-Means Clustering

            **Dataset**  
            Online Retail II
            """
        )

        st.divider()

        st.caption("Built with Python • Scikit-learn • Streamlit")