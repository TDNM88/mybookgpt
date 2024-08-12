import openai
import groqapi
import streamlit as st
import json
from io import StringIO, BytesIO

## Lấy API key từ Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]
groqapi.api_key = st.secrets["groq"]["api_key"]

# Hàm sử dụng GPT-4 để tạo outline
def generate_outline(book_topic, writing_requirements, style_requirements, reference_info):
    outline_prompt = f"Create a book outline about {book_topic}. Consider the following requirements:\n{writing_requirements}\n{style_requirements}\n{reference_info}"
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Sử dụng đúng model GPT-4
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": outline_prompt}
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

# Hàm sử dụng GPT-4 để tạo nội dung từng phần
def generate_chapter_content(chapter, writing_requirements, style_requirements, reference_info):
    content_prompt = f"Write a detailed chapter for a book about {chapter}. Consider the following requirements:\n{writing_requirements}\n{style_requirements}\n{reference_info}"
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Sử dụng đúng model GPT-4
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content_prompt}
        ],
        max_tokens=1500,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

# Hàm sử dụng Groq API để kết hợp nội dung
def combine_and_extend_content(chapter_contents):
    combined_content = groqapi.combine_texts(chapter_contents)
    extended_content = groqapi.extend_text(combined_content)
    return extended_content

# Hàm tạo file PDF, DOCX hoặc TXT từ nội dung đã tạo
def save_content_to_file(content, file_format):
    if file_format == "TXT":
        return content.encode('utf-8')
    elif file_format == "DOCX":
        from io import BytesIO
        from docx import Document
        doc = Document()
        doc.add_paragraph(content)
        bio = BytesIO()
        doc.save(bio)
        bio.seek(0)
        return bio
    elif file_format == "PDF":
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in content.split("\n"):
            pdf.multi_cell(0, 10, line)
        bio = BytesIO()
        pdf.output(bio)
        bio.seek(0)
        return bio

# Hàm lưu metadata thành file JSON
def save_metadata_to_file(metadata):
    bio = BytesIO()
    bio.write(json.dumps(metadata).encode('utf-8'))
    bio.seek(0)
    return bio

# Hàm tải metadata từ file JSON
def load_metadata_from_file(uploaded_file):
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    return json.load(stringio)

# Streamlit UI
def main():
    st.set_page_config(page_title="AI Book Writer", layout="wide")

    # Giao diện sáng/tối
    st.sidebar.title("Tùy chọn giao diện")
    theme = st.sidebar.radio("Chọn giao diện:", options=["Sáng", "Tối"])
    
    if theme == "Tối":
        st.markdown("""
            <style>
            body {background-color: #1e1e1e; color: white;}
            .stTextInput, .stTextArea, .stSelectbox {color: white;}
            </style>
        """, unsafe_allow_html=True)

    st.title("AI Book Writer")
    st.write("Tạo sách tự động theo yêu cầu của bạn.")

    metadata = None
    if 'saved_metadata' not in st.session_state:
        st.session_state['saved_metadata'] = None

    # Tải metadata nếu có
    uploaded_file = st.file_uploader("Tải lên tệp metadata (JSON) để tiếp tục dự án trước:")
    if uploaded_file is not None:
        metadata = load_metadata_from_file(uploaded_file)
        st.session_state['saved_metadata'] = metadata

    # Sử dụng metadata đã tải nếu có
    if st.session_state['saved_metadata'] is not None:
        metadata = st.session_state['saved_metadata']
        book_topic = metadata['book_topic']
        writing_requirements = metadata['writing_requirements']
        style_requirements = metadata['style_requirements']
        reference_info = metadata['reference_info']
        outline = metadata['outline']
        chapter_contents = metadata['chapter_contents']
        st.success("Đã tải thành công dự án trước đó.")
    else:
        book_topic = st.text_input("Chủ đề của cuốn sách:")
        writing_requirements = st.text_area("Yêu cầu về cách viết:")
        style_requirements = st.text_area("Yêu cầu về văn phong:")
        reference_info = st.text_area("Thông tin tham khảo (nếu có):")
        outline = None
        chapter_contents = []

    if st.button("Đề xuất Outline"):
        with st.spinner("Đang tạo đề xuất outline..."):
            outline = generate_outline(book_topic, writing_requirements, style_requirements, reference_info)
            st.session_state['saved_metadata'] = {
                'book_topic': book_topic,
                'writing_requirements': writing_requirements,
                'style_requirements': style_requirements,
                'reference_info': reference_info,
                'outline': outline,
                'chapter_contents': chapter_contents
            }
            st.subheader("Outline được đề xuất:")
            st.write(outline)

    if outline and st.button("Đồng ý Outline và Bắt đầu Viết"):
        st.header("Bước 2: Viết Nội Dung Sách")
        st.write("Ứng dụng sẽ tạo nội dung chi tiết cho từng chương dựa trên outline đã được đồng ý.")

        chapters = [chapter.strip() for chapter in outline.split("\n") if chapter.strip()]
        
        for chapter in chapters:
            if st.button(f"Viết nội dung chương: {chapter}"):
                content = generate_chapter_content(chapter, writing_requirements, style_requirements, reference_info)
                chapter_contents.append(content)
                st.session_state['saved_metadata']['chapter_contents'] = chapter_contents
                with st.beta_expander(f"Nội dung chương {chapter}"):
                    st.text_area("", value=content, height=200)

    if chapter_contents:
        if st.button("Kết hợp và Mở rộng Nội dung"):
            with st.spinner("Đang kết hợp và mở rộng nội dung..."):
                full_book_content = combine_and_extend_content(chapter_contents)
                st.text_area("Nội dung sách đã viết:", value=full_book_content, height=400)

    # Tải xuống metadata
    if st.button("Tải xuống Metadata"):
        if st.session_state['saved_metadata']:
            metadata_file = save_metadata_to_file(st.session_state['saved_metadata'])
            st.download_button(label="Tải xuống tệp Metadata (JSON)", data=metadata_file, file_name="project_metadata.json", mime="application/json")

    # Lưu nội dung thành file
    if chapter_contents and st.button("Lưu và Tải Xuống"):
        st.header("Lưu và Tải Xuống")
        file_format = st.selectbox("Chọn định dạng tệp để lưu:", ("TXT", "DOCX", "PDF"))
        if full_book_content:
            file_data = save_content_to_file(full_book_content, file_format)
            if file_format == "TXT":
                st.download_button(label="Tải xuống tệp TXT", data=file_data, file_name="generated_book.txt", mime="text/plain")
            elif file_format == "DOCX":
                st.download_button(label="Tải xuống tệp DOCX", data=file_data, file_name="generated_book.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            elif file_format == "PDF":
                st.download_button(label="Tải xuống tệp PDF", data=file_data, file_name="generated_book.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
