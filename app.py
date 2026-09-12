import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="UniProject AI", page_icon="🎓", layout="wide")

st.title("🎓 UniProject AI — دليل مشروعك الجامعي")
st.write("أدخلي تفاصيل مشروعك وسيقوم فريق من 4 وكلاء ذكاء اصطناعي بتحليل المشروع وتوليد الدليل الشامل.")

# 2. حقل إدخال المتطلبات
user_input = st.text_area(
    "أدخلي متطلبات مشروعك الجامعي:", 
    placeholder="مثال: تطبيق جوال لإدارة طلبات الفنادق...",
    height=150
)

# 3. زر التشغيل والربط بـ n8n
if st.button("🚀 توليد دليل المشروع", type="primary"):
    if not user_input.strip():
        st.warning("يرجى إدخال متطلبات المشروع أولاً.")
    else:
        with st.spinner("جاري استدعاء وكلاء الذكاء الاصطناعي الأربعة وتحليل مشروعك..."):
            # ⬇️ ضعي رابط الـ Production URL الذي نسختيه بين التنصيص
N8N_WEBHOOK_URL = "https://rsll.app.n8n.cloud/webhook/55ef47d6-32e4-48df-a29d-e2f7103943d4"
            
            try:
                # إرسال الطلب إلى n8n
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json={"prompt": user_input}
                )
                
                if response.status_code == 200:
                    st.success("تم توليد التقرير بنجاح!")
                    result = response.json()
                    
                    # عرض التقرير النهائي
                    # ملاحظة: احرصي على أن اسم المفتاح يطابق ما ترجعه عقدة Respond to Webhook
                    report_content = result.get("output", result.get("fullReport", str(result)))
                    st.markdown(report_content)
                else:
                    st.error(f"حدث خطأ أثناء الاتصال بالنظام: {response.status_code}")
            except Exception as e:
                st.error(f"تعذر الاتصال بالـ Webhook: {e}")
