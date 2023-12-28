# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any

import numpy as np

import streamlit as st
from streamlit.hello.utils import show_code

st.set_page_config(page_title="Animation Demo", page_icon="📹")
st.markdown("# Legal AIDD demo")
st.sidebar.header("Upload your files")
st.write(
    """Test."""
)

main()

def categorize_document(doc_content):
    # Use GPT-4 to categorize document
    response = openai.Completion.create(
        model="text-davinci-004",
        prompt=f"Categorize this document: {doc_content}",
        max_tokens=50
    )
    return response.choices[0].text.strip()

def check_custom_points(doc_content, custom_points):
    # Check for custom points in the document
    results = {}
    for point in custom_points:
        response = openai.Completion.create(
            model="text-davinci-004",
            prompt=f"Does this document contain the following point: '{point}'? Document: {doc_content}",
            max_tokens=50
        )
        results[point] = response.choices[0].text.strip()
    return results

def main():
    st.title('Legal Document Due Diligence Tool')

    # File upload
    uploaded_files = st.file_uploader("Upload Documents", accept_multiple_files=True, type=['pdf', 'docx'])

    # Custom points input
    custom_points = st.text_area("Enter custom points to check (one per line)").split('\n')

    if st.button('Process Documents'):
        categorized_docs = {}
        custom_checks = {}

        for uploaded_file in uploaded_files:
            # Read file content
            doc_content = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            category = categorize_document(doc_content)
            checks = check_custom_points(doc_content, custom_points)

            categorized_docs[uploaded_file.name] = category
            custom_checks[uploaded_file.name] = checks

        # Display results
        st.write("Categorized Documents:")
        st.json(categorized_docs)

        st.write("Custom Points Checks:")
        st.json(custom_checks)

        # Export to CSV (example)
        df = pd.DataFrame.from_dict(categorized_docs, orient='index', columns=['Category'])
        st.download_button('Download Summary Report', df.to_csv().encode('utf-8'), 'summary_report.csv')




