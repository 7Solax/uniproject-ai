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
                    
                    # معالجة النتيجة سواء كانت List أو Dict
                    if isinstance(result, list) and len(result) > 0:
                        first_item = result[0]
                        if isinstance(first_item, dict):
                            report_content = first_item.get("output", first_item.get("fullReport", first_item.get("text", str(first_item))))
                        else:
                            report_content = str(first_item)
                    elif isinstance(result, dict):
                        report_content = result.get("output", result.get("fullReport", result.get("text", str(result))))
                    else:
                        report_content = str(result)
                        
                    # عرض التقرير النهائي
                    st.markdown(report_content)
                else:
                    st.error(f"حدث خطأ أثناء الاتصال بالنظام: {response.status_code}")
            except Exception as e:
                st.error(f"تعذر الاتصال بالـ Webhook: {e}")
