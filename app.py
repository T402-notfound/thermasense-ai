import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="ThermaSense AI", layout="wide")

# تصميم الواجهة بالألوان الداكنة الصناعية
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #eceff4; }
    .metric-box {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 20px;
    }
    .metric-box-danger {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ef4444;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏭 ThermaSense AI — MVP")
st.write("تحسين وتوجيه الحرارة المهدورة الصناعية بالذكاء الاصطناعي")

# شريط التحكم الجانبي للمحاكاة
st.sidebar.header("🛠️ خيارات التحكم للمحاكاة")
mode = st.sidebar.selectbox("اختر حالة تشغيل المصنع:", ["وضع التشغيل الطبيعي", "وضع رصد التسريب النشط"])

# تحديد المتغيرات بناء على الوضع
if mode == "وضع رصد التسريب النشط":
    current_temp, current_press, is_anomaly = 72.4, 1.9, True
else:
    current_temp, current_press, is_anomaly = 50.8, 4.1, False

# عرض المؤشرات
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="metric-box"><h4>🌡️ درجة حرارة العادم</h4><h2>{current_temp} °C</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-box"><h4>💨 الضغط الحالي</h4><h2>{current_press} Bar</h2></div>', unsafe_allow_html=True)
with col3:
    if is_anomaly:
        st.markdown('<div class="metric-box-danger"><h4>⚠️ حالة النظام (AI)</h4><h2 style="color:#ef4444;">تسريب حراري! (خسارة: 450 درهم/س)</h2></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="metric-box"><h4>✅ حالة النظام (AI)</h4><h2 style="color:#10b981;">مستقر وفعّال (خسارة: 0 درهم)</h2></div>', unsafe_allow_html=True)

# الرسوم البيانية
st.subheader("📈 التوأم الرقمي والتدقيق الافتراضي")
np.random.seed(42)
times = [datetime.datetime.now() - datetime.timedelta(minutes=i*15) for i in range(50)]
times.reverse()
temps = np.random.normal(loc=53.0, scale=2.0, size=50)
if is_anomaly:
    temps[-10:] += 20.0

fig = go.Figure()
fig.add_trace(go.Scatter(x=times, y=temps, name="درجة الحرارة (°C)", line=dict(color='#ef4444', width=2)))
fig.update_layout(template="plotly_dark", height=300, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig, use_container_width=True)

# مصفوفة التوجيه
st.write("---")
st.subheader("🔀 مصفوفة التوجيه الذكي (Smart Routing)")
if is_anomaly:
    st.success("🤖 قرار الذكاء الاصطناعي: تم فتح الصمامات تلقائياً وتوجيه الحرارة إلى حوض الغسيل. نسبة توفير الغاز الطبيعي: 100%")
else:
    st.info("🔄 النظام في وضع المراقبة المستمرة لمصفوفة العرض والطلب الحراري...")
