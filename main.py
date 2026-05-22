import os
import pandas as pd
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import scr.treatment as tr

st.bar_chart(tr.contar(tr.agrupar(["Year",'Segment'])))